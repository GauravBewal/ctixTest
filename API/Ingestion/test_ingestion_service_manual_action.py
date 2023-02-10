import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of ingestion -->  Manual action
'''

service = 'ingestion'
obj_id = []

class ManualAction(unittest.TestCase):

    object_id = ""

    @classmethod
    def setUpClass(self):
        pass

    def get_object_id(self):
        endpoint = "/quick-intel/create-stix"
        payload ={
                 "create_intel_feed": True,
                 "indicators": {"ipv4-addr": "231.2.19.92"},
                 "metadata": {
                 "confidence": 70,
                 "tlp": "RED",
                 "description": "This is created via-api for manual action"
                 },
                 "parsed_indicators": {},
                 "custom_objects": {},
                 "title": "API_Manual_Action"
                }
        url = f"{base_url}conversion{endpoint}"
        temp = requests.post(f"{url}/{authentication()}", json=payload)
        print(temp.status_code)
        print(temp.text)
        sleep(10)

        payload = getJsonFileData('api_payload/test_01_list_threat_data.json')
        endpoint = "/threat-data/list"
        param = {
            "page": 1,
            "page_size": 20,
            "page_limit": 100
        }
        url = f"{base_url}{service}{endpoint}"
        response = requests.post(f"{url}/{authentication()}", json=payload, params=param)
        print(f"This is status code for creating the intel {response.status_code}")
        print(f"This is response for creating the intel {response.text}")
        for val in json.loads(response.text)["results"]:
            if val["name"] == "231.2.19.92":
                obj_id.append(val["id"])
                break
        print(obj_id)

    def perform_action(self, test_case_name, action, payloads=""):
        print(f"----- Test Case: {test_case_name} -----")
        payload = payloads
        if payload == "":
            payload = getJsonFileData('api_payload/test_01_payload_manual_action.json')
        else:
            payload = payloads

        # assumes that threat data object file is executed before
        if len(obj_id) == 0:
            self.get_object_id()

        payload["object_id"] = obj_id[0]
        endpoint = f"/threat-data/action/{action}"

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', f'{test_case_name}_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/manual_action/test_manual_action_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_01_manual_deprecate_indicator(self):
        self.perform_action("test_01_manual_deprecate_indicator", "deprecate")

    def test_02_manual_undeprecate_indicator(self):
        self.perform_action("test_02_manual_undeprecate_indicator", "un_deprecate")

    def test_03_mnl_manual_reviewed_indicator(self):
        self.perform_action("test_03_mnl_manual_reviewed_indicator", "manual_review")

    def test_04_mnl_reviewed_indicator(self):
        self.perform_action("test_04_mnl_reviewed_indicator", "reviewed")

    def test_05_manual_whitelist_indicator(self):
        self.perform_action("test_05_manual_whitelist_indicator", "whitelist")

    def test_06_manual_un_whitelist_indicator(self):
        self.perform_action("test_06_manual_un_whitelist_indicator", "un_whitelist")

    def test_07_manual_false_positive_indicator(self):
        self.perform_action("test_07_manual_false_positive_indicator", "false_positive")

    def test_08_manual_un_false_positive_indicator(self):
        self.perform_action("test_08_manual_un_false_positive_indicator", "un_false_positive")

    def test_09_manual_analyst_tlp(self):
        payload = getJsonFileData('api_payload/test_01_payload_manual_action.json')
        payload["data"]["analyst_tlp"] = "GREEN"
        self.perform_action("test_09_manual_analyst_tlp", "analyst_tlp", payload)

    def test_10_manual_analyst_score(self):
        payload = getJsonFileData('api_payload/test_01_payload_manual_action.json')
        payload["data"]["analyst_score"] = 47
        self.perform_action("test_10_manual_analyst_score", "analyst_score", payload)

    def test_11_manual_add_tag(self):
        # creating a tag
        payload = getJsonFileData('api_payload/test_01_create_tags.json')
        endpoint = "/tags"
        url = f"{base_url}{service}{endpoint}"
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code of creating tag is  : {response.status_code}")
        print(response.text)
        res = json.loads(response.text)
        # ends here

        payload1 = getJsonFileData('api_payload/test_01_payload_manual_action.json')
        payload1["data"]["tag_id"] = [res["id"]]
        self.perform_action("test_11_manual_add_tag", "add_tag", payload1)
        # deleting the tag here
        endpoint = f"/tags/{res['id']}"
        url = f"{base_url}{service}{endpoint}"
        requests.delete(f"{url}/{authentication()}")
        # ends here

    def test_12_manual_watchlist_indicator(self):
        res = getJsonFileData('api_response_runtime/test_01_list_threat_data_runtime.json')["results"]
        name = []
        for val in res:
            name.append(val["name"])
        payload1 = getJsonFileData('api_payload/test_01_payload_manual_action.json')
        payload1["data"]["name"] = name
        self.perform_action("test_12_manual_watchlist_indicator", "watchlist", payload1)

    def test_13_manual_un_watchlist_indicator(self):
        res = getJsonFileData('api_response_runtime/test_01_list_threat_data_runtime.json')["results"]
        name = []
        for val in res:
            name.append(val["name"])
        payload1 = getJsonFileData('api_payload/test_01_payload_manual_action.json')
        payload1["data"]["name"] = name
        self.perform_action("test_13_manual_un_watchlist_indicator", "un_watchlist", payload1)

    def test_14_manual_analyst_description(self):
        payload = getJsonFileData('api_payload/test_01_payload_manual_action.json')
        payload["data"]["analyst_description"] = "This is API automation description"
        self.perform_action("test_14_manual_analyst_description", "analyst_description", payload)

    def test_15_manual_delete(self):
        self.perform_action("test_15_manual_delete", "delete_sdo")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())