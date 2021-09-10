import json
from json import JSONDecodeError


def verify_data_dict(incoming_string):
    """
    The purpose of this function is merely to test if a json_string is valid json, and print a clear Exception if not

    :param incoming_string: The variable we want verified before sending out.
    :return:

    :raises: JSONDecodeError
    """
    try:
        json.loads(incoming_string)
    except JSONDecodeError as json_excp:
        print("JSONDecodeError occurred on incoming_string: " + str(incoming_string) + ", please correct and try again. " + str(json_excp))
        raise json_excp
    except TypeError as type_error:
        print("TypeError occurred on incoming_string: " + str(incoming_string) + ", please make sure you're sending a string and try again." + str(type_error))
        raise type_error


def verify_json_dict(incoming_dict):

    try:
        json.dumps(incoming_dict)
    except Exception as excp:
        print("Exception occurred on incoming_dict: " + str(incoming_dict) + ", please make sure you're sending a dictionary as JSON and try again. " + str(excp))
        raise excp


def verify_full_url_string(incoming_string):
    # No http (non-tls) traffic is expected through this API client
    assert("https://" in incoming_string)