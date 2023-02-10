import unittest
import requests
from lib.api.common_utilities import *
from jsonschema import validate
service = ""
'''
This module contains all the testcases of the Ping
'''


class Ping(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_validate_status_code_ping(self):
        print("----- Test Case: test_01_validate_status_code_ping -----")
        endpoint = "ping"
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

    def test_02_validate_response_ping(self):
        print("----- Test Case: test_02_validate_response_ping -----")
        endpoint = "ping"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)
        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_02_validate_response_ping', response)
        save_runtime_response('testdata/api_response_runtime', 'test_02_validate_response_ping_runtime', response)

        file_name = os.path.join(os.environ["PYTHONPATH"], "testdata", f"api_response/test_02_validate_response_ping.json")
        f = open(file_name)
        # This will load json file as a dict object
        schema = json.load(f)
        # response = json.loads(response.text)
        f.close()
        response = {"result":"None"
                    }
        try:
            validate(instance=response, schema=schema)
            print("Schema is valid")
        except Exception as e:
            print(e)
            print("Invalid JSON")
        # if compare_responses(response, 'test_02_validate_response_ping'):
        #     print("Response Matched")
        #     print("[PASSED] Get request is successful")
        # else:
        #     print("[FAILED] Get request is not successful")
        #     self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())