import unittest
import requests
from lib.api.common_utilities import *
service = 'ingestion'
'''
This module contains all the testcases of the Ingestion Service Custom Objects and Attributes
'''


class CustomObjectAttribute(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_create_custom_attribute(self):
        """
            Test case to verify the post request by creating custom attribute
        """
        print("----- Test Case: Test case to verify the post request by creating custom attribute -----")
        payload = getJsonFileData('api_payload/test_01_create_custom_attribute.json')
        payload["name"] = "location_"+uniquestr
        print(payload)
        endpoint = "/configuration/custom-attribute"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_create_custom_attribute_runtime', response)

        if response.status_code == 201 and validate_schema(response, 'ingestion/custom_objects_and_attributes/test_01_create_custom_attribute_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_02_get_attribute_with_ID(self):
        """
            Test case to verify the get request by using custom attribute ID
        """
        print("----- Test Case: Test case to verify the get request by using custom attribute ID -----")
        custom_attribute_id = getJsonFileData("api_response_runtime/test_01_create_custom_attribute_runtime.json")["id"]
        endpoint = "/configuration/custom-attribute/"+custom_attribute_id
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_02_get_attribute_with_ID_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'ingestion/custom_objects_and_attributes/test_02_get_attribute_with_ID_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_03_get_attribute_details(self):
        """
            Test case to verify the get request by fetching details of all custom attribute
        """
        print("----- Test Case: Test case to verify the get request by fetching details of all custom attribute -----")
        endpoint = "/configuration/custom-attribute"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_03_get_attribute_details_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'ingestion/custom_objects_and_attributes/test_03_get_attribute_details_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_04_update_custom_attribute(self):
        print("----- Test Case: Test case to verify the put request by updating details of a custom attribute -----")
        payload = getJsonFileData('api_payload/test_04_update_custom_attribute.json')
        payload["name"] = "pin_"+uniquestr
        custom_attribute_id = getJsonFileData("api_response_runtime/test_01_create_custom_attribute_runtime.json")["id"]
        endpoint = "/configuration/custom-attribute/" + custom_attribute_id
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(response.text)
        print(f"response code is : {response.status_code}")
        save_runtime_response("testdata/api_response_runtime", "test_04_update_custom_attribute_runtime", response)
        if response.status_code == 200 and validate_schema(response, "ingestion/custom_objects_and_attributes/test_04_update_custom_attribute_schema"):
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_05_create_custom_object(self):
        """
            Test case to verify the post request by creating custom object
        """
        print("----- Test Case: Test case to verify the post request by creating custom object -----")
        payload = getJsonFileData('api_payload/test_05_create_custom_object.json')
        payload["name"] = "Cred"+uniquestr
        payload["fields"][0]["id"] = getJsonFileData("api_response_runtime/test_01_create_custom_attribute_runtime.json")["id"]
        endpoint = "/configuration/custom-object"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"Received response is: {response.text}")
        print(f"response code is : {response.status_code}")
        save_runtime_response('testdata/api_response_runtime', 'test_05_create_custom_object_runtime', response)

        if response.status_code == 201 and validate_schema(response,
                                                           'ingestion/custom_objects_and_attributes/test_05_create_custom_object_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_06_get_object_with_ID(self):
        """
            Test case to verify the get request by using custom object ID
        """
        print("----- Test Case: Test case to verify the get request by using custom object ID -----")
        custom_object_id = getJsonFileData("api_response_runtime/test_05_create_custom_object_runtime.json")["id"]
        endpoint = "/configuration/custom-object/" + custom_object_id
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"Received response is: {response.text}")
        print(f"response code is : {response.status_code}")
        save_runtime_response('testdata/api_response_runtime', 'test_06_get_object_with_ID_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'ingestion/custom_objects_and_attributes/test_06_get_object_with_ID_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_07_get_object_details(self):
        """
            Test case to verify the get request by fetching details of all custom object
        """
        print("----- Test Case: Test case to verify the get request by fetching details of all custom object -----")
        endpoint = "/configuration/custom-object"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"Received response is: {response.text}")
        print(f"response code is : {response.status_code}")
        save_runtime_response('testdata/api_response_runtime', 'test_07_get_object_details_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'ingestion/custom_objects_and_attributes/test_07_get_object_details_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_08_update_custom_object(self):
        print("----- Test Case: Test case to verify the put request by updating details of a custom object -----")
        payload = getJsonFileData('api_payload/test_05_create_custom_object.json')
        payload["name"] = "Cred_updated" + uniquestr
        payload["fields"][0]["id"] = getJsonFileData("api_response_runtime/test_01_create_custom_attribute_runtime.json")["id"]
        print(payload)
        custom_object_id = getJsonFileData("api_response_runtime/test_05_create_custom_object_runtime.json")["id"]
        endpoint = "/configuration/custom-object/" + custom_object_id
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(response.text)
        print(f"response code is : {response.status_code}")
        save_runtime_response("testdata/api_response_runtime", "test_08_update_custom_object_runtime", response)
        if response.status_code == 200 and validate_schema(response,
                                                           "ingestion/custom_objects_and_attributes/test_08_update_custom_object_schema"):
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_09_deactivate_custom_attribute(self):
        print("----- Test Case: Test case to verify the delete request by deactivating the custom attribute -----")

        #   Creating a Custom Attribute to deactivate it
        payload = getJsonFileData('api_payload/test_01_create_custom_attribute.json')
        payload["name"] = "location_" + uniquestr
        print(payload)
        endpoint = "/configuration/custom-attribute"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)
        res = json.loads(response.text)
        custom_attribute_id = res["id"]
        print("Deactivating Custom Attribute...")
        endpoint = "/configuration/custom-attribute/" + custom_attribute_id
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_15_deactivate_custom_attribute_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/custom_objects_and_attributes/test_15_deactivate_custom_attribute_scehema'):
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
