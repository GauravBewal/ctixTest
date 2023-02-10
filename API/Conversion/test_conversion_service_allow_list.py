import unittest
import requests
from lib.api.common_utilities import *
service = 'conversion'
'''
This module contains all the testcases of the Conversion Service Allow List (Indicator Allowed)
'''


class AllowedIndicators(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_create_allow_list(self):
        log("----- Test Case: test_01_create_allow_list -----")
        payload = getJsonFileData('api_payload/test_01_validate_status_code_create_allow_list.json')
        endpoint = "/whitelist"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_create_allow_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Allow_List/test_01_create_allow_list_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_02_allowed_indicator_list(self):
        log("----- Test Case: test_02_allowed_indicator_list -----")
        endpoint = "/whitelist"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_allowed_indicator_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Allow_List/test_02_allowed_indicator_list_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_03_allowed_options_list(self):
        log("----- Test Case: test_03_allowed_options_list -----")
        endpoint = "/whitelist/getoptions"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_03_allowed_options_list_runtime', response)

        if response.status_code == 200 and validate_schema(response,'conversion/Allow_List/test_03_allowed_options_list_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_04_single_allowed_indicator(self):
        log("----- Test Case: test_04_single_allowed_indicator -----")
        intel_id = list_of_values(getJsonFileData('api_response_runtime/test_02_allowed_indicator_list_runtime.json'), 'id')
        endpoint = f"/whitelist/{intel_id[1]}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_04_single_allowed_indicator_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Allow_List/test_04_single_allowed_indicator_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_05_update_allowed_indicator(self):
        log("----- Test Case: test_05_update_allowed_indicator -----")
        payload = getJsonFileData('api_payload/test_05_update_allowed_indicator.json')
        result = getJsonFileData('api_response_runtime/test_02_allowed_indicator_list_runtime.json')
        intel_id = result["results"][0]["id"]
        value = result["results"][0]["value"]
        payload["value"] = value
        payload["type"] = result["results"][0]["type"]
        endpoint = f"/whitelist/{intel_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_05_update_allowed_indicator_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Allow_List/test_05_update_allowed_indicator_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

    def test_06_reason_list(self):
        log("----- Test Case: test_06_reason_list -----")
        intel_id = list_of_values(getJsonFileData('api_response_runtime/test_02_allowed_indicator_list_runtime.json'), 'id')
        endpoint = f"/whitelist/reasons/?whitelist={intel_id[1]}&"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}{authentication().replace('?', '')}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_06_reason_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Allow_List/test_06_reason_list_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

    def test_07_delete_reason(self):
        log("----- Test Case: test_07_delete_reason -----")
        reason_id = list_of_values(getJsonFileData('api_response_runtime/test_06_reason_list_runtime.json'), 'id')
        endpoint = f"/whitelist/reasons/{reason_id[1]}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the DELETE request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_07_delete_reason_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Allow_List/test_07_delete_reason_schema'):
            log("[PASSED] DELETE request is successful")
        else:
            log("[FAILED] DELETE request is not successful")
            self.fail()

    def test_08_create_reason(self):
        log("----- Test Case: test_08_create_reason -----")
        payload = getJsonFileData('api_payload/test_08_create_reason.json')
        intel_id = list_of_values(getJsonFileData('api_response_runtime/test_02_allowed_indicator_list_runtime.json'), 'id')
        endpoint = f"/whitelist/reasons/?whitelist={intel_id[1]}&"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}{authentication().replace('?', '')}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_08_create_reason_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Allow_List/test_08_create_reason_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_09_update_reason(self):
        log("----- Test Case: test_09_update_reason -----")
        payload = getJsonFileData('api_payload/test_09_update_reason.json')
        payload["created"] = list_of_values(getJsonFileData('api_response_runtime/test_08_create_reason_runtime.json'), 'created')[0]
        payload["id"] = list_of_values(getJsonFileData('api_response_runtime/test_08_create_reason_runtime.json'), 'id')[0]
        payload["modified"] = list_of_values(getJsonFileData('api_response_runtime/test_08_create_reason_runtime.json'), 'modified')[0]
        payload["created_by"] = list_of_values(getJsonFileData('api_response_runtime/test_08_create_reason_runtime.json'), 'created_by')[0]
        payload["modified_by"] = list_of_values(getJsonFileData('api_response_runtime/test_08_create_reason_runtime.json'), 'modified_by')[0]
        payload["whitelist"] = list_of_values(getJsonFileData('api_response_runtime/test_08_create_reason_runtime.json'), 'whitelist')[0]

        reason_id = list_of_values(getJsonFileData('api_response_runtime/test_08_create_reason_runtime.json'), 'id')
        endpoint = f"/whitelist/reasons/{reason_id[0]}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_09_update_reason_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Allow_List/test_09_update_reason_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

    def test_10_parse_IOC(self):
        log("----- Test Case: test_10_parse_IOC -----")
        payload = getJsonFileData('api_payload/test_10_parse_IOC.json')
        endpoint = "/whitelist/parse-ioc"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")
        save_runtime_response('testdata/api_response_runtime', 'test_10_parse_IOC_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Allow_List/test_10_parse_IOC_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_11_bulk_action(self):
        log("----- Test Case: test_11_bulk_action -----")
        payload = getJsonFileData('api_payload/test_11_bulk_action.json')
        intel_id = list_of_values(getJsonFileData('api_response_runtime/test_02_allowed_indicator_list_runtime.json'), 'id')
        payload["ids"][0] = intel_id[1]
        endpoint = "/whitelist/bulk-actions"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")
        save_runtime_response('testdata/api_response_runtime', 'test_11_bulk_action_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Allow_List/test_11_bulk_action_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_12_delete_allowed_indicator(self):
        log("----- Test Case: test_12_delete_allowed_indicator -----")
        intel_id = list_of_values(getJsonFileData('api_response_runtime/test_02_allowed_indicator_list_runtime.json'), 'id')
        endpoint = f"/whitelist/{intel_id[1]}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the DELETE request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_12_delete_allowed_indicator_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Allow_List/test_12_delete_allowed_indicator_schema'):
            log("[PASSED] DELETE request is successful")
        else:
            log("[FAILED] DELETE request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
