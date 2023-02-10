import unittest
import requests
from lib.api.common_utilities import *
service = "conversion"
'''
This module contains all the testcases of the Conversion Service --> Feed Sources --> CQL
'''


class CQL(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_combined_source_list(self):
        log("----- Test Case: test_01_combined_source_list -----")
        endpoint = "/feed-sources"
        param = {
            "nominal" : True,
            "page_size" : 10
        }
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_combined_source_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/CQL/test_01_combined_source_list_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_02_source_collection(self):
        log("----- Test Case: test_02_source_collection -----")
        endpoint = "/feed-sources/collection"
        param = {
            "nominal": True,
            "page_size": 10
        }
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_source_collection_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/CQL/test_02_source_collection_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_03_source_type_list(self):
        log("----- Test Case: test_03_source_type_list -----")
        endpoint = "/feed-sources/types"

        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_03_source_type_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/CQL/test_03_source_type_list_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())