import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of ingestion --> Threat Data Overview
Threat data objects cases needs to be run before these cases
'''

service = 'ingestion'

class ThreatDataOverview(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def get_object_id(self, ob_type):
        object_id = getJsonFileData('api_response_runtime/test_01_list_threat_data_runtime.json')["results"][0][ob_type]
        return object_id

    def test_01_quick_view_card_details(self):
        print("----- Test Case: test_01_quick_view_card_details -----")
        object_id = self.get_object_id("id")
        endpoint = f"/threat-data/indicator/{object_id}/quick_card"

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_01_quick_view_card_details_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/threat_data_overview/test_01_quick_view_card_details_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_02_action_card(self):
        print("----- Test Case: test_02_action_card -----")
        object_id = self.get_object_id("id")
        endpoint = f"/actions"
        param = {
            "page":1,
            "page_size":2,
            "object_id":object_id,
            "object_type":"indicator",
            "layout":"overview"
        }
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_02_action_card_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/threat_data_overview/test_02_action_card_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_03_task_card(self):
        print("----- Test Case: test_03_task_card -----")
        object_id = self.get_object_id("id")
        endpoint = f"/tasks"
        param = {
            "page":1,
            "page_size":2,
            "object_id":object_id,
            "object_type":"indicator",
            "layout":"overview"
        }
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_03_task_card_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/threat_data_overview/test_03_task_card_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_04_custom_attributes_card(self):
        print("----- Test Case: test_04_custom_attributes_card -----")
        object_id = self.get_object_id("id")
        object_type = self.get_object_id("type")

        endpoint = f"/threat-data/{object_type}/{object_id}/custom_attributes"

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_04_custom_attributes_card_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/threat_data_overview/test_04_custom_attributes_card_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_05_source_details_card(self):
        print("----- Test Case: test_05_source_details_card -----")
        object_id = self.get_object_id("id")
        ioc_type = self.get_object_id("type")
        endpoint = f"/threat-data/{ioc_type}/{object_id}/source_details"
        param = {
            "page": 1,
            "page_size": 2
        }
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_05_source_details_card_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/threat_data_overview/test_05_source_details_card_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())