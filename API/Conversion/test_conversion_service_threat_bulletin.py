import unittest
import requests
from lib.api.common_utilities import *
service = "conversion"
'''
This module contains all the testcases of the Conversion --> Threat Bulletin
'''

class ThreatBulletin(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_create_threat_bulletin(self):
        """
        Test case to validate the status code and response of the create threat bulletin API
        """
        print("----- Test Case: Test case to validate the status code and response of the create threat bulletin -----")
        payload = getJsonFileData('api_payload/test_01_create_threat_bulletin.json')
        payload["title"] = payload["title"]+str(int(datetime.datetime.now().timestamp()))
        endpoint = "/threat-bulletin"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the post request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response('testdata/api_response_runtime', 'test_01_create_threat_bulletin_runtime', response)
        if response.status_code == 201 and validate_schema(response,
                                                           'conversion/Feed_Sources/Threat_Bulletin/test_01_create_threat_bulletin_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_02_update_threat_bulletin(self):
        """
        test case to validate the status code and response of the update threat bulletin
        """
        print("----- Test Case: Test case to validate the status code and response of the update threat bulletin -----")
        payload = getJsonFileData('api_payload/test_02_update_threat_bulletin.json')
        source_id = getJsonFileData('api_response_runtime/test_01_create_threat_bulletin_runtime.json')["id"]
        print(source_id)
        endpoint = f'/threat-bulletin/{source_id}'
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response("testdata/api_response_runtime", "test_02_update_threat_bulletin_runtime", response)
        if response.status_code == 200 and validate_schema(response,
                                                           "conversion/Feed_Sources/Threat_Bulletin/test_02_update_threat_bulletin_schema"):
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_03_Details_of_one_bulletin(self):
        """
        test case to verify the response code and status of the details of one bulletin API
        """
        print("----- Test Case: Test case to verify the response code and status of the details of one bulletin API ---")
        source_id = getJsonFileData('api_response_runtime/test_01_create_threat_bulletin_runtime.json')["id"]
        print(source_id)
        endpoint = f"/threat-bulletin/{source_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_03_Details_of_one_bulletin_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'conversion/Feed_Sources/Threat_Bulletin/test_03_Details_of_one_bulletin_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_04_Details_Of_All_Bulletin(self):
        """
        test Case o verify the response and status code of details of all bulletins
        """
        print(
            "----- Test Case: Test case to verify the response code and status of the details of one bulletin API ---")
        endpoint = "/threat-bulletin"
        param = {
            "page": 1
        }
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_04_Details_Of_All_Bulletin_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'conversion/Feed_Sources/Threat_Bulletin/test_04_Details_Of_All_Bulletin_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_05_send_email(self):
        """
        test case to verify the status code and response of send email api
        """
        print("----- Test Case: Test case to verify the status code and response of send email api  -----")
        payload = getJsonFileData('api_payload/test_05_send_email.json')
        source_id = getJsonFileData('api_response_runtime/test_01_create_threat_bulletin_runtime.json')["id"]
        payload["id"]=source_id
        endpoint = "/threat-bulletin/send-email"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the post request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response('testdata/api_response_runtime', 'test_05_send_email_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'conversion/Feed_Sources/Threat_Bulletin/test_05_send_email_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_06_attachment_links(self):
        """
        test case to verify the status code and response of the attachment links API
        """
        print("----- Test Case: Test case to verify the status code and response of the attachment links API-----")
        source_id = getJsonFileData('api_response_runtime/test_01_create_threat_bulletin_runtime.json')["id"]
        print(source_id)
        endpoint = f"/threat-bulletin/{source_id}/attachments/link"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_06_attachment_links_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'conversion/Feed_Sources/Threat_Bulletin/test_06_attachment_links_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_07_Attachments_of_one_bulletin(self):
        """
        Test case to verify the status code and response of the attachments of one bulletin
        """
        print("----- Test Case: Test case to verify the status code and response of the attachments of one bulletin-----")
        source_id = getJsonFileData('api_response_runtime/test_01_create_threat_bulletin_runtime.json')["id"]
        print(source_id)
        endpoint = f"/threat-bulletin/{source_id}/attachments"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_07_Attachments_of_one_bulletin_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'conversion/Feed_Sources/Threat_Bulletin/test_07_Attachments_of_one_bulletin_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    # def test_08_Download_attachment(self):
    #     """
    #     Test case to verify the status code and response of the Download Attachment
    #     """
    #     print("----- Test Case: Test case to verify the status code and response of the Download Attachment-----")
    #     point = getJsonFileData('api_response_runtime/test_06_attachment_links_runtime.json')["result"]
    #     endpoint = f"{point}"
    #     url = f"{base_url}{service}{endpoint}"
    #     print(f'Making the GET request for the {url}')
    #     print("Calling authentication function for getting the unique authenticator")
    #     response = requests.get(f"{url}/{authentication()}")
    #     print(f"response code is : {response.status_code}")
    #     print(f"Received response is: {response.text}")
    #     save_runtime_response('testdata/api_response_runtime', 'test_08_Download_attachment_runtime', response)
    #     if response.status_code == 200 and validate_schema(response,
    #                                                        'conversion/Feed_Sources/Threat_Bulletin/test_08_Download_attachment_schema'):
    #         print("[PASSED] GET request is successful")
    #     else:
    #         print("[FAILED] GET request is not successful")
    #         self.fail()
    #
    # def test_09_Deactivate_Bulletin(self):
    #     """
    #     Test case to verify the status code of Deactivate Bulletin, should not be included in test plan
    #     """
    #     print("----- Test Case: Test case to verify the status code of Deactivate Bulletin-----")
    #     source_id = getJsonFileData('api_response_runtime/test_01_create_threat_bulletin_runtime.json')["id"]
    #     endpoint = f"/threat-bulletin/{source_id}"
    #     url = f"{base_url}{service}{endpoint}"
    #     print("Validating response got from the endpoint")
    #     print(f'Making the DELETE request for the {url}')
    #     print("Calling authentication function for getting the unique authenticator")
    #     response = requests.delete(f"{url}/{authentication()}")
    #     print(f"response code is : {response.status_code}")
    #     if response.status_code == 204:
    #         print("[PASSED] DELETE request is successful")
    #     else:
    #         print("[FAILED] DELETE request is not successful")
    #         self.fail()
    #

if __name__ == '__main__':
    unittest.main(testRunner=reporting())