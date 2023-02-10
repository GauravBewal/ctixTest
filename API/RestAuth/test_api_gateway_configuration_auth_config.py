import unittest
import requests
from lib.api.common_utilities import *
service = 'rest-auth'
'''
This module contains all the testcases of API Gateway --> Configuration --> authentication configuration
'''


class AuthConfiguration(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_validate_status_code_LDAP_config_details(self):
        print("----- Test Case: test_01_validate_status_code_LDAP_config_details -----")
        endpoint = "/auth-config/ldap"
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

    def test_02_validate_response_LDAP_config_details(self):
        print("----- Test Case: test_02_validate_response_LDAP_config_details -----")
        endpoint = "/auth-config/ldap"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_02_validate_response_LDAP_config_details', response)
        save_runtime_response('testdata/api_response_runtime', 'test_02_validate_response_LDAP_config_details_runtime', response)

        if compare_responses(response, 'test_02_validate_response_LDAP_config_details'):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_03_validate_status_code_password_policy_details(self):
        print("----- Test Case: test_03_validate_status_code_password_policy_details -----")
        endpoint = "/auth-config/password-policy"
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

    def test_04_validate_resp_password_policy_details(self):
        print("----- Test Case: test_04_validate_resp_password_policy_details -----")
        endpoint = "/auth-config/password-policy"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_04_validate_resp_password_policy_details', response)
        save_runtime_response('testdata/api_response_runtime', 'test_04_validate_resp_password_policy_details_runtime', response)

        if compare_responses(response, 'test_04_validate_resp_password_policy_details'):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_05_validate_status_code_update_password_policy(self):
        print("----- Test Case: test_05_validate_status_code_update_password_policy -----")
        payload = getJsonFileData('api_payload/test_05_validate_status_code_update_password_policy.json')

        endpoint = "/auth-config/password-policy"
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

    def test_06_validate_resp_update_password_policy(self):
        print("----- Test Case: test_06_validate_resp_update_password_policy -----")
        payload = getJsonFileData('api_payload/test_05_validate_status_code_update_password_policy.json')

        endpoint = "/auth-config/password-policy"
        url = f"{base_url}{service}{endpoint}"

        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_06_validate_resp_update_password_policy", response)
        save_runtime_response("testdata/api_response_runtime", "test_06_validate_resp_update_password_policy_runtime", response)

        if compare_responses(response, 'test_06_validate_resp_update_password_policy'):
            print("Response Matched")
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_07_validate_status_code_google_sign_in_config(self):
        print("----- Test Case: test_07_validate_status_code_google_sign_in_config -----")
        endpoint = "/auth-config/google"
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

    def test_08_validate_resp_google_sign_in_config(self):
        print("----- Test Case: test_08_validate_resp_google_sign_in_config -----")
        endpoint = "/auth-config/google"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_08_validate_resp_google_sign_in_config', response)
        save_runtime_response('testdata/api_response_runtime', 'test_08_validate_resp_google_sign_in_config_runtime', response)

        if compare_responses(response, 'test_08_validate_resp_google_sign_in_config'):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_09_validate_status_code_user_password_config(self):
        print("----- Test Case: test_09_validate_status_code_user_password_config -----")
        endpoint = "/auth-config/user-pass"
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

    def test_10_validate_resp_user_password_config(self):
        print("----- Test Case: test_10_validate_resp_user_password_config -----")
        endpoint = "/auth-config/user-pass"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_10_validate_resp_user_password_config', response)
        save_runtime_response('testdata/api_response_runtime', 'test_10_validate_resp_user_password_config_runtime', response)

        if compare_responses(response, 'test_10_validate_resp_user_password_config'):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_11_validate_status_code_update_user_password_config(self):
        print("----- Test Case: test_11_validate_status_code_update_user_password_config -----")
        payload = getJsonFileData('api_payload/test_11_validate_status_code_update_user_password_config.json')

        endpoint = "/auth-config/user-pass"
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

    def test_12_validate_resp_update_user_password_config(self):
        print("----- Test Case: test_12_validate_resp_update_user_password_config -----")
        payload = getJsonFileData('api_payload/test_11_validate_status_code_update_user_password_config.json')

        endpoint = "/auth-config/user-pass"
        url = f"{base_url}{service}{endpoint}"

        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_12_validate_resp_update_user_password_config", response)
        save_runtime_response("testdata/api_response_runtime", "test_12_validate_resp_update_user_password_config_runtime", response)

        if compare_responses(response, 'test_12_validate_resp_update_user_password_config'):
            print("Response Matched")
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())