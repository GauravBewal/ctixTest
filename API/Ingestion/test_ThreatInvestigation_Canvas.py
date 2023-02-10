import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of the Rules
'''

service = 'ingestion'

class ThreatInvestigationCanvas(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_validate_status_code_canvas_list(self):
        print("----- Test Case: test_01_validate_status_code_canvas_list -----")
        endpoint = "/canvas"
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

    def test_02_validate_response_canvas_list(self):
        print("----- Test Case: test_02_validate_response_canvas_list -----")
        endpoint = "/canvas"
        url = f"{base_url}{service}{endpoint}"
        print("Validating response got from the endpoint")
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_02_validate_response_canvas_list', response)

        save_runtime_response('testdata/api_response_runtime', 'test_02_validate_response_canvas_list_runtime', response)

        if compare_responses(response, 'test_02_validate_response_canvas_list'):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()


    def test_03_validate_status_code_canvas_detail(self):
        print("----- Test Case: test_03_validate_status_code_canvas_detail -----")
        canvas_id = list_of_values(getJsonFileData('api_response_runtime/test_02_validate_response_canvas_list_runtime.json'), 'id', {'created_by'})
        for i in range(0, len(canvas_id)):
            endpoint = f"/canvas/{canvas_id[i]}"
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

if __name__ == '__main__':
    unittest.main(testRunner=reporting())