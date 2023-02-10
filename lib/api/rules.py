import requests
from lib.api.common_utilities import *
from lib.common_functions import *


def get_rule_id(rule_name):
    print("Function to get id of the rule name provided")
    endpoint = "/rules/"
    query = f"&page=1&page_size=10&q={rule_name}"
    url = f"{base_url}ingestion{endpoint}"
    print(f'Getting list of rules : {url}')
    response = requests.get(f"{url}{authentication()}{query}")
    print(f"response code is : {response.status_code}")
    print(f"Rule id for {rule_name} is "+response.json()["results"][0]["id"])
    return response.json()["results"][0]["id"]


def run_rule_delta(rule_name, **kwargs):
    """
        Function to run rule on specified date range
    """
    endpoint = "/rules/one-rule/"
    rule_id = get_rule_id(rule_name)
    delta = kwargs.get("delta", None)
    start_time = kwargs.get("start_time", None)
    end_time = kwargs.get("end_time", None)
    if delta:
        end_time = str(int(time.time()))
        start_time = str(int(end_time) - int(delta) * (86400))
    print(rule_id)
    query = f"&rule={rule_id}&start_time={start_time}&end_time={end_time}"
    url = f"{base_url}ingestion{endpoint}"
    print(f'Running rule on date range : {url}')
    response = requests.get(f"{url}{authentication()}{query}")
    print(f"response code is : {response.status_code}")
    return start_time, end_time


def enable_rule(rule_name):
    """
        Function to enable provided rule
    """
    rule_id = get_rule_id(rule_name)
    endpoint = f"/rules/{rule_id}/"
    url = f"{base_url}ingestion{endpoint}"
    print(f"Enabling Rule : {rule_name} of id {rule_id}")
    requests.put(url=f"{url}{authentication()}", json={"status":"ACTIVE"})


def disable_rule_api(rule_name):
    """
        Function to enable provided rule
    """
    rule_id = get_rule_id(rule_name)
    endpoint = f"/rules/{rule_id}/"
    url = f"{base_url}ingestion{endpoint}"
    print(f"Disabling Rule : {rule_name} of id {rule_id}")
    requests.put(url=f"{url}{authentication()}", json={"status":"INACTIVE"})


def run_all_rules(pattern):
    """
        Function to run all rules matching the pattern:
        args:
            pattern: pattern found in all rule names to be run
    """
    print("Function to get ids of all rules matching pattern in name")
    endpoint = "/rules/"
    end_time = str(int(time.time()))
    start_time = str(int(end_time)-int(2)*(86400))
    set_value("client_start_time", start_time)
    set_value("client_end_time", end_time)
    query = f"&page=1&page_size=100&q={pattern}"
    url = f"{base_url}ingestion{endpoint}"
    print(f'Getting list of rules : {url}')
    response = requests.get(f"{url}{authentication()}{query}")
    print(f"response code is : {response.status_code}")
    for i in response.json()["results"]:
        try:
            print(f"Running {i['name']} with id {i['id']}")
            enable_rule(i["name"])
            run_rule_delta(i["name"], start_time=start_time, end_time=end_time)
            disable_rule_api(i["name"])
        except:
            print(f"Operations failed to be performed on {i['name']}")
