import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of cyware threat intel crawler
'''

service = 'rest-auth'

class ThreatIntelCrawler(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass

    def test_01_validate_status_code_list_creds(self):
        print("----- Test Case: test_01_validate_status_code_list_creds -----")
        endpoint = "/openapi/credentials"
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

    def test_02_validate_response_list_creds(self):
        print("----- Test Case: test_02_validate_response_list_creds -----")
        endpoint = "/openapi/credentials"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_02_validate_response_list_creds', response)
        save_runtime_response('testdata/api_response_runtime', 'test_02_validate_response_list_creds_runtime', response)

        if compare_responses(response, 'test_02_validate_response_list_creds', {'id', 'last_access', 'start_date', 'expiry_date'}):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_03_validate_status_code_scan_intel(self):
        print("----- Test Case: test_03_validate_status_code_scan_intel -----")
        payload = getJsonFileData('api_payload/test_03_validate_status_code_scan_intel.json')

        service = 'ingestion'
        endpoint = "/browser-extension/scan"
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

    def test_04_validate_resp_scan_intel(self):
        print("----- Test Case: test_04_validate_resp_scan_intel -----")
        payload = getJsonFileData('api_payload/test_03_validate_status_code_scan_intel.json')

        service = 'ingestion'
        endpoint = "/browser-extension/scan"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_04_validate_resp_scan_intel', response)
        save_runtime_response('testdata/api_response_runtime', 'test_04_validate_resp_scan_intel_runtime', response)

        if compare_responses(response, 'test_04_validate_resp_scan_intel'):
            print("Response Matched")
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_05_validate_status_code_crawler_create_intel(self):
        print("----- Test Case: test_05_validate_status_code_crawler_create_intel -----")
        payload = getJsonFileData('api_payload/test_05_validate_status_code_crawler_create_intel.json')

        service = 'conversion'
        endpoint = "/browser-extension/create-intel"
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

    def test_06_validate_resp_crawler_create_intel(self):
        print("----- Test Case: test_06_validate_resp_crawler_create_intel -----")
        payload = getJsonFileData('api_payload/test_06_validate_resp_crawler_create_intel.json')

        service = 'conversion'
        endpoint = "/browser-extension/create-intel"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_06_validate_resp_crawler_create_intel', response)
        save_runtime_response('testdata/api_response_runtime', 'test_06_validate_resp_crawler_create_intel_runtime', response)

        if compare_responses(response, 'test_06_validate_resp_crawler_create_intel'):
            print("Response Matched")
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())