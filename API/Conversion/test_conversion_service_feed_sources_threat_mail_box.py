import unittest
import requests
from lib.api.common_utilities import *
service = "conversion"
'''
This module contains all the testcases of the Conversion Service --> Feed Sources --> Threat Mailbox
'''


class ThreatMailBox(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_create_email_source(self):
        log("----- Test Case: test_01_create_email_source -----")
        payload = getJsonFileData('api_payload/test_01_create_email_source.json')
        log(payload)
        endpoint = "/feed-sources/email_accounts"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        log(response.url)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_create_email_source_runtime', response)

        if response.status_code == 201 and validate_schema(response, 'conversion/Feed_Sources/Threat_Mail_Box/test_01_create_email_source_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_02_folder_list(self):
        log("----- Test Case: test_02_folder_list -----")
        account_id = list_of_values(getJsonFileData('api_response_runtime/test_01_create_email_source_runtime.json'), 'id')[0]
        endpoint = f"/feed-sources/email/{account_id}/folders"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_folder_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Threat_Mail_Box/test_02_folder_list_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_03_email_message_list(self):
        log("----- Test Case: test_03_email_message_list -----")
        # start Making request so that mail gets listed
        payload = getJsonFileData('api_response_runtime/test_02_folder_list_runtime.json')
        for val in payload["folders"]:
            val["create_intel_feed"] = True
            val["allowed_to_fetch"] = True

        log(payload)
        email_id = getJsonFileData('api_response_runtime/test_01_create_email_source_runtime.json')["id"]
        log(email_id)
        endpoint1 = f"/feed-sources/email/{email_id}/folders"

        url = f"{base_url}{service}{endpoint1}"
        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        requests.put(f"{url}/{authentication()}", json=payload)
        # ends
        sleep(60)
        account_id = list_of_values(getJsonFileData('api_response_runtime/test_01_create_email_source_runtime.json'), 'id')[0]
        endpoint = f"/feed-sources/email/inbox"
        param = {
            "email_config" : account_id,
        }
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_03_email_message_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Threat_Mail_Box/test_03_email_message_list_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_04_attachment_listing(self):
        log("----- Test Case: test_04_attachment_listing -----")
        result = list_of_values(getJsonFileData('api_response_runtime/test_03_email_message_list_runtime.json'), 'id')
        email_id ="c3dee68b-4ed5-4040-ae36-a6d669ab2785"
        if len(result) >0:
            email_id = result[0]
        endpoint = f"/feed-sources/email/inbox/{email_id}/attachments"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_04_attachment_listing_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Threat_Mail_Box/test_04_attachment_listing_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_05_download_all_attachments(self):
        log("----- Test Case: test_05_download_all_attachments -----")
        result = list_of_values(getJsonFileData('api_response_runtime/test_03_email_message_list_runtime.json'), 'id')
        email_id = "c3dee68b-4ed5-4040-ae36-a6d669ab2785"
        if len(result) > 0:
            email_id = result[0]
        endpoint = f"/feed-sources/email/inbox/{email_id}/attachments"
        param = {
            "all_files" : True
        }
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_05_download_all_attachments_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Threat_Mail_Box/test_05_download_all_attachments_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_06_email_source_list(self):
        log("----- Test Case: test_06_email_source_list -----")
        endpoint = "/feed-sources/EMAIL_ACCOUNTS"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_06_email_source_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Threat_Mail_Box/test_06_email_source_list_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_07_email_detail(self):
        log("----- Test Case: test_07_email_detail -----")
        email_id = getJsonFileData('api_response_runtime/test_06_email_source_list_runtime.json')["results"][0]["id"]
        endpoint = f"/feed-sources/EMAIL_ACCOUNTS/{email_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_07_email_detail_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Threat_Mail_Box/test_07_email_detail_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_08_update_email_source(self):
        log("----- Test Case: test_08_update_email_source -----")
        payload = getJsonFileData('api_payload/test_08_update_email_source.json')
        email_id = getJsonFileData('api_response_runtime/test_06_email_source_list_runtime.json')["results"][0]["id"]
        endpoint = f"/feed-sources/EMAIL_ACCOUNTS/{email_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_08_update_email_source_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Threat_Mail_Box/test_08_update_email_source_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

    def test_09_update_folder_configuration(self):
        log("----- Test Case: test_09_update_folder_configuration -----")
        payload = getJsonFileData('api_response_runtime/test_02_folder_list_runtime.json')
        for val in payload["folders"]:
            val["create_intel_feed"] = True
            val["allowed_to_fetch"] = True
        email_id = getJsonFileData('api_response_runtime/test_06_email_source_list_runtime.json')["results"][0]["id"]
        log(email_id)
        endpoint = f"/feed-sources/email/{email_id}/folders"
        log(endpoint)
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_09_update_folder_configuration_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Threat_Mail_Box/test_09_update_folder_configuration_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

    def test_10_email_message_details(self):
        log("----- Test Case: test_10_email_message_details -----")

        mail_id = getJsonFileData('api_response_runtime/test_03_email_message_list_runtime.json')["results"][0]["id"]
        endpoint = f"/feed-sources/email/inbox/{mail_id}/"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_10_email_message_details_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Threat_Mail_Box/test_10_email_message_details_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_11_update_email_message(self):
        log("----- Test Case: test_11_update_email_message -----")
        mail_id = getJsonFileData('api_response_runtime/test_03_email_message_list_runtime.json')["results"][0]["id"]
        endpoint = f"/feed-sources/email/inbox/{mail_id}/"
        url = f"{base_url}{service}{endpoint}"
        payload = {
            "is_read": True
        }
        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_11_update_email_message_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Threat_Mail_Box/test_11_update_email_message_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

    def test_12_iocs_count(self):
        log("----- Test Case: test_12_iocs_count -----")
        mail_id = getJsonFileData('api_response_runtime/test_03_email_message_list_runtime.json')["results"][0]["id"]
        endpoint = f"/feed-sources/email/inbox/{mail_id}/iocs-count"
        url = f"{base_url}{service}{endpoint}"

        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_12_iocs_count_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Threat_Mail_Box/test_12_iocs_count_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_13_iocs_listing(self):
        pass

    def test_14_create_intel(self):
        pass

    def test_15_delete_email_source(self):
        log("----- Test Case: test_15_delete_email_source -----")
        result = getJsonFileData('api_response_runtime/test_01_create_email_source_runtime.json')
        source_id = result["id"]
        endpoint = f"/feed-sources/EMAIL_ACCOUNTS/{source_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the DELETE request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_15_delete_email_source_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Threat_Mail_Box/test_15_delete_email_source_schema'):
            log("[PASSED] DELETE request is successful")
        else:
            log("[FAILED] DELETE request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())