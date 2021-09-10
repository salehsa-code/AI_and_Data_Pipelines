import os
import fnmatch
import yaml

from swb.mlops.db.batch_model import create_start_cluster
from swb.mlops.db.batch_model import const
from swb.mlops.db.core.db_api_client import execute_post_request


def find_file(directory='.', file_format='pip') -> list:
    """
    Return a list of files based on the directory parameter and the file_format.

    :param directory: source code directory
    :param file_format: conda or pip
    :return: file as a list.
    """
    print("looking for requirement file in directory {}".format(directory))
    result = []
    for file in os.listdir(directory):
        if fnmatch.fnmatch(file, const.package_format[file_format]):
            result.append(file)
    if result == []:
        raise ValueError('No requirement file found in directory with the format specified {}'.format(file_format))
    print("found files : {}".format(result))
    return result


def convert_file_to_db(directory: str, file_format='pip'):
    """
    Converts a pip requirement file or a conda environment python dependencies to a list of tuple required by databricks.
    :param directory: A posix directory containing the pip or conda files.
    :param file_format: Valid values : conda, pip.

    :return:

    :raises: ValueError
    """
    file_req = ''.join(find_file(directory=directory, file_format=file_format))
    print('reading file : {}'.format(os.path.join(directory , file_req)))
    json = {"libraries": []}
    if file_format == 'pip':
        with open(directory + ''.join(file_req)) as f:
            for line in f:
                val = {"pypi": {"package": line}}
                json["libraries"].append(val)
        return json
    if file_format == 'conda':
        path_to_conda = os.path.join(directory, file_req)
        with open(path_to_conda) as f:
            dependencies = yaml.load(f)['dependencies'][0]['pip']
            if dependencies is not [] or dependencies is not None:
                print(dependencies)
                for pack in dependencies:
                    val = {"pypi": {"package": pack}}
                    json["libraries"].append(val)
                return json
            else:
                print('There are no pip dependencies')
    else:
        raise ValueError("Unexpected input on file_format, expected 'pip' or 'conda' but got " + str(file_format))


def db_libraries_install(db_workspace_uri: str, db_token: str, cluster_name: str, directory, file_format):
    """
    perform the post to install libraries onto clusters

    See: https://docs.databricks.com/dev-tools/api/latest/libraries.html#install

    :param db_workspace_uri: The Databricks workspace URI to use for this API call.
    :param db_token: The Databricks personal token to use for this API call.
    :param cluster_name: Name of the cluster to install additional libraries to.
    :param directory: where to look for the requirements.txt
    :param file_format: conda or pip.
    :return: HTTP API Response if no errors
    """

    libraries_to_install = convert_file_to_db(directory=directory, file_format=file_format)
    cluster_id = create_start_cluster.get_cluster_id(cluster_name=cluster_name,
                                                     db_workspace_uri=db_workspace_uri,
                                                     db_token=db_token)

    full_uri = db_workspace_uri + '/api/2.0/libraries/install'

    json_dict = {
        "cluster_id": "{}".format(cluster_id[0]),
        "libraries": libraries_to_install["libraries"]

    }

    response = execute_post_request(full_uri, db_token, json_dict)
    return response