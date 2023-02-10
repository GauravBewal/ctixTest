import unittest
import requests

from lib.api.common_utilities import *

'''
This module contains all the testcases of the Feed Source --> Custom Source --> Source
'''

service = "conversion"

class CustomSource(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_add_custom_source(self):
        log("----- Test Case: test_01_add_custom_source -----")
        payload = getJsonFileData('api_payload/test_01_add_custom_source.json')
        feed_id = ""
        for dic in json.loads((requests.get(f"{base_url}{service}/feed-sources/category/{authentication()}")).text):
            if dic["name"] == "System Feeds":
                feed_id = dic["id"]
                break

        payload["category"]["id"] = feed_id
        endpoint = "/feed-sources/custom_stix_sources"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_add_custom_source_runtime', response)

        if response.status_code == 201 and validate_schema(response, 'conversion/Feed_Sources/Custom_Source/Source/test_01_add_custom_source_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_02_update_custom_source(self):
        log("----- Test Case: test_02_update_custom_source -----")
        payload = getJsonFileData('api_payload/test_02_update_custom_source.json')
        result = getJsonFileData('api_response_runtime/test_01_add_custom_source_runtime.json')
        payload["category"]["id"] = result["category"]["id"]
        source_id = result["id"]
        endpoint = f"/feed-sources/custom_stix_sources/{source_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_update_custom_source_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Custom_Source/Source/test_02_update_custom_source_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

    def test_03_delete_custom_source(self):
        log("----- Test Case: test_03_delete_custom_source -----")
        result = getJsonFileData('api_response_runtime/test_01_add_custom_source_runtime.json')
        source_id = result["id"]
        endpoint = f"/feed-sources/custom_stix_sources/{source_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the DELETE request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_03_delete_custom_source_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Custom_Source/Source/test_03_delete_custom_source_schema'):
            log("[PASSED] DELETE request is successful")
        else:
            log("[FAILED] DELETE request is not successful")
            self.fail()

    def test_04_custom_source_list(self):
        log("----- Test Case: test_04_custom_source_list   -----")
        endpoint = "/feed-sources/custom_stix_sources"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_04_custom_source_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Custom_Source/Source/test_04_custom_source_list_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
