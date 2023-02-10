import unittest
import requests
from lib.api.common_utilities import *
service = 'rest-auth'
'''
This module contains all the testcases of the API Gateway Users
'''


class Users(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_validate_status_code_list_users(self):
        print("----- Test Case: test_01_validate_status_code_list_users -----")
        endpoint = "/users"
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

    def test_02_validate_response_list_users(self):
        print("----- Test Case: test_02_validate_response_list_users -----")
        endpoint = "/users"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_02_validate_response_list_users', response)
        save_runtime_response('testdata/api_response_runtime', 'test_02_validate_response_list_users_runtime', response)

        if compare_responses(response, 'test_02_validate_response_list_users'):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_03_validate_status_code_user_details(self):
        print("----- Test Case: test_03_validate_status_code_list_components -----")
        endpoint = "/user-details"
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

    def test_04_validate_response_user_details(self):
        print("----- Test Case: test_04_validate_response_user_details -----")
        endpoint = "/user-details"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_04_validate_response_user_details', response)
        save_runtime_response('testdata/api_response_runtime', 'test_04_validate_response_user_details_runtime',response)

        if compare_responses(response, 'test_04_validate_response_user_details', {'id', 'user_id' ,'created', 'date_joined', 'last_active_session', 'last_login_location', 'last_login_ip'}):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_05_validate_status_code_user_boarding(self):
        print("----- Test Case: test_05_validate_status_code_user_boarding -----")
        endpoint = "/user-boarding"
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

    def test_06_validate_response_user_boarding(self):
        print("----- Test Case: test_06_validate_response_user_boarding -----")
        endpoint = "/user-boarding"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_06_validate_response_user_boarding', response)
        save_runtime_response('testdata/api_response_runtime', 'test_06_validate_response_user_boarding_runtime',response)

        if compare_responses(response, 'test_06_validate_response_user_boarding', {'tenant_name', 'tenant_service_end_time'}):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_07_validate_status_code_user_share(self):
        print("----- Test Case: test_07_validate_status_code_user_share -----")
        endpoint = "/user-share"
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

    def test_08_validate_response_user_share(self):
        print("----- Test Case: test_08_validate_response_user_share -----")
        endpoint = "/user-share"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_08_validate_response_user_share', response)
        save_runtime_response('testdata/api_response_runtime', 'test_08_validate_response_user_share_runtime',response)

        if compare_responses(response, 'test_08_validate_response_user_share'):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_09_validate_status_code_user_logs(self):
        print("----- Test Case: test_09_validate_status_code_user_logs -----")
        user_id = list_of_values(getJsonFileData('api_response_runtime/test_04_validate_response_user_details_runtime.json'), 'user_id')[0]
        endpoint = f"/logs/user/{user_id}"
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

    def test_10_validate_response_user_logs(self):
        print("----- Test Case: test_10_validate_response_user_logs -----")
        user_id = \
        list_of_values(getJsonFileData('api_response_runtime/test_04_validate_response_user_details_runtime.json'),'user_id')[0]
        endpoint = f"/logs/user/{user_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_10_validate_response_user_logs', response)
        save_runtime_response('testdata/api_response_runtime', 'test_10_validate_response_user_logs_runtime',response)

        if compare_responses(response, 'test_10_validate_response_user_logs', {'next', 'api_start_time', 'ip_address', 'timestamp', 'user_id', 'api_end_time', 'api_process_time', 'user_agent'}):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())