import unittest
import requests
from lib.api.common_utilities import *

'''
IS : IS stands for Integration service
This modules contains all the test cases for Integration Service Reset Apps
'''

service = 'integration'

class IntegrationServicesResetApp(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def get_id(self, title):
        '''
        This funuction help in getting the id of the integration application if the title is provided
        '''
        integration_app_id = list_of_values(getJsonFileData('api_response_runtime/test_04_validate_response_IS_apps_application_runtime.json'),'results')
        id = ""
        for i in range(0, len(integration_app_id[0])):
            if integration_app_id[0][i]['title'] == title:
                id = integration_app_id[0][i]['id']
        return id

    def test_01_validate_status_code_reset_apps_AlienVault(self):
        print("----- Test Case: test_01_validate_status_code_reset_apps_AlienVault -----")
        integration_app_id = self.get_id('Alien Vault')
        endpoint = f'/apps/reset_tool/{integration_app_id}'
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # save_runtime_response("testdata/api_response_runtime","test_07_validate_status_code_create_accounts_AlienVault_runtime", response)

        if response.status_code == 200:
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())