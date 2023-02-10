import unittest
import requests
from lib.api.common_utilities import *
service = "conversion"
'''
This module contains all the testcases of the Conversion Service Stix Form.
'''


class StixForm(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_list_vocab(self):
        print("----- Test Case: Test Case to verify the status code  and response of the list_vocab -----")
        endpoint = "/shareable-intel/vocab/country-ov"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response('testdata/api_response_runtime', 'test_01_list_vocab_runtime', response)
        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Stix_Form/test_01_list_vocab_schema' ):
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_02_list_relation(self):
        print("----- Test Case: Test Case to verify that the status code  and response of the list_relation -----")
        endpoint = "/shareable-intel/relation"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response('testdata/api_response_runtime', 'test_02_list_relation_runtime', response)
        if response.status_code == 200 and validate_schema(response, "conversion/Feed_Sources/Stix_Form/test_02_list_relation_schema"):
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_03_create_draft(self):
        print("----- Test Case: Test Case to verify the status code and response of the code_create_draft -----")
        payload = getJsonFileData('api_payload/test_03_create_draft.json')
        endpoint = '/shareable-intel'
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response("testdata/api_response_runtime", "test_03_create_runtime", response)
        if response.status_code == 201 and validate_schema(response, "conversion/Feed_Sources/Stix_Form/test_03_create_draft_schema"):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_04_update_draft(self):
        print("----- Test Case: Test case to verify that the status code and response of the code of the status_code_update_draft -----")
        payload = getJsonFileData('api_payload/test_04_update_draft.json')
        form_id = list_of_values(getJsonFileData('api_response_runtime/test_03_create_runtime.json'), 'id')[0]
        endpoint = f'/shareable-intel/{form_id}'
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response("testdata/api_response_runtime", "test_04_update_draft_runtime", response)
        if response.status_code == 200 and validate_schema(response, "conversion/Feed_Sources/Stix_Form/test_04_update_draft_schema"):
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_05_retrieve_draft(self):
        print("----- Test Case: Test case to verify the status code and response of the status_retrieve_draft -----")
        form_id = list_of_values(getJsonFileData('api_response_runtime/test_04_update_draft_runtime.json'), 'id')[0]
        endpoint = f'/shareable-intel/{form_id}'
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response('testdata/api_response_runtime', 'test_05_retrieve_draft_runtime', response)
        if response.status_code == 200 and validate_schema(response, "conversion/Feed_Sources/Stix_Form/test_05_retrieve_draft_schema") :
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    # def test_06_create_sdo_indicator(self):
    #     """
    #     Test case to verify the status code and reponse of the create sdo  indicator API
    #     """
    #     print("----- Test Case: Test case to verify the status code and response of the create sdo indicator -----")
    #     payload = getJsonFileData('api_payload/test_06_create_sdo_indicator.json')
    #     source_id = getJsonFileData('')
    #     endpoint = f'/shareable-intel/{source_id}/indicator'
    #     url = f"{base_url}{service}{endpoint}"
    #     print(f'Making the POST request for the {url}')
    #     print("Calling authentication function for getting the unique authenticator")
    #     response = requests.post(f"{url}/{authentication()}", payload)
    #     print(f"response code is : {response.status_code}")
    #     print(response.text)
    #     save_runtime_response("testdata/api_response_runtime", "test_06_create_sdo_indicator_runtime", response)
    #     if response.status_code == 200 and validate_schema(response, "conversion/Feed_Sources/Stix_Form/test_06_create_sdo_indicator_schema"):
    #         print("[PASSED] POST request is successful")
    #     else:
    #         print("[FAILED] POST request is not successful")
    #         self.fail()
    #
    # def test_07_update_sdo_indicator(self):
    #     """
    #     test case to verify the status code and response of the update sdo indicator api
    #     """
    #     print("----- Test Case: Test case to verify the status code and response of the update sdo indicator api  -----")
    #     payload = getJsonFileData('api_payload/test_07_update_sdo_indicator.json')
    #     endpoint = '/shareable-intel'
    #     url = f"{base_url}{service}{endpoint}"
    #     print(f'Making the PUT request for the {url}')
    #     print("Calling authentication function for getting the unique authenticator")
    #     response = requests.put(f"{url}/{authentication()}", json=payload)
    #     print(f"response code is : {response.status_code}")
    #     print(response.text)
    #     save_runtime_response("testdata/api_response_runtime", "test_07_update_sdo_indicator_runtime", response)
    #     if response.status_code == 200 and validate_schema(response, "conversion/Feed_Sources/Stix_Form/test_07_update_sdo_indicator_schema"):
    #         print("[PASSED] PUT request is successful")
    #     else:
    #         print("[FAILED] PUT request is not successful")
    #         self.fail()
    #
    # def test_08_


if __name__ == '__main__':
    unittest.main(testRunner=reporting())