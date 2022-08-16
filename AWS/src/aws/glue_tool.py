from typing import Optional, Dict

import boto3


class GlueTool:
    def __init__(self,
                 aws_access_key_id: str,
                 aws_secret_access_key: str,
                 region: Optional[str] = 'us-east-1'):

        self.session = boto3.Session(aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key,
                                     region_name=region)
        self.client = boto3.client('glue', verify=False)

    defaultArgs = {
        '--enable-continuous-cloudwatch-log': 'true'
    }

    def create_job(self,
                   job_name: str,
                   script_location: str,
                   script_type: Optional[str] = None,
                   connection: Optional[str] = None,
                   role: Optional[str] = None,
                   arguments: Optional[Dict] = None,
                   max_retries: Optional[int] = None,
                   workers_nb: Optional[int] = None,
                   worker_type: Optional[str] = None):
        body = (self.get_default_glue_job_args(script_location, role, workers_nb, worker_type, arguments, max_retries)
                if script_type == 'glueetl'
                else self.get_default_python_job_args(script_location, role, arguments, max_retries))
        body['Name'] = job_name
        if connection:
            body['Connections'] = {'Connections': [ connection ]}

        return self.client.create_job(**body)

    def get_default_job_args(self,
                             glue_version: str,
                             role: Optional[str] = None,
                             arguments: Optional[Dict] = None,
                             max_retries: Optional[int] = None):
        return {
            'Role': role or 'usamea-glue-otdata-prod-veslink-api-downloader-job-role',
            'GlueVersion': glue_version,
            'DefaultArguments': arguments or {},
            'NonOverridableArguments': self.defaultArgs,
            'MaxRetries': max_retries if max_retries else 0
        }

    def get_default_python_job_args(self,
                                    script_location: str,
                                    role: Optional[str] = None,
                                    arguments: Optional[Dict] = None,
                                    max_retries: Optional[int] = None):
        job = self.get_default_job_args("1.0", role, arguments, max_retries)
        return job.update({
            'Command': {
                'Name': 'pythonshell',
                'ScriptLocation': script_location,
                'PythonVersion': '3'
            },
            'GlueVersion': '1.0',
        })

    def get_default_glue_job_args(self,
                                  script_location: str,
                                  role: Optional[str] = None,
                                  workers_nb: Optional[int] = None,
                                  worker_type: Optional[str] = None,
                                  arguments: Optional[Dict] = None,
                                  max_retries: Optional[int] = None):
        job = self.get_default_job_args("3.0", role, arguments, max_retries)
        return job.update({
            'Command': {
                'Name': 'glueetl',
                'ScriptLocation': script_location,
                'PythonVersion': '3'
            },
            'NumberOfWorkers': workers_nb or 10,
            'WorkerType': worker_type or "Standard",
        })

    def list_jobs(self):
        return self.client.list_jobs()

    def start_job(self, job_name: str):
        return self.client.start_job_run(
            JobName=job_name
        )

    def stop_job(self, job_name: str, job_id: str):
        return self.client.batch_stop_job_run(
            JobName=job_name,
            JobRunIds=[job_id]
        )

    def delete_job(self, job_name: str):
        return self.client.delete_job(
            JobName=job_name
        )

    def update_job(self,
                   job_name: str,
                   script_location: str,
                   role: Optional[str] = None,
                   script_type: Optional[str] = None,
                   connection: Optional[str] = None,
                   workers_nb: Optional[int] = None,
                   worker_type: Optional[str] = None,
                   arguments: Optional[Dict] = None,
                   max_retries: Optional[int] = None):
        body = (self.get_default_glue_job_args(script_location, role, workers_nb, worker_type, arguments, max_retries)
                if script_type == 'glueetl'
                else self.get_default_python_job_args(script_location, role, arguments, max_retries))
        if connection:
            body['Connections'] = {'Connections': [connection]}

        return self.client.update_job(
            JobName=job_name,
            JobUpdate=body
        )

    def create_trigger(self,
                       trigger_name: str,
                       job_name: str,
                       cron: str,
                       description: str,
                       timeout: Optional[int] = 10,
                       start_on_create: Optional[bool] = True):
        return self.client.create_trigger(
            Name=trigger_name,
            Type='SCHEDULED',
            Schedule=cron,
            Actions=[
                {
                    'JobName': job_name,
                    'Timeout': timeout
                },
            ],
            Description=description,
            StartOnCreation=start_on_create,
        )

    def update_trigger(self,
                       trigger_name: str,
                       job_name: str,
                       cron: str,
                       description: str,
                       timeout: Optional[int] = 10):
        return self.client.update_trigger(
            Name=trigger_name,
            TriggerUpdate={
                'Name': trigger_name,
                'Schedule': cron,
                'Actions': [
                    {
                        'JobName': job_name,
                        'Timeout': timeout
                    },
                ],
                'Description': description})

    def delete_trigger(self, name: str):
        return self.client.delete_trigger(Name=name)

    def start_trigger(self, name: str):
        return self.client.start_trigger(Name=name)
