import unittest
import requests
from lib.api.common_utilities import *
service = 'conversion'
'''
This module contains all the testcases of the Conversion Service Certificate
'''


class Certificate(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_create_certificate(self):
        log("----- Test Case: test_01_create_certificate -----")
        payload = getJsonFileData("api_payload/test_01_create_certificate.json")
        payload["certificate_name"] = payload["certificate_name"] + str(int(datetime.datetime.now().timestamp()))
        endpoint = "/certificate"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_create_certificate_runtime', response)

        if response.status_code == 201 and validate_schema(response, 'conversion/Certificate/test_01_create_certificate_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_02_update_certificate(self):
        log("----- Test Case: test_02_update_certificate -----")
        payload = {
            "is_active": True
        }
        cert_id = list_of_values(getJsonFileData("api_response_runtime/test_01_create_certificate_runtime.json"), 'cert_id')[0]
        endpoint = f'/certificate/{cert_id}'
        url = f"{base_url}{service}{endpoint}"

        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_update_certificate_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Certificate/test_02_update_certificate_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

    def test_03_list_certificate(self):
        log("----- Test Case: test_03_list_certificate -----")
        endpoint = "/certificate"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_03_list_certificate_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Certificate/test_03_list_certificate_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())