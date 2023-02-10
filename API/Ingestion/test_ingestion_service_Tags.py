import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of the Integration Services Tags
'''

service = 'ingestion'

class Tags(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_create_tags(self):
        print("----- Test Case: test_01_create_tags -----")
        payload = getJsonFileData('api_payload/test_01_create_tags.json')
        endpoint = "/tags"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response('testdata/api_response_runtime', 'test_01_create_tags_runtime', response)

        if response.status_code == 201 and validate_schema(response, 'ingestion/tags/test_01_create_tags_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_02_update_tags(self):
        print("----- Test Case: test_02_update_tags -----")
        payload = getJsonFileData('api_payload/test_02_update_tags.json')
        tag_id = getJsonFileData('api_response_runtime/test_01_create_tags_runtime.json')["id"]
        endpoint = f"/tags/{tag_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response('testdata/api_response_runtime', 'test_02_update_tags_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/tags/test_02_update_tags_schema'):
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_03_tag_lists(self):
        print("----- Test Case: test_03_tag_lists -----")
        endpoint = "/tags"
        param = {"page" : 1}
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_03_tag_lists_runtime', response)

        if response.status_code == 200 and validate_schema(response,'ingestion/tags/test_03_tag_lists_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_04_tag_details(self):
        print("----- Test Case: test_04_tag_details -----")
        tag_id = getJsonFileData('api_response_runtime/test_03_tag_lists_runtime.json')["results"][0]["id"]
        endpoint = f"/tags/{tag_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_04_tag_details_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/tags/test_04_tag_details_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_05_delete_tag(self):
        print("----- Test Case: test_05_delete_tag -----")
        tag_id = getJsonFileData('api_response_runtime/test_01_create_tags_runtime.json')["id"]
        endpoint = f"/tags/{tag_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_05_delete_tag_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/tags/test_05_delete_tag_schema'):
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()

    def test_06_delete_tag_bulk(self):
        print("----- Test Case: test_06_delete_tag_bulk -----")
        # creating tag
        payload1 = getJsonFileData('api_payload/test_01_create_tags.json')
        payload1["name"] = "API-ThreatActor"
        endpoint1 = "/tags"
        url = f"{base_url}{service}{endpoint1}"
        response1 = requests.post(f"{url}/{authentication()}", json=payload1)
        # creating tag ends here

        tag_id = json.loads(response1.text)["id"]

        payload = getJsonFileData('api_payload/test_06_delete_tag_bulk.json')
        payload["ids"].append(tag_id)
        print(payload)
        endpoint = "/tags/bulk-actions"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_06_delete_tag_bulk_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/tags/test_06_delete_tag_bulk_schema'):
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())