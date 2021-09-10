import requests

from utils.verifiers import verify_data_dict, verify_full_url_string, verify_json_dict


def execute_post_request_for_files(full_uri, db_token, data_dict, files=None):
    """


    :param full_uri: The full URI of the POST request
    :param db_token: Bearer token to use
    :param data_dict: Data input for POST, must be dict
    :param files: Optionally POST files

    :return: The POST HTTP response if no error

    :raises: HTTPError
    """
    verify_full_url_string(full_uri)

    headers = {'Authorization': 'Bearer %s' % db_token}  # Must be a dictionary

    verify_data_dict(str(data_dict).replace("\'", "\""))  # Plain STR of dict will not yield JSON. Needs Dbl Quotes

    try:
        if files is None:
            raise ValueError("This function is only for sending files via POST.  but files was None.")
        else:
            # IS there a way to verify files one last time?
            response = requests.post(url=full_uri, headers=headers, data=data_dict, files=files)
            response.raise_for_status()
            return response
    except requests.exceptions.HTTPError as http_error:
        print("[POST] URI=\'" + str(full_uri) + "\' json_data=\'" + str(data_dict) + "\' got exception " + str(http_error))
        raise http_error


def execute_post_request(full_uri, db_token, json_dict_input):
    """


    :param full_uri: The full URI of the POST request
    :param db_token: Bearer token to use
    :param json_dict_input: A Dict expected to be ready to turn into JSON string

    :return: The POST HTTP response if no error

    :raises: HTTPError
    """
    verify_full_url_string(full_uri)

    verify_json_dict(json_dict_input)

    headers = {
        "Authorization": "Bearer " + db_token
    }  # Must be a dictionary

    try:
        response = requests.post(url=full_uri, headers=headers, json=json_dict_input)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as http_error:
        print("[POST] URI=\'" + str(full_uri) + "\' json_input=\'" + str(json_dict_input) + "\' got HTTPError: " + str(http_error))
        raise http_error


def execute_get_request(full_uri, db_token):
    verify_full_url_string(full_uri)

    headers = {"Authorization": "Bearer " + db_token}  # Must be a dictionary

    try:
        response = requests.get(url=full_uri, headers=headers)
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as http_error:
        print("[GET] URI \'" + str(full_uri) + "\' got exception " + str(http_error))
        raise http_error
