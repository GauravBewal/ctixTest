import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of ingestion --> reports
'''

service = 'ingestion'

class Reports(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_create_reports(self):
        print("----- Test Case: test_01_create_reports -----")
        payload = getJsonFileData('api_payload/test_01_create_reports.json')
        endpoint = "/reports"

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_01_create_reports_runtime', response)

        if response.status_code == 201 and validate_schema(response, 'ingestion/report/test_01_create_reports_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_02_report_details(self):
        print("----- Test Case: test_02_report_details -----")
        report_id = getJsonFileData('api_response_runtime/test_01_create_reports_runtime.json')["data"]["id"]
        endpoint = f"/reports/{report_id}"

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_02_report_details_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/report/test_02_report_details_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_03_edit_report(self):
        print("----- Test Case: test_03_edit_report -----")
        payload = getJsonFileData('api_payload/test_03_edit_report.json')
        report_id = getJsonFileData('api_response_runtime/test_01_create_reports_runtime.json')["data"]["id"]
        endpoint = f"/reports/{report_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response('testdata/api_response_runtime', 'test_03_edit_report_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/report/test_03_edit_report_schema'):
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_04_run_report(self):
        print("----- Test Case: test_04_run_report -----")
        payload = getJsonFileData('api_payload/test_04_run_report.json')
        report_id = getJsonFileData('api_response_runtime/test_01_create_reports_runtime.json')["data"]["id"]
        endpoint = f"/reports/{report_id}/run"

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_04_run_report_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/report/test_04_run_report_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_05_report_run_logs(self):
        print("----- Test Case: test_05_report_run_logs -----")
        report_id = getJsonFileData('api_response_runtime/test_01_create_reports_runtime.json')["data"]["id"]
        endpoint = f"/reports/{report_id}/run"

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_05_report_run_logs_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/report/test_05_report_run_logs_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_06_download_file(self):
        print("----- Test Case: test_06_download_file -----")
        file_id = getJsonFileData('api_response_runtime/test_05_report_run_logs_runtime.json')["results"][0]["files"][0]["id"]
        endpoint = f"/file/{file_id}"

        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        # print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_06_download_file_runtime', response)

        if response.status_code == 200 and validate_schema(response,
                                                           'ingestion/report/test_06_download_file_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_07_download_external_file(self):
        print("----- Test Case: test_07_download_external_file -----")
        url = getJsonFileData('api_response_runtime/test_06_download_file_runtime.json')["url"]

        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}&{str(authentication()).replace('?', '')}")
        print(f"response code is : {response.status_code}")
        # print(response.text)

        # save_runtime_response('testdata/api_response_runtime', 'test_07_download_external_file_runtime', response)

        # Don't need to validate the schema as the response is text file not json
        if response.status_code == 200:
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_08_list_reports(self):
        print("----- Test Case: test_08_list_reports -----")
        endpoint = f"/reports"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_08_list_reports_runtime', response)

        if response.status_code == 200 and validate_schema(response,'ingestion/report/test_08_list_reports_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_09_delete_report(self):
        print("----- Test Case: test_09_delete_report -----")
        report_id = getJsonFileData('api_response_runtime/test_01_create_reports_runtime.json')["data"]["id"]
        endpoint = f"/reports/{report_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        # print(response.text)

        # save_runtime_response('testdata/api_response_runtime', 'test_09_delete_report_runtime', response)

        # response body is empty so no need to verify the schema
        if response.status_code == 204:
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
