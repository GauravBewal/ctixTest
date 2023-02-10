import unittest
from lib.api.csol_internal import *
from lib.api.threat_data import *
from lib.api.rules import *
from lib.api.tags import *


class CywareProducts(unittest.TestCase):
    service = 'integration'

    def test_01_validate_count_csol_confscore(self):
        print("----- Test Case: test_01_validate_count_csol_confscore -----")
        fprint(self, "Running Rule_cc_CSOL_conf_playbook")
        _rule_name = "Rule_cc_CSOL_conf_playbook"
        start_time = get_value("client_start_time")
        end_time = get_value("client_end_time")
        csol_package_count = 0
        source_id = get_source_id("Recorded Future")
        print(source_id)
        query = f'type = \"indicator\" AND source = \"{source_id}\" AND confidence_score >= \"71\" AND ctix_created RANGE (\"{start_time}\",\"{end_time}\")'
        print(query)
        filter_query = {"query" : query}
        ctix_filter_count = get_filter_count(payload=filter_query)    # Query for threat data
        rule_id = get_rule_id(rule_name=_rule_name)
        rule_query = "{"+f'"query":"type = \\"indicator\\" AND rule = \\"{rule_id}\\"","q":""'+"}"
        print(rule_query)
        ctix_rule_count = get_filter_count(payload=json.loads(rule_query))
        get_ids = get_event_ids(label_name="rule_confscore"+get_value("csol_timestamp"))
        for i in get_ids:
            csol_package_count += get_event_count(i)
        print(ctix_filter_count, ctix_rule_count, csol_package_count)
        assert ctix_rule_count == ctix_filter_count == csol_package_count

    def test_02_validate_count_csol_tags(self):
        print("----- Test Case: test_01_validate_count_csol_confscore -----")
        _rule_name = "Rule_cc_CSOL_tags"
        start_time = get_value("client_start_time")
        end_time = get_value("client_end_time")
        csol_package_count = 0
        source_id = get_source_id("Recorded Future")
        tag_id = get_tag_id("Devo24")
        print(source_id, tag_id)
        query = f'type = \"indicator\" AND source = \"{source_id}\" AND tag=\"{tag_id}\" AND ctix_created RANGE (\"{start_time}\",\"{end_time}\")'
        print(query)
        filter_query = {"query": query}
        ctix_filter_count = get_filter_count(payload=filter_query)  # Query for threat data
        rule_id = get_rule_id(rule_name=_rule_name)
        rule_query = "{" + f'"query":"type = \\"indicator\\" AND rule = \\"{rule_id}\\"","q":""' + "}"
        print(rule_query)
        ctix_rule_count = get_filter_count(payload=json.loads(rule_query))
        get_ids = get_event_ids(label_name="rule_tags" + get_value("csol_timestamp"))
        for i in get_ids:
            csol_package_count += get_event_count(i)
        print(ctix_filter_count, ctix_rule_count, csol_package_count)
        assert ctix_rule_count == ctix_filter_count == csol_package_count

    def test_03_validate_count_csol_domainall(self):
        print("----- Test Case: test_03_validate_count_csol_domainall -----")
        _rule_name = "Rule_cc_CSOL_domainAll_playbook"
        start_time = get_value("client_start_time")
        end_time = get_value("client_end_time")
        csol_package_count = 0
        source_id = get_source_id("Recorded Future")
        print(source_id)
        query = f'type = \"indicator\" AND source = \"{source_id}\" AND ioc_type = \"domain-name\" AND ctix_created RANGE (\"{start_time}\",\"{end_time}\")'
        print(query)
        filter_query = {"query": query}
        ctix_filter_count = get_filter_count(payload=filter_query)  # Query for threat data
        rule_id = get_rule_id(rule_name=_rule_name)
        rule_query = "{" + f'"query":"type = \\"indicator\\" AND rule = \\"{rule_id}\\"","q":""' + "}"
        print(rule_query)
        ctix_rule_count = get_filter_count(payload=json.loads(rule_query))
        get_ids = get_event_ids(label_name="rule_domainAll" + get_value("csol_timestamp"))
        for i in get_ids:
            csol_package_count += get_event_count(i)
        print(ctix_filter_count, ctix_rule_count, csol_package_count)
        assert ctix_rule_count == ctix_filter_count == csol_package_count

    def test_04_validate_count_indicator_all_publish(self):
        print("----- Test Case: test_04_validate_count_indicator_all_publish -----")
        _rule_name = "Rule_cc_IndicatorAll_publish"
        start_time = get_value("client_start_time")
        end_time = get_value("client_end_time")
        source_id = get_source_id("Mandiant Threat Intelligence")
        query = f'type = \"indicator\" AND source = \"{source_id}\" AND ctix_created RANGE (\"{start_time}\",\"{end_time}\")'
        filter_query = {"query": query}
        ctix_filter_count = get_filter_count(payload=filter_query)  # Query for threat data
        rule_id = get_rule_id(rule_name=_rule_name)
        rule_query = "{" + f'"query":"type = \\"indicator\\" AND rule = \\"{rule_id}\\"","q":""' + "}"
        ctix_rule_count = get_filter_count(payload=json.loads(rule_query))
        print(ctix_filter_count, ctix_rule_count)
        assert ctix_rule_count == ctix_filter_count


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
