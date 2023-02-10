import unittest
import requests
from lib.api.common_utilities import *

service = "conversion"
'''
This module contains all the testcases of the Feed Source --> Source Category
'''


class SourceCategory(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_list_source_category(self):
        print("----- Test Case: Test case to verify the status code and response of the list source collection -----")
        endpoint = "/feed-sources/category/"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response('testdata/api_response_runtime', 'test_01_list_source_category_runtime',
                              response)
        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Source_Category/test_01_list_source_category_schema' ):
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_02_create_source_category(self):
        print("----- Test Case: Test case to verify the status code and response of the create source category -----")
        result = getJsonFileData("api_response_runtime/test_01_list_source_category_runtime.json")
        source_id = ""
        for val in result:
            if val["name"] == "TEST_CATEGORY":
                source_id = val["id"]

        """ delete the source if already exist"""
        endpoint1 = f"/feed-sources/category/{source_id}"
        url = f"{base_url}{service}{endpoint1}"
        print(f'Making the DELETE request for the {url}')
        requests.delete(f"{url}/{authentication()}")
        """ ending the statement"""
        payload = {
            "name": "TEST_CATEGORY"
        }
        endpoint = "/feed-sources/category"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response('testdata/api_response_runtime', 'test_02_create_source_category_runtime',
                              response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Source_Category/test_02_create_source_category_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_03_update_source_category(self):
        print("----- Test Case: Test Case to verify the source code and response of the update source category -----")

        payload = {
            "name": "TEST_CATEGORY_UPDATED"
        }
        source_id = getJsonFileData("api_response_runtime/test_02_create_source_category_runtime.json")["id"]
        endpoint = f'/feed-sources/category/{source_id}'
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response('testdata/api_response_runtime', 'test_03_update_source_category_runtime',
                              response)
        if response.status_code == 400 and validate_schema(response, "conversion/Feed_Sources/Source_Category/test_03_update_source_category_schema"):
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_04_delete_source_category(self):
        print("----- Test Case: Test case to verify the status code and response of the delete source category-----")
        source_id = getJsonFileData("api_response_runtime/test_02_create_source_category_runtime.json")["id"]
        endpoint = f"/feed-sources/category/{source_id}"
        url = f"{base_url}{service}{endpoint}"
        print("Validating response got from the endpoint")
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response('testdata/api_response_runtime', 'test_04_delete_source_category_runtime',
                              response)
        if response.status_code == 200 and validate_schema(response, "conversion/Feed_Sources/Source_Category/test_04_delete_source_category_schema"):
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())