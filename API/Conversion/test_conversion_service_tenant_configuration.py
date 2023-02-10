import unittest
import requests
from lib.api.common_utilities import *
service = 'conversion'
'''
This module contains all the testcases of the Configuration
'''


class TenantConfiguration(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_tenant_config_retrieve(self):
        log("----- Test Case: test_01_tenant_config_retrieve -----")
        endpoint = "/tenant/config"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_tenant_config_retrieve_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Tenant_Configuration/test_01_tenant_config_retrieve_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_02_update_tenant_config(self):
        log("----- Test Case: test_02_update_tenant_config -----")
        payload = getJsonFileData('api_payload/test_02_update_tenant_config.json')
        endpoint = '/tenant/config'
        url = f"{base_url}{service}{endpoint}"

        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_update_tenant_config_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Tenant_Configuration/test_02_update_tenant_config_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())