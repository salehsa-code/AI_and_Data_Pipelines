# *******************************************************************************************
# START OF THE PIPELINE CODE
# *******************************************************************************************

# Change the environment type from Test to Prod (this will switch the job configName and adapt the S3 prefix not to mix up prod with test workflows)
from datetime import datetime

from src.veslink_client import VeslinkClient


if __name__ == '__main__':

    environment_type = 'Test'  # Test or Prod

    secret_id = 'dev/TAT-Veson-Test-OT'

    veslink_client = VeslinkClient(environment_type=environment_type,
                                   secret_id=secret_id)

    veslink_client.run_job()



