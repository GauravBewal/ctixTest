import unittest
import requests
from lib.api.common_utilities import *
service = 'rest-auth'
'''
This module contains all the testcases of the LMS
'''


class LicenseManagement(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_validate_status_code_tenant_permit(self):
        print("----- Test Case: test_01_validate_status_code_tenant_permit -----")
        endpoint = "/tenant-permit"
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

    def test_02_validate_response_tenant_permit(self):
        print("----- Test Case: test_02_validate_response_tenant_permit -----")
        endpoint = "/tenant-permit"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_02_validate_response_tenant_permit', response)
        save_runtime_response('testdata/api_response_runtime', 'test_02_validate_response_tenant_permit_runtime', response)

        if compare_responses(response, 'test_02_validate_response_tenant_permit', {'license_id', 'tenant_expiry', 'tenant_name', 'tenant_code', 'ctix_version', 'license_version'}):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_03_validate_status_code_resource_list(self):
        print("----- Test Case: test_03_validate_status_code_resource_list -----")
        endpoint = "/resource/list"
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

    def test_04_validate_response_resource_list(self):
        print("----- Test Case: test_04_validate_response_resource_list -----")
        endpoint = "/resource/list"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_04_validate_response_resource_list', response)
        save_runtime_response('testdata/api_response_runtime', 'test_04_validate_response_resource_list_runtime', response)

        if compare_responses(response, 'test_04_validate_response_resource_list', {'soft_limit', 'hard_limit'}):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())