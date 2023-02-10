import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of the Integration Enrichment tools
'''

service = 'integration'

class IntegrationServicesEnrichmentTools(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    #     this test case need to rechecked, whether we support the enrichment in threat investigation or not
    def test_01_validate_status_code_enrichment_tools(self):
        print("----- Test Case: test_01_validate_status_code_enrichment_tools -----")
        endpoint = f"/apps/actions/?action_name=get_ip%2Cget_domain%2Cget_hash%2Cget_cve%2Cget_url&full_list=true/"
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

if __name__ == '__main__':
    unittest.main(testRunner=reporting())