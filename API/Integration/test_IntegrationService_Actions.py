import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of the Integration Services Actions
'''
service = 'integration'

class IntegrationServicesAction(unittest.TestCase):

    @classmethod
    def setUpClass(self):
       pass

    def get_app_id(self, title):
        result = getJsonFileData('api_response_runtime/test_02_list_applications_runtime.json')
        for val in result["results"]:
            if val["title"] == title:
                app_id = val["id"]
                return app_id

    def get_app_action_config(self, test_case_name, app_name):
        print(f"----- Test Case: {test_case_name} -----")
        endpoint = f"/apps/{self.get_app_id(app_name)}/action_configs"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', f'{test_case_name}_runtime', response)

        if response.status_code == 200 and validate_schema(response,f'integration/actions/{test_case_name}_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def update_app_action(self, test_case_name, app_name, result_file):
        print(f"----- Test Case: {test_case_name} -----")
        payload = getJsonFileData(f'api_payload/{test_case_name}.json')
        result = getJsonFileData(f'api_response_runtime/{result_file}.json')
        for i in range(0,len(result["results"][0]["actions"])):
            integration_action_id = result["results"][0]["actions"][i]["third_party_action_id"]
            third_party_config_id = result["results"][0]["third_party_config_id"]
            slug = result["results"][0]["actions"][i]["action_slug"]
            payload["id"] = integration_action_id
            payload["third_party_config_id"] = third_party_config_id
            payload["slug"] = slug
            endpoint = f"/apps/{self.get_app_id(app_name)}/actions/{integration_action_id}"
            url = f"{base_url}{service}{endpoint}"
            print(f'Making the PUT request for the {url}')
            print("Calling authentication function for getting the unique authenticator")
            response = requests.put(f"{url}/{authentication()}", json=payload)
            print(f"response code is : {response.status_code}")
            print(f"Received response is: {response.text}")

            save_runtime_response('testdata/api_response_runtime', f'{test_case_name}_runtime', response)

            if response.status_code == 200 and validate_schema(response, f'integration/actions/{test_case_name}_schema'):
                print("[PASSED] PUT request is successful")
            else:
                print("[FAILED] PUT request is not successful")
                self.fail()

    def get_app_action(self, test_case_name, app_name, result_file):
        print(f"----- Test Case: {test_case_name} -----")
        result = getJsonFileData(f'api_response_runtime/{result_file}.json')
        integration_action_id = result["results"][0]["actions"][0]["third_party_action_id"]
        third_party_config_id = result["results"][0]["third_party_config_id"]
        param = {
            "third_party_config_id": third_party_config_id
        }
        endpoint = f"/apps/{self.get_app_id(app_name)}/actions/{integration_action_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', f'{test_case_name}_runtime', response)

        if response.status_code == 200 and validate_schema(response, f'integration/actions/{test_case_name}_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_01_action_configs_CFTR(self):
        self.get_app_action_config('test_01_action_configs_CFTR', 'CFTR')

    def test_02_update_action_CFTR(self):
        self.update_app_action('test_02_update_action_CFTR', 'CFTR', 'test_01_action_configs_CFTR_runtime')

    def test_03_actions_CFTR(self):
        self.get_app_action('test_03_actions_CFTR', 'CFTR', 'test_01_action_configs_CFTR_runtime')

    def test_04_action_configs_CSAP(self):
        self.get_app_action_config('test_04_action_configs_CSAP', 'CSAP')

    def test_05_update_action_CSAP(self):
        self.update_app_action('test_05_update_action_CSAP', 'CSAP', 'test_04_action_configs_CSAP_runtime')

    def test_06_actions_CSAP(self):
        self.get_app_action('test_06_actions_CSAP', 'CSAP', 'test_04_action_configs_CSAP_runtime')

    def test_07_action_configs_CSOL(self):
        self.get_app_action_config('test_07_action_configs_CSOL', 'CSOL')

    def test_08_update_action_CSOL(self):
        self.update_app_action('test_08_update_action_CSOL', 'CSOL', 'test_07_action_configs_CSOL_runtime')

    def test_09_actions_CSOL(self):
        self.get_app_action('test_09_actions_CSOL', 'CSOL', 'test_07_action_configs_CSOL_runtime')

    def test_10_action_configs_QRadar(self):
        self.get_app_action_config('test_10_action_configs_QRadar', 'QRadar')

    def test_11_update_action_QRadar(self):
        self.update_app_action('test_11_update_action_QRadar', 'QRadar', 'test_10_action_configs_QRadar_runtime')

    def test_12_actions_QRadar(self):
        self.get_app_action('test_12_actions_QRadar', 'QRadar', 'test_10_action_configs_QRadar_runtime')

    def test_13_action_configs_Splunk(self):
        self.get_app_action_config('test_13_action_configs_Splunk', 'Splunk')

    def test_14_update_action_Splunk(self):
        self.update_app_action('test_14_update_action_Splunk', 'Splunk', 'test_13_action_configs_Splunk_runtime')

    def test_15_actions_Splunk(self):
        self.get_app_action('test_15_actions_Splunk', 'Splunk', 'test_13_action_configs_Splunk_runtime')

    def test_16_action_configs_CORTEX_XSOAR(self):
        self.get_app_action_config('test_16_action_configs_CORTEX_XSOAR', 'CORTEX-XSOAR')

    def test_17_update_action_CORTEX_XSOAR(self):
        self.update_app_action('test_17_update_action_CORTEX_XSOAR', 'CORTEX-XSOAR', 'test_16_action_configs_CORTEX_XSOAR_runtime')

    def test_18_actions_CORTEX_XSOAR(self):
        self.get_app_action('test_18_actions_CORTEX_XSOAR', 'CORTEX-XSOAR', 'test_16_action_configs_CORTEX_XSOAR_runtime')

    def test_19_action_configs_Zscaler_Network_Security(self):
        self.get_app_action_config('test_19_action_configs_Zscaler_Network_Security', 'Zscaler Network Security')

    def test_20_update_action_Zscaler_Network_Security(self):
        self.update_app_action('test_20_update_action_Zscaler_Network_Security', 'Zscaler Network Security', 'test_19_action_configs_Zscaler_Network_Security_runtime')

    def test_21_actions_Zscaler_Network_Security(self):
        self.get_app_action('test_21_actions_Zscaler_Network_Security', 'Zscaler Network Security', 'test_19_action_configs_Zscaler_Network_Security_runtime')

    def test_22_action_configs_Alien_Vault(self):
        self.get_app_action_config('test_22_action_configs_Alien_Vault', 'Alien Vault')

    def test_23_update_action_Alien_Vault(self):
        self.update_app_action('test_23_update_action_Alien_Vault', 'Alien Vault', 'test_22_action_configs_Alien_Vault_runtime')

    def test_24_actions_Alien_Vault(self):
        self.get_app_action('test_24_actions_Alien_Vault', 'Alien Vault', 'test_22_action_configs_Alien_Vault_runtime')

    def test_25_action_configs_AbuseIPDB(self):
        self.get_app_action_config('test_25_action_configs_AbuseIPDB', 'AbuseIPDB')

    def test_26_update_action_AbuseIPDB(self):
        self.update_app_action('test_26_update_action_AbuseIPDB', 'AbuseIPDB', 'test_25_action_configs_AbuseIPDB_runtime')

    def test_27_actions_AbuseIPDB(self):
        self.get_app_action('test_27_actions_AbuseIPDB', 'AbuseIPDB', 'test_25_action_configs_AbuseIPDB_runtime')

    def test_28_action_configs_Alexa_Ranking(self):
        self.get_app_action_config('test_28_action_configs_Alexa_Ranking', 'Alexa Ranking')

    def test_29_update_action_Alexa_Ranking(self):
        self.update_app_action('test_29_update_action_Alexa_Ranking', 'Alexa Ranking', 'test_28_action_configs_Alexa_Ranking_runtime')

    def test_30_actions_Alexa_Ranking(self):
        self.get_app_action('test_30_actions_Alexa_Ranking', 'Alexa Ranking', 'test_28_action_configs_Alexa_Ranking_runtime')

    def test_04_rule_actions(self):
        print("----- Test Case: test_04_rule_actions -----")
        endpoint = f"/apps/rule-actions"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_04_rule_actions_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'integration/actions/test_04_rule_actions_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())