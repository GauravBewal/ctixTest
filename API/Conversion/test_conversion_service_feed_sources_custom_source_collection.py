import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of the Feed Source --> Custom Source --> Collection
'''

service = "conversion"

class CustomSourceCollection(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_get_collection_list(self):
        log("----- Test Case: test_01_get_collection_list   -----")
        result = getJsonFileData('api_response_runtime/test_04_custom_source_list_runtime.json')
        source_id = result["results"][0]["id"]
        param = {
            "source": source_id
        }
        endpoint = "/feed-sources/collection"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_get_collection_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Custom_Source/Collection/test_01_get_collection_list_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_02_get_collection_detail(self):
        log("----- Test Case: test_02_get_collection_detail   -----")
        result = getJsonFileData('api_response_runtime/test_01_get_collection_list_runtime.json')
        collection_id = result["results"][0]["id"]

        endpoint = f"/feed-sources/collection/{collection_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_get_collection_detail_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Custom_Source/Collection/test_02_get_collection_detail_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_03_create_collection(self):
        log("----- Test Case: test_03_create_collection -----")
        payload = getJsonFileData('api_payload/test_03_create_collection.json')
        payload["name"] = payload["name"] + str(int(datetime.datetime.now().timestamp()))
        result = getJsonFileData('api_response_runtime/test_04_custom_source_list_runtime.json')
        source_id = ""
        for val in result["results"]:
            if val["name"] == "Import":
                source_id = val["id"]

        payload["source"]["id"] = source_id
        endpoint = "/feed-sources/collection"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_03_create_collection_runtime', response)

        if response.status_code == 201 and validate_schema(response, 'conversion/Feed_Sources/Custom_Source/Collection/test_03_create_collection_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_04_update_collection(self):
        pass

    def test_05_collection_polling_log(self):
        pass

    # def test_06_delete_collection(self):
    #     log("----- Test Case: test_06_delete_collection -----")
    #     result = getJsonFileData('api_response_runtime/test_03_create_collection_runtime.json')
    #     collection_id = result["collection_id"]
    #     endpoint = f"/feed-sources/collection/{collection_id}"
    #     url = f"{base_url}{service}{endpoint}"
    #     log(f'Making the DELETE request for the {url}')
    #     log("Calling authentication function for getting the unique authenticator")
    #     response = requests.delete(f"{url}/{authentication()}")
    #     log(f"response code is : {response.status_code}")
    #     log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")
    #
    #     save_runtime_response('testdata/api_response_runtime', 'test_03_delete_custom_source_runtime', response)

        # if response.status_code == 200 and validate_schema(response, 'conversion/Feed_sources/Custom_Source/Source/test_03_delete_custom_source_schema'):
        #     log("[PASSED] DELETE request is successful")
        # else:
        #     log("[FAILED] DELETE request is not successful")
        #     self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())
