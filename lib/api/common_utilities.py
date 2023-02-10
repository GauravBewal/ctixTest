import hmac
import json
import urllib
from base64 import urlsafe_b64encode, b64encode
# from hashlib import sha1
from lib.common_functions import *
# from PROJECTS.API import creds
import hashlib
from jsonschema import validate

ctix_creds = get_credentials("ctix")
base_url = ctix_creds["base_url"]
access_id = ctix_creds["access_id"]
secret_key = ctix_creds["secret_key"]
csol_creds = get_credentials("csol")
csol_base_url = csol_creds["base_url"]
csol_access_id = csol_creds["access_id"]
csol_secret_key = csol_creds["secret_key"]
csap_creds = get_credentials("csap")
csap_base_url = csap_creds["base_url"]
csap_access_id = csap_creds["access_id"]
csap_secret_key = csap_creds["secret_key"]

def csol_authenticator():
    """
    return: authenticator
    This function will use suitable algorithm and generate the authenticator for the api
    Access id and secret key can be generated from the integration management and also via api
    """
    expires = int(datetime.datetime.now().timestamp()) + 10
    to_sign = "%s\n%i" % (csol_access_id, expires)

    signature = b64encode(
        hmac.new(
            csol_secret_key.encode("UTF-8"), to_sign.encode("UTF-8"), hashlib.sha1
        ).digest()
    ).decode("UTF-8")
    lis = {
        "Expires" : expires,
        "AccessID" : csol_access_id,
        "Signature" : signature
    }

    authenticator = "?" + urllib.parse.urlencode(lis)
    return authenticator


def authentication():
    expires = int(datetime.datetime.now().timestamp()) + 10
    to_sign = "%s\n%i" % (access_id, expires)

    signature = b64encode(
        hmac.new(
            secret_key.encode("UTF-8"), to_sign.encode("UTF-8"), hashlib.sha1
        ).digest()
    ).decode("UTF-8")
    lis = {
        "Expires" : expires,
        "AccessID" : access_id,
        "Signature" : signature
    }

    authenticator = "?" + urllib.parse.urlencode(lis)
    return authenticator


def csap_authenticator():
    """
    This function will use suitable algorithm and generate the authenticator for the csap api
        return: authenticator
    """
    expires = int(datetime.datetime.now().timestamp()) + 10
    to_sign = "%s\n%i" % (csap_access_id, expires)

    signature = b64encode(
        hmac.new(
            csap_secret_key.encode("UTF-8"), to_sign.encode("UTF-8"), hashlib.sha1
        ).digest()
    ).decode("UTF-8")
    lis = {
        "Expires" : expires,
        "AccessID" : csap_access_id,
        "Signature" : signature
    }

    authenticator = "?" + urllib.parse.urlencode(lis)
    return authenticator

# def authentication():
#     """
#     parameter access_id:
#     parameter secret_key:
#     return: authenticator
#     This function will use suitable algorithm and generate the authenticator for the api
#     Access id and secret key can be generated from the integration management and also via api
#     """
#     access_id = creds.credentials["access_id"]
#     secret_key = creds.credentials["secret_key"].encode("UTF-8")
#     signature = "+"
#     expires = int(datetime.datetime.now().timestamp()) + 10
#     while signature.__contains__('+'):
#         expires = int(datetime.datetime.now().timestamp()) + 10
#         string_to_sign = (access_id + "\n" + str(expires)).encode("UTF-8")
#         signature = b64encode(hmac.new(secret_key, string_to_sign, sha1).digest()).decode("utf-8")
#         # print(signature)
#
#     authenticator = f"?Expires={expires}&AccessID={access_id}&Signature={signature}"
#     return authenticator


