import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of ingestion --> Fang/Defang endpoints
'''
service = 'ingestion'

class FangDefang(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_indicator_type(self):
        print("----- Test Case: test_01_indicator_type -----")
        endpoint = "/utilities/ioc-types"
        param = {
            "q": "dom"
        }
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_01_indicator_type_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/fang_defang/test_01_indicator_type_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_02_retrieve_country_data(self):
        print("----- Test Case: test_02_retrieve_country_data -----")
        endpoint = "/utilities/countries/"
        param = {
            "full_list": True
        }
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(response.text)

        save_runtime_response('testdata/api_response_runtime', 'test_02_retrieve_country_data_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'ingestion/fang_defang/test_02_retrieve_country_data_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())