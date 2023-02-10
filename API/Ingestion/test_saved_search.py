import unittest
import requests
from lib.api.common_utilities import *
service = 'ingestion'
'''
This module contains all the testcases of the Ingestion Service Saved Search
'''


class SavedSearch(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_create_saved_search(self):
        """
            Test case to verify the post request by creating saved search
        """
        print("----- Test Case: Test case to verify the post request by creating saved search -----")
        payload = getJsonFileData('api_payload/test_01_create_saved_search.json')
        payload["name"] = "search_"+uniquestr
        print(payload)
        endpoint = "/saved-searches"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_create_saved_search_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/saved_search/test_01_create_saved_search_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_02_update_saved_search(self):
        """
            Test case to verify the put request by updating the saved search
        """
        print("----- Test Case: Test case to verify the put request by updating the saved search -----")
        payload = getJsonFileData('api_payload/test_02_update_saved_search.json')
        payload["name"] = "search_updated_"+uniquestr
        saved_search_id = getJsonFileData("api_response_runtime/test_01_create_saved_search_runtime.json")["id"]
        endpoint = "/saved-searches/"+saved_search_id
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_02_update_saved_search_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'ingestion/saved_search/test_02_update_saved_search_schema'):
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_03_get_saved_search_list(self):
        """
            Test case to verify the get request by fetching the saved search list
        """
        print("----- Test Case: Test case to verify the get request by fetching the saved search list -----")
        endpoint = "/saved-searches"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"Received response is: {response.text}")
        print(f"response code is : {response.status_code}")
        save_runtime_response('testdata/api_response_runtime', 'test_03_get_saved_search_list_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'ingestion/saved_search/test_03_get_saved_search_list_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_04_get_saved_search_details(self):
        """
            Test case to verify the get request by fetching the saved search details
        """
        print("----- Test Case: Test case to verify the get request by fetching the saved search details -----")
        saved_search_id = getJsonFileData("api_response_runtime/test_01_create_saved_search_runtime.json")["id"]
        endpoint = "/saved-searches/" + saved_search_id
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"Received response is: {response.text}")
        print(f"response code is : {response.status_code}")
        save_runtime_response('testdata/api_response_runtime', 'test_04_get_saved_search_details_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'ingestion/saved_search/test_04_get_saved_search_details_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_05_pin_post_request(self):
        """
            Test case to verify the post request by pinning the saved search
        """
        print("----- Test Case: Test case to verify the post request by pinning the saved search -----")
        payload = getJsonFileData('api_payload/test_05_pin_post_request.json')
        saved_search_id = getJsonFileData("api_response_runtime/test_01_create_saved_search_runtime.json")["id"]
        payload["saved_search"] = saved_search_id
        print(payload)
        endpoint = "/saved-searches/pin-saved-search"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_05_pin_post_request_runtime', response)

        if response.status_code == 201 and validate_schema(response, 'ingestion/saved_search/test_05_pin_post_request_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_06_update_pin_request(self):
        """
            Test case to verify the put request by updating the pin request
        """
        print("----- Test Case: Test case to verify the put request by updating the pin request -----")
        payload = getJsonFileData('api_payload/test_06_update_pin_request.json')
        saved_search_id = getJsonFileData("api_response_runtime/test_01_create_saved_search_runtime.json")["id"]
        payload["saved_search"] = saved_search_id
        print(payload)
        endpoint = "/saved-searches/pin-saved-search"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_06_update_pin_request_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'ingestion/saved_search/test_06_update_pin_request_schema'):
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_07_reorder_saved_search(self):
        """
            Test case to verify the post request by reordering the saved search
        """
        print("----- Test Case: Test case to verify the post request by reordering the saved search -----")
        payload = getJsonFileData('api_payload/test_07_reorder_saved_search.json')
        saved_search_id = getJsonFileData("api_response_runtime/test_01_create_saved_search_runtime.json")["id"]
        payload["saved_search"] = saved_search_id
        print(payload)
        endpoint = "/saved-searches/order-saved-search"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_07_reorder_saved_search_runtime', response)

        if response.status_code == 201 and validate_schema(response, 'ingestion/saved_search/test_07_reorder_saved_search_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_08_delete_pin_request(self):
        print("----- Test Case: Test case to verify the delete request by deleting the pin request -----")
        saved_search_id = getJsonFileData("api_response_runtime/test_01_create_saved_search_runtime.json")["id"]
        payload = getJsonFileData("api_payload/test_08_delete_pin_request.json")
        payload["saved_search"] = saved_search_id
        print(payload)
        endpoint = "/saved-searches/pin-saved-search"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_08_delete_pin_request_runtime', response)

        if response.status_code == 200 and validate_schema(response,
                                                           'ingestion/custom_objects_and_attributes/test_08_delete_pin_request_schema'):
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()

    def test_09_delete_saved_search(self):
        print("----- Test Case: Test case to verify the delete request by deleting the saved search -----")
        saved_search_id = getJsonFileData("api_response_runtime/test_01_create_saved_search_runtime.json")["id"]
        endpoint = "/saved-searches/" + saved_search_id
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_09_delete_saved_search_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'ingestion/custom_objects_and_attributes/test_09_delete_saved_search_schema'):
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
