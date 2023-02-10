import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains testcases of the Enricment Policy and Confidence score - Subscriber weightage
'''

service = 'publishing'

class SubscriberWeightage(unittest.TestCase):

    @classmethod
    def setUpClass(self):
       pass

    def test_01_validate_status_code_subscriber_weightage(self):
        print("----- Test Case: test_01_validate_status_code_subscriber_weightage -----")
        endpoint = '/subscriber/source-weightage'
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        if response.status_code == 200:
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_02_validate_response_subscriber_weightage(self):
        print("----- Test Case: test_02_validate_response_subscriber_weightage -----")
        endpoint = '/subscriber/source-weightage'
        url = f"{base_url}{service}{endpoint}"
        print("Validating response got from the endpoint")
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_02_validate_response_subscriber_weightage', response)

        save_runtime_response('testdata/api_response_runtime', 'test_02_validate_response_subscriber_weightage_runtime', response)

        if compare_responses(response, 'test_02_validate_response_subscriber_weightage', {'next', 'total'}):
            print("Response matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())