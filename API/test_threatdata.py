from urllib.parse import quote
import requests
from lib.api.common_utilities import *


def get_filter_count(payload):
    print("----- Test Case: test_01_validate_status_code_rules_json -----")
    print(payload)
    endpoint = "/threat-data/list/"
    url = f"{base_url}ingestion{endpoint}"
    print(f'Making the get request for the {url}')
    print("Calling authentication function for getting the unique authenticator")
    main_url = f"{url}{authentication()}&page=1&page_size=100&page_limit=100"
    response = requests.post(main_url, json=payload)
    print(f"response code is : {response.status_code}")
    print(response.json())
    return response.json()["total"]


def get_source_id(source_name):
    """
        Function to get id of the provided source
    """
    endpoint = "/feed-sources/"
    url = f"{base_url}conversion{endpoint}"
    query = f"&page=1&page_size=8&nominal=true&q={urllib.parse.quote(source_name)}"
    print(f'Making the get request for the {url}')
    print("Calling authentication function for getting the unique authenticator")
    print(f"{url}{authentication()}{query}")
    response = requests.get(f"{url}{authentication()}{query}")
    print(f"response code is : {response.status_code}")
    return response.json()["results"][0]["id"]


def get_collection_id(collection_name):
    """
        Function to get collection id of the provided collection
    """
    print("collection - ", collection_name)
    endpoint = "/feed-sources/collection/"
    url = f"{base_url}conversion{endpoint}"
    param = {
        "page": 1,
        "page_size": 8,
        "nominal": True,
        "q": collection_name
    }
    print(f'Making the get request for the {url}')
    print("Calling authentication function for getting the unique authenticator")
    print(f"{url}{authentication()}")
    response = requests.get(f"{url}{authentication()}", params=param)
    print("res - ", response.text)
    print(f"response code is : {response.status_code}")
    return json.loads(response.text)["results"][0]["id"]

