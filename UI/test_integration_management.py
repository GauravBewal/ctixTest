import unittest
from lib.ui.integration_management import *


class IntegrationMgmt(unittest.TestCase):

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

    def test_01_feed_sources(self):
        """
        Checking if STIX sources pages are loading
        """
        nav_menu_admin(self, "Integration Management")
        fprint(self, "\n----------- TC_ID 1: Checking load screen of STIX sources -----------")
        waitfor(self, 2, By.XPATH, "//ul//span[text()='STIX ']")
        self.driver.find_element_by_xpath("//span[text()='STIX ']").click()
        waitfor(self, 2, By.XPATH, "//div/preceding-sibling::div[contains(text(), 'STIX')]")
        fprint(self, "[PASSED] Page loading successfully for STIX feed source")
        #Todo: Add testcases for all feed types
        process_console_logs(self)

    def test_02_API_sources(self):
        """
        Checking if APIs sources pages are loading
        """
        fprint(self, "\n----------- TC_ID 2: Checking load screen of APIs sources -----------")
        waitfor(self, 2, By.XPATH, "//ul//span[text()='APIs ']")
        self.driver.find_element_by_xpath("//span[text()='APIs ']").click()
        waitfor(self, 2, By.XPATH, "//div/preceding-sibling::div[contains(text(), 'APIs')]")
        fprint(self, "[PASSED] Page loading successfully for APIs feed source")
        process_console_logs(self)

    def test_03_isac_sources(self):
        """
        Checking if ISAC sources pages are loading
        """
        fprint(self, "\n----------- TC_ID 3: Checking load screen of ISAC sources -----------")
        waitfor(self, 2, By.XPATH, "//ul//span[text()='ISAC ']")
        self.driver.find_element_by_xpath("//span[text()='ISAC ']").click()
        waitfor(self, 2, By.XPATH, "//div/preceding-sibling::div[contains(text(), 'ISAC')]")
        fprint(self, "[PASSED] Page loading successfully for ISAC feed source")
        process_console_logs(self)

    def test_04_rss_sources(self):
        """
        Checking if RSS sources pages are loading
        """
        fprint(self, "\n----------- TC_ID 4: Checking load screen of RSS sources -----------")
        waitfor(self, 2, By.XPATH, "//ul//span[text()='RSS ']")
        self.driver.find_element_by_xpath("//span[text()='RSS ']").click()
        waitfor(self, 2, By.XPATH, "//div/preceding-sibling::div[contains(text(), 'RSS')]")
        fprint(self, "[PASSED] Page loading successfully for RSS feed source")
        process_console_logs(self)

    def test_05_Email_sources(self):
        """
        Checking if Email sources pages are loading
        """
        fprint(self, "\n----------- TC_ID 5: Checking load screen of Email sources -----------")
        waitfor(self, 2, By.XPATH, "//ul//span[text()='Email ']")
        self.driver.find_element_by_xpath("//span[text()='Email ']").click()
        waitfor(self, 2, By.XPATH, "//div/preceding-sibling::div[contains(text(), 'Email')]")
        fprint(self, "[PASSED] Page loading successfully for Email feed source")
        process_console_logs(self)

    def test_06_twitter_sources(self):
        """
        Checking if Twitter sources pages are loading
        """
        fprint(self, "\n----------- TC_ID 6: Checking load screen of Twitter sources -----------")
        waitfor(self, 2, By.XPATH, "//ul//span[text()='Twitter ']")
        self.driver.find_element_by_xpath("//span[text()='Twitter ']").click()
        waitfor(self, 2, By.XPATH, "//div/preceding-sibling::div/div[contains(text(), 'Twitter')]")
        fprint(self, "[PASSED] Page loading successfully for Twitter feed source")
        process_console_logs(self)

    def test_07_web_scraper_sources(self):
        """
        Checking if Web Scraper sources pages are loading
        """
        fprint(self, "\n----------- TC_ID 7: Checking load screen of Web Scraper sources -----------")
        waitfor(self, 2, By.XPATH, "//ul//span[text()='Web Scraper ']")
        self.driver.find_element_by_xpath("//span[text()='Web Scraper ']").click()
        waitfor(self, 2, By.XPATH, "//div/preceding-sibling::div[contains(text(), 'Web Scraper')]")
        fprint(self, "[PASSED] Page loading successfully for Web Scraper feed source")
        process_console_logs(self)

    def test_08_webhooks_sources(self):
        """
        Checking if Webhooks sources pages are loading
        """
        fprint(self, "\n----------- TC_ID 8: Checking load screen of Webhooks sources -----------")
        waitfor(self, 2, By.XPATH, "//ul//span[text()='Webhooks ']")
        self.driver.find_element_by_xpath("//span[text()='Webhooks ']").click()
        waitfor(self, 2, By.XPATH, "//div/preceding-sibling::div[contains(text(), 'Webhooks')]")
        fprint(self, "[PASSED] Page loading successfully for Webhooks feed source")
        process_console_logs(self)

    def test_09_stix_subscribers(self):
        """
        Checking if STIX Subscriber pages are loading
        """
        fprint(self, "\n----------- TC_ID 9: Checking load screen of STIX Subscribers -----------")
        fprint(self, "Loading page for STIX Subscribers sources")
        self.driver.find_element_by_xpath("//span[text()='STIX Subscribers ']").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(), 'STIX Subscribers')]")
        fprint(self, "[PASSED] Page loading successfully for STIX Subscribers")
        process_console_logs(self)

    def test_10_spoke_management(self):
        """
        Checking if Spoke Management pages are loading
        """
        fprint(self, "\n----------- TC_ID 10: Checking load screen of Spokes/Subsidiaries -----------")
        fprint(self, "Loading page for Spokes/Subsidiaries")
        self.driver.find_element_by_xpath("//span[text()='Spokes/Subsidiaries ']").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(), 'Spokes/Subsidiaries')]")
        fprint(self, "[PASSED] Page loading successfully for Spokes/Subsidiaries")
        process_console_logs(self)

    def test_11_siem_tool(self):
        """
        Checking if SIEM pages are loading
        """
        fprint(self, "\n----------- TC_ID 11: Checking load screen of SIEM tools -----------")
        fprint(self, "Loading page for SIEM tools")
        # Todo: Add testcase for CSOL agent tasks slider
        self.driver.find_element_by_xpath("//span[text()='Internal Applications ']").click()
        waitfor(self, 2, By.XPATH, "//span[text()='Internal Applications ']")
        self.driver.find_element_by_xpath("//p[text()='Security Information and Event Managment System']").click()
        waitfor(self, 2, By.XPATH, "//h1[contains(text(),'Security Information and Event Managment System')]")
        fprint(self, "[PASSED] Page loading successfully for SIEM tools")
        process_console_logs(self)

    def test_12_soar_tool(self):
        """
        Checking if SOAR pages are loading
        """
        fprint(self, "\n----------- TC_ID 12: Checking load screen of SOAR Tools -----------")
        fprint(self, "Loading page for SOAR Tools")
        self.driver.find_element_by_xpath("//span[text()='Internal Applications ']").click()
        waitfor(self, 2, By.XPATH, "//span[text()='Internal Applications ']")
        self.driver.find_element_by_xpath("//p[text()='Security Orchestration Automation Response']").click()
        waitfor(self, 2, By.XPATH, "//h1[contains(text(),'Security Orchestration Automation Response')]")
        fprint(self, "[PASSED] Page loading successfully for SOAR Tools")
        process_console_logs(self)

    def test_13_firewall_tool(self):
        """
        Checking if Firewall pages are loading
        """
        fprint(self, "\n----------- TC_ID 13: Checking load screen of Firewall -----------")
        fprint(self, "Loading page for Firewall Tools")
        self.driver.find_element_by_xpath("//span[text()='Internal Applications ']").click()
        waitfor(self, 2, By.XPATH, "//span[text()='Internal Applications ']")
        self.driver.find_element_by_xpath("//p[text()='Firewall']").click()
        waitfor(self, 2, By.XPATH, "//h1[contains(text(),'Firewall')]")
        fprint(self, "[PASSED] Page loading successfully for Firewall Tools ")
        process_console_logs(self)

    def test_14_network_security_tool(self):
        """
        Checking if Network Security pages are loading
        """
        fprint(self, "\n----------- TC_ID 14: Checking load screen of Network Security -----------")
        fprint(self, "Loading page for Network Security tools")
        self.driver.find_element_by_xpath("//span[text()='Internal Applications ']").click()
        waitfor(self, 2, By.XPATH, "//span[text()='Internal Applications ']")
        self.driver.find_element_by_xpath("//p[text()='Network Security']").click()
        waitfor(self, 2, By.XPATH, "//h1[contains(text(),'Network Security')]")
        fprint(self, "[PASSED] Page loading successfully for Network Security Tools")
        process_console_logs(self)

    def test_15_endpoint_detection_response_tool(self):
        """
        Checking if Endpoint Detection Response pages are loading
        """
        fprint(self, "\n----------- TC_ID 15: Checking load screen of Endpoint Detection Response -----------")
        fprint(self, "Loading page for Endpoint Detection Response tools")
        self.driver.find_element_by_xpath("//span[text()='Internal Applications ']").click()
        waitfor(self, 2, By.XPATH, "//span[text()='Internal Applications ']")
        self.driver.find_element_by_xpath("//p[text()='Endpoint Detection Response']").click()
        waitfor(self, 2, By.XPATH, "//h1[contains(text(),'Endpoint Detection Response')]")
        fprint(self, "[PASSED] Page loading successfully for Endpoint Detection Response Tools")
        process_console_logs(self)

    def test_16_security_communication_tool(self):
        """
        Checking if Security Communication tool pages are loading
        """
        fprint(self, "\n----------- TC_ID 16: Checking load screen of Security Communication -----------")
        fprint(self, "Loading page for Security Communication tools")
        self.driver.find_element_by_xpath("//span[text()='Communication Tools ']").click()
        waitfor(self, 2, By.XPATH, "//span[text()='Communication Tools ']")
        self.driver.find_element_by_xpath("//p[text()='Security Communication']").click()
        waitfor(self, 2, By.XPATH, "//h1[contains(text(),'Security Communication')]")
        fprint(self, "[PASSED] Page loading successfully for Security Communication Tools")
        process_console_logs(self)

    def test_17_threat_intelligence_sharing_platform(self):
        """
        Checking if Threat Intelligence Sharing Platform pages are loading
        """
        fprint(self, "\n----------- TC_ID 17: Checking load screen of Threat Intelligence Sharing Platforms -----------")
        fprint(self, "Loading page for Threat Intelligence Sharing Platforms tools")
        self.driver.find_element_by_xpath("//span[text()='Communication Tools ']").click()
        waitfor(self, 2, By.XPATH, "//span[text()='Communication Tools ']")
        self.driver.find_element_by_xpath("//p[text()='Threat Intelligence Sharing Platforms']").click()
        waitfor(self, 2, By.XPATH, "//h1[contains(text(),'Threat Intelligence Sharing Platforms')]")
        fprint(self, "[PASSED] Page loading successfully for Threat Intelligence Sharing Platforms Tools")
        process_console_logs(self)

    def test_18_cyware_products(self):
        """
        Checking if Cyware Products Page is loading
        """
        fprint(self, "\n----------- TC_ID 18: Checking load screen of Cyware Products -----------")
        fprint(self, "Loading page for Threat Intelligence Sharing Platforms tools")
        self.driver.find_element_by_xpath("//span[text()='Cyware Products ']").click()
        waitfor(self, 2, By.XPATH, "//span[text()='Cyware Products ']")
        fprint(self, "[PASSED] Page loading successfully for Threat Intelligence Sharing Platforms Tools")
        process_console_logs(self)

    def test_19_ctix_integrations(self):
        """
        Checking if CTIX Integrations page is loading
        """
        fprint(self, "\n----------- TC_ID 19: Checking load screen of Third Party Developers -----------")
        fprint(self, "Loading page for CTIX Integrators")
        self.driver.find_element_by_xpath("//span[text()='CTIX Integrators ']").click()
        waitfor(self, 2, By.XPATH, "//span[text()='CTIX Integrators ']")
        fprint(self, "[PASSED] Page loading successfully for CTIX Integrators")
        # Todo: Add testcase for REST API doc redirection
        process_console_logs(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
