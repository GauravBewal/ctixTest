import unittest

from lib.api.csol_internal import get_event_ids, get_event_count
from lib.ui.cyware_products import *
from lib.ui.integration_management import *
from lib.ui.nav_threat_data import verify_data_in_threatdata, click_on_intel
from lib.ui.quick_add import create_intel
from lib.ui.rules import create_basic_rule, add_source, add_condition_title, add_action_csol

csol = get_credentials("csol")
csol_cred = ['CSOL', csol["base_url"], csol["access_id"], csol["secret_key"]]
CSOL_login_cred = ['jeet.raikar@cyware.com', 'Jet@cware123@csol']
csol_domain = "csoltp"+uniquestr[:4]+".com"
csol_domain_v3 = "csolv3"+uniquestr[:4]+".com"
csol_event_name = "RULE_tags3488"



class CywareProducts(unittest.TestCase):

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

    def apply_filter(self):
        waitfor(self, 10, By.XPATH, "//button[contains(@class,'walkthrough-filter show-filters-button')]")
        self.driver.find_element_by_xpath("//button[contains(@class,'walkthrough-filter show-filters-button')]").click()
        fprint(self, "Clicked on the Filter Button")
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search by Labels']")
        self.driver.find_element_by_xpath("//input[@placeholder='Search by Labels']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search by Labels']").send_keys(csol_event_name.lower())
        fprint(self, "Searching for the label - " + csol_event_name.lower())
        waitfor(self, 10, By.XPATH, "//li[@id='list-item0']//p[contains(text(),'"+csol_event_name.lower()+"')]")
        self.driver.find_element_by_xpath("//li[@id='list-item0']//p[contains(text(),'"+csol_event_name.lower()+"')]").click()
        fprint(self, "Label is visible, clicked on it")
        sleep(2)

    def test_01_verify_add_csol_product(self):
        """
            Testcase to configure CSOL account in CTIX
        """
        fprint(self, "TC_ID: 701101 - test_01_verify_add_csol_product")
        nav_menu_admin(self, "Integration Management")
        self.driver.find_element_by_xpath("//span[contains(text(),'Cyware Products ')]/parent::a").click()
        add_account(self, product_name="CO", credentials=csol_cred)
        manage_actions(self)
        waitfor(self, 10, By.XPATH, "//div[contains(@class,'cy-page__back-button')]")
        self.driver.find_element_by_xpath("//div[contains(@class,'cy-page__back-button')]").click()
        search(self, "CO")
        if waitfor(self, 8, By.XPATH, "//p[contains(text(),'CO')]/ancestor::div[2]//div[contains(@class,'enabled')]", False):
            pass
        elif waitfor(self, 2, By.XPATH, "//p[contains(text(),'CO')]/ancestor::div[1]/following-sibling::div//input[@value='true']"):
            pass
        fprint(self, "CSOL Enabled Card is visible")

    def test_02_verify_csol_triggerPlaybook_action(self):
        """
                    Testcase to check CSOL trigger playbook action
        """
        fprint(self, "TC_ID: 701102 - test_02_verify_csol_triggerPlaybook_action")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, "CSOL_rule_playbook")
        add_source(self, source="Import", collection='Select All')
        add_action_csol(self, event=csol_event_name)
        add_condition_title(self, value="csoltp")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        create_intel(self, type="Domain", title="CSOL_Domain", value=csol_domain)
        fprint(self, "Waiting for the 5 minutes...")
        sleep(300)      # 5 minutes of wait before verification of rule run
        verify_data_in_threatdata(self, value=csol_domain, source="Import")
        click_on_intel(self, source="Import", value=csol_domain)
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Action Taken')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Action Taken')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'3rd Party Actions')]/ancestor::div[2]//following-sibling::div//span[contains(text(),'Trigger Playbook')]")
        fprint(self, "[Passed] Trigger Playbook action is visible under Actions Taken Section")

    def test_03_verify_csol_triggerPlaybook_action_in_csol(self):
        """
                Testcase to check CSOL trigger data is visible in the CSOL
        """

        fprint(self, "TC_ID: 701103 - test_03_verify_csol_triggerPlaybook_action_in_csol")
        self.driver.execute_script(f'''window.open("{csol_cred[1]}/soar/","_blank");''')
        sleep(5)
        fprint(self, "Opening Up CSOL platform")
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        cyware_product_login(self, credentials=CSOL_login_cred)
        self.driver.find_element_by_xpath("//i[contains(@class,'cyicon-menu')]/parent::div").click()
        fprint(self, "Clicked on the main menu")
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Trigger Events') and contains(@class,'cs-menu-item--title')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Trigger Events') and contains(@class,'cs-menu-item--title')]").click()
        fprint(self, "Clicked on the Triggered Events")
        self.apply_filter()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Package From CTIX')]/ancestor::td[1]/parent::tr/td[1]//a")
        id = self.driver.find_element_by_xpath("//span[contains(text(),'Package From CTIX')]/ancestor::td[1]/parent::tr/td[1]//a").text
        print("id - "+id)
        self.driver.find_element_by_xpath("//a[contains(text(),'"+id+"')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Table')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Table')]").click()
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'title')]")
        value = self.driver.find_element_by_xpath("//div[contains(text(),'title')]/parent::div/div[2]/div").text
        print("value - "+value)
        if value.__contains__(csol_domain):
            fprint(self, "[Passed] Added Domain is visible in the CSOL")
        else:
            fprint(self, "[Failed] Added Domain is not visible in the CSOL")
            self.fail("[Failed] Added Domain is not visible in the CSOL")

        # event_id = get_event_ids(label_name="rule_tags5010")
        # print("event id - ", event_id)
        # response = get_event_count(event_id=event_id)
        # print("final response -", response)

    def test_04_verify_csol_triggerPlaybook_v3_action(self):
        """
                    Testcase to check CSOL trigger playbook V3 action
        """
        fprint(self, "TC_ID: 701104 - test_04_verify_csol_triggerPlaybook_v3_action")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, "CSOL_rule_playbook_v3")
        add_source(self, source="Import", collection='Select All')
        add_action_csol(self, type="Trigger Playbook V3", event=csol_event_name)
        add_condition_title(self, value="csolv3")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        create_intel(self, type="Domain", title="CSOL_Domain", value=csol_domain_v3)
        fprint(self, "Waiting for the 5 minutes...")
        sleep(300)  # 5 minutes of wait before verification of rule run
        verify_data_in_threatdata(self, value=csol_domain_v3, source="Import")
        click_on_intel(self, source="Import", value=csol_domain_v3)
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Action Taken')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Action Taken')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'3rd Party Actions')]/ancestor::div[2]//following-sibling::div//span[contains(text(),'Trigger Playbook V3')]")
        # waitfor(self, 20, By.XPATH, "//span[@data-testid='action_name' and contains(text(),'Trigger Playbook V3')]")
        fprint(self, "[Passed] Trigger Playbook V3 action is visible under Actions Taken Section")

    def test_05_verify_csol_triggerPlaybook_v3_action_in_csol(self):
        """
                    Testcase to check CSOL trigger data is visible in the CSOL
        """
        fprint(self, "TC_ID: 701105 - test_05_verify_csol_triggerPlaybook_v3_action_in_csol")
        self.driver.execute_script(f'''window.open("{csol_cred[1]}/soar/","_blank");''')
        sleep(5)
        fprint(self, "Opening Up CSOL platform")
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        cyware_product_login(self, credentials=CSOL_login_cred)
        self.driver.find_element_by_xpath("//i[contains(@class,'cyicon-menu')]/parent::div").click()
        fprint(self, "Clicked on the main menu")
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Trigger Events') and contains(@class,'cs-menu-item--title')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Trigger Events') and contains(@class,'cs-menu-item--title')]").click()
        fprint(self, "Clicked on the Triggered Events")
        self.apply_filter()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Package From CTIX')]/ancestor::td[1]/parent::tr/td[1]//a")
        id = self.driver.find_element_by_xpath("//span[contains(text(),'Package From CTIX')]/ancestor::td[1]/parent::tr/td[1]//a").text
        print("id - " + id)
        self.driver.find_element_by_xpath("//a[contains(text(),'" + id + "')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Table')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Table')]").click()
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'sdo name')]")
        value = self.driver.find_element_by_xpath("//div[contains(text(),'sdo name')]/parent::div/div[2]/div").text
        print("value - " + value)
        if value.__contains__(csol_domain_v3):
            fprint(self, "[Passed] Added Domain is visible in the CSOL")
        else:
            fprint(self, "[Failed] Added Domain is not visible in the CSOL")
            self.fail("[Failed] Added Domain is not visible in the CSOL")

    def test_06_configure_csap(self):
        """
            Testcase to configure CSAP account in CTIX
        """
        fprint(self, "TC_ID: 701106 - verify is CSAP account can be configured successfully in CSAP")
        set_value("tstamp", uniquestr[-4:])
        set_value("csap_category_name", "ctix_auto_cat")
        set_value("csap_recipient_group", "ctix_recipient")
        launch_csap(self)
        create_category(self, "ctix_auto_cat")
        create_receipent_group(self, "ctix_recipient")
        create_csap_creds(self)
        handles = self.driver.window_handles
        fprint(self, "Redirecting back to CTIX")
        self.driver.switch_to.window(handles[0])
        nav_menu_admin(self, "Integration Management")
        waitfor(self, 20, By.XPATH, "//a/span[contains(text(), 'Cyware Products')]")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Cyware Products')]").click()
        add_csap_account(self)
        manage_actions(self)

    def test_07_verify_csap_old_draft(self):
        """
            Testcase to validate if old feed sent as draft
        """
        _intel = "csap_old_draft_domain"+get_value("tstamp")
        fprint(self, "TC_ID: 701107 - Validate if old draft feed is received in CSAP")
        launch_csap(self)
        validate_csap_intel(self, _intel, "draft")

    def test_08_verify_csap_new_draft(self):
        """
            Testcase to validate if new feed sent as draft
        """
        _intel = "csap_new_draft_domain"+get_value("tstamp")
        fprint(self, "TC_ID: 701108 - Validate if old draft feed is received in CSAP")
        launch_csap(self)
        validate_csap_intel(self, _intel, "draft")

    def test_09_verify_csap_old_publish(self):
        """
            Testcase to validate if old feed sent as published
        """
        _intel = "csap_old_publish_domain"+get_value("tstamp")
        fprint(self, "TC_ID: 701109 - Validate if old publish feed is received in CSAP")
        launch_csap(self)
        validate_csap_intel(self, _intel, "published")

    def test_10_verify_csap_new_publish(self):
        """
            Testcase to validate if new feed sent as publish
        """
        _intel = "csap_new_publish_domain"+get_value("tstamp")
        fprint(self, "TC_ID: 701110 - Validate if new publish feed is received in CSAP")
        launch_csap(self)
        validate_csap_intel(self, _intel, "published")

    def test_11_delete_created_creds(self):
        """
            Testcase to delete any created OpenAPI creds from CSAP
        """
        cred_title = get_value("csap_cred_title")
        fprint(self, "TC_ID: 701111 - Validate if OpenAPI creds of CSAP can be deleted")
        launch_csap(self)
        waitfor(self, 20, By.XPATH, "//a[@cy-test-id='user-mngmnt-menu']")
        self.driver.find_element_by_xpath("//a[@cy-test-id='user-mngmnt-menu']").click()
        waitfor(self, 20, By.XPATH, "//a/span[text()='Integrations']")
        sleep(2)
        self.driver.find_element_by_xpath("//a/span[text()='Integrations']").click()
        waitfor(self, 20, By.XPATH, "//div[text()='CSAP INTEGRATIONS']")
        self.driver.find_element_by_xpath("//div[text()='CSAP INTEGRATIONS']").click()
        waitfor(self, 20, By.XPATH, "//div[span[text()='Open API Credentials']]")
        self.driver.find_element_by_xpath("//div[span[text()='Open API Credentials']]").click()
        sleep(2)    # required
        self.driver.find_element_by_xpath("//div[@class='action-icon']").click()
        waitfor(self, 20, By.XPATH, "//input[@id='main-input']")
        self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys(cred_title)
        self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys(Keys.ENTER)
        waitfor(self, 20, By.XPATH, "//td[span[normalize-space(text())='"+cred_title+"']]")
        self.driver.find_element_by_xpath("//td[span[normalize-space(text())='"+cred_title+
                                          "']]/following-sibling::td/p/a[text()='Revoke']").click()
        waitfor(self, 20, By.XPATH, "//button[span[text()='Yes, Revoke']]")
        self.driver.find_element_by_xpath("//button[span[text()='Yes, Revoke']]").click()

    def test_12_cc_add_csol_label_events(self):
        """
            Testcase to add labels and events for the respective test cases
        """
        self.driver.execute_script(f'''window.open("{csol_cred[1]}/soar/","_blank");''')
        sleep(5)
        fprint(self, "Opening Up CSOL platform")
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        cyware_product_login(self, credentials=CSOL_login_cred)
        self.driver.find_element_by_xpath("//i[contains(@class,'cyicon-menu')]/parent::div").click()
        fprint(self, "Clicked on the main menu")
        waitfor(self, 20, By.XPATH, "//div[normalize-space(text())='Labels' and contains(@class,'cs-menu-item--title')]")
        self.driver.find_element_by_xpath\
            ("//div[normalize-space(text())='Labels' and contains(@class,'cs-menu-item--title')]").click()
        csol_cc_val = uniquestr[-4:]
        set_value("csol_timestamp", csol_cc_val)
        csol_substrings = ["tags", "confscore", "domainAll"]
        [csol_add_label(self, label+csol_cc_val) for label in csol_substrings]
        # Todo need to check if label was added with success message
        sleep(5)
        self.driver.find_element_by_xpath("//i[contains(@class,'cyicon-menu')]/parent::div").click()
        fprint(self, "Clicked on the main menu")
        waitfor(self, 20, By.XPATH, "//div[normalize-space(text())='Configure Triggers' and contains(@class,'cs-menu-item--title')]")
        self.driver.find_element_by_xpath\
            ("//div[normalize-space(text())='Configure Triggers' and contains(@class,'cs-menu-item--title')]").click()
        [csol_add_event(self, event+csol_cc_val) for event in csol_substrings]

    def test_13_generate_cftr_credentials(self):
        """ Test case to generate the cftr credentials"""
        fprint(self, "TC_ID: 701113 - Test case to generate the cftr credentials")
        create_cftr_creds(self)
        fprint(self, "[Passed]-Cftr credentials generated successfully")

    def test_14_add_cftr_account(self):
        """
        test case to add the cftr account to ctix
        """
        fprint(self, "TC_ID: 701114 - Test case to add the cftr credentials to ctix")
        cftr = get_credentials("cftr")
        cftr_cred = ['CFTR', cftr["api_url"], cftr["access_id"], cftr["secret_key"]]
        nav_menu_admin(self, "Integration Management")
        self.driver.find_element_by_xpath("//span[contains(text(),'Cyware Products ')]/parent::a").click()
        add_account(self, product_name="CFTR", credentials=cftr_cred)
        manage_actions(self)
        waitfor(self, 10, By.XPATH, "//div[contains(@class,'cy-page__back-button')]")
        self.driver.find_element_by_xpath("//div[contains(@class,'cy-page__back-button')]").click()
        search(self, "CFTR")
        if waitfor(self, 8, By.XPATH, "//p[contains(text(),'CFTR')]/ancestor::div[2]//div[contains(@class,'enabled')]",False):
            pass
        elif waitfor(self, 2, By.XPATH,"//p[contains(text(),'CFTR')]/ancestor::div[1]/following-sibling::div//input[@value='true']"):
            pass
        fprint(self, "CFTR Enabled Card is visible")

    # def add_ctix_account_cftr(self):
    #     """
    #     test case to add the ctix account to cftr
    #     """
    #

    def test_15_create_alert_in_csap(self):
        """
            Testcase to create alert in CSAP to be sent to CTIX
        """
        launch_csap(self)
        _random_str = uniquestr[-4:]
        _tille = "CSAP_to_CTIX_"+_random_str
        _summary = f"Summary for intel from CSAP to CTIX {_random_str}"
        _category = get_value("csap_category_name")
        _recipient = get_value("csap_recipient_group")
        ioc_body = f"mailicidomain{_random_str}.com"
        csap_add_ctix_integration(self)
        create_new_csap_alert(self, title="Samp_title", summary="my_summary", category=get_value("csap_category_name"), recipient=get_value("csap_recipient_group"), tlp="white", ioc_body=ioc_body)
        waitfor(self, 20, By.XPATH, "//span[button[span[text()='Save As Draft']]]"
                                    "/following-sibling::span/button[span[text()='Publish']]")
        self.driver.find_element_by_xpath("//span[button[span[text()='Save As Draft']]]"
                                          "/following-sibling::span/button[span[text()='Publish']]").click()
        waitfor(self, 20, By.XPATH, "//h1[normalize-space(text())='Alert Preview']")
        self.driver.find_element_by_xpath("//button[span[text()='Edit']]"
                                          "/following-sibling::button[span[text()='Publish']]").click()
        waitfor(self, 20, By.XPATH, "//div/button[span[text()='Publish']]")
        self.driver.find_element_by_xpath("//div/button[span[text()='Publish']]").click()
        sleep(20)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())