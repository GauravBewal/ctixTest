import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of the Enrichment Policy and Confidence score - Enrichment Policy
'''

service = 'ingestion'

class EnrichmentPolicy(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_validate_status_code_list_of_policies(self):
        print("----- Test Case: test_01_validate_status_code_list_of_policies -----")
        endpoint = '/policy'
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        if response.status_code == 200:
            print("[PASSED] Get request is successful")
        else:
            print(response.text)
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_02_validate_response_list_of_policies(self):
        print("----- Test Case: test_02_validate_response_list_of_policies -----")
        endpoint = '/policy'
        url = f"{base_url}{service}{endpoint}"
        print("Validating response got from the endpoint")
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_02_validate_response_list_of_policies', response)

        save_runtime_response('testdata/api_response_runtime', 'test_02_validate_response_list_of_policies_runtime', response)
        if compare_responses(response,'test_02_validate_response_list_of_policies'):
            print("Response matched")
            print("[PASSED] Get request is successful")
        else:
            print(response.text)
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_03_validate_status_code_details_of_policy(self):
        print("----- Test Case: test_03_validate_status_code_details_of_policy -----")
        policy_id = list_of_values(getJsonFileData('api_response_runtime/test_02_validate_response_list_of_policies_runtime.json'), 'id', {'created_by', 'collection', 'enrichment', 'source', 'updated_by'})
        for id in policy_id:
            endpoint = f'/policy/{id}'
            url = f"{base_url}{service}{endpoint}"
            print(f'Making the get request for the {url}')
            print("Calling authentication function for getting the unique authenticator")
            response = requests.get(f"{url}/{authentication()}")
            print(f"response code is : {response.status_code}")

            if response.status_code == 200:
                print("[PASSED] Get request is successful")
            else:
                print(response.text)
                print("[FAILED] Get request is not successful")
                self.fail()

    def test_04_validate_response_details_of_policy(self):
        pass

if __name__ == '__main__':
    unittest.main(testRunner=reporting())
