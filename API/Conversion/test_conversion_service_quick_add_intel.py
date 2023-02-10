import unittest
import requests
from lib.api.common_utilities import *
service = 'conversion'
'''
This module contains all the testcases of the Conversion Quick Add Intel
'''


class QuickAddIntel(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_IOC_Options(self):
        log("----- Test Case: test_01_IOC_Options -----")
        endpoint = "/quick-intel/ioc-options"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_IOC_Options_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Quick_Add_Intel/test_01_IOC_Options_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_02_region_vocab_listing(self):
        log("----- Test Case: test_02_region_vocab_listing -----")
        endpoint = "/quick-intel/vocabs/region_ov"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_region_vocab_listing_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Quick_Add_Intel/test_02_region_vocab_listing_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_03_country_enum_listing(self):
        log("----- Test Case: test_03_country_enum_listing -----")
        endpoint = "/quick-intel/vocabs/country_enum/"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_03_country_enum_listing_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Quick_Add_Intel/test_03_country_enum_listing_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_04_create_intel(self):
        log("----- Test Case: test_04_create_intel -----")
        endpoint = "/quick-intel/create-stix"
        payload = getJsonFileData('api_payload/test_04_create_intel.json')

        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json = payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_04_create_intel_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Quick_Add_Intel/test_04_create_intel_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_05_create_parse_ioc_task(self):
        log("----- Test Case: test_05_create_parse_ioc_task -----")
        endpoint = "/quick-intel/free-text"
        payload = getJsonFileData('api_payload/test_05_create_parse_ioc_task.json')

        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json = payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")
        sleep(60)
        save_runtime_response('testdata/api_response_runtime', 'test_05_create_parse_ioc_task_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Quick_Add_Intel/test_05_create_parse_ioc_task_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_06_parse_ioc_task_result(self):
        log("----- Test Case: test_06_parse_ioc_task_result -----")
        parse_ioc_task_id = list_of_values(getJsonFileData('api_response_runtime/test_05_create_parse_ioc_task_runtime.json'), 'task_id')[0]
        endpoint = f"/tasks/{parse_ioc_task_id}/parse-iocs"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_06_parse_ioc_task_result_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Quick_Add_Intel/test_06_parse_ioc_task_result_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_07_parse_ioc_task_status(self):
        log("----- Test Case: test_07_parse_ioc_task_status -----")
        parse_ioc_task_id = list_of_values(getJsonFileData('api_response_runtime/test_05_create_parse_ioc_task_runtime.json'), 'task_id')[0]
        endpoint = f"/tasks/{parse_ioc_task_id}/?fields=status&"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}{authentication().replace('?', '')}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_07_parse_ioc_task_status_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Quick_Add_Intel/test_07_parse_ioc_task_status_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())