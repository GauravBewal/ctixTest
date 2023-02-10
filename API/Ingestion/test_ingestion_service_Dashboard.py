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

    def test_01_create_dashboard(self):
        print("----- Test Case: test_01_create_dashboard -----")
        payload = getJsonFileData('api_payload/test_01_create_dashboard.json')
        endpoint = "/analytics/dashboard"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_01_create_dashboard_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/dashboard/test_01_create_dashboard_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_02_update_dashboard(self):
        print("----- Test Case: test_02_update_dashboard -----")
        payload = getJsonFileData('api_payload/test_02_update_dashboard.json')
        dashboard_id = list_of_values(getJsonFileData('api_response_runtime/test_01_create_dashboard_runtime.json'), 'dashboard_id')
        endpoint = f"/analytics/dashboard/{dashboard_id[0]}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_update_dashboard_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/dashboard/test_02_update_dashboard_schema'):
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_03_all_dashboard_details(self):
        print("----- Test Case: test_03_all_dashboard_details -----")
        endpoint = "/analytics/dashboard"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_03_all_dashboard_details_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/dashboard/test_03_all_dashboard_details_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_04_specific_dashboard_details(self):
        print("----- Test Case: test_04_specific_dashboard_details -----")
        result = getJsonFileData('api_response_runtime/test_03_all_dashboard_details_runtime.json')
        dashboard_id = ""
        for val in result["results"]:
            if val["name"] == "Analyst Dashboard":
                dashboard_id = val["dashboard_id"]
                break

        endpoint = f"/analytics/dashboard/{dashboard_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_04_specific_dashboard_details_runtime', response)

        if response.status_code == 200 and validate_schema(response,'ingestion/dashboard/test_04_specific_dashboard_details_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_05_widget_list(self):
        print("----- Test Case: test_05_widget_list -----")
        endpoint = "/analytics/widget"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_05_widget_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/dashboard/test_05_widget_list_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_06_top_level_domain(self):
        print("----- Test Case: test_06_top_level_domain -----")
        endpoint = "/analytics/utilities/tld/data"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_06_top_level_domain_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/dashboard/test_06_top_level_domain_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_07_search_widget(self):
        print("----- Test Case: test_07_search_widget -----")
        endpoint = "/analytics/widget/sdo_vs_sources"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_07_search_widget_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/dashboard/test_07_search_widget_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_08_retrieve_widget_data(self):
        print("----- Test Case: test_08_retrieve_widget_data -----")
        endpoint = "/analytics/widget/top5_sdos/data"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_08_retrieve_widget_data_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/dashboard/test_08_retrieve_widget_data_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_09_export_dashboard(self):
        print("----- Test Case: test_09_export_dashboard -----")
        payload = getJsonFileData('api_payload/test_09_export_dashboard.json')
        payload["dashboards"].append(getJsonFileData('api_response_runtime/test_01_create_dashboard_runtime.json')["dashboard_id"])
        endpoint = "/analytics/dashboard_export"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_09_export_dashboard_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/dashboard/test_09_export_dashboard_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_10_export_widget(self):
        print("----- Test Case: test_10_export_widget -----")
        payload = getJsonFileData('api_payload/test_10_export_widget.json')
        payload["dashboards"].append( getJsonFileData('api_response_runtime/test_01_create_dashboard_runtime.json')["dashboard_id"])
        endpoint = "/analytics/dashboard_export"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_10_export_widget_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/dashboard/test_10_export_widget_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_11_delete_dashboard(self):
        print("----- Test Case: test_11_delete_dashboard -----")
        dashboard_id = getJsonFileData('api_response_runtime/test_01_create_dashboard_runtime.json')["dashboard_id"]
        endpoint = f"/analytics/dashboard/{dashboard_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_11_delete_dashboard_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/dashboard/test_11_delete_dashboard_schema'):
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())