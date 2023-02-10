import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of ingestion --> Attack navigator.
'''
service = 'ingestion'

class AttackNavigator(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_create_attack_layer(self):
        print("----- Test Case: test_01_create_attack_layer -----")
        payload = getJsonFileData('api_payload/test_01_create_attack_layer.json')
        endpoint = "/attack-navigator/attack-layer"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_01_create_attack_layer_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/attack_navigator/attack_layer/test_01_create_attack_layer_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_02_update_attack_layer(self):
        print("----- Test Case: test_02_update_attack_layer -----")
        payload = getJsonFileData('api_payload/test_02_update_attack_layer.json')
        layer_id = getJsonFileData('api_response_runtime/test_01_create_attack_layer_runtime.json')["id"]
        endpoint = f"/attack-navigator/attack-layer/{layer_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_update_attack_layer_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/attack_navigator/attack_layer/test_02_update_attack_layer_schema'):
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_03_attack_layer_listing(self):
        print("----- Test Case: test_03_attack_layer_listing -----")
        endpoint = "/attack-navigator/attack-layer"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_03_attack_layer_listing_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/attack_navigator/attack_layer/test_03_attack_layer_listing_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_04_attack_layer_details(self):
        print("----- Test Case: test_04_attack_layer_details -----")
        layer_id = getJsonFileData('api_response_runtime/test_01_create_attack_layer_runtime.json')["id"]
        endpoint = f"/attack-navigator/attack-layer/{layer_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_04_attack_layer_details_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/attack_navigator/attack_layer/test_04_attack_layer_details_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_05_tactics(self):
        print("----- Test Case: test_05_tactics -----")
        endpoint = f"/attack-navigator/tactics"
        param = {
            "domain": "enterprise"
        }
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_05_tactics_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/attack_navigator/test_05_tactics_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_06_technique_list_view(self):
        print("----- Test Case: test_06_technique_list_view -----")
        endpoint = f"/attack-navigator/techniques"
        param = {
            "domain": "enterprise"
        }
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_06_technique_list_view_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/attack_navigator/test_06_technique_list_view_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_07_technique_detail_view(self):
        print("----- Test Case: test_07_technique_detail_view -----")
        technique_id = getJsonFileData('api_response_runtime/test_06_technique_list_view_runtime.json')["results"][0]["id"]
        endpoint = f"/attack-navigator/techniques/{technique_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_07_technique_detail_view_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/attack_navigator/test_07_technique_detail_view_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_08_technique_sublist_view(self):
        print("----- Test Case: test_08_technique_sublist_view -----")
        endpoint = f"/attack-navigator/sub-techniques"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        # print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_08_technique_sublist_view_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/attack_navigator/test_08_technique_sublist_view_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_09_technique_sub_detail_view(self):
        print("----- Test Case: test_09_technique_sub_detail_view -----")
        technique_id = getJsonFileData('api_response_runtime/test_06_technique_list_view_runtime.json')["results"][0]["id"]
        endpoint = f"/attack-navigator/sub-techniques/{technique_id}"
        param = {
            "domain": "enterprise"
        }
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_09_technique_sub_detail_view_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/attack_navigator/test_09_technique_sub_detail_view_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_10_filter(self):
        print("----- Test Case: test_10_filter -----")
        endpoint = f"/attack-navigator/software"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_10_filter_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/attack_navigator/test_10_filter_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_11_ioc_heat_map(self):
        print("----- Test Case: test_11_ioc_heat_map -----")
        endpoint = f"/attack-navigator/tactic-technique-ioc-heat"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_11_ioc_heat_map_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/attack_navigator/test_11_ioc_heat_map_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_12_attack_technique_filter(self):
        print("----- Test Case: test_12_attack_technique_filter -----")
        payload = getJsonFileData('api_payload/test_12_attack_technique_filter.json')
        software_id = getJsonFileData('api_response_runtime/test_10_filter_runtime.json')["results"][0]["id"]
        payload["query"]["software"]["value"].append(software_id)
        print(payload)
        endpoint = "/attack-navigator/attack-technique-filter"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_12_attack_technique_filter_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/attack_navigator/test_12_attack_technique_filter_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_13_relation_list(self):
        print("----- Test Case: test_13_relation_list -----")
        technique_id = getJsonFileData('api_response_runtime/test_06_technique_list_view_runtime.json')["results"][0]["id"]
        endpoint = f"/attack-navigator/techniques/{technique_id}/relation"
        tactic_id = getJsonFileData("api_response_runtime/test_05_tactics_runtime.json")["results"][0]["id"]
        param = {
            "tactic_id": tactic_id
        }
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_13_relation_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/attack_navigator/test_13_relation_list_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_14_reference_api(self):
        print("----- Test Case: test_14_reference_api -----")
        technique_id = getJsonFileData('api_response_runtime/test_06_technique_list_view_runtime.json')["results"][0]["id"]
        endpoint = f"/attack-navigator/techniques/{technique_id}/reference"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_14_reference_api_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/attack_navigator/test_14_reference_api_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_15_delete_attack_layer(self):
        print("----- Test Case: test_15_delete_attack_layer -----")
        layer_id = getJsonFileData('api_response_runtime/test_01_create_attack_layer_runtime.json')["id"]
        endpoint = f"/attack-navigator/attack-layer/{layer_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_15_delete_attack_layer_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/attack_navigator/attack_layer/test_15_delete_attack_layer_schema'):
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())