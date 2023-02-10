import hmac
import json
import requests
from lib.api.common_utilities import *
from base64 import urlsafe_b64encode
from base64 import urlsafe_b64encode, b64encode
from hashlib import sha1
from lib.common_functions import *


def get_tag_id(tag_name):
    print("Function to get id of the tag name provided")
    endpoint = "/tags/"
    query = f"&page=1&page_size=10&q={tag_name}"
    url = f"{base_url}ingestion{endpoint}"
    print(f'Getting id for tag {tag_name} : {url}')
    response = requests.get(f"{url}{authentication()}{query}")
    print(f"response code is : {response.status_code}")
    print(response.json())
    return response.json()["results"][0]["id"]

