import unittest
import requests
from lib.api.common_utilities import *
service = 'rest-auth'
'''
This module contains all the testcases of API Gateway --> Configuration --> tenant configuration
'''


class Configuration(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_validate_status_code_tenant_config(self):
        print("----- Test Case: test_01_validate_status_code_tenant_config -----")
        endpoint = "/tenant/config"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_02_validate_response_tenant_config(self):
        print("----- Test Case: test_02_validate_response_tenant_config -----")
        endpoint = "/tenant/config"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_02_validate_response_tenant_config', response)
        save_runtime_response('testdata/api_response_runtime', 'test_02_validate_response_tenant_config_runtime', response)

        if compare_responses(response, 'test_02_validate_response_tenant_config', {'tenant_id','domain', 'system_user', 'technical_support_mail', 'support_mail'}):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_03_validate_status_code_auth_config(self):
        print("----- Test Case: test_03_validate_status_code_auth_config -----")
        endpoint = "/auth-config"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_04_validate_response_auth_config(self):
        print("----- Test Case: test_04_validate_response_auth_config -----")
        endpoint = "/auth-config"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_04_validate_response_auth_config', response)
        save_runtime_response('testdata/api_response_runtime', 'test_04_validate_response_auth_config_runtime', response)

        if compare_responses(response, 'test_04_validate_response_auth_config'):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_05_validate_status_code_recaptcha_creds(self):
        print("----- Test Case: test_05_validate_status_code_recaptcha_creds -----")
        endpoint = "/auth-config/recaptcha"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_06_validate_response_recaptcha_creds(self):
        print("----- Test Case: test_06_validate_response_recaptcha_creds -----")
        endpoint = "/auth-config/recaptcha"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_06_validate_response_recaptcha_creds', response)
        save_runtime_response('testdata/api_response_runtime', 'test_06_validate_response_recaptcha_creds_runtime', response)

        if compare_responses(response, 'test_06_validate_response_recaptcha_creds'):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_07_validate_status_code_update_recaptcha_creds(self):
        print("----- Test Case: test_07_validate_status_code_update_recaptcha_creds -----")
        payload = getJsonFileData('api_payload/test_07_validate_status_code_update_recaptcha_creds.json')

        endpoint = "/auth-config/recaptcha"
        url = f"{base_url}{service}{endpoint}"

        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json = payload)
        print(f"response code is : {response.status_code}")

        if response.status_code == 200:
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_08_validate_resp_update_recaptcha_creds(self):
        print("----- Test Case: test_08_validate_resp_update_recaptcha_creds -----")
        payload = getJsonFileData('api_payload/test_07_validate_status_code_update_recaptcha_creds.json')

        endpoint = "/auth-config/recaptcha"
        url = f"{base_url}{service}{endpoint}"

        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_08_validate_resp_update_recaptcha_creds", response)

        save_runtime_response("testdata/api_response_runtime", "test_08_validate_resp_update_recaptcha_creds_runtime", response)

        if compare_responses(response, 'test_08_validate_resp_update_recaptcha_creds'):
            print("Response Matched")
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_09_validate_status_code_update_auth_config(self):
        print("----- Test Case: test_09_validate_status_code_update_auth_config -----")
        payload = getJsonFileData('api_payload/test_09_validate_status_code_update_auth_config.json')
        endpoint = '/auth-config'
        url = f"{base_url}{service}{endpoint}"

        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_10_validate_resp_update_auth_config(self):
        print("----- Test Case: test_10_validate_resp_update_auth_config -----")
        payload = getJsonFileData('api_payload/test_09_validate_status_code_update_auth_config.json')
        endpoint = '/auth-config'
        url = f"{base_url}{service}{endpoint}"

        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_10_validate_resp_update_auth_config', response)
        save_runtime_response('testdata/api_response_runtime', 'test_10_validate_resp_update_auth_config_runtime', response)

        if compare_responses(response, 'test_10_validate_resp_update_auth_config'):
            print("Response Matched")
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_11_validate_status_code_tenant_details(self):
        print("----- Test Case: test_11_validate_status_code_tenant_details -----")
        endpoint = "/tenant"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_12_validate_status_code_upload_logo(self):
        print("----- Test Case: test_12_validate_status_code_upload_logo -----")
        payload = getJsonFileData('api_payload/test_12_validate_status_code_upload_logo.json')
        file_name = os.path.join(os.environ["PYTHONPATH"], "testdata", "api_payload/cyware.png")
        test_file = open(file_name, "rb")
        payload["logo"] = test_file
        endpoint = "/tenant/config/logo"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", files=payload)
        print(f"response code is : {response.status_code}")
        test_file.close()
        print(response.text)
        if response.status_code == 200:
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_13_validate_resp_upload_logo(self):
        print("----- Test Case: test_13_validate_resp_upload_logo -----")
        payload = getJsonFileData('api_payload/test_12_validate_status_code_upload_logo.json')
        file_name = os.path.join(os.environ["PYTHONPATH"], "testdata", "api_payload/cyware.png")
        test_file = open(file_name, "rb")
        payload["logo"] = test_file
        endpoint = "/tenant/config/logo"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", files=payload)
        print(f"response code is : {response.status_code}")
        test_file.close()

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_13_validate_resp_upload_logo', response)
        save_runtime_response('testdata/api_response_runtime', 'test_13_validate_resp_upload_logo_runtime', response)

        if compare_responses(response, 'test_13_validate_resp_upload_logo'):
            print("Response Matched")
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_14_validate_status_code_logo_details(self):
        print("----- Test Case: test_14_validate_status_code_logo_details -----")
        endpoint = "/tenant/config/logo/?logo=true&"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}{str(authentication()).replace('?', '')}")
        print(f"response code is : {response.status_code}")

        if response.status_code == 200:
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_15_validate_status_code_delete_logo(self):
        print("----- Test Case: test_15_validate_status_code_delete_logo -----")

        endpoint = "/tenant/config/logo/?logo=true&"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}{str(authentication()).replace('?', '')}")
        print(f"response code is : {response.status_code}")

        if response.status_code == 200:
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()

    def test_16_validate_resp_delete_logo(self):
        print("----- Test Case: test_16_validate_resp_delete_logo -----")

        endpoint = "/tenant/config/logo/?logo=true&"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}{str(authentication()).replace('?', '')}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_16_validate_resp_delete_logo', response)
        save_runtime_response('testdata/api_response_runtime', 'test_16_validate_resp_delete_logo_runtime', response)

        if compare_responses(response, 'test_16_validate_resp_delete_logo'):
            print("Response Matched")
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()

    def test_17_validate_status_code_firewall_config(self):
        print("----- Test Case: test_17_validate_status_code_firewall_config -----")
        endpoint = "/tenant/config/access-restriction"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_18_validate_resp_firewall_config(self):
        print("----- Test Case: test_18_validate_resp_firewall_config -----")
        endpoint = "/tenant/config/access-restriction"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_18_validate_resp_firewall_config', response)
        save_runtime_response('testdata/api_response_runtime', 'test_18_validate_resp_firewall_config_runtime', response)

        if compare_responses(response, 'test_18_validate_resp_firewall_config'):
            print("Response Matched")
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())