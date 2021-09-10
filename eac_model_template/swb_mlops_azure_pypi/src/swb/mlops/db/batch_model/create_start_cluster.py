"""
This command is designed to create start an existing cluster depending on the parameters given.
The existing cluster is supposed to exist in QA (Workspace) or Production (Workspace).
I will use the databrick api to trigger this action.

Source reference:
https://dev.azure.com/GBI-ODL/AnalyticsOps/_git/cashflow2-mvp?path=%2Fpython_scripts%2Fcreate_cluster.py&version=GBfeature%2Fgeneralize-adb-automation&_a=contents
"""
from requests import HTTPError

from swb.mlops.db.core.db_api_client import execute_post_request, execute_get_request


def db_clusters_create(db_workspace_uri: str, db_token: str, cluster_name: str, spark_version: str, node_type: str,
                       min_workers=1, max_workers=3) -> str:
    """
    Creates a cluster based on needs define in the repo variable

    See: https://docs.databricks.com/dev-tools/api/latest/clusters.html#create

    :param db_workspace_uri: The Databricks workspace URI to use for this API call.
    :param db_token: The Databricks personal token to use for this API call.
    :param cluster_name: a name for the cluster
    :param spark_version: a valid spark version. see https://docs.microsoft.com/en-us/azure/databricks/dev-tools/api/latest/clusters#clusterclusterservicelistsparkversions
    :param node_type: a valid node type. see https://docs.microsoft.com/en-us/azure/databricks/dev-tools/api/latest/clusters#clusterclusterservicelistnodetypes
    :param min_workers: an integer specifying the minimum node workers. Those parameters are limited by cluster policies.
    :param max_workers: an integer specifying the maximum node workers. Those parameters are limited by cluster policies.
    :return: a cluster id belonging to the cluster created or found with the given requirements

    :raises: HTTPError
    :raises: Exception
    """

    if db_workspace_uri is None or db_workspace_uri == "":
        raise ValueError("db_workspace_uri of " + str(db_workspace_uri) + " is not valid input.")
    if db_token is None or db_token == "":
        raise ValueError("databricks_token of " + str(db_token) + " is not valid input.")
    if cluster_name is None or cluster_name == "":
        raise ValueError("cluster_name of " + str(cluster_name) + " is not valid input.")
    if spark_version is None or spark_version == "":
        raise ValueError("spark_version of " + str(spark_version) + " is not valid input.")
    if node_type is None or node_type == "":
        raise ValueError("node_type of " + str(node_type) + " is not valid input.")

    try:
        result_cluster_id, result_cluster_status = get_cluster_id(cluster_name=cluster_name,
                                                                  db_workspace_uri=db_workspace_uri, db_token=db_token)
        return result_cluster_id
    except Exception as excp:
        print("While checking for the existence of a cluster, exception occurred.. ignoring: " + str(excp))

    full_uri = '%s/api/2.0/clusters/create' % db_workspace_uri

    json_dict = {
        "cluster_name": "%s" % cluster_name,
        "spark_version": "%s" % spark_version,
        "node_type_id": "%s" % node_type,
        "autoscale": {
            "min_workers": min_workers,
            "max_workers": max_workers
        },
        "spark_env_vars": {
            "PYSPARK_PYTHON": "/databricks/python3/bin/python3",
        }
    }

    response = execute_post_request(full_uri, db_token, json_dict)

    if response.status_code == 200:
        print(response.json()['cluster_id'])
        return response.json()['cluster_id']
    else:
        raise Exception("Error launching cluster: %s: %s" % (response.json()["error_code"], response.json()["message"]))


def get_cluster_id(db_workspace_uri: str, db_token: str, cluster_name: str):
    """
    Retrieve the cluster id based on the cluster name.  Uses the Clusters API List command

    See: https://docs.databricks.com/dev-tools/api/latest/clusters.html#list

    :param db_workspace_uri: The Databricks workspace URI to use for this API call.
    :param db_token: The Databricks personal token to use for this API call.
    :param cluster_name: The cluster name to retreive the id from.

    :return: A tuple containing the cluster id of the named cluster and its state
    """

    if db_workspace_uri is None or db_workspace_uri == "":
        raise ValueError("db_workspace_uri of " + str(db_workspace_uri) + " is not valid input.")
    if db_token is None or db_token == "":
        raise ValueError("databricks_token of " + str(db_token) + " is not valid input.")
    if cluster_name is None or cluster_name == "":
        raise ValueError("cluster_name of " + str(cluster_name) + " is not valid input.")

    full_uri = db_workspace_uri + "/api/2.0/clusters/list"

    response = execute_get_request(full_uri, db_token)

    for cluster in response.json()['clusters']:
        print("retrieving cluster id{} from : {}".format(cluster['cluster_id'], cluster['cluster_name']))
        if cluster['cluster_name'] == cluster_name:
            return cluster['cluster_id'], cluster['state']

    raise Exception("%s cluster_name not found", cluster_name)


