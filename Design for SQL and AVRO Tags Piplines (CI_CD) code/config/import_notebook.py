import requests
import fnmatch
import os
import argparse

from utils import const
from core.db_api_client import execute_post_request, execute_post_request_for_files
from utils.paths import create_full_target_path


def db_wkspace_mdkir(db_workspace_uri, db_token, path_to_mkdir):
    """
    This function takes in a path_to_create string, and attempts to create that path under the databricks workspace
    given by db_workspace_uri via the Databricks token db_token.

    See: https://docs.databricks.com/dev-tools/api/latest/workspace.html#mkdirs

    :param db_workspace_uri: The Databricks workspace URI to use for this API call.
    :param db_token: The Databricks personal token to use for this API call.
    :param path_to_mkdir: workspace path to create the new directory.
    :return: returns the REST response if no error

    :raises: HTTPError
    """
    print("dbfs_mdkir(): starting...")

    full_uri = db_workspace_uri + "/api/2.0/workspace/mkdirs"
    json_dict = {
                    "path": path_to_mkdir
                }

    response = execute_post_request(full_uri, db_token, json_dict)
    print("dbfs_mkdir(): Complete, returning response.")
    return response


def db_wkspace_import(db_workspace_uri, db_token, source_file, target_file, language='SQL'):
    """
    This function imports the notebook or lang file to a specified databricks workspace directory

    See: https://docs.databricks.com/dev-tools/api/latest/workspace.html#import

    :param db_workspace_uri: The Databricks workspace URI to use for this API call.
    :param db_token: The Databricks personal token to use for this API call.
    :param source_file: a posix path to a notebook file.
    :param target_file: a workspace path.
    :param language: This is the language of the notebook.  In most cases Python.
    :return: returns the REST response if no error

    :raises: ValueError
    :raises: HTTPError
    """
    print("db_wkspace_import(): starting...")
    if db_workspace_uri is None or db_workspace_uri == "":
        raise ValueError("db_workspace_uri of " + str(db_workspace_uri) + " is not valid input.")
    if db_token is None or db_token == "":
        raise ValueError("db_token of " + str(db_token) + " is not valid input.")
    if target_file is None or target_file == "":
        raise ValueError("target_file of " + str(target_file) + " is not valid input.")
    if source_file is None or source_file == "":
        raise ValueError("source_path of " + str(source_file) + " is not valid input.")

    uri = db_workspace_uri + "/api/2.0/workspace/import"
    json_dict = {
        "language": "%s" % language,
        "overwrite": "true",
        "path": "%s" % target_file,
    }
    # Does not handle a list
    files = {'{}'.format(source_file.split('/')[-1]): open('{}'.format(source_file), 'rb')}

    print("db_wkspace_import(): file to be imported : {}".format(files))
    response = execute_post_request_for_files(uri, db_token, data_dict=json_dict, files=files)
    print("db_wkspace_import(): Complete, returning response.")
    return response

def notebook_copy():
    """
    This is the Main function called on by consuming pipelines, including pipelines/template_stage_model_train.yml

    :param db_workspace_uri: The Databricks workspace URI to use for this API call.
    :param db_token: The Databricks personal token to use for this API call.
    :param source_nb_dir: The file path from which you want to copy the notebook(s)
    :param target_nb_dir: The workspace path into which you want to copy the notebook(s).  Ex: /Shared/use_case/...
    :param language: Select which file will be copied. Valid values (PYTHON, SCALA)

    :return: void

    :raises: ValueError on Bad Inputs
    :raises: HTTPError on Non-200 HTTP Error codes
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-workspace_uri")
    parser.add_argument("-token")
    parser.add_argument("-source_file")
    parser.add_argument("-target_file")

    args = parser.parse_args()


    db_workspace_uri =  args.workspace_uri
    db_token         =  args.token
    source_nb_dir    =  args.source_file
    target_nb_dir    =  args.target_file
    language='SQL'

    db_workspace_uri = str(db_workspace_uri)
    db_token        = str(db_token)
    source_nb_dir   = str(source_nb_dir)
    target_nb_dir   = str(target_nb_dir)

    print("notebook_copy(): starting...")
    if db_workspace_uri is None or db_workspace_uri == "":
        raise ValueError("db_workspace_uri of " + str(db_workspace_uri) + " is not valid input.")
    if db_token is None or db_token == "":
        raise ValueError("databricks_token of " + str(db_token) + " is not valid input.")
    if target_nb_dir is None or target_nb_dir == "":
        raise ValueError("target_nb_dir of " + str(target_nb_dir) + " is not valid input.")
    if source_nb_dir is None or source_nb_dir == "":
        raise ValueError("source_nb_dir of " + str(source_nb_dir) + " is not valid input.")

    print("notebook_copy(): db_workspace_uri : {}".format(db_workspace_uri))
    # Create the Root Dir

    db_wkspace_mdkir(db_workspace_uri=db_workspace_uri, db_token=db_token, path_to_mkdir=target_nb_dir)

    # TODO: Recursion of sub-dirs is necessary.  Right now we only copy over files 1 sub-dir deep
    # SEE: https://docs.python.org/3/library/os.html#os.walk
    for root, dirs, files in os.walk(source_nb_dir):

        for dir in dirs:
            cleaned_dir = create_full_target_path(root, dir, source_nb_dir, target_nb_dir)
            print("notebook_copy(): Creating the directory : {}".format(cleaned_dir))
            db_wkspace_mdkir(db_workspace_uri=db_workspace_uri, db_token=db_token, path_to_mkdir=cleaned_dir)

        for f in files:
            if f.endswith('.{}'.format(const.file_format['SQL'])):
                target_file_path = create_full_target_path(root, f, source_nb_dir, target_nb_dir, drop_extensions=True)
                source_file = root.replace('\\', '/') + '/' + f
                print("notebook_copy(): Source file {}".format(source_file))
                db_wkspace_import(
                    db_workspace_uri=db_workspace_uri,
                    db_token=db_token,
                    language=language,
                    target_file=target_file_path,
                    source_file=source_file
                )
        print("notebook_copy(): copy_notebook completed.")








if __name__ == '__main__':
    notebook_copy()



