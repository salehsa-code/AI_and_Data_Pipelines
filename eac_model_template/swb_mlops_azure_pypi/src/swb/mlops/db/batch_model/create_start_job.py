import json
from time import sleep

from swb.mlops.db.batch_model import create_start_cluster
from swb.mlops.db.core.db_api_client import execute_post_request, execute_get_request
from swb.mlops.db.batch_model import install_libraries


def db_jobs_create(db_workspace_uri: str, db_token: str, cluster_name: str, job_name: str, notebook_full_path):
    """
    This function just focuses on creation a job with no scheduling and assigns the job to an existing cluster.

    See: https://docs.databricks.com/dev-tools/api/latest/jobs.html#create

    :param db_workspace_uri: The Databricks workspace URI to use for this API call.
    :param db_token: The Databricks personal token to use for this API call.
    :param cluster_name : The cluster name associated with the new job.
    :param job_name : The new job's name.
    :param notebook_full_path : A notebook databrick workspace path.
    :return: a job id as a string.
    """

    if db_workspace_uri is None or db_workspace_uri == "":
        raise ValueError("db_workspace_uri of " + str(db_workspace_uri) + " is not valid input.")
    if db_token is None or db_token == "":
        raise ValueError("databricks_token of " + str(db_token) + " is not valid input.")

    full_uri = db_workspace_uri + '/api/2.0/jobs/create'
    cluster_id = create_start_cluster.get_cluster_id(cluster_name=cluster_name,
                                                     db_workspace_uri=db_workspace_uri,
                                                     db_token=db_token)
    json_dict = {
        "notebook_task": {
            "notebook_path": "{}".format(notebook_full_path)
        },
        "existing_cluster_id": "{}".format(cluster_id[0]),
        "name": "{}".format(job_name),
        "max_concurrent_runs": 1,
        # "timeout_seconds": 86400,
        # "libraries": [],
        "email_notifications": {}
    }

    response = execute_post_request(full_uri, db_token, json_dict)
    result = json.loads(response.text)
    return result['job_id']


def db_jobs_run_now(db_workspace_uri: str, db_token: str, job_id: int, nb_parameters={}):
    """
    Starts a given job based on job id.

    See: https://docs.databricks.com/dev-tools/api/latest/jobs.html#run-now

    :param db_workspace_uri: The Databricks workspace URI to use for this API call.
    :param db_token: The Databricks personal token to use for this API call.
    :param job_id : This a unique identifier given by databricks.
    :param nb_parameters : A dict containing possible parameters for the notebook.
    :return job_id
    """

    if db_workspace_uri is None or db_workspace_uri == "":
        raise ValueError("db_workspace_uri of " + str(db_workspace_uri) + " is not valid input.")
    if db_token is None or db_token == "":
        raise ValueError("databricks_token of " + str(db_token) + " is not valid input.")

    uri = db_workspace_uri + '/api/2.0/jobs/run-now'
    json_dict = {
        "job_id": job_id,
        "notebook_params": nb_parameters
    }

    response = execute_post_request(uri, db_token, json_dict)
    json_response = json.loads(response.text)

    run_id, number_in_job = json_response['run_id'], json_response['number_in_job']
    return run_id, number_in_job


def db_runs_list(db_workspace_uri: str, db_token: str, job_id: int):
    """
    This function will check the status of a DB Job and return it as a string

    See: https://docs.databricks.com/dev-tools/api/latest/jobs.html#runs-list

    :param db_workspace_uri: The Databricks workspace URI to use for this API call.
    :param db_token: The Databricks personal token to use for this API call.
    :param job_id: This a unique identifier given by databricks.
    :return status
    """

    if db_workspace_uri is None or db_workspace_uri == "":
        raise ValueError("db_workspace_uri of " + str(db_workspace_uri) + " is not valid input.")
    if db_token is None or db_token == "":
        raise ValueError("databricks_token of " + str(db_token) + " is not valid input.")

    full_uri = db_workspace_uri + '/api/2.0/jobs/runs/list'
    params_dict = {
        "job_id": job_id,
        "active_only": False
    }

    response = execute_get_request(full_uri, db_token, params_dict)

    return response