def compare_responses(response, stored_response_file_name, ignore_params={}):
    """
    parameter: response(This is the current response received from api call)
    parameter: stored_response_file_name (This is the file name with which a particular response is saved)
    parameter: ignore_params(This is list of attributes which can be ignored during comparison of the responses)
    return: True/False
    This function helps in comparing the two api responses
    """
    # opening the response file for validating the response got
    if ignore_params is None:
        ignore_params = {}
    file_name = os.path.join(os.environ["PYTHONPATH"], "testdata",f"api_response/{stored_response_file_name}.json")
    f = open(file_name)
    # This will load json file as a dict object
    data = json.load(f)
    f.close()
    # This will load json file as a dict object
    json_format = json.loads(response.text)

    print(f"Expected Response : {data}")
    print(f"Received Response : {json_format}")
    # Calling helper function that will help in comparing different type of objects
    if compare_object(json_format, data, ignore_params):
        return True
    else:
        return False


def compare_object(a, b, ignore_params):
    if type(a) != type(b):
        return False
    elif type(a) is dict:
        return compare_dict(a, b, ignore_params)
    elif type(a) is list:
        return compare_list(a, b, ignore_params)
    else:
        return a == b


def compare_dict(a, b, ignore_params):
    if len(a) != len(b):
        print("Failed due to difference in length of dictionaries")
        return False
    else:
        for k, v in a.items():
            if not k in b:
                print(f"Failed because key {k} is not present stored response")
                return False
            else:
                if k in ignore_params:
                    continue
                if not compare_object(v, b[k], ignore_params):
                    print(f"Values mismatch, For key '{k}':  {v} is received and {b[k]} is expected")
                    return False
    return True


def compare_list(a, b, ignore_params):
    if len(a) != len(b):
        print("Failed due to difference in length of list")
        return False
    else:
        for i in range(len(a)):
            if not compare_object(a[i], b[i], ignore_params):
                return False
    return True


def list_of_values(response, attribute, ignore_params={}):
    """
     parameter: response(json format - response from which values will be picked)
     parameter: attribute(string - attribute name for which values to be fetched)
     parameter: ignore_params:(list - values in string)
     return list of values of particular attribute
     This function helps in finding the list of values of particular attribute
    """
    result = []
    if type(response) is list:
        temp = get_value_from_list(response, attribute, ignore_params)
        for val in temp:
            result.append(val)
    if type(response) is dict:
        temp = get_value_from_dict(response, attribute, ignore_params)
        for val in temp:
            result.append(val)
    return result

def get_value_from_list(response, attribute, ignore_params):
    result = []
    for i in response:
        if type(i) is dict:
            temp = get_value_from_dict(i, attribute, ignore_params)
            for val in temp:
                result.append(val)
        if type(i) is list:
            temp = get_value_from_list(i, attribute, ignore_params)
            for val in temp:
                result.append(val)
    return result

def get_value_from_dict(response, attribute, ignore_params):
    result = []
    for k, v, in response.items():
        if k in ignore_params:
            continue
        if type(v) is dict:
            temp = get_value_from_dict(v, attribute, ignore_params)
            for val in temp:
                result.append(val)
        if type(v) is list:
            temp = get_value_from_list(v, attribute, ignore_params)
            for val in temp:
                result.append(val)
        if k == attribute:
            result.append(v)
    return result


def getJsonFileData(filepath):
    """
    param filepath: (string : path should be within the foldr testdata
    return: content of the response file in json format

    """
    file_name = os.path.join(os.environ["PYTHONPATH"], "testdata", f"{filepath}")
    f = open(file_name)
    # This will load json file as a dict object
    data = json.load(f)
    f.close()
    return data

def save_runtime_response(directory, filename, response):
    '''
    parameter directory (string - directory name ex - testdata/api_response)
    parameter filename: (string - filename format is fixed as json)
    parameter response:
    return:
    '''
    filepath = os.path.join(os.environ["PYTHONPATH"], f"{directory}",f'{filename}.json')
    with open(filepath, "w") as outfile:
        json.dump(json.loads(response.text), outfile, indent=2)

def validate_schema(response, schema_file):
    schema = getJsonFileData(f'api_schema/{schema_file}.json')
    response = json.loads(response.text)

    try:
        validate(instance=response, schema=schema)
        log("Schema is valid")
        return True
    except Exception as e:
        log("Invalid Schema")
        log(e)
        return False


def log(text):
    print(text)
    print("<hr>")
