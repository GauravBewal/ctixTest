import unittest
import requests
from lib.api.common_utilities import *
service = 'conversion'
'''
This module contains all the testcases of the Conversion Service Intel history
'''


class IntelHistory(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_list_intel_history(self):
        log("----- Test Case: test_01_list_intel_history -----")
        endpoint = "/intel-history"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_list_intel_history_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Intel_history/test_01_list_intel_history_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_02_search_intel_history(self):
        log("----- Test Case: test_02_search_intel_history -----")
        endpoint = "/intel-history"
        param = {
            "q": 3
        }
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_search_intel_history_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Intel_history/test_02_search_intel_history_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_03_sort_intel_history_title(self):
        log("----- Test Case: test_03_sort_intel_history_title -----")
        endpoint = "/intel-history"
        param = {
            "sort": "title"
        }
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_03_sort_intel_history_title_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Intel_history/test_03_sort_intel_history_title_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_04_intel_history_stat(self):
        log("----- Test Case: test_04_intel_history_stat -----")
        endpoint = "/intel-history-stat"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_04_intel_history_stat_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Intel_history/test_04_intel_history_stat_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())