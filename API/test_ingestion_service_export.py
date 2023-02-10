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

    def test_01_validate_status_code_generate_link(self):
        print("----- Test Case: test_01_validate_status_code_generate_link -----")
        payload = getJsonFileData('api_payload/test_01_validate_status_code_generate_link.json')
        endpoint = "/export"

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)

        if response.status_code == 200:
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_02_validate_resp_generate_link(self):
        print("----- Test Case: test_02_validate_resp_generate_link -----")
        payload = getJsonFileData('api_payload/test_01_validate_status_code_generate_link.json')
        endpoint = "/export"

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_02_validate_resp_generate_link', response)
        save_runtime_response('testdata/api_response_runtime', 'test_02_validate_resp_generate_link_runtime', response)

        if compare_responses(response, 'test_02_validate_resp_generate_link', {'result'}):
            print("Response Matched")
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_03_validate_status_code_download_file(self):
        print("----- Test Case: test_03_validate_status_code_download_file -----")
        data = getJsonFileData('api_response_runtime/test_02_validate_resp_generate_link_runtime.json')
        part = data["result"].split('&')[2]
        endpoint = "/export/threat_data/?file_format=csv&query=type='indicator'&" + part + "&"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}{str(authentication()).replace('?', '')}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())