import unittest
import requests
from lib.api.common_utilities import *
service = 'rest-auth'
'''
This module contains all the testcases of the API Gateway groups
'''


class Groups(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_validate_status_code_list_groups(self):
        print("----- Test Case: test_01_validate_status_code_list_groups -----")
        endpoint = "/groups"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_02_validate_response_list_groups(self):
        print("----- Test Case: test_02_validate_response_list_groups -----")
        endpoint = "/groups"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_02_validate_response_list_groups', response)
        save_runtime_response('testdata/api_response_runtime', 'test_02_validate_response_list_groups_runtime', response)

        if compare_responses(response, 'test_02_validate_response_list_groups', {'id', 'created'}):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_03_validate_status_code_list_components(self):
        print("----- Test Case: test_03_validate_status_code_list_components -----")
        endpoint = "/components"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_04_validate_response_list_components(self):
        print("----- Test Case: test_04_validate_response_list_components -----")
        endpoint = "/components"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_04_validate_response_list_components', response)
        save_runtime_response('testdata/api_response_runtime', 'test_04_validate_response_list_components_runtime',response)

        if compare_responses(response, 'test_04_validate_response_list_components', {'id'}):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_05_validate_status_code_admin_group(self):
        print("----- Test Case: test_05_validate_status_code_retrieve_groups -----")
        group_id = list_of_values(getJsonFileData('api_response_runtime/test_02_validate_response_list_groups_runtime.json'), 'id')[0]
        endpoint = f"/groups/{group_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_06_validate_response_admin_group(self):
        print("----- Test Case: test_06_validate_response_admin_group -----")
        group_id = list_of_values(getJsonFileData('api_response_runtime/test_02_validate_response_list_groups_runtime.json'),'id')[0]
        endpoint = f"/groups/{group_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_06_validate_response_admin_group', response)
        save_runtime_response('testdata/api_response_runtime', 'test_06_validate_response_admin_group_runtime',response)

        if compare_responses(response, 'test_06_validate_response_admin_group', {'id'}):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())