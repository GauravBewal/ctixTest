import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of ingestion -->  Bulk action
'''

service = 'ingestion'

class BulkAction(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def get_list_of_object(self):
        object_ids = []
        for val in getJsonFileData('api_response_runtime/test_01_list_threat_data_runtime.json')["results"]:
            object_ids.append(val["id"])
        return object_ids

    def perform_action(self, test_case_name, action, payloads=""):
        print(f"----- Test Case: {test_case_name} -----")
        payload = payloads
        if payload == "":
            payload = getJsonFileData('api_payload/test_01_payload_bulk_action.json')
        else:
            payload = payloads

        # assumes that threat data object file is executed before
        object_ids = self.get_list_of_object()
        payload["object_ids"] = object_ids
        endpoint = f"/threat-data/bulk-action/{action}"

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', f'{test_case_name}_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/bulk_action/test_bulk_action_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_01_deprecate_indicator(self):
        self.perform_action("test_01_deprecate_indicator", "deprecate")

    def test_02_undeprecate_indicator(self):
        self.perform_action("test_02_undeprecate_indicator", "un_deprecate")

    def test_03_manual_reviewed_indicator(self):
        self.perform_action("test_03_manual_reviewed_indicator", "manual_review")

    def test_04_reviewed_indicator(self):
        self.perform_action("test_04_reviewed_indicator", "reviewed")

    def test_05_whitelist_indicator(self):
        self.perform_action("test_05_whitelist_indicator", "whitelist")

    def test_06_un_whitelist_indicator(self):
        self.perform_action("test_06_un_whitelist_indicator", "un_whitelist")

    def test_07_false_positive_indicator(self):
        self.perform_action("test_07_false_positive_indicator", "false_positive")

    def test_08_un_false_positive_indicator(self):
        self.perform_action("test_08_un_false_positive_indicator", "un_false_positive")

    def test_09_analyst_tlp(self):
        payload = getJsonFileData('api_payload/test_01_payload_bulk_action.json')
        payload["data"]["analyst_tlp"] = "GREEN"
        self.perform_action("test_09_analyst_tlp", "analyst_tlp", payload)

    def test_10_analyst_score(self):
        payload = getJsonFileData('api_payload/test_01_payload_bulk_action.json')
        payload["data"]["analyst_score"] = 47
        self.perform_action("test_10_analyst_score", "analyst_score", payload)

    def test_11_add_tag(self):
        # creating a tag
        payload = getJsonFileData('api_payload/test_01_create_tags.json')
        endpoint = "/tags"
        url = f"{base_url}{service}{endpoint}"
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code of creating tag is  : {response.status_code}")
        print(response.text)
        res = json.loads(response.text)
        # ends here

        payload1 = getJsonFileData('api_payload/test_01_payload_bulk_action.json')
        payload1["data"]["tag_id"] = [res["id"]]
        self.perform_action("test_11_add_tag", "add_tag", payload1)
        # deleting the tag here
        endpoint = f"/tags/{res['id']}"
        url = f"{base_url}{service}{endpoint}"
        requests.delete(f"{url}/{authentication()}")
        # ends here

    def test_12_watchlist_indicator(self):
        res = getJsonFileData('api_response_runtime/test_01_list_threat_data_runtime.json')["results"]
        name = []
        for val in res:
            name.append(val["name"])
        payload1 = getJsonFileData('api_payload/test_01_payload_bulk_action.json')
        payload1["data"]["name"] = name
        self.perform_action("test_12_watchlist_indicator", "watchlist", payload1)

    def test_13_un_watchlist_indicator(self):
        res = getJsonFileData('api_response_runtime/test_01_list_threat_data_runtime.json')["results"]
        name = []
        for val in res:
            name.append(val["name"])
        payload1 = getJsonFileData('api_payload/test_01_payload_bulk_action.json')
        payload1["data"]["name"] = name
        self.perform_action("test_13_un_watchlist_indicator", "un_watchlist", payload1)

    def test_14_analyst_description(self):
        payload = getJsonFileData('api_payload/test_01_payload_bulk_action.json')
        payload["data"]["analyst_description"] = "This is API automation description"
        self.perform_action("test_14_analyst_description", "analyst_description", payload)

    def test_15_delete_bulk(self):
        self.perform_action("test_15_delete_bulk", "delete")

if __name__ == '__main__':
    unittest.main(testRunner=reporting())