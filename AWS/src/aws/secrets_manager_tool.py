import base64
import json
import typing
from typing import Optional

import boto3
from botocore.exceptions import ClientError


class SecretsManagerTool:
    def __init__(self,
                 aws_access_key_id: str,
                 aws_secret_access_key: str,
                 region: Optional[str] = 'us-east-1'):
        self.session = boto3.Session(aws_access_key_id=aws_access_key_id,
                                     aws_secret_access_key=aws_secret_access_key,
                                     region_name=region)

        self.client = boto3.client('secretsmanager', verify=False)

    def update_secret(self, secret_id: str, secret_string: typing.Dict):
        return self.client.update_secret(
            SecretId=secret_id,
            SecretString=json.dumps(secret_string)
        )

    def get_secret(self, secret_name: str):

        try:
            get_secret_value_response = self.client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                raise e
        else:
            if 'SecretString' in get_secret_value_response:
                secret = get_secret_value_response['SecretString']
                return json.loads(secret)
            else:
                return base64.b64decode(get_secret_value_response['SecretBinary'])