import unittest
import requests
from lib.api.common_utilities import *
service = 'conversion'
'''
This module contains the test case to verify that the webhooks are working fine from the API automation side 
'''
class Webhooks(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass

    def test_01_get_webhook_list(self):
        """
        test case to get the webhook list that are present in the module
        """
        print("----- Test Case: Test case to verify the status code and response of the webhook list-----")
        endpoint = "/feed-sources/webhooks/"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_01_get_webhook_list_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                        'conversion/Feed_Sources/Webhooks/test_01_get_webhook_list_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_02_create_webhook(self):
        """
        test case to create webhook using API
        """
        print("----- Test Case: Test case to verify the status code and response of the webhook-----")
        payload = getJsonFileData('api_payload/test_02_create_webhook.json')
        endpoint = "/feed-sources/webhooks"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_02_create_webhook_runtime', response)
        if response.status_code == 201 and validate_schema(response, 'conversion/Feed_Sources/Webhooks/test_02_create_webhook_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_03_edit_webhooks(self):
        """
        test case to verify that the edit functionality is working fine
        """
        print("----- Test Case: Test case to verify that the satus and response code of the edit webhooks-----")
        payload = getJsonFileData('api_payload/test_03_edit_webhooks.json')
        dct = getJsonFileData('api_response_runtime/test_02_create_webhook_runtime.json')
        source_id = dct["id"]
        payload["id"] = dct["id"]
        payload["endpoint"] = dct["endpoint"]
        payload["created_by"] = dct["created_by"]
        payload["ctix_token"] = dct["ctix_token"]
        payload["tenant"] = dct["tenant"]
        endpoint = f"/feed-sources/webhooks/{source_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_03_edit_webhooks_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'conversion/Feed_Sources/Webhooks/test_03_edit_webhooks_schema'):
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    # def test_04_Send_Webhook_data(self):
    #     """
    #     test case to verify that send webhook functionality is working fine
    #     """
    #     print("----- Test Case: Test case to verify the status code and the response of the send webhook data  -----")
    #     payload = getJsonFileData('api_payload/test_04_Send_Webhook_data.json')
    #     print(payload)
    #     source_id = getJsonFileData('api_response_runtime/test_02_create_webhook_runtime.json')["id"]
    #     endpoint = f"/feed-sources/webhook/?token={source_id}/"
    #     url = f"{base_url}{service}{endpoint}"
    #     print(f'Making the POST request for the {url}')
    #     print("Calling authentication function for getting the unique authenticator")
    #     response = requests.post(f"{url}/{authentication()}", json=payload)
    #     print(response.url)
    #     print(f"response code is : {response.status_code}")
    #     print(f"Received response is: {response.text}")
    #
    #     save_runtime_response('testdata/api_response_runtime', 'test_04_Send_Webhook_data_runtime', response)
    #
    #     if response.status_code == 201 and validate_schema(response,
    #                                                        'conversion/Feed_Sources/Webhooks/test_04_Send_Webhook_data_schema'):
    #         print("[PASSED] POST request is successful")
    #     else:
    #         print("[FAILED] POST request is not successful")
    #         self.fail()

    def test_05_Delete_Webhook(self):
        """
        test case to verify the delete action of the webhook
        """
        print("----- Test Case: Test case to verify the status code the delete source category-----")
        source_id = getJsonFileData('api_response_runtime/test_02_create_webhook_runtime.json')["id"]
        endpoint = f"/feed-sources/webhooks/{source_id}"
        url = f"{base_url}{service}{endpoint}"
        print("Validating response got from the endpoint")
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        if response.status_code == 204:
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())


