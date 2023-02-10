import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of ingestion --> Threat Data Objects
'''

service = 'ingestion'

class ThreatDataObjects(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_list_threat_data(self):
        print("----- Test Case: test_01_list_threat_data -----")
        #  We will create intel which gets ingested in threat data
        endpoint1 = "/quick-intel/create-stix"
        payload1 = getJsonFileData('api_payload/test_04_create_intel.json')
        url1 = f"{base_url}conversion{endpoint1}"
        log(f'Making the POST request for the {url1}')
        log("Calling authentication function for getting the unique authenticator")
        requests.post(f"{url1}/{authentication()}", json=payload1)
        sleep(8)
        # intel creation ends here

        payload = getJsonFileData('api_payload/test_01_list_threat_data.json')
        endpoint = "/threat-data/list"
        param = {
            "page":1,
            "page_size":10,
            "page_limit":10
        }
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload, params=param)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_01_list_threat_data_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/threat_data_object/test_01_list_threat_data_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_02_threat_data_object_details(self):
        print("----- Test Case: test_02_threat_data_object_details -----")
        object_id = getJsonFileData('api_response_runtime/test_01_list_threat_data_runtime.json')["results"][0]["id"]
        endpoint = f"/threat-data/indicator/{object_id}/basic"

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_02_threat_data_object_details_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/threat_data_object/test_02_threat_data_object_details_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_03_object_details_in_table_view(self):
        print("----- Test Case: test_03_object_details_in_table_view -----")
        result = getJsonFileData('api_response_runtime/test_01_list_threat_data_runtime.json')
        object_id = result["results"][0]["id"]
        object_type = result["results"][0]["type"]
        endpoint = f"/threat-data/source-overview"

        param = {
            "object_id":object_id,
            "object_type":object_type,
            "page":1,
            "page_size":10
        }

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_03_object_details_in_table_view_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/threat_data_object/test_03_object_details_in_table_view_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_04_object_source_details_list_view(self):
        print("----- Test Case: test_04_object_source_details_list_view -----")
        result = getJsonFileData('api_response_runtime/test_01_list_threat_data_runtime.json')
        object_id = result["results"][0]["id"]
        object_type = result["results"][0]["type"]
        source_id = result["results"][0]["sources"][0]["id"]
        endpoint = f"/threat-data/source-references"

        param = {
            "object_id": object_id,
            "object_type": object_type,
            "page": 1,
            "page_size": 10,
            "source_id":source_id
        }

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_04_object_source_details_list_view_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/threat_data_object/test_04_object_source_details_list_view_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_05_advanced_view_of_object(self):
        print("----- Test Case: test_05_advanced_view_of_object -----")
        result = getJsonFileData('api_response_runtime/test_01_list_threat_data_runtime.json')
        object_id = result["results"][0]["id"]
        endpoint = f"/threat-data/indicator/{object_id}/advanced-details"

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_05_advanced_view_of_object_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/threat_data_object/test_05_advanced_view_of_object_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_06_source_details(self):
        print("----- Test Case: test_06_source_details -----")
        result = getJsonFileData('api_response_runtime/test_01_list_threat_data_runtime.json')
        object_id = result["results"][0]["id"]
        object_type = result["results"][0]["type"]
        endpoint = f"/threat-data/{object_type}/{object_id}/source-description"

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_06_source_details_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/threat_data_object/test_06_source_details_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_07_details_about_external_references(self):
        print("----- Test Case: test_07_details_about_external_references -----")
        result = getJsonFileData('api_response_runtime/test_01_list_threat_data_runtime.json')
        object_id = result["results"][0]["id"]
        object_type = result["results"][0]["type"]
        endpoint = f"/threat-data/{object_type}/{object_id}/external-references"

        param = {
            "page_size":3,
            "page":1
        }
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_07_details_about_external_references_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/threat_data_object/test_07_details_about_external_references_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())