import unittest
import requests
from lib.api.common_utilities import *
service = 'rest-auth'
'''
This module contains all the testcases of API Gateway --> Configuration --> Rate Limit
'''


class RateLimit(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_validate_status_code_open_api_rate_limit_details(self):
        print("----- Test Case: test_01_validate_status_code_open_api_rate_limit_details -----")
        endpoint = "/rate-limit/openapi"
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

    def test_02_validate_response_open_api_rate_limit_details(self):
        print("----- Test Case: test_02_validate_response_open_api_rate_limit_details -----")
        endpoint = "/rate-limit/openapi"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_02_validate_response_open_api_rate_limit_details', response)
        save_runtime_response('testdata/api_response_runtime', 'test_02_validate_response_open_api_rate_limit_details_runtime', response)

        if compare_responses(response, 'test_02_validate_response_open_api_rate_limit_details'):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_03_validate_status_code_update_open_api_rate_limit(self):
        print("----- Test Case: test_03_validate_status_code_update_open_api_rate_limit -----")
        payload = getJsonFileData('api_payload/test_03_validate_status_code_update_open_api_rate_limit.json')

        endpoint = "/rate-limit/openapi"
        url = f"{base_url}{service}{endpoint}"

        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json = payload)
        print(f"response code is : {response.status_code}")

        if response.status_code == 200:
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_04_validate_resp_update_open_api_rate_limit(self):
        print("----- Test Case: test_04_validate_resp_update_open_api_rate_limit -----")
        payload = getJsonFileData('api_payload/test_03_validate_status_code_update_open_api_rate_limit.json')

        endpoint = "/rate-limit/openapi"
        url = f"{base_url}{service}{endpoint}"

        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_04_validate_resp_update_open_api_rate_limit", response)
        save_runtime_response("testdata/api_response_runtime", "test_04_validate_resp_update_open_api_rate_limit_runtime", response)

        if compare_responses(response, 'test_04_validate_resp_update_open_api_rate_limit'):
            print("Response Matched")
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_05_validate_status_code_taxii_rate_limit(self):
        print("----- Test Case: test_05_validate_status_code_taxii_rate_limit -----")
        endpoint = "/rate-limit/taxii"
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

    def test_06_validate_resp_taxii_rate_limit(self):
        print("----- Test Case: test_06_validate_resp_taxii_rate_limit -----")
        endpoint = "/rate-limit/taxii"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        save_runtime_response('testdata/api_response', 'test_06_validate_resp_taxii_rate_limit', response)
        save_runtime_response('testdata/api_response_runtime', 'test_06_validate_resp_taxii_rate_limit_runtime', response)

        if compare_responses(response, 'test_06_validate_resp_taxii_rate_limit'):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_07_validate_status_code_update_taxii_rate_limit(self):
        print("----- Test Case: test_07_validate_status_code_update_taxii_rate_limit -----")
        payload = getJsonFileData('api_payload/test_07_validate_status_code_update_taxii_rate_limit.json')

        endpoint = "/rate-limit/taxii"
        url = f"{base_url}{service}{endpoint}"

        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json = payload)
        print(f"response code is : {response.status_code}")

        if response.status_code == 200:
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_08_validate_resp_update_taxii_rate_limit(self):
        print("----- Test Case: test_08_validate_resp_update_taxii_rate_limit -----")
        payload = getJsonFileData('api_payload/test_07_validate_status_code_update_taxii_rate_limit.json')

        endpoint = "/rate-limit/taxii"
        url = f"{base_url}{service}{endpoint}"

        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_08_validate_resp_update_taxii_rate_limit", response)
        save_runtime_response("testdata/api_response_runtime", "test_08_validate_resp_update_taxii_rate_limit_runtime", response)

        if compare_responses(response, 'test_08_validate_resp_update_taxii_rate_limit'):
            print("Response Matched")
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())