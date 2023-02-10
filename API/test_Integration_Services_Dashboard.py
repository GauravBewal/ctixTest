import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of the Integration Services Dashboard
'''

service = 'ingestion'

class Dashboard(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_validate_status_code_create_dashboard(self):
        print("----- Test Case: test_01_validate_status_code_create_dashboard -----")
        payload = getJsonFileData('api_payload/test_01_validate_status_code_create_dashboard.json')
        endpoint = "/analytics/dashboard"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_02_validate_resp_create_dashboard(self):
        print("----- Test Case: test_02_validate_resp_create_dashboard -----")
        payload = getJsonFileData('api_payload/test_01_validate_status_code_create_dashboard.json')
        endpoint = "/analytics/dashboard"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_02_validate_resp_create_dashboard', response)
        save_runtime_response('testdata/api_response_runtime', 'test_02_validate_resp_create_dashboard_runtime', response)

        if compare_responses(response, 'test_02_validate_resp_create_dashboard', {"id", "dashboard_id"}):
            print("Response Matched")
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_03_validate_status_code_update_dashboard(self):
        print("----- Test Case: test_03_validate_status_code_update_dashboard -----")
        payload = getJsonFileData('api_payload/test_03_validate_status_code_update_dashboard.json')
        dashboard_id = list_of_values(getJsonFileData('api_response_runtime/test_02_validate_resp_create_dashboard_runtime.json'), 'dashboard_id')
        endpoint = f"/analytics/dashboard/{dashboard_id[0]}"
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

    def test_04_validate_resp_update_dashboard(self):
        print("----- Test Case: test_04_validate_resp_update_dashboard -----")
        payload = getJsonFileData('api_payload/test_03_validate_status_code_update_dashboard.json')
        dashboard_id = list_of_values(getJsonFileData('api_response_runtime/test_02_validate_resp_create_dashboard_runtime.json'), 'dashboard_id')
        endpoint = f"/analytics/dashboard/{dashboard_id[0]}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_04_validate_resp_update_dashboard", response)
        save_runtime_response("testdata/api_response_runtime", "test_04_validate_resp_update_dashboard_runtime", response)

        if compare_responses(response, 'test_04_validate_resp_update_dashboard', {"id", "dashboard_id"}):
            print("Response Matched")
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_05_validate_status_code_all_dashboard_details(self):
        print("----- Test Case: test_05_validate_status_code_all_dashboard_details -----")
        endpoint = "/analytics/dashboard"
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

    def test_06_validate_resp_all_dashboard_details(self):
        print("----- Test Case: test_06_validate_resp_all_dashboard_details -----")
        endpoint = "/analytics/dashboard"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_06_validate_resp_all_dashboard_details', response)
        save_runtime_response('testdata/api_response_runtime', 'test_06_validate_resp_all_dashboard_details_runtime', response)

        if compare_responses(response, 'test_06_validate_resp_all_dashboard_details', {"dashboard_id", "id"}):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_07_validate_status_code_delete_dashboard(self):
        print("----- Test Case: test_07_validate_status_code_delete_dashboard -----")
        dashboard_id = list_of_values(getJsonFileData('api_response_runtime/test_06_validate_resp_all_dashboard_details_runtime.json'), 'dashboard_id')
        endpoint = f"/analytics/dashboard/{dashboard_id[2]}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")

        response = requests.delete(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()

    def test_08_validate_resp_delete_dashboard(self):
        print("----- Test Case: test_08_validate_resp_delete_dashboard -----")
        dashboard_id = list_of_values(getJsonFileData('api_response_runtime/test_06_validate_resp_all_dashboard_details_runtime.json'),'dashboard_id')
        endpoint = f"/analytics/dashboard/{dashboard_id[3]}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_08_validate_resp_delete_dashboard", response)
        save_runtime_response("testdata/api_response_runtime", "test_08_validate_resp_delete_dashboard_runtime", response)

        if compare_responses(response, 'test_08_validate_resp_delete_dashboard'):
            print("Response Matched")
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()

    def test_09_validate_status_code_specific_dashboard_details(self):
        print("----- Test Case: test_09_validate_status_code_specific_dashboard_details -----")
        dashboard_id = list_of_values(getJsonFileData('api_response_runtime/test_06_validate_resp_all_dashboard_details_runtime.json'), 'dashboard_id')
        endpoint = f"/analytics/dashboard/{dashboard_id[0]}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_10_validate_resp_specific_dashboard_details(self):
        print("----- Test Case: test_10_validate_resp_specific_dashboard_details -----")
        dashboard_id = list_of_values(getJsonFileData('api_response_runtime/test_06_validate_resp_all_dashboard_details_runtime.json'),'dashboard_id')
        endpoint = f"/analytics/dashboard/{dashboard_id[0]}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_10_validate_resp_specific_dashboard_details", response)
        save_runtime_response("testdata/api_response_runtime", "test_10_validate_resp_specific_dashboard_details_runtime", response)

        if compare_responses(response, 'test_10_validate_resp_specific_dashboard_details', {"id", "dashboard_id"}):
            print("Response Matched")
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_11_validate_status_code_widget_list(self):
        print("----- Test Case: test_11_validate_status_code_widget_list -----")
        endpoint = "/analytics/widget"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_12_validate_resp_widget_list(self):
        print("----- Test Case: test_12_validate_resp_widget_list -----")
        endpoint = "/analytics/widget"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_12_validate_resp_widget_list", response)
        save_runtime_response("testdata/api_response_runtime", "test_12_validate_resp_widget_list_runtime", response)

        if compare_responses(response, 'test_12_validate_resp_widget_list', {"next"}):
            print("Response Matched")
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_13_validate_status_code_top_level_domain(self):
        print("----- Test Case: test_13_validate_status_code_top_level_domain -----")
        endpoint = "/analytics/utilities/tld/data"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_14_validate_resp_top_level_domain(self):
        print("----- Test Case: test_14_validate_resp_top_level_domain -----")
        endpoint = "/analytics/utilities/tld/data"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_14_validate_resp_top_level_domain", response)
        save_runtime_response("testdata/api_response_runtime", "test_14_validate_resp_top_level_domain_runtime", response)

        if compare_responses(response, 'test_14_validate_resp_top_level_domain', {"next"}):
            print("Response Matched")
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_15_validate_status_code_search_widget(self):
        print("----- Test Case: test_15_validate_status_code_search_widget -----")
        endpoint = "/analytics/widget/sdo_vs_sources"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_16_validate_resp_search_widget(self):
        print("----- Test Case: test_16_validate_resp_search_widget -----")
        endpoint = "/analytics/widget/sdo_vs_sources"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_16_validate_resp_search_widget", response)
        save_runtime_response("testdata/api_response_runtime", "test_16_validate_resp_search_widget_runtime", response)

        if compare_responses(response, 'test_16_validate_resp_search_widget'):
            print("Response Matched")
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_17_validate_status_code_retrieve_widget_data(self):
        print("----- Test Case: test_17_validate_status_code_retrieve_widget_data -----")
        endpoint = "/analytics/widget/top5_sdos/data"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        print(response.text)
        if response.status_code == 200:
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_18_validate_resp_retrieve_widget_data(self):
        print("----- Test Case: test_18_validate_resp_retrieve_widget_data -----")
        endpoint = "/analytics/widget/top5_sdos/data"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response("testdata/api_response", "test_18_validate_resp_retrieve_widget_data", response)
        save_runtime_response("testdata/api_response_runtime", "test_18_validate_resp_retrieve_widget_data_runtime", response)

        if compare_responses(response, 'test_18_validate_resp_retrieve_widget_data'):
            print("Response Matched")
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())