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

    def test_01_validate_status_code_create_tags(self):
        print("----- Test Case: test_01_validate_status_code_create_tags -----")
        payload = getJsonFileData('api_payload/test_01_create_tags.json')
        endpoint = "/tags"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 201:
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_02_validate_resp_create_tags(self):
        print("----- Test Case: test_02_validate_resp_create_tags -----")
        payload = getJsonFileData('api_payload/test_01_create_tags.json')
        payload["name"] = "HSThreatActor"
        endpoint = "/tags"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_02_validate_resp_create_tags', response)
        save_runtime_response('testdata/api_response_runtime', 'test_02_validate_resp_create_tags_runtime', response)

        if compare_responses(response, 'test_02_validate_resp_create_tags', {"id", "created", "created_by", "modified_by", "modified"}):
            print("Response Matched")
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_03_validate_status_code_update_tags(self):
        print("----- Test Case: test_03_validate_status_code_update_tags -----")
        payload = getJsonFileData('api_payload/test_02_update_tags.json')
        tag_id = list_of_values(getJsonFileData('api_response_runtime/test_02_validate_resp_create_tags_runtime.json'), 'id')
        endpoint = f"/tags/{tag_id[0]}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_04_validate_resp_update_tags(self):
        print("----- Test Case: test_04_validate_resp_update_tags -----")
        payload = getJsonFileData('api_payload/test_02_update_tags.json')
        tag_id = list_of_values(getJsonFileData('api_response_runtime/test_02_validate_resp_create_tags_runtime.json'),'id')
        endpoint = f"/tags/{tag_id[0]}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_04_validate_resp_update_tags", response)
        save_runtime_response("testdata/api_response_runtime", "test_04_validate_resp_update_tags_runtime", response)

        if compare_responses(response, 'test_04_validate_resp_update_tags', {"id", "created", "created_by", "modified_by", "modified"}):
            print("Response Matched")
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_05_validate_status_code_tag_lists(self):
        print("----- Test Case: test_05_validate_status_code_tag_lists -----")
        endpoint = "/tags"
        param = {"page" : 1}
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_06_validate_resp_tag_lists(self):
        print("----- Test Case: test_06_validate_resp_tag_lists -----")
        endpoint = "/tags"
        param = {"page": 1}
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_06_validate_resp_tag_lists', response)
        save_runtime_response('testdata/api_response_runtime', 'test_06_validate_resp_tag_lists_runtime', response)

        if compare_responses(response, 'test_06_validate_resp_tag_lists', {"created", "modified", "id", "next"}):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_07_validate_status_code_tag_details(self):
        print("----- Test Case: test_07_validate_status_code_tag_details -----")
        tag_id = list_of_values(getJsonFileData('api_response_runtime/test_06_validate_resp_tag_lists_runtime.json'), 'id', {"created_by"})
        endpoint = f"/tags/{tag_id[0]}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_08_validate_resp_tag_details(self):
        print("----- Test Case: test_08_validate_resp_tag_details -----")
        tag_id = list_of_values(getJsonFileData('api_response_runtime/test_06_validate_resp_tag_lists_runtime.json'),'id', {"created_by"})
        endpoint = f"/tags/{tag_id[0]}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_08_validate_resp_tag_details", response)
        save_runtime_response("testdata/api_response_runtime", "test_08_validate_resp_tag_details_runtime", response)

        if compare_responses(response, 'test_08_validate_resp_tag_details', {"created", "created_by", "id", "modified", "modified_by"}):
            print("Response Matched")
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_09_validate_status_code_delete_tag(self):
        print("----- Test Case: test_09_validate_status_code_delete_tag -----")
        tag_id = list_of_values(getJsonFileData('api_response_runtime/test_06_validate_resp_tag_lists_runtime.json'), 'id', {"created_by"})
        endpoint = f"/tags/{tag_id[0]}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()

    def test_10_validate_resp_delete_tag(self):
        print("----- Test Case: test_10_validate_resp_delete_tag -----")
        tag_id = list_of_values(getJsonFileData('api_response_runtime/test_06_validate_resp_tag_lists_runtime.json'), 'id', {"created_by", "modified_by"})
        endpoint = f"/tags/{tag_id[1]}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_10_validate_resp_delete_tag", response)
        save_runtime_response("testdata/api_response_runtime", "test_10_validate_resp_delete_tag_runtime", response)

        if compare_responses(response, 'test_10_validate_resp_delete_tag'):
            print("Response Matched")
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()

    def test_11_validate_status_code_delete_tag_bulk(self):
        print("----- Test Case: test_11_validate_status_code_delete_tag_bulk -----")
        # creating tag
        tpayload = getJsonFileData('api_payload/test_01_create_tags.json')
        tpayload["name"] = "HSBulkThreatActor"
        tendpoint = "/tags"
        url = f"{base_url}{service}{tendpoint}"
        tresponse = requests.post(f"{url}/{authentication()}", json=tpayload)
        json_format = json.loads(tresponse.text)

        tag_id = list_of_values(json_format, 'id', {"created_by"})
        payload = getJsonFileData('api_payload/test_06_delete_tag_bulk.json')
        payload["ids"].append(tag_id[0])
        endpoint = "/tags/bulk-actions"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()

    def test_12_validate_resp_delete_tag_bulk(self):
        print("----- Test Case: test_12_validate_resp_delete_tag_bulk -----")
        # creating tag
        tpayload = getJsonFileData('api_payload/test_01_create_tags.json')
        tpayload["name"] = "HSBulkThreatActor"
        tendpoint = "/tags"
        url = f"{base_url}{service}{tendpoint}"
        tresponse = requests.post(f"{url}/{authentication()}", json=tpayload)
        json_format = json.loads(tresponse.text)

        tag_id = list_of_values(json_format, 'id', {"created_by"})
        payload = getJsonFileData('api_payload/test_06_delete_tag_bulk.json')
        payload["ids"].append(tag_id[0])
        endpoint = "/tags/bulk-actions"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_12_validate_resp_delete_tag_bulk", response)
        save_runtime_response("testdata/api_response_runtime", "test_12_validate_resp_delete_tag_bulk_runtime", response)

        if compare_responses(response, 'test_12_validate_resp_delete_tag_bulk'):
            print("Response Matched")
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())