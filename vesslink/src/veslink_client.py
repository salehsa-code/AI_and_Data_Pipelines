import requests
from datetime import datetime, timezone, timedelta
from dateutil import parser
from time import time, sleep
import json
import boto3
import concurrent.futures


class VeslinkClient:

    def __init__(self, environment_type: str, secret_id: str):
        self.environment_type = environment_type  # Test or Prod

        self.client_id, self.client_secret, self.bucket_name, aws_access_key_id, secret_key_id = self._extract_secret(
            secret_id=secret_id)

        self.session, self.client, self.bucket = self.init_aws_client(aws_access_key_id, secret_key_id)
        self.token = self.get_token()
        self.timeout = (60, 120)
        self.seconds = 60

        self.initialize_log()

    def _extract_secret(self, secret_id):
        secret = self._get_secrets(secret_id)
        return secret['Veson_client_id'], secret['Veson_client_secret'], secret['AWS_bucket'], \
               secret['AWS_access_key_id'], secret['AWS_secret_key_id']

    @property
    def config_name(self) -> str:
        return f"onDemandExtract1Day{self.environment_type}"

    @property
    def job_remote_folder(self) -> str:
        return 'DEV/IMOSDL/Hourly' if self.environment_type == 'Test' else 'IMOSDL/Hourly'

    @staticmethod
    def log(message):
        print(f'[{datetime.utcnow()}] {message}')

    @staticmethod
    def _get_secrets(secret_id: str):
        """
        Requires credentials to be placed in AWS secret manager
        """
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(
            SecretId=secret_id
        )
        return json.loads(response['SecretString'])

    def get_token(self):
        """
        VIP Data Lake API step 1: get a token (60 minutes validity)
        """
        url = 'https://auth.veslink.com/connect/token'
        body = {
            'grant_type': 'client_credentials',
            'scope': 'datalake',
            'client_secret': self.client_secret,
            'client_id': self.client_id
        }
        self.log(f'get_token starting...')
        api_request = requests.post(url, data=body)
        access_token = json.loads(api_request.content)['access_token'] if api_request.status_code == 200 else 'error'
        expires_in = json.loads(api_request.content)['expires_in'] if api_request.status_code == 200 else 'error'
        token_validity_limit = int(time()) + expires_in
        self.log(f'get_token request status: {api_request.status_code}')
        return {
            'access_token': access_token,
            'expires_at': token_validity_limit
        }

    def _check_token_validity(self, token):
        """
        Check that the token is still valid (if process beyond the hour is tolerated)
        """
        try:
            self.log(f'checkTokenValidity starting...')

            remaining_time = int(token['expires_at'] - time())
            if remaining_time < 30:
                self.log('token has expired and will be refreshed')
                token = self.get_token()
                remaining_time = int(token['expires_at'] - time())
            self.log(f'Token validity remaining time: {remaining_time}')
            return remaining_time

        except Exception as e:
            self.log(f'Error: {e}')
            raise

    def call_api(self):
        """
        Trigger a replication job on Veson's side. This step can be run only once per hour.

        """

        try:
            # **  We check the token validity, which will be refreshed if necessary
            self._check_token_validity(self.token)

            # *  API Call
            url = 'https://emea.veslink.com/api/datalake/v1/export'
            body = '{"configName": "' + self.config_name + '"}'
            headers = {'Authorization': f'Bearer {self.token["access_token"]}'}
            req = requests.post(url, timeout=self.timeout, data=body, headers=headers, verify=False)
            code = json.loads(req.content)
            self.log(f'code: {code}')

            # Based on the response we get (if calls are "intempestive"), the jobGUID are extracted in different manners
            def sleep_until_next_trigger(code, sec):
                """
                In case the job is triggered below the hourly frequency, an error message is returned by the API.
                This function captures the next available time slot to trigger a new job
                """
                try:
                    td = parser.parse(code['Message'], fuzzy=True)
                    now = datetime.now()
                    now_rounded = datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
                    time_to_sleep = td - now_rounded.replace(tzinfo=timezone.utc) + timedelta(seconds=sec)
                    self.log(f'Time to sleep (seconds): {time_to_sleep.seconds}')
                    sleep(time_to_sleep.seconds)
                except Exception as e:
                    self.log(f'Error: {e}')
                    raise

            while req.status_code != 200:
                sleep_until_next_trigger(code, 0)
                self.log(f'New attempt, api response = {req.status_code}')
                req = requests.post(url, timeout=self.timeout, data=body, headers=headers, verify=False)
            job_guid = json.loads(req.content)['JobGuid']

            return job_guid

        except Exception as e:
            self.log(f'Error: {e}')
            raise

    def run_job(self):
        job_guid = self.call_api()

        count = 50
        attempts = 10
        workers = 3

        while count > 0:
            try:
                self.log(f'Remaining attempts: {count}')
                job_status = self.job_status(job_guid)
                self.log(f'Job Status: {job_status}')

                if job_status == 'Complete':
                    break

                self.log(f'Waiting {self.seconds} seconds before next attempt...')

                sleep(self.seconds)
                count -= 1

            except Exception as e:
                self.log(e)

        if job_status == 'Complete':
            self.log(f'Waiting {self.seconds} seconds before trying to download the files list...')
            sleep(self.seconds)
            folder = f'{self.job_remote_folder}/'
            pre_signed_urls = self.load_pre_signed_url(self.environment_type, job_guid, attempts)
            list_urls_and_table_names = self.get_url_and_table_list(pre_signed_urls)
            self.log(f'Files generated: {len(list_urls_and_table_names)}')

            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                res = list(executor.map(self.upload_aws, list_urls_and_table_names))

            self.log(f'Elements: {len(res)}')

            self.upload_presigned_urls_aws()  # Upload the presigned urls for data observability purposes

            #  Sanity checks: tactical solution to mitigate the problem of upload concurrency with Boto3
            self.log('****************************************************')
            self.log('*** Sanity check')
            self.log('****************************************************')

            try:
                utcnow = datetime.utcnow()
                t = utcnow.strftime('%Y%m%d%H')

                sanity_check = self.check_files(t)
                check_pass = 0
                num_missing_files = sanity_check["numMissingFiles"]
                self.log(f'Found {num_missing_files} missing files')

                while num_missing_files > 0:
                    self.log(f'Available files : {sanity_check["numAvailableFiles"]}')
                    self.log(f'Uploaded files : {sanity_check["numUploadedFiles"]}')
                    self.log(f'Missing files : {sanity_check["numMissingFiles"]}')
                    self.log(f'Sanity check passed? {sanity_check["checkIsOk"]}')
                    self.log(f'Attempt {check_pass}')

                    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
                        res = list(executor.map(self.upload_aws, sanity_check['missingFilesListAndUrls']))

                    sanity_check = self.check_files(t)
                    num_missing_files = sanity_check["numMissingFiles"]
                    check_pass += 1

                sanity_check_final = self.check_files(t)

                self.log(f'Available files : {sanity_check_final["numAvailableFiles"]}')
                self.log(f'Uploaded files : {sanity_check_final["numUploadedFiles"]}')
                self.log(f'Missing files : {sanity_check_final["numMissingFiles"]}')
                self.log(f'Sanity check passed? {sanity_check_final["checkIsOk"]}, in {check_pass} pass(es)')
            except:
                self.log('Sanity check failed')

        self.log('Job done')

    # **************** STEP 3: Check the status of the replication job

    def job_status(self, job_guid):
        """
        Run every minute to check the replication job status, until the 'completed' status is returned by the API
        """

        try:
            # We check the token validity, which will be refreshed if necessary
            self._check_token_validity(self.token)

            #  API Call
            url = 'https://emea.veslink.com/api/datalake/v1/CheckJobStatus'
            body = '{"jobGuid":"' + job_guid + '"}'
            headers = {'Authorization': f'Bearer {self.token["access_token"]}'}
            req = requests.post(url, timeout=self.timeout, data=body, headers=headers)
            return json.loads(req.content)['JobStatus']

        except Exception as e:
            self.log(f'Error: {e}')
            raise

    def load_pre_signed_url(self, job_guid, attempts):
        """
        Once the replication job completeed, the json with pre-signed url is called to upload the files
        """

        while attempts > 0:
            try:
                #  We check the token validity, which will be refreshed if necessary
                self._check_token_validity(self.token)

                #  API Call
                url = f'https://api.veslink.com/v1/datalake/presignedUrls/CARG?apiToken={self.client_secret}&environmentType={self.environment_type}&jobGuid={job_guid}&fileFilter=*&hideMetaData=False&expirationInMinutes=60'
                req = requests.get(url, timeout=self.timeout)
                return json.loads(req.content)

            except Exception as e:
                self.log(f'Error: {e}')
                attempts -= 1
                if attempts == 0:
                    raise
                self.log(f'Waiting {self.seconds} seconds before next attempt...')
                sleep(self.seconds)

    def get_url_and_table_list(self, pre_signed_urls):
        """
        Helper function to reshape pre-signed urls files into an array, to be passed for parallel upload
        """

        try:
            self.log('getUrlAndTableList')
            files_urls_list = [(n['key'].split('/')[-1], n['presignedDownloadURL'], n['size']) for n in pre_signed_urls]
            return files_urls_list

        except Exception as e:
            self.log(f'Error: {e}')
            raise

    def create_folder_s3_bucket(self):
        """
        Create a new folder on S3 as a landing area. The name of the folder is the extraction time
        """

        return f'{self.job_remote_folder}/{datetime.utcnow.strftime("%Y%m%d")}/{datetime.utcnow.strftime("%H")}/'

    def upload_presigned_urls_aws(self, pre_signed_urls):
        """
        Function to upload the presigned urls json file into  S3.
        For sanity check, the presigned urls is the proof of what was promised on Veson's S3
        """
        try:
            folder_name = self.create_folder_s3_bucket()
            # Creating S3 Resource From the Session.
            s3 = self.session.resource('s3')
            object = s3.Object(self.bucket, folder_name + '_PresignedUrls.json')
            object.put(Body=json.dumps(pre_signed_urls))
            self.log("_PresignedUrls.json uploaded to S3 bucket")

        except Exception as e:
            self.log(e)

    def upload_aws(self, element):
        """
        Function to upload the files into  S3
        """
        try:
            folder_name = self.create_folder_s3_bucket()
            table_id, url, size = element
            file = requests.get(url, timeout=self.timeout).content
            # Creating S3 Resource From the Session.
            s3 = self.session.resource('s3')
            object = s3.Object(self.bucket, folder_name + table_id)
            object.put(Body=file)

            self.log(f"{table_id} uploaded to S3 bucket")

        except Exception as e:
            self.log(e)

        return element

    # ********************************************************************
    # SANITY CHECK FUNCTIONS
    # ********************************************************************

    def init_aws_client(self, access_key_id, secret_key_id):
        """
        Initialize the AWS connection to access S3, where the files are uploaded
        """

        try:
            session = boto3.session.Session(aws_access_key_id=access_key_id, aws_secret_access_key=secret_key_id)
            s3 = session.resource('s3')
            client = boto3.client(
                's3',
                aws_access_key_id=access_key_id,
                aws_secret_access_key=secret_key_id
            )
            bucket = s3.Bucket(self.bucket_name)
            if client:
                return s3, client, bucket
        except Exception as e:
            self.log(e)
            return None

    def get_list_files_day(self, t):
        """
        Get the list of delivered files at a certain timestamp
        """
        try:
            day = t[:-2]
            hour = t[-2:]
            prefix = f'{self.job_remote_folder}/{day}/{hour}'
            list_files = [s3_file.key for s3_file in self.bucket.objects.filter(Prefix=prefix)]
            file = [s3_file.split('/')[-1] for s3_file in list_files]
            return file
        except Exception as e:
            self.log(e)
            return None

    def load_presigned_urls(self, t):
        """
        Access the pre-signed urls file on S3.
        Used to check if all promised files are uploaded
        """

        try:
            day = t[:-2]
            hour = t[-2:]
            Key = f'{self.job_remote_folder}/{day}/{hour}/_PresignedUrls.json'
            obj = self.client.get_object(
                Bucket=self.bucket,
                Key=Key
            )
            presigned_urls = json.loads(obj['Body'].read().decode('utf-8'))
            data = {'presignedUrls': presigned_urls,
                    # 'listFiles': [i['key'].split('/')[-1].split('_')[0] for i in presignedUrls],
                    'listFiles': [i['key'].split('/')[-1] for i in presigned_urls]}
            return data
        except Exception as e:
            self.log(e)
            return None

    def return_missing_tables(self, t):
        """
        Check missing files and return a the missing pre-signed urls for recovery
        """
        try:
            files_delivered = self.get_list_files_day(t)
            files_available = self.load_presigned_urls(t)
            if files_available:
                missing_files = list(set(files_available['listFiles']).difference(files_delivered))
                files_urls_list = [(i['key'].split('/')[-1], i['presignedDownloadURL'], i['size'])
                                   for i in files_available['presignedUrls']
                                   if i['key'].split('/')[-1] in missing_files]
            else:
                files_urls_list = None
            return files_urls_list
        except Exception as e:
            self.log(e)
            return None

    def check_files(self, t):
        """
        Run and return results of a sanity check
        """
        try:
            available_files = self.load_presigned_urls(t)['listFiles']
            uploaded_files = self.get_list_files_day(t)
            missing_files = self.return_missing_tables(t)
            num_available_files = len(available_files)
            num_uploaded_files = len(uploaded_files) - 1
            num_missing_files = len(missing_files)
            check_is_ok = num_uploaded_files == num_available_files
            result = {
                'checkIsOk': check_is_ok,
                'numAvailableFiles': num_available_files,
                'numUploadedFiles': num_uploaded_files,
                'numMissingFiles': num_missing_files,
                'missingFilesListAndUrls': num_missing_files
            }
            return result
        except Exception as e:
            self.log(e)
            return None

    def initialize_log(self):
        self.log('*********************************')
        self.log('*** IMOS Data Lake Downloader ***')
        self.log('*********************************')
