import unittest
from lib.ui.quick_add import *

listItem = ["Malware", "Threat Actor", "Attack Pattern", "Campaign",
            "Course of Action", "Infrastructure", "Intrusion Set", "Tool"]

parameters = ["Relations", "Source Scoring", "Enrichment Policy", "Sightings"]

categories = ["APIs", "RSS", "STIX", "Email", "Web Scraper", "Twitter", "Subscriber"]

filePath = os.path.join(os.environ["PYTHONPATH"], "lib", "ui/confidenceScore_IPs.properties")
config = configparser.ConfigParser()
config.read(filePath)


class ConfidenceScore(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.driver = initialize_browser(self)
        login(self, Admin_Email, Admin_Password)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    @classmethod
    def setUp(self):
        clear_console_logs(self)

    def test_01_confidence_score_loading(self):
        """
        Verify if confidence score page is loading
        """
        fprint(self, "\n--------- TC_ID 1: Checking Confidence Score page loading ---------")
        nav_menu_admin(self, "Confidence Score")
        fprint(self, "[PASSED] Confidence Score page loaded successfully")
        process_console_logs(self)

    def test_02_check_confidence_options(self):
        """
        Verify if confidence score options are all present
        """
        fprint(self, "\n--------- TC_ID 2: Validating confidence score options -----------")
        nav_menu_admin(self, "Confidence Score")
        fprint(self, "Validating if Confidence Score options are displayed")
        waitfor(self, 2, By.XPATH, "//div[contains(text(), 'Custom Confidence Score Engine')]")
        waitfor(self, 2, By.XPATH, "//div[contains(text(), 'CTIX Confidence Score Engine')]")
        fprint(self, "[PASSED] All Confidence score options are found")

    def test_03_enable_CTIX_confidence_score_engine(self):
        fprint(self, "\n--------- TC_ID 3: Enabling CTIX Confidence Score Engine options -----------")
        nav_menu_admin(self, "Confidence Score")
        fprint(self, "Checking CTIX Confidence Score Engine is Enabled or Disabled")
        if waitfor(self, 5, By.XPATH, "//div[contains(text(), 'CTIX Confidence Score Engine')]/ancestor::div[1]/following-sibling::span[text()='Enabled']", False):
            fprint(self, "CTIX Confidence Score is Already Enabled")
        else:
            fprint(self, "CTIX Confidence Score is Disabled")
            fprint(self, "Enabling CTIX Confidence Score")
            self.driver.find_element_by_xpath("//div[contains(text(), 'CTIX Confidence Score Engine')]").click()
            self.driver.find_element_by_xpath("//button[contains(text(), 'Proceed')]").click()
            fprint(self, "Clicked on the Proceed button")
            waitfor(self, 10, By.XPATH, "//button[contains(text(), 'Enable CTIX Confidence Score')]")
            self.driver.find_element_by_xpath("//button[contains(text(), 'Enable CTIX Confidence Score')]").click()
            fprint(self, "Clicked on the Enable CTIX Confidence Score button")
            waitfor(self, 10, By.XPATH, "//button[contains(text(), 'SKIP')]")
            self.driver.find_element_by_xpath("//button[contains(text(), 'SKIP')]").click()
            waitfor(self, 10, By.XPATH, "//button[contains(text(), 'OK, GOT IT')]")
            self.driver.find_element_by_xpath("//button[contains(text(), 'OK, GOT IT')]").click()
            waitfor(self, 10, By.XPATH, "//span[contains(text(), 'Enabled')]")
            fprint(self, "[Passed] CTIX Confidence Score is Enabled successfully")
            process_console_logs(self)

    def test_04_addIntel_no_relation_enrichment_weightage(self):
        fprint(self, "TC_ID: 399104 - test_04_addIntel_no_relation_enrichment_weightage")
        quick_create_ip(self, config.get('IPV4', 'no_rel_enrich_weight'), "no_rel_enrich_weight", metadata_confidence=0)
        fprint(self, "[Passed] - test_04_addIntel_no_relation_enrichment_weightage")

    def test_05_addIntel_no_relation_enrichment_weightage_two_sources(self):
        fprint(self, "TC_ID: 399105 - test_05_addIntel_no_relation_enrichment_weightage_two_sources")
        # IP is picked from the threat_mailbox_data.json file
        quick_create_ip(self, config.get('IPV4', 'no_rel_enrich_weight_twoSources'), "no_rel_enrich_weight_two_sources", metadata_confidence=0)
        fprint(self, "[Passed] - test_05_addIntel_no_relation_enrichment_weightage_two_sources")

    def test_06_addIntel_no_relation_enrichment_yes_weightage(self):
        fprint(self, "TC_ID: 399106 - test_06_addIntel_no_relation_enrichment_yes_weightage")
        quick_create_ip(self, config.get('IPV4', 'no_rel_enrich_yes_weight'), "no_rel_enrich_yes_weight")
        fprint(self, "[Passed] - test_06_addIntel_no_relation_enrichment_yes_weightage")

    def test_07_verify_no_relation_enrichment_weightage(self):
        fprint(self, "TC_ID: 399107 - test_07_verify_no_relation_enrichment_weightage")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'no_rel_enrich_weight'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'no_rel_enrich_weight'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'20')]")
        fprint(self, "Confidence Score 20 is visible")

    def test_08_verify_no_relation_enrichment_weightage_two_sources(self):
        fprint(self, "TC_ID: 399108 - test_08_verify_no_relation_enrichment_weightage_two_sources")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'no_rel_enrich_weight_twoSources'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'no_rel_enrich_weight_twoSources'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'40')]")
        fprint(self, "Confidence Score 40 is visible")

    def test_9_verify_no_relation_enrichment_yes_weightage(self):
        fprint(self, "TC_ID: 399109 - test_9_verify_no_relation_enrichment_yes_weightage")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'no_rel_enrich_yes_weight'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'no_rel_enrich_yes_weight'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'85')]")
        fprint(self, "Confidence Score 85 is visible")

    def test_10_addIntel_yes_relation_with_sdo_no_enrichment_weightage(self):
        fprint(self, "TC_ID: 399110 - test_10_addIntel_yes_relation_with_sdo_no_enrichment_weightage")
        nav_menu_main(self, 'Threat Data')
        for sdo in listItem:
            if sdo.__contains__(' '):
                data = sdo.replace(' ', '')
                quick_add_intel_with_ioc_sdo(self,
                                             ioc_type="IPv4",
                                             title="rel_with_"+sdo,
                                             ioc_value=config.get('IPV4',
                                                                  'yes_rel_with_'+data+'_no_enrich_weight'),
                                             sdo_type=sdo,
                                             sdo_value="test_r_"+sdo,
                                             metadata_confidence=0)
            else:
                quick_add_intel_with_ioc_sdo(self,
                                             ioc_type="IPv4",
                                             title="rel_with_" + sdo,
                                             ioc_value=config.get('IPV4',
                                                                  'yes_rel_with_'+sdo+'_no_enrich_weight'),
                                             sdo_type=sdo,
                                             sdo_value="test_r_" + sdo,
                                             metadata_confidence=0)
        fprint(self, "[Passed] - test_10_addIntel_yes_relation_with_sdo_no_enrichment_weightage")

    def test_11_verify_yes_relation_with_threatActor_no_enrichment_weightage(self):
        fprint(self, "TC_ID: 399111 - test_11_verify_yes_relation_with_threatActor_no_enrichment_weightage")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_rel_with_ThreatActor_no_enrich_weight'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_rel_with_ThreatActor_no_enrich_weight'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'75')]")
        fprint(self, "Confidence Score 75 is visible")

    def test_12_verify_yes_relation_with_malware_no_enrichment_weightage(self):
        fprint(self, "TC_ID: 399112 - test_12_verify_yes_relation_with_malware_no_enrichment_weightage")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_rel_with_Malware_no_enrich_weight'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_rel_with_Malware_no_enrich_weight'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'75')]")
        fprint(self, "Confidence Score 75 is visible")

    def test_13_verify_yes_relation_with_infrastructure_no_enrichment_weightage(self):
        fprint(self, "TC_ID: 399113 - test_13_verify_yes_relation_with_infrastructure_no_enrichment_weightage")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_rel_with_Infrastructure_no_enrich_weight'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_rel_with_Infrastructure_no_enrich_weight'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'75')]")
        fprint(self, "Confidence Score 75 is visible")

    def test_14_verify_yes_relation_with_attackPattern_no_enrichment_weightage(self):
        fprint(self, "TC_ID: 399114 - test_14_verify_yes_relation_with_attackPattern_no_enrichment_weightage")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_rel_with_AttackPattern_no_enrich_weight'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_rel_with_AttackPattern_no_enrich_weight'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'65')]")
        fprint(self, "Confidence Score 65 is visible")

    def test_15_verify_yes_relation_with_intrusionSet_no_enrichment_weightage(self):
        fprint(self, "TC_ID: 399115 - test_15_verify_yes_relation_with_intrusionSet_no_enrichment_weightage")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_rel_with_IntrusionSet_no_enrich_weight'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_rel_with_IntrusionSet_no_enrich_weight'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'65')]")
        fprint(self, "Confidence Score 65 is visible")

    def test_16_verify_yes_relation_with_tool_no_enrichment_weightage(self):
        fprint(self, "TC_ID: 399116 - test_16_verify_yes_relation_with_tool_no_enrichment_weightage")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_rel_with_Tool_no_enrich_weight'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_rel_with_Tool_no_enrich_weight'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'60')]")
        fprint(self, "Confidence Score 60 is visible")

    def test_17_verify_yes_relation_with_courseOfAction_no_enrichment_weightage(self):
        fprint(self, "TC_ID: 399117 - test_17_verify_yes_relation_with_courseOfAction_no_enrichment_weightage")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_rel_with_CourseOfAction_no_enrich_weight'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_rel_with_CourseOfAction_no_enrich_weight'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'50')]")
        fprint(self, "Confidence Score 50 is visible")

    def test_18_verify_yes_relation_with_campaign_no_enrichment_weightage(self):
        fprint(self, "TC_ID: 399118 - test_18_verify_yes_relation_with_campaign_no_enrichment_weightage")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_rel_with_Campaign_no_enrich_weight'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_rel_with_Campaign_no_enrich_weight'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'75')]")
        fprint(self, "Confidence Score 75 is visible")

    def test_19_addIntel_yes_weightage_relation_with_sdo_no_enrichment(self):
        fprint(self, "TC_ID: 399119 - test_19_addIntel_yes_weightage_relation_with_sdo_no_enrichment")
        nav_menu_main(self, 'Threat Data')
        for sdo in listItem:
            if sdo.__contains__(' '):
                data = sdo.replace(' ', '')
                quick_add_intel_with_ioc_sdo(self,
                                             ioc_type="IPv4",
                                             title="rel_with_"+sdo,
                                             ioc_value=config.get('IPV4',
                                                                  'yes_weight_rel_with_'+data+'_no_enrich'),
                                             sdo_type=sdo,
                                             sdo_value="test_wr_"+sdo,
                                             metadata_confidence=40)
            else:
                quick_add_intel_with_ioc_sdo(self,
                                             ioc_type="IPv4",
                                             title="rel_with_" + sdo,
                                             ioc_value=config.get('IPV4',
                                                                  'yes_weight_rel_with_'+sdo+'_no_enrich'),
                                             sdo_type=sdo,
                                             sdo_value="test_wr_" + sdo,
                                             metadata_confidence=40)
        fprint(self, "[Passed] - test_19_addIntel_yes_weightage_relation_with_sdo_no_enrichment")

    def test_20_verify_yes_weightage_relation_with_threatActor_no_enrichment(self):
        fprint(self, "TC_ID: 399120 - test_20_verify_yes_weightage_relation_with_threatActor_no_enrichment")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_weight_rel_with_ThreatActor_no_enrich'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_weight_rel_with_ThreatActor_no_enrich'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'89')]")
        fprint(self, "Confidence Score 89 is visible")

    def test_21_verify_yes_weightage_relation_with_malware_no_enrichment(self):
        fprint(self, "TC_ID: 399121 - test_21_verify_yes_weightage_relation_with_malware_no_enrichment")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_weight_rel_with_Malware_no_enrich'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_weight_rel_with_Malware_no_enrich'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'89')]")
        fprint(self, "Confidence Score 89 is visible")

    def test_22_verify_yes_weightage_relation_with_infrastructure_no_enrichment(self):
        fprint(self, "TC_ID: 399122 - test_22_verify_yes_weightage_relation_with_infrastructure_no_enrichment")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_weight_rel_with_Infrastructure_no_enrich'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_weight_rel_with_Infrastructure_no_enrich'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'89')]")
        fprint(self, "Confidence Score 89 is visible")

    def test_23_verify_yes_weightage_relation_with_attackPattern_no_enrichment(self):
        fprint(self, "TC_ID: 399123 - test_23_verify_yes_weightage_relation_with_attackPattern_no_enrichment")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_weight_rel_with_AttackPattern_no_enrich'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_weight_rel_with_AttackPattern_no_enrich'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'79')]")
        fprint(self, "Confidence Score 79 is visible")

    def test_24_verify_yes_weightage_relation_with_intrusionSet_no_enrichment(self):
        fprint(self, "TC_ID: 399124 - test_24_verify_yes_weightage_relation_with_intrusionSet_no_enrichment")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_weight_rel_with_IntrusionSet_no_enrich'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_weight_rel_with_IntrusionSet_no_enrich'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'79')]")
        fprint(self, "Confidence Score 79 is visible")

    def test_25_verify_yes_weightage_relation_with_tool_no_enrichment(self):
        fprint(self, "TC_ID: 399125 - test_25_verify_yes_weightage_relation_with_tool_no_enrichment")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_weight_rel_with_Tool_no_enrich'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_weight_rel_with_Tool_no_enrich'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'74')]")
        fprint(self, "Confidence Score 74 is visible")

    def test_26_verify_yes_weightage_relation_with_courseOfAction_no_enrichment(self):
        fprint(self, "TC_ID: 399124 - test_26_verify_yes_weightage_relation_with_courseOfAction_no_enrichment")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_weight_rel_with_CourseOfAction_no_enrich'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_weight_rel_with_CourseOfAction_no_enrich'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'64')]")
        fprint(self, "Confidence Score 64 is visible")

    def test_27_verify_yes_weightage_relation_with_campaign_no_enrichment(self):
        fprint(self, "TC_ID: 399124 - test_27_verify_yes_weightage_relation_with_campaign_no_enrichment")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_weight_rel_with_Campaign_no_enrich'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_weight_rel_with_Campaign_no_enrich'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'89')]")
        fprint(self, "Confidence Score 89 is visible")

    def test_28_addIntel_yes_enrichment_no_relation_weightage(self):
        fprint(self, "TC_ID: 399128 - test_28_addIntel_yes_enrichment_no_relation_weightage")
        quick_create_ip(self, config.get('IPV4', 'yes_enrichment_no_relation_weightage'), "yes_enrichment_no_relation_weightage", metadata_confidence=0)
        fprint(self, "[Passed] - test_28_addIntel_yes_enrichment_no_relation_weightage")

    def test_29_verify_yes_enrichment_no_relation_weightage(self):
        fprint(self, "TC_ID: 399129 - test_29_verify_yes_enrichment_no_relation_weightage")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_enrichment_no_relation_weightage'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_enrichment_no_relation_weightage'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'100')]")
        fprint(self, "Confidence Score 100 is visible")

    def test_30_addIntel_yes_relation_enrichment_weightage(self):
        fprint(self, "TC_ID: 399130 - test_30_addIntel_yes_relation_enrichment_weightage")
        nav_menu_main(self, 'Threat Data')
        quick_add_intel_with_ioc_sdo(self,
                                     ioc_type="IPv4",
                                     title="rel_with_malware",
                                     ioc_value=config.get('IPV4',
                                                          'yes_rel_enrich_weight'),
                                     sdo_type="Malware",
                                     sdo_value="test_rew_Malware",
                                     metadata_confidence=40)
        fprint(self, "[Passed] - test_30_addIntel_yes_relation_enrichment_weightage")

    def test_31_verify_yes_relation_enrichment_weightage(self):
        fprint(self, "TC_ID: 399131 - test_31_verify_yes_relation_enrichment_weightage")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_rel_enrich_weight'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_rel_enrich_weight'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'100')]")
        fprint(self, "Confidence Score 100 is visible")

    def test_32_addIntel_yes_relation_weightage_enrich_not_malicious(self):
        fprint(self, "TC_ID: 399132 - test_32_addIntel_yes_relation_weightage_enrich_not_malicious")
        nav_menu_main(self, 'Threat Data')
        quick_add_intel_with_ioc_sdo(self,
                                     ioc_type="IPv4",
                                     title="rel_with_malware_not_malicious",
                                     ioc_value=config.get('IPV4',
                                                          'yes_rel_weight_enrich_not_malicious'),
                                     sdo_type="Malware",
                                     sdo_value="test_rew_Malware_not_malicious",
                                     metadata_confidence=40)
        fprint(self, "[Passed] - test_32_addIntel_yes_relation_weightage_enrich_not_malicious")

    def test_33_verify_yes_relation_enrichment_weightage_not_malicious(self):
        fprint(self, "TC_ID: 399133 - test_33_verify_yes_relation_enrichment_weightage_not_malicious")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'yes_rel_weight_enrich_not_malicious'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'yes_rel_weight_enrich_not_malicious'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'89')]")
        fprint(self, "Confidence Score 82 is visible")

    def test_34_addIntel_no_relation_weightage_yes_enrich_not_malicious(self):
        fprint(self, "TC_ID: 399134 - test_34_addIntel_no_relation_weightage_yes_enrich_not_malicious")
        quick_create_ip(self, config.get('IPV4', 'no_rel_weight_yes_enrich_not_malicious'), "no_rel_weight_yes_enrich_not_malicious", metadata_confidence=0)
        fprint(self, "[Passed] - test_34_addIntel_no_relation_weightage_yes_enrich_not_malicious")

    def test_35_verify_no_relation_weightage_yes_enrich_not_malicious(self):
        fprint(self, "TC_ID: 399135 - test_35_verify_no_relation_weightage_yes_enrich_not_malicious")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'no_rel_weight_yes_enrich_not_malicious'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'no_rel_weight_yes_enrich_not_malicious'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'20')]")
        fprint(self, "Confidence Score 20 is visible")

    def test_36_addIntel_no_relation_yes_weightage_enrich_not_malicious(self):
        fprint(self, "TC_ID: 399136 - test_36_addIntel_no_relation_yes_weightage_enrich_not_malicious")
        quick_create_ip(self, config.get('IPV4', 'no_rel_yes_weight_enrich_not_malicious'), "no_rel_yes_weight_enrich_not_malicious", metadata_confidence=40)
        fprint(self, "[Passed] - test_36_addIntel_no_relation_yes_weightage_enrich_not_malicious")

    def test_37_verify_no_relation_yes_weightage_enrich_not_malicious(self):
        fprint(self, "TC_ID: 399137 - test_37_verify_no_relation_yes_weightage_enrich_not_malicious")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'no_rel_yes_weight_enrich_not_malicious'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'no_rel_yes_weight_enrich_not_malicious'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'55')]")
        fprint(self, "Confidence Score 55 is visible")

    def test_38_addIntel_no_weightage_yes_relation_enrich(self):
        fprint(self, "TC_ID: 399138 - test_38_addIntel_no_weightage_yes_relation_enrich")
        nav_menu_main(self, 'Threat Data')
        quick_add_intel_with_ioc_sdo(self,
                                     ioc_type="IPv4",
                                     title="rel_re_with_malware",
                                     ioc_value=config.get('IPV4',
                                                          'no_weight_yes_rel_enrich'),
                                     sdo_type="Malware",
                                     sdo_value="test_re_Malware",
                                     metadata_confidence=0)
        fprint(self, "[Passed] - test_38_addIntel_no_weightage_yes_relation_enrich")

    def test_39_verify_no_weightage_yes_relation_enrich(self):
        fprint(self, "TC_ID: 399139 - test_39_verify_no_weightage_yes_relation_enrich")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'no_weight_yes_rel_enrich'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'no_weight_yes_rel_enrich'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'100')]")
        fprint(self, "Confidence Score 100 is visible")

    def test_40_addIntel_no_weightage_yes_relation_enrich_not_malicious(self):
        fprint(self, "TC_ID: 399140 - test_30_addIntel_yes_relation_enrichment_weightage")
        nav_menu_main(self, 'Threat Data')
        quick_add_intel_with_ioc_sdo(self,
                                     ioc_type="IPv4",
                                     title="rel_re_with_malware_not_malicious",
                                     ioc_value=config.get('IPV4',
                                                          'no_weight_yes_rel_enrich_not_malicious'),
                                     sdo_type="Malware",
                                     sdo_value="test_rew_Malware",
                                     metadata_confidence=0)
        fprint(self, "[Passed] - test_30_addIntel_yes_relation_enrichment_weightage")

    def test_41_verify_no_weightage_yes_relation_enrich_not_malicious(self):
        fprint(self, "TC_ID: 399141 - test_39_verify_no_weightage_yes_relation_enrich")
        nav_menu_main(self, 'Threat Data')
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, config.get('IPV4', 'no_weight_yes_rel_enrich_not_malicious'), "Import")
        click_on_eye_button(self, "Import", config.get('IPV4', 'no_weight_yes_rel_enrich_not_malicious'))
        waitfor(self, 20, By.XPATH, "//div[@id='confidencescorechart']/following-sibling::div/p[contains(text(),'75')]")
        fprint(self, "Confidence Score 75 is visible")

    def test_42_verify_elements_under_ctix_cs_engine(self):
        fprint(self, "TC_ID: 399142 - test_42_verify_elements_under_ctix_cs_engine")
        failures = []
        nav_menu_admin(self, "Confidence Score")
        # waitfor(self, 20, By.XPATH, "//h1[contains(text(),'Choose a Confidence Score Setup')]")
        # fprint(self, "Checking CTIX Confidence Score Engine is visible and its Enabled")
        # if waitfor(self, 10, By.XPATH, "//div[contains(text(),'CTIX Confidence Score Engine')]/parent::div/div[contains(@class,'cy-radio__btn--checked')]", False):
        #     fprint(self, "CTIX Confidence Score Engine - Visible and found Enabled")
        # else:
        #     fprint(self, "CTIX Confidence Score Engine - Not Visible or Not Enabled")
        #     failures.append("CTIX Confidence Score Engine - Not Visible or Not Enabled")
        #
        # waitfor(self, 10, By.XPATH, "//button[contains(text(),'Proceed')]")
        # self.driver.find_element_by_xpath("//button[contains(text(),'Proceed')]").click()
        # fprint(self, "Clicked on the Proceed Button")
        waitfor(self, 20, By.XPATH, "//h2[contains(text(),'Relations')]")
        fprint(self, "Redirected to the CTIX Confidence Score Engine page now")

        for param in parameters:
            fprint(self, "Clicking on the - "+param)
            self.driver.find_element_by_xpath("//h2[contains(text(),'"+param+"')]/parent::div").click()
            if waitfor(self, 10, By.XPATH, "//div[@class='cy-modal-header__title']/div[contains(text(),'"+param+"')]", False):
                fprint(self, "Slider is visible, checking "+param+" video is visible or not")
                if param == "Source Scoring":
                    if waitfor(self, 10, By.XPATH, "//video[@src='https://cdn.cyware.com/ctix-client/Source%20scoring_final.mp4']", False):
                        fprint(self, "Video of " + param + " is also visible")
                    else:
                        fprint(self, "[Failed] Video of " + param + " is not visible")
                        failures.append("Video of " + param + " is not visible")
                else:
                    if waitfor(self, 10, By.XPATH, "//video[@src='https://cdn.cyware.com/ctix-client/"+param.replace(" ", "+")+"_final.mp4']", False):
                        fprint(self, "Video of "+param+" is also visible")
                    else:
                        fprint(self, "[Failed] Video of "+param+" is not visible")
                        failures.append("Video of "+param+" is not visible")
            else:
                fprint(self, "[Failed] Slider of "+param+" is not visible")
                failures.append("Slider of "+param+" is not visible")
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(1)

        fprint(self, "Clicking on the - CTIX Confidence Score Algorithm")
        self.driver.find_element_by_xpath("//div[contains(text(),'CTIX Confidence Score Algorithm')]/parent::div").click()
        if waitfor(self, 10, By.XPATH, "//div[@class='cy-modal-header__title']/div[contains(text(),'CTIX Confidence Score Algorithm')]", False):
            if waitfor(self, 10, By.XPATH, "//video[@src='https://cdn.cyware.com/ctix-client/Confidence%20score%20overall%20video_v7.mp4']", False):
                fprint(self, "Video of CTIX Confidence Score Algorithm is also visible")
                self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
                sleep(1)
            else:
                fprint(self, "[Failed] Video of CTIX Confidence Score Algorithm is not visible")
                failures.append("Video of CTIX Confidence Score Algorithm is not visible")
                self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
                sleep(1)
        else:
            fprint(self, "[Failed] Slider of CTIX Confidence Score Algorithm is not visible")
            failures.append("Slider of CTIX Confidence Score Algorithm is not visible")

        waitfor(self, 10, By.XPATH, "//button[contains(text(),'Configure Source Scoring')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Configure Source Scoring')]").click()
        waitfor(self, 10, By.XPATH, "//span[normalize-space()='Category - APIs']")
        self.driver.find_element_by_xpath("//span[normalize-space()='Category - APIs']").click()
        for cat in categories:
            if waitfor(self, 10, By.XPATH, "//li[contains(text(),'"+cat+"')]", False):
                fprint(self, "Category visible - "+cat)
            else:
                fprint(self, "[Failed] Category not visible - "+cat)
                failures.append("Category not visible - "+cat)
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        sleep(1)

        waitfor(self, 10, By.XPATH, "//button[contains(text(),'Manage Enrichment Policy')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Manage Enrichment Policy')]").click()
        sleep(5)
        self.driver.switch_to_window(self.driver.window_handles[1])
        if waitfor(self, 20, By.XPATH, "//h1[contains(text(),'Enrichment Management')]", False):
            fprint(self, "Enrichment management page is visible")
        else:
            fprint(self, "[Failed] Enrichment management page is not visible")
            failures.append("Enrichment management page is not visible")
        self.assert_(failures == [], str(failures))


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
