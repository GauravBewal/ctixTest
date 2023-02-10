import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of the Enricment Policy and Confidence score - Enrichment Policy
'''

service = 'conversion'

class SourceWeightage(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_source_weightage(self):
        log("----- Test Case: test_01_source_weightage -----")
        endpoint = '/feed-sources/source-weightage/api_feeds'
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_source_weightage_runtime', response)

        if response.status_code == 200 and validate_schema(response,'conversion/test_01_source_weightage_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_02_update_source_weightage(self):
        log("----- Test Case: test_02_update_source_weightage -----")

        result = getJsonFileData('api_response_runtime/test_01_source_weightage_runtime.json')["results"]
        if len(result) == 0:
            exit()

        payload = {
            str(result[0]["id"]) : {
                "name": result[0]["name"],
                "weightage" : 80
            }
        }

        endpoint = f"/feed-sources/source-weightage"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_update_source_weightage_runtime', response)

        if response.status_code == 201 and validate_schema(response, 'conversion/test_02_update_source_weightage_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())