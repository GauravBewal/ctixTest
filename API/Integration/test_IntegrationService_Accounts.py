import unittest
import requests
from lib.api.common_utilities import *

'''
This modules contains all the test cases for Integration Service Accounts
'''

service = 'integration'


class IntegrationServicesAccounts(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def get_app_id(self, title):
        result = getJsonFileData('api_response_runtime/test_02_list_applications_runtime.json')
        for val in result["results"]:
            if val["title"] == title:
                app_id = val["id"]
                return app_id

    def create_account(self, test_case_name, app_name):
        print(f"----- Test Case: {test_case_name} -----")
        payload = getJsonFileData(f'api_payload/{test_case_name}.json')
        endpoint = f"/apps/{self.get_app_id(app_name)}/accounts"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response('testdata/api_response_runtime', f'{test_case_name}_runtime', response)

        if response.status_code == 201 and validate_schema(response, f'integration/accounts/{test_case_name}_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def update_account(self, test_case_name, app_name, result_file):
        print(f"----- Test Case: {test_case_name} -----")
        payload = getJsonFileData(f'api_payload/{test_case_name}.json')
        integration_app_id = self.get_app_id(app_name)
        result = getJsonFileData(f'api_response_runtime/{result_file}.json')
        integration_account_id = result["results"][0]["third_party_config_id"]
        payload["id"] = integration_account_id
        endpoint = f"/apps/{integration_app_id}/accounts/{integration_account_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', f'{test_case_name}_runtime', response)

        if response.status_code == 200 and validate_schema(response, f'integration/accounts/{test_case_name}_schema'):
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def get_account(self, test_case_name, app_name):
        print(f"----- Test Case: {test_case_name} -----")
        endpoint = f"/apps/{self.get_app_id(app_name)}/accounts"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', f'{test_case_name}_runtime', response)

        if response.status_code == 200 and validate_schema(response, f'integration/accounts/{test_case_name}_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def delete_account(self, test_case_name, app_name, result_file):
        print(f"----- Test Case: {test_case_name} -----")
        integration_app_id = self.get_app_id(app_name)
        result = getJsonFileData(f'api_response_runtime/{result_file}.json')
        integration_account_id = result["results"][0]["third_party_config_id"]
        endpoint = f"/apps/{integration_app_id}/accounts/{integration_account_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', f'{test_case_name}_runtime', response)

        if response.status_code == 200 and validate_schema(response, f'integration/accounts/{test_case_name}_schema'):
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()

    def test_01_create_CFTR_account(self):
        self.create_account('test_01_create_CFTR_account', 'CFTR')

    def test_02_update_CFTR_account(self):
        self.update_account('test_02_update_CFTR_account', 'CFTR', 'test_01_action_configs_CFTR_runtime')

    def test_03_get_CFTR_accounts(self):
        self.get_account('test_03_get_CFTR_accounts', 'CFTR')

    def test_04_delete_CFTR_account(self):
        self.delete_account('test_04_delete_CFTR_account', 'CFTR', 'test_01_action_configs_CFTR_runtime')

    def test_05_create_CSAP_account(self):
        self.create_account('test_05_create_CSAP_account', 'CSAP')

    def test_06_update_CSAP_account(self):
        self.update_account('test_06_update_CSAP_account', 'CSAP', 'test_04_action_configs_CSAP_runtime')

    def test_07_get_CSAP_accounts(self):
        self.get_account('test_07_get_CSAP_accounts', 'CSAP')

    def test_08_delete_CSAP_account(self):
        self.delete_account('test_08_delete_CSAP_account', 'CSAP', 'test_04_action_configs_CSAP_runtime')

    def test_09_create_CSOL_account(self):
        self.create_account('test_09_create_CSOL_account', 'CSOL')

    def test_10_update_CSOL_account(self):
        self.update_account('test_10_update_CSOL_account', 'CSOL', 'test_07_action_configs_CSOL_runtime')

    def test_11_get_CSOL_accounts(self):
        self.get_account('test_11_get_CSOL_accounts', 'CSOL')

    def test_12_delete_CSOL_account(self):
        self.delete_account('test_12_delete_CSOL_account', 'CSOL', 'test_07_action_configs_CSOL_runtime')

    def test_13_create_QRadar_account(self):
        self.create_account('test_13_create_QRadar_account', 'QRadar')

    def test_14_update_QRadar_account(self):
        self.update_account('test_14_update_QRadar_account', 'QRadar', 'test_10_action_configs_QRadar_runtime')

    def test_15_get_QRadar_accounts(self):
        self.get_account('test_15_get_QRadar_accounts', 'QRadar')

    def test_16_delete_QRadar_account(self):
        self.delete_account('test_16_delete_QRadar_account', 'QRadar', 'test_10_action_configs_QRadar_runtime')

    def test_17_create_Splunk_account(self):
        self.create_account('test_17_create_Splunk_account', 'Splunk')

    def test_18_update_Splunk_account(self):
        self.update_account('test_18_update_Splunk_account', 'Splunk', 'test_13_action_configs_Splunk_runtime')

    def test_19_get_Splunk_accounts(self):
        self.get_account('test_19_get_Splunk_accounts', 'Splunk')

    def test_20_delete_Splunk_account(self):
        self.delete_account('test_20_delete_Splunk_account', 'Splunk', 'test_13_action_configs_Splunk_runtime')

    def test_21_create_CORTEX_XSOAR_account(self):
        self.create_account('test_21_create_CORTEX_XSOAR_account', 'CORTEX-XSOAR')

    def test_22_update_CORTEX_XSOAR_account(self):
        self.update_account('test_22_update_CORTEX_XSOAR_account', 'CORTEX-XSOAR', 'test_16_action_configs_CORTEX_XSOAR_runtime')

    def test_23_get_CORTEX_XSOAR_accounts(self):
        self.get_account('test_23_get_CORTEX_XSOAR_accounts', 'CORTEX-XSOAR')

    def test_24_delete_CORTEX_XSOAR_account(self):
        self.delete_account('test_24_delete_CORTEX_XSOAR_account', 'CORTEX-XSOAR', 'test_16_action_configs_CORTEX_XSOAR_runtime')

    def test_25_create_Zscaler_Network_Security_account(self):
        self.create_account('test_25_create_Zscaler_Network_Security_account', 'Zscaler Network Security')

    def test_26_update_Zscaler_Network_Security_account(self):
        self.update_account('test_26_update_Zscaler_Network_Security_account', 'Zscaler Network Security', 'test_19_action_configs_Zscaler_Network_Security_runtime')

    def test_27_get_Zscaler_Network_Security_accounts(self):
        self.get_account('test_27_get_Zscaler_Network_Security_accounts', 'Zscaler Network Security')

    def test_28_delete_Zscaler_Network_Security_account(self):
        self.delete_account('test_28_delete_Zscaler_Network_Security_account', 'Zscaler Network Security', 'test_19_action_configs_Zscaler_Network_Security_runtime')

    def test_29_create_Alien_Vault_account(self):
        self.create_account('test_29_create_Alien_Vault_account', 'Alien Vault')

    def test_30_update_Alien_Vault_account(self):
        self.update_account('test_30_update_Alien_Vault_account', 'Alien Vault', 'test_22_action_configs_Alien_Vault_runtime')

    def test_31_get_Alien_Vault_accounts(self):
        self.get_account('test_31_get_Alien_Vault_accounts', 'Alien Vault')

    def test_32_delete_Alien_Vault_account(self):
        self.delete_account('test_32_delete_Alien_Vault_account', 'Alien Vault', 'test_22_action_configs_Alien_Vault_runtime')

    def test_33_create_AbuseIPDB_account(self):
        self.create_account('test_33_create_AbuseIPDB_account', 'AbuseIPDB')

    def test_34_update_AbuseIPDB_account(self):
        self.update_account('test_34_update_AbuseIPDB_account', 'AbuseIPDB', 'test_25_action_configs_AbuseIPDB_runtime')

    def test_35_get_AbuseIPDB_accounts(self):
        self.get_account('test_35_get_AbuseIPDB_accounts', 'AbuseIPDB')

    def test_36_delete_AbuseIPDB_account(self):
        self.delete_account('test_36_delete_AbuseIPDB_account', 'AbuseIPDB', 'test_25_action_configs_AbuseIPDB_runtime')

    def test_37_create_AbuseIPDB_account(self):
        self.create_account('test_33_create_AbuseIPDB_account', 'AbuseIPDB')

    def test_38_update_AbuseIPDB_account(self):
        self.update_account('test_34_update_AbuseIPDB_account', 'AbuseIPDB', 'test_25_action_configs_AbuseIPDB_runtime')

    def test_39_get_AbuseIPDB_accounts(self):
        self.get_account('test_35_get_AbuseIPDB_accounts', 'AbuseIPDB')

    def test_40_delete_AbuseIPDB_account(self):
        self.delete_account('test_36_delete_AbuseIPDB_account', 'AbuseIPDB', 'test_25_action_configs_AbuseIPDB_runtime')

    def test_41_create_Alexa_Ranking_account(self):
        self.create_account('test_41_create_Alexa_Ranking_account', 'Alexa Ranking')

    def test_42_update_Alexa_Ranking_account(self):
        self.update_account('test_42_update_Alexa_Ranking_account', 'Alexa Ranking', 'test_28_action_configs_Alexa_Ranking_runtime')

    def test_43_get_Alexa_Ranking_accounts(self):
        self.get_account('test_43_get_Alexa_Ranking_accounts', 'Alexa Ranking')

    def test_44_delete_Alexa_Ranking_account(self):
        self.delete_account('test_44_delete_Alexa_Ranking_account', 'Alexa Ranking', 'test_28_action_configs_Alexa_Ranking_runtime')


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