def db_clusters_list(db_workspace_uri: str, db_token: str):
    """
    Retrieve the cluster list, uses the Clusters API List command

    See: https://docs.databricks.com/dev-tools/api/latest/clusters.html#list

    :param db_workspace_uri: The Databricks workspace URI to use for this API call.
    :param db_token: The Databricks personal token to use for this API call.

    :return: A tuple containing the cluster id of the named cluster and its state
    """

    if db_workspace_uri is None or db_workspace_uri == "":
        raise ValueError("db_workspace_uri of " + str(db_workspace_uri) + " is not valid input.")
    if db_token is None or db_token == "":
        raise ValueError("databricks_token of " + str(db_token) + " is not valid input.")

    full_uri = db_workspace_uri + "/api/2.0/clusters/list"

    response = execute_get_request(full_uri, db_token)

    for cluster in response.json()['clusters']:
        print("retrieving cluster id{} from : {}".format(cluster['cluster_id'], cluster['cluster_name']))
        return cluster['cluster_id'], cluster['state']

    raise Exception("clusters not found")


def db_clusters_start(db_workspace_uri: str, db_token: str, cluster_id: str):
    """
    Starts a cluster given the cluster id.

    See: https://docs.databricks.com/dev-tools/api/latest/clusters.html#start

    :param db_workspace_uri: The Databricks workspace URI to use for this API call.
    :param db_token: The Databricks personal token to use for this API call.
    :param cluster_id: The cluster id of the cluster to start.
    :return: The HTTP API Response if no error

    :raises: HTTPError
    """

    if db_workspace_uri is None or db_workspace_uri == "":
        raise ValueError("db_workspace_uri of " + str(db_workspace_uri) + " is not valid input.")
    if db_token is None or db_token == "":
        raise ValueError("databricks_token of " + str(db_token) + " is not valid input.")
    if cluster_id is None or cluster_id == "":
        raise ValueError("cluster_id of " + str(cluster_id) + " is not valid input.")

    full_uri = db_workspace_uri + "/api/2.0/clusters/start"
    json_dict = {
        "cluster_id": cluster_id
    }
    try:
        response = execute_post_request(full_uri, db_token, json_dict)
        return response
    except HTTPError as httperr:
        # When the cluster is in certain states, you will get a 400 error, which you must handle and discern if
        # it is okay to ignore.. or reraise if a real error
        if verify_safe_error_to_ignore(httperr):
            return httperr.response


def verify_safe_error_to_ignore(httperror):
    """
    This function checks if the API is telling us the cluster requested to start is already starting or running
    :param httperror:
    :return: True if we're already running or pending, otherwise raise original Exception
    """
    if "is in unexpected state Running" in httperror.response.text:
        print("The requested cluster appears to already be running.")
        return True
    elif "is in unexpected state Pending" in httperror.response.text:
        print("The requested cluster appears to trying to start..")
        return True
    else:
        print("Got a response we do not want or know how to handle.. ")
        raise httperror


def db_clusters_delete(db_workspace_uri: str, db_token: str, cluster_id: str):
    """
    This is a basic cluster deletion based on cluster id.

    :param db_workspace_uri: The Databricks workspace URI to use for this API call.
    :param db_token: The Databricks personal token to use for this API call.
    :param cluster_id: The cluster id of the cluster to delete.
    :return: The HTTP API Response if no error

    :raises: HTTPError
    """

    if db_workspace_uri is None or db_workspace_uri == "":
        raise ValueError("db_workspace_uri of " + str(db_workspace_uri) + " is not valid input.")
    if db_token is None or db_token == "":
        raise ValueError("db_token of " + str(db_token) + " is not valid input.")
    if cluster_id is None or cluster_id == "":
        raise ValueError("cluster_id of " + str(cluster_id) + " is not valid input.")

    full_uri = db_workspace_uri + "/api/2.0/clusters/delete"
    json_dict = {
        "cluster_id": cluster_id
    }
    print("deleting cluster {}".format(cluster_id))
    response = execute_post_request(full_uri, db_token, json_dict)
    return response


def db_clusters_deletebyname(db_workspace_uri: str, db_token: str, cluster_name: str):
    """
    This is a basic cluster deletion based on cluster name. It takes the first matching name. The function does not process list if a name matches multiple clusters.
    if unsure please use delete with cluster id instead.

    :param db_workspace_uri: The Databricks workspace URI to use for this API call.
    :param db_token: The Databricks personal token to use for this API call.
    :param cluster_id: The cluster name of the cluster to delete.
    :return: The HTTP API Response if no error

    :raises: HTTPError
    """
    if db_workspace_uri is None or db_workspace_uri == "":
        raise ValueError("db_workspace_uri of " + str(db_workspace_uri) + " is not valid input.")
    if db_token is None or db_token == "":
        raise ValueError("databricks_token of " + str(db_token) + " is not valid input.")
    if cluster_name is None or cluster_name == "":
        raise ValueError("cluster_name of " + str(cluster_name) + " is not valid input.")

    full_uri = db_workspace_uri + "/api/2.0/clusters/delete"
    cluster_id = get_cluster_id(db_workspace_uri, db_token, cluster_name)
    json_dict = {
        "cluster_id": cluster_id
    }
    print("deleting cluster {}".format(cluster_name))
    response = execute_post_request(full_uri, db_token, json_dict)
    return response
