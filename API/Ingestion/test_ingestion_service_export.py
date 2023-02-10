import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of ingestion --> export
'''

service = 'ingestion'

class Export(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_generate_link(self):
        print("----- Test Case: test_01_generate_link -----")
        payload = getJsonFileData('api_payload/test_01_generate_link.json')
        endpoint = "/export"

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_01_generate_link_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/export/test_01_generate_link_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_02_download_file(self):
        print("----- Test Case: test_02_download_file -----")
        data = getJsonFileData('api_response_runtime/test_01_generate_link_runtime.json')
        token = data["result"].split('token=')[1]
        param = {
            "file_format":"csv",
            "query=type=" :"indicator",
            "token":token
        }

        endpoint = "/export/threat_data"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")

        # print(response.text)
        # save_runtime_response('testdata/api_response_runtime', 'test_02_download_file_runtime', response)

        # for this test case schema is not being validated as response is not of json type
        if response.status_code == 200:
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())