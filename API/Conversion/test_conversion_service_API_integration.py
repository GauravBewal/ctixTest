import unittest
import requests
from lib.api.common_utilities import *
service = 'conversion'

'''
This module contains all the testcases of the Conversion Service API integrations
'''


class APIIntegrations(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_verify_api_feed_list(self):
        log("----- Test Case: test_01_verify_api_feed_list -----")
        endpoint = "/api-feeds/apps"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")
        save_runtime_response('testdata/api_response_runtime', 'test_01_verify_api_feed_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/API_Integration/test_01_verify_api_feed_list_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_02_create_api_feed_account(self):
        log("----- Test Case: test_02_create_api_feed_account -----")
        results = getJsonFileData("api_response_runtime/test_01_verify_api_feed_list_runtime.json")['results']
        app_id  = ""
        for val in results:
            if val["title"] == 'Alien Vault':
                app_id = val["id"]
                if val["configured_once"] == True:
                    requests.delete(f"{base_url}{service}/api-feeds/apps/reset_tool/{app_id}/{authentication()}")

        payload = getJsonFileData("api_payload/test_02_create_api_feed_account.json")
        endpoint = f"/api-feeds/apps/{app_id}/accounts"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_create_api_feed_account_runtime', response)

        if response.status_code == 201 and validate_schema(response, 'conversion/API_Integration/test_02_create_api_feed_account_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_03_action_configuration_list(self):
        log("----- Test Case: test_03_action_configuration_list -----")
        results = getJsonFileData("api_response_runtime/test_01_verify_api_feed_list_runtime.json")['results']
        app_id = ""
        for val in results:
            if val["title"] == 'Alien Vault':
                app_id = val["id"]
                break

        endpoint = f"/api-feeds/apps/{app_id}/action_configs"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")
        save_runtime_response('testdata/api_response_runtime', 'test_03_action_configuration_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/API_Integration/test_03_action_configuration_list_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_04_update_api_feed_action(self):
        log("----- Test Case: test_04_update_api_feed_action -----")
        account_id = list_of_values(getJsonFileData('api_response_runtime/test_03_action_configuration_list_runtime.json'), 'third_party_action_id')[0]
        results = getJsonFileData("api_response_runtime/test_01_verify_api_feed_list_runtime.json")['results']
        app_id = ""
        for val in results:
            if val["title"] == 'Alien Vault':
                app_id = val["id"]
                break

        payload = getJsonFileData('api_payload/test_04_update_api_feed_action.json')
        payload["third_party_config_id"] = list_of_values(getJsonFileData('api_response_runtime/test_03_action_configuration_list_runtime.json'),'third_party_config_id')[0]
        endpoint = f'/api-feeds/apps/{app_id}/actions/{account_id}'
        url = f"{base_url}{service}{endpoint}"

        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_04_update_api_feed_action_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/API_Integration/test_04_update_api_feed_action_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

    # this case need to be redone. Not sure what this endpooint is doing
    def test_05_configure_manual_polling(self):
        log("----- Test Case: test_05_configure_manual_polling -----")
        third_party_config_id =list_of_values(getJsonFileData('api_response_runtime/test_03_action_configuration_list_runtime.json'),'third_party_config_id')[0]
        results = getJsonFileData("api_response_runtime/test_01_verify_api_feed_list_runtime.json")['results']
        app_id = ""
        for val in results:
            if val["title"] == 'Alien Vault':
                app_id = val["id"]
                break

        payload = getJsonFileData('api_payload/test_04_update_api_feed_action.json')
        payload["third_party_config_id"] = third_party_config_id
        endpoint = f'/api-feeds/apps/{app_id}/update/actions'
        url = f"{base_url}{service}{endpoint}"

        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        # save_runtime_response('testdata/api_response_runtime', 'test_04_update_api_feed_action_runtime', response)
        #
        # if response.status_code == 200 and validate_schema(response, 'conversion/API_Integration/test_04_update_api_feed_action_schema'):
        #     log("[PASSED] GET request is successful")
        # else:
        #     log("[FAILED] GET request is not successful")
        #     self.fail()

    def test_06_api_feeds_details(self):
        log("----- Test Case: test_06_api_feeds_details -----")
        results = getJsonFileData("api_response_runtime/test_01_verify_api_feed_list_runtime.json")['results']
        app_id = ""
        for val in results:
            if val["title"] == 'Alien Vault':
                app_id = val["id"]
                break
        endpoint = f"/api-feeds/apps/detail/{app_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")
        save_runtime_response('testdata/api_response_runtime', 'test_06_api_feeds_details_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/API_Integration/test_06_api_feeds_details_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_07_retrieve_api_feed_account_details(self):
        log("----- Test Case: test_07_retrieve_api_feed_account_details -----")
        results = getJsonFileData("api_response_runtime/test_01_verify_api_feed_list_runtime.json")['results']
        app_id = ""
        for val in results:
            if val["title"] == 'Alien Vault':
                app_id = val["id"]
                break
        account_id = list_of_values(getJsonFileData("api_response_runtime/test_02_create_api_feed_account_runtime.json"), "id")[0]

        endpoint = f"/api-feeds/apps/{app_id}/accounts/{account_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_07_retrieve_api_feed_account_details_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/API_Integration/test_07_retrieve_api_feed_account_details_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_08_accounts_of_an_api_feed_connector(self):
        log("----- Test Case: test_08_accounts_of_an_api_feed_connector -----")
        results = getJsonFileData("api_response_runtime/test_01_verify_api_feed_list_runtime.json")['results']
        app_id = ""
        for val in results:
            if val["title"] == 'Alien Vault':
                app_id = val["id"]
                break
        endpoint = f"/api-feeds/apps/{app_id}/accounts"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_08_accounts_of_an_api_feed_connector_runtime', response)

        if response.status_code == 200 and validate_schema(response,'conversion/API_Integration/test_08_accounts_of_an_api_feed_connector_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_09_update_api_feed_account_details(self):
        log("----- Test Case: test_09_update_api_feed_account_details -----")
        account_id = list_of_values(getJsonFileData('api_response_runtime/test_03_action_configuration_list_runtime.json'), 'third_party_config_id')[0]
        results = getJsonFileData("api_response_runtime/test_01_verify_api_feed_list_runtime.json")['results']
        app_id = ""
        for val in results:
            if val["title"] == 'Alien Vault':
                app_id = val["id"]
                break

        payload = getJsonFileData('api_payload/test_09_update_api_feed_account_details.json')
        endpoint = f'/api-feeds/apps/{app_id}/accounts/{account_id}'
        url = f"{base_url}{service}{endpoint}"

        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_09_update_api_feed_account_details_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/API_Integration/test_09_update_api_feed_account_details_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

    def test_10_api_feed_app_action_list(self):
        log("----- Test Case: test_10_api_feed_app_action_list -----")
        results = getJsonFileData("api_response_runtime/test_01_verify_api_feed_list_runtime.json")['results']
        app_id = ""
        for val in results:
            if val["title"] == 'Alien Vault':
                app_id = val["id"]
                break

        param = {
             "third_party_config_id" : f"{list_of_values(getJsonFileData('api_response_runtime/test_03_action_configuration_list_runtime.json'), 'third_party_config_id')[0]}"
              }
        endpoint = f"/api-feeds/apps/{app_id}/actions"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_10_api_feed_app_action_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/API_Integration/test_10_api_feed_app_action_list_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_11_action_details(self):
        log("----- Test Case: test_11_action_details -----")
        results = getJsonFileData("api_response_runtime/test_01_verify_api_feed_list_runtime.json")['results']
        app_id = ""
        for val in results:
            if val["title"] == 'Alien Vault':
                app_id = val["id"]
                break
        param = {
            "third_party_config_id": f"{list_of_values(getJsonFileData('api_response_runtime/test_03_action_configuration_list_runtime.json'), 'third_party_config_id')[0]}"
        }
        third_party_action_id = list_of_values(getJsonFileData('api_response_runtime/test_03_action_configuration_list_runtime.json'), 'third_party_action_id')[0]
        endpoint = f"/api-feeds/apps/{app_id}/actions/{third_party_action_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params = param)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_11_action_details_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/API_Integration/test_11_action_details_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_12_configured_connector_list(self):
        log("----- Test Case: test_12_configured_connector_list -----")
        endpoint = f"/feed-sources/api_feeds"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_12_configured_connector_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/API_Integration/test_12_configured_connector_list_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_13_reset_tool(self):
        print("----- Test Case: test_13_reset_tool -----")
        results = getJsonFileData("api_response_runtime/test_01_verify_api_feed_list_runtime.json")['results']
        app_id = ""
        for val in results:
            if val["title"] == 'Alien Vault':
                app_id = val["id"]
                break
        endpoint = f"/api-feeds/apps/reset_tool/{app_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        if response.status_code == 200:
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())