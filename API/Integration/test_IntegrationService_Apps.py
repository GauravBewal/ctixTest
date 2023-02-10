import unittest
import requests
from lib.api.common_utilities import *

'''
This modules contains all the test cases for Integration Service APPS
'''

service = 'integration'

class IntegrationServicesApps(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def get_app_id(self, title):
        result = getJsonFileData('api_response_runtime/test_02_list_applications_runtime.json')
        for val in result["results"]:
            if val["title"] == title:
                app_id = val["id"]
                return app_id

    def application_details(self, test_case_name, app_name):
        print(f"----- Test Case: {test_case_name} -----")
        endpoint = f"/apps/detail/{self.get_app_id(app_name)}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', f'{test_case_name}_runtime', response)

        if response.status_code == 200 and validate_schema(response, f'integration/apps/{test_case_name}_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_01_apps_category(self):
        print("----- Test Case: test_01_apps_category -----")
        endpoint = "/apps/category"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_apps_category_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'integration/apps/test_01_apps_category_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_02_list_applications(self):
        print("----- Test Case: test_02_list_applications -----")
        endpoint = "/apps"
        param = {
            "page_size" : 100
        }
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_list_applications_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'integration/apps/test_02_list_applications_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_03_CFTR_application_details(self):
        self.application_details('test_03_CFTR_application_details', 'CFTR')

    def test_04_CSAP_application_details(self):
        self.application_details('test_04_CSAP_application_details', 'CSAP')

    def test_05_CSOL_application_details(self):
        self.application_details('test_05_CSOL_application_details', 'CSOL')

    def test_06_CTIX_application_details(self):
        self.application_details('test_06_CTIX_application_details', 'CTIX')

    def test_07_ArcSight_application_details(self):
        self.application_details('test_07_ArcSight_application_details', 'ArcSight')

    def test_08_Exabeam_application_details(self):
        self.application_details('test_08_Exabeam_application_details', 'Exabeam')

    def test_09_Humio_application_details(self):
        self.application_details('test_09_Humio_application_details', 'Humio')

    def test_10_QRadar_application_details(self):
        self.application_details('test_10_QRadar_application_details', 'QRadar')

    def test_11_Splunk_application_details(self):
        self.application_details('test_11_Splunk_application_details', 'Splunk')

    def test_12_CORTEX_XSOAR_application_details(self):
        self.application_details('test_12_CORTEX_XSOAR_application_details', 'CORTEX-XSOAR')

    def test_13_Splunk_Phantom_application_details(self):
        self.application_details('test_13_Splunk_Phantom_application_details', 'Splunk Phantom')

    def test_14_Swimlane_application_details(self):
        self.application_details('test_14_Swimlane_application_details', 'Swimlane')

    def test_15_Zscaler_Network_Security_application_details(self):
        self.application_details('test_15_Zscaler_Network_Security_application_details', 'Zscaler Network Security')

    def test_16_Carbon_Black_application_details(self):
        self.application_details('test_16_Carbon_Black_application_details', 'Carbon Black')

    def test_17_McAfee_application_details(self):
        self.application_details('test_17_McAfee_application_details', 'McAfee')

    def test_18_McAfee_application_details(self):
        self.application_details('test_17_McAfee_application_details', 'McAfee')

    def test_19_Alien_Vault_application_details(self):
        self.application_details('test_19_Alien_Vault_application_details', 'Alien Vault')

    def test_20_AbuseIPDB_application_details(self):
        self.application_details('test_20_AbuseIPDB_application_details', 'AbuseIPDB')

    def test_21_Alexa_Ranking_application_details(self):
        self.application_details('test_21_Alexa_Ranking_application_details', 'Alexa Ranking')

    def test_22_alphaMountain_application_details(self):
        self.application_details('test_22_alphaMountain_application_details', 'alphaMountain')

    def test_23_APIVoid_application_details(self):
        self.application_details('test_23_APIVoid_application_details', 'APIVoid')

    def test_24_ArcSight_application_details(self):
        self.application_details('test_24_ArcSight_application_details', 'ArcSight')

    def test_25_Blue_Coat_Systems_application_details(self):
        self.application_details('test_25_Blue_Coat_Systems_application_details', 'Blue Coat Systems')

    def test_26_Cisco_Umbrella_application_details(self):
        self.application_details('test_26_Cisco_Umbrella_application_details', 'Cisco Umbrella')

    def test_27_Comodo_application_details(self):
        self.application_details('test_27_Comodo_application_details', 'Comodo')

    def test_28_CVE_Details_application_details(self):
        self.application_details('test_28_CVE_Details_application_details', 'CVE Details')

    def test_29_Cybersixgill_application_details(self):
        self.application_details('test_29_Cybersixgill_application_details', 'Cybersixgill')

    def test_30_EXPLOIT_DATABASE_application_details(self):
        self.application_details('test_30_EXPLOIT_DATABASE_application_details', 'EXPLOIT DATABASE')

    def test_31_Farsight_DNSDB_application_details(self):
        self.application_details('test_31_Farsight_DNSDB_application_details', 'Farsight DNSDB')

    def test_32_Google_Safe_Browsing_application_details(self):
        self.application_details('test_32_Google_Safe_Browsing_application_details', 'Google Safe Browsing')

    def test_33_GreyNoise_application_details(self):
        self.application_details('test_33_GreyNoise_application_details', 'GreyNoise')

    def test_34_Have_I_Been_Pwned_application_details(self):
        self.application_details('test_34_Have_I_Been_Pwned_application_details', 'Have I Been Pwned')

    def test_35_Hybrid_Analysis_application_details(self):
        self.application_details('test_35_Hybrid_Analysis_application_details', 'Hybrid Analysis')

    def test_36_IANA_whois_application_details(self):
        self.application_details('test_36_IANA_whois_application_details', 'IANA whois')

    def test_37_IBM_X_Force_application_details(self):
        self.application_details('test_37_IBM_X_Force_application_details', 'IBM X-Force')

    def test_38_Kaspersky_application_details(self):
        self.application_details('test_38_Kaspersky_application_details', 'Kaspersky')

    def test_39_Mandiant_Threat_Intelligence_application_details(self):
        self.application_details('test_39_Mandiant_Threat_Intelligence_application_details', 'Mandiant Threat Intelligence')

    def test_40_Mandiant_Threat_Intelligence_v4_application_details(self):
        self.application_details('test_40_Mandiant_Threat_Intelligence_v4_application_details', 'Mandiant Threat Intelligence v4')

    def test_41_MaxMind_GeoIP_application_details(self):
        self.application_details('test_41_MaxMind_GeoIP_application_details', 'MaxMind (GeoIP)')

    def test_42_Misp_WarningList_application_details(self):
        self.application_details('test_42_Misp_WarningList_application_details', 'Misp WarningList')

    def test_43_MX_Toolbox_application_details(self):
        self.application_details('test_43_MX_Toolbox_application_details', 'MX Toolbox')

    def test_44_NVD_application_details(self):
        self.application_details('test_44_NVD_application_details', 'NVD')

    def test_45_Phishtank_application_details(self):
        self.application_details('test_45_Phishtank_application_details', 'Phishtank')

    def test_46_PolySwarm_application_details(self):
        self.application_details('test_46_PolySwarm_application_details', 'PolySwarm')

    def test_47_Recorded_Future_application_details(self):
        self.application_details('test_47_Recorded_Future_application_details', 'Recorded Future')

    def test_48_RiskIQ_application_details(self):
        self.application_details('test_48_RiskIQ_application_details', 'RiskIQ')

    def test_49_Shodan_application_details(self):
        self.application_details('test_49_Shodan_application_details', 'Shodan')

    def test_50_SlashNext_application_details(self):
        self.application_details('test_50_SlashNext_application_details', 'SlashNext')

    def test_51_Threat_Miner_application_details(self):
        self.application_details('test_51_Threat_Miner_application_details', 'Threat Miner')

    def test_52_Virus_Total_application_details(self):
        self.application_details('test_52_Virus_Total_application_details', 'Virus Total')

    def test_53_VMRay_application_details(self):
        self.application_details('test_53_VMRay_application_details', 'VMRay')

    def test_54_Zscaler_Enrichment_application_details(self):
        self.application_details('test_54_Zscaler_Enrichment_application_details', 'Zscaler Enrichment')

    def test_55_siem_soar_apps(self):
        print("----- Test Case: test_55_siem_soar_apps -----")
        endpoint = "/apps/actioned"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_55_siem_soar_apps_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'integration/apps/test_55_siem_soar_apps_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    # this test case need to be run once the account is configured for the application
    def test_56_app_on_off(self):
        print("----- Test Case: test_05_app_on_off -----")
        payload = getJsonFileData('api_payload/test_05_app_on_off.json')
        result = getJsonFileData('api_response_runtime/test_02_list_applications_runtime.json')
        app_id = ""
        for val in result["results"]:
            if val["title"] == "CFTR":
                app_id = val["id"]
                break
        endpoint = f"/apps/reset_tool/{app_id}"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the PUT request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")

        save_runtime_response('testdata/api_response_runtime', 'test_05_app_on_off_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'integration/apps/test_05_app_on_off_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())