def db_hold_until_run_complete(db_workspace_uri: str, db_token: str, job_id: int, number_in_job: int, timeout=30):
    """
    This function will poll until the number_in_job of job_id is completed or timeout occurs

    See: https://docs.databricks.com/dev-tools/api/latest/jobs.html#runs-get

    :param db_workspace_uri: The Databricks workspace URI to use for this API call.
    :param db_token: The Databricks personal token to use for this API call.
    :param job_id: This a unique identifier given by databricks.
    :param number_in_job: Each job_id has multiple runs, so you must specify which run
    :return status

    :raises: TimeoutError
    """

    if db_workspace_uri is None or db_workspace_uri == "":
        raise ValueError("db_workspace_uri of " + str(db_workspace_uri) + " is not valid input.")
    if db_token is None or db_token == "":
        raise ValueError("databricks_token of " + str(db_token) + " is not valid input.")

    full_uri = db_workspace_uri + '/api/2.0/jobs/runs/get'
    params_dict = {
        'job_id': job_id,
        'number_in_job': number_in_job
    }

    response = execute_get_request(full_uri, db_token, params_dict)

    if parse_runs_life_cycle_state(response) != "TERMINATED":
        print("We have not terminated yet... waiting.... timeout = " + str(timeout) + "(s)")
        sleep(timeout)
        print("retrying now...")
        retry_response = execute_get_request(full_uri, db_token, params_dict)

        if parse_runs_life_cycle_state(retry_response) != "TERMINATED":
            # Give up
            raise TimeoutError("Job Did not finish within timeout " + str(timeout) + "(s): Retry response was: " + str(retry_response))

        return retry_response

    return response


def parse_runs_life_cycle_state(response):
    """
    Function takes in an HTTP response and attempts to retrieve just the runs lifecycle state
    :param response:
    :return:
    """
    json_response = json.loads(response.text)

    print(str(json_response))

    life_cycle_state = json_response['state']['life_cycle_state']

    if life_cycle_state == "TERMINATED":
        # Job finished, which is good
        print("Astalavista baby- Job WAS FOUND TERMINATED")
        return json_response['state']['life_cycle_state']
    elif life_cycle_state == "PENDING":
        # Job finished, which is good
        print("We were found to be in pending state")
        return json_response['state']['life_cycle_state']
    else:
        raise Exception("Unexpected Job State Found: " + str(response))


def db_jobs_create_job_cluster(db_workspace_uri: str,
                                db_token : str,
                                spark_version: str,
                                node_type_id: str,
                                job_name: str,
                                source_dir: str,
                                notebook_full_path,
                                num_workers: 3,
                                file_format='conda'):
    """
    Here we create a job and the cluster associated with it.
    
    :param db_workspace_uri: 
    :param db_token: 
    :param spark_version: 
    :param node_type_id: 
    :param job_name: 
    :param source_dir: 
    :param notebook_full_path: 
    :param num_workers: 
    :param file_format: 
    :return: 
    """
    
    if db_workspace_uri is None or db_workspace_uri == "":
        raise ValueError("db_workspace_uri of " + str(db_workspace_uri) + " is not valid input.")
    if db_token is None or db_token == "":
        raise ValueError("databricks_token of " + str(db_token) + " is not valid input.")

    full_uri = db_workspace_uri+'/api/2.0/jobs/create'
    librairies_to_install = install_libraries.convert_file_to_db(directory=source_dir, file_format=file_format)
    json = {
            "notebook_task" : {
                    "notebook_path": "{}".format(notebook_full_path)
            },
            "new_cluster" : {
                "spark_version" : "{}".format(spark_version),
                "node_type_id" : "{}".format(node_type_id),
                "num_workers" : num_workers,
            },
            "libraries" : librairies_to_install["libraries"],
            "name" : "{}".format(job_name),
            "max_concurrent_runs" : 1,
            #"timeout_seconds": 86400,
            "email_notifications" : {}
            }
    print(json)
    response = execute_post_request(full_uri, db_token, json)
    return response


def db_jobs_delete(db_workspace_uri: str, db_token: str, job_id: int):
    """
    deletes a given job based on job id.

    See: https://docs.databricks.com/dev-tools/api/latest/jobs.html#run-now

    :param db_workspace_uri: The Databricks workspace URI to use for this API call.
    :param db_token: The Databricks personal token to use for this API call.
    :param job_id : This a unique identifier given by databricks.
    :return job_id
    """

    if db_workspace_uri is None or db_workspace_uri == "":
        raise ValueError("db_workspace_uri of " + str(db_workspace_uri) + " is not valid input.")
    if db_token is None or db_token == "":
        raise ValueError("databricks_token of " + str(db_token) + " is not valid input.")

    uri = db_workspace_uri + '/api/2.0/jobs/delete'
    json_dict = {
        "job_id": job_id,
    }
    print("deleting job : {}".format(job_id))
    response = execute_post_request(uri, db_token, json_dict)

    return response
