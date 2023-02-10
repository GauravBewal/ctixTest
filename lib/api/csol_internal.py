import requests
from lib.api.common_utilities import *


def get_event_ids(label_name, page=1):
    """
        Function to obtain unique_id of the event
        params:
            event_name: name of the event to be searched
        returns:
            unique_id: id of the provided event in CSOL
    """
    endpoint = '/soarapi/openapi/v1/events/'
    event_ids = []
    url = f"{csol_base_url}{endpoint}"
    print(f'Making the get request for the {csol_base_url}')
    print("Calling authentication function for getting the unique authenticator")
    query = f"&labels={label_name}&page_size=100000&page={page}"
    print(f"==================== {page} =======================\n\n\n")
    print(f"{url}{csol_authenticator()}{query}")
    response = requests.get(f"{url}{csol_authenticator()}{query}")
    print(f"Validating response and fetching unique id for label - {label_name}")
    print(f"response code is : {response.status_code}")
    print(response.text)
    event_ids.extend([i["unique_id"] for i in response.json()["results"]])
    if response.json()["link"] is None:
        pass
    elif "next" in response.json()["link"].keys():
        event_ids.extend(get_event_ids(label_name=label_name, page=page+1))
    print(len(event_ids))
    return event_ids


def get_event_count(event_id):
    """
        Function to return count of intel based on event id
    """
    endpoint = f'/soarapi/openapi/v1/events/{event_id}/'
    url = f"{csol_base_url}{endpoint}"
    print(f'Making the get request to get event count {csol_base_url}')
    print(f"{url}/{csol_authenticator()}")
    response = requests.get(f"{url}{csol_authenticator()}")
    print(f"response code is : {response.status_code}")
    if type(response.json()["data"]) == list:
        return len(response.json()["data"])
    return 0
