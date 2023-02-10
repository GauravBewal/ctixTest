import unittest
from lib.api.external_apis import get_ref_set_data_qradar, delete_ref_set_qradar
from lib.api.rules import *
from lib.api.threat_data import get_filter_count, get_collection_id

'''
This module contains all the testcases of the Rules
'''

service = 'ingestion'


class Rules(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_validate_status_code_rules_json(self):
        print("----- Test Case: test_01_validate_status_code_rules_json -----")
        endpoint = "/rules/json"
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

    def test_02_validate_response_rules_json(self):
        print("----- Test Case: test_02_validate_response_rules_json -----")
        endpoint = "/rules/json"
        url = f"{base_url}{service}{endpoint}"
        print("Validating response got from the endpoint")
        print(f'Making the get request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")

        # Intentionally commented
        # save_runtime_response('testdata/api_response', 'test_02_validate_response_rules_json', response)
        save_runtime_response('testdata/api_response_runtime', 'test_02_validate_response_rules_json_runtime', response)

        if compare_responses(response, 'test_02_validate_response_rules_json'):
            print("Response Matched")
            print("[PASSED] Get request is successful")
        else:
            print("[FAILED] Get request is not successful")
            self.fail()

    def test_128_cc_verify_publishToCol_UpdateRefSet_for_allHashes(self):
        try:
            fprint(self, "TC_ID: 61128 - test_128_cc_verify_publishToCol_UpdateRefSet_for_allHashes")
            _rule_name = "Rule_cc_updateRefSet_PublishToCol_allHashes"
            start_time = get_value("client_start_time")
            end_time = get_value("client_end_time")
            collection_id = get_collection_id(get_value("RF_hash_collname"))
            print("collection_id - ", collection_id)
            query = f'type = \"indicator\" AND source_collection = \"{collection_id}\" AND ctix_created RANGE (\"{start_time}\",\"{end_time}\")'
            ctix_filter_count = get_filter_count(payload=query)  # Query for threat data
            rule_id = get_rule_id(rule_name=_rule_name)
            print("rule id - ", rule_id)
            rule_query = "{" + f'"query":"type = \\"indicator\\" AND rule = \\"{rule_id}\\"","q":""' + "}"
            print("rule_query - ", rule_query)
            ctix_rule_count = get_filter_count(payload=json.loads(rule_query))
            qrad_count = get_ref_set_data_qradar(set_name="REFERENCE_SET_124").json()["number_of_elements"]
            print("ctix - ", ctix_rule_count, "qrad - ", qrad_count)
            assert ctix_rule_count == qrad_count == ctix_filter_count
        finally:
            delete_ref_set_qradar(set_name="REFERENCE_SET_124")

    def test_129_cc_verify_publishToCol_UpdateRefSet_for_allDomains(self):
        try:
            fprint(self, "TC_ID: 61129 - test_129_cc_verify_publishToCol_UpdateRefSet_for_allDomains")
            _rule_name = "Rule_cc_updateRefSet_PublishToCol_allDomains"
            start_time = get_value("client_start_time")
            end_time = get_value("client_end_time")
            collection_id = get_collection_id(get_value("RF_domain_collname"))
            query = f'type = \"indicator\" AND source_collection = \"{collection_id}\" AND ctix_created RANGE (\"{start_time}\",\"{end_time}\")'
            ctix_filter_count = get_filter_count(payload=query)  # Query for threat data
            rule_id = get_rule_id(rule_name=_rule_name)
            rule_query = "{" + f'"query":"type = \\"indicator\\" AND rule = \\"{rule_id}\\"","q":""' + "}"
            ctix_rule_count = get_filter_count(payload=json.loads(rule_query))
            qrad_count = get_ref_set_data_qradar(set_name="REFERENCE_SET_125").json()["number_of_elements"]
            assert ctix_filter_count == ctix_rule_count == qrad_count
        finally:
            delete_ref_set_qradar(set_name="REFERENCE_SET_125")

    def test_130_cc_verify_publishToCol_UpdateRefSet_for_allIPs(self):
        try:
            fprint(self, "TC_ID: 61130 - test_130_cc_verify_publishToCol_UpdateRefSet_for_allIPs")
            _rule_name = "Rule_cc_updateRefSet_PublishToCol_allIPs"
            start_time = get_value("client_start_time")
            end_time = get_value("client_end_time")
            collection_id = get_collection_id(get_value("RF_ip_collname"))
            print("collection_id - ", collection_id)
            query = f'type = \"indicator\" AND source_collection = \"{collection_id}\" AND ctix_created RANGE (\"{start_time}\",\"{end_time}\")'
            ctix_filter_count = get_filter_count(payload=query)  # Query for threat data
            rule_id = get_rule_id(rule_name=_rule_name)
            rule_query = "{" + f'"query":"type = \\"indicator\\" AND rule = \\"{rule_id}\\"","q":""' + "}"
            print("rule_query - ", rule_query)
            ctix_rule_count = get_filter_count(payload=json.loads(rule_query))
            qrad_count = get_ref_set_data_qradar(set_name="REFERENCE_SET_126").json()["number_of_elements"]
            assert ctix_filter_count == ctix_rule_count == qrad_count
        finally:
            delete_ref_set_qradar(set_name="REFERENCE_SET_126")

    def test_131_cc_verify_publishToCol_UpdateRefSet_for_allURL(self):
        try:
            fprint(self, "TC_ID: 61131 - test_131_cc_verify_publishToCol_UpdateRefSet_for_allURL")
            _rule_name = "Rule_cc_updateRefSet_PublishToCol_allUrl"
            start_time = get_value("client_start_time")
            end_time = get_value("client_end_time")
            collection_id = get_collection_id(get_value("RF_url_collname"))
            print("collection_id - ", collection_id)
            query = f'type = \"indicator\" AND source_collection = \"{collection_id}\" AND ctix_created RANGE (\"{start_time}\",\"{end_time}\")'
            ctix_filter_count = get_filter_count(payload=query)  # Query for threat data
            rule_id = get_rule_id(rule_name=_rule_name)
            rule_query = "{" + f'"query":"type = \\"indicator\\" AND rule = \\"{rule_id}\\"","q":""' + "}"
            print("rule_query - ", rule_query)
            ctix_rule_count = get_filter_count(payload=json.loads(rule_query))
            qrad_count = get_ref_set_data_qradar(set_name="REFERENCE_SET_127").json()["number_of_elements"]
            assert ctix_filter_count == ctix_rule_count == qrad_count
        finally:
            delete_ref_set_qradar(set_name="REFERENCE_SET_127")

    def test_03_run_all_client_rules(self):
        print("---- Test case: test_03_run_all_client_rules ----")
        run_all_rules(pattern='Rule_cc')
        print(self, "All rules matching pattern are triggered successfully")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())