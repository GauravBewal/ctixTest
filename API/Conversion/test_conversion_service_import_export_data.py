import unittest
import requests
from lib.api.common_utilities import *
service = 'conversion'
'''
This module contains all the testcases of the Conversion Service Import Export Data in CTIX
'''


class DataImportExport(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_import_allowed_indicator(self):
        log("----- Test Case: test_01_import_allowed_indicator -----")
        payload = getJsonFileData('api_payload/test_01_import_allowed_indicator.json')
        file_name = os.path.join(os.environ["PYTHONPATH"], "testdata", "api_payload/indicator_allowed_csv.csv")
        test_file = open(file_name, "rb")
        payload["file"] = test_file
        endpoint = "/import/csv"
        temp = {"component": "whitelist"}
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", data=temp, files=payload)
        test_file.close()
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_import_allowed_indicator_runtime', response)

        if response.status_code == 201 and validate_schema(response, 'conversion/Import_And_Export_Data_In_CTIX/test_01_import_allowed_indicator_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_02_export_allowed_indicator(self):
        log("----- Test Case: test_02_export_allowed_indicator -----")
        payload = getJsonFileData('api_payload/test_02_export_allowed_indicator.json')
        endpoint = "/export"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", data=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_export_allowed_indicator_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Import_And_Export_Data_In_CTIX/test_02_export_allowed_indicator_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_03_import_stix1_dot_x(self):
        log("----- Test Case: test_03_import_stix1_dot_x -----")
        payload = getJsonFileData('api_payload/test_03_import_stix1_dot_x.json')
        file_name = os.path.join(os.environ["PYTHONPATH"], "testdata", "import_intel/STIX-1.x.xml")
        test_file = open(file_name, "rb")
        payload["file"] = test_file
        endpoint = "/import/stix1"
        temp = {"send_to_kafka": True}
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", data=temp, files=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_03_import_stix1_dot_x_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Import_And_Export_Data_In_CTIX/test_03_import_stix1_dot_x_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_04_import_stix2_dot_1(self):
        log("----- Test Case: test_04_import_stix2_dot_1 -----")
        payload = getJsonFileData('api_payload/test_04_import_stix2_dot_1.json')
        file_name = os.path.join(os.environ["PYTHONPATH"], "testdata", "import_intel/STIX-2.1.json")
        test_file = open(file_name, "rb")
        payload["file"] = test_file
        endpoint = "/import/stix2"
        temp = {"send_to_kafka": True, "version" : 2.1}
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", params=temp, files=payload)
        test_file.close()
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_04_import_stix2_dot_1_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Import_And_Export_Data_In_CTIX/test_04_import_stix2_dot_1_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_05_download_template(self):
        log("----- Test Case: test_05_download_template -----")
        payload = {"component": "whitelist"}
        endpoint = "/export/template"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_05_download_template_runtime', response)

        if response.status_code == 200 and validate_schema(response,'conversion/Import_And_Export_Data_In_CTIX/test_05_download_template_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())