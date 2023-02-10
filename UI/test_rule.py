import random
import unittest

from lib.ui.nav_tableview import *
from lib.ui.rules import *
from lib.ui.quick_add import quick_create_ip
from lib.ui.quick_add import quick_add_domain_object
from lib.ui.nav_threat_data import *
from lib.ui.nav_tags import *
from lib.ui.integration_management import *
from lib.ui.quick_add import create_intel
from lib.api.rules import run_rule_delta, disable_rule_api
from lib.api.external_apis import *


failures = []
collection = ["coll_1.x", "coll_2.0", "coll_2.1"]
stix_source = ["sub_1dotx", "sub_2dot0", "sub_2dot1"]


class Rules(unittest.TestCase):

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


    def quick_create_intel(self, name, ioc_type, ioc_value):
        fprint(self, "Waiting for the New Button...")
        self.driver.find_element_by_xpath("//button[contains(text(),'New')]").click()
        fprint(self, "Clicked on the New Button")
        waitfor(self, 5, By.XPATH, "//li/div[contains(text(),'Quick Add Intel')]")
        self.driver.find_element_by_xpath("//li/div[contains(text(),'Quick Add Intel')]").click()
        fprint(self, "Clicked on the 'Quick Add Intel' option")
        waitfor(self, 5, By.XPATH, qai_ioc_type_search)
        sleep(5)
        fprint(self, "Searching - " + ioc_type)
        waitfor(self, 5, By.XPATH, "//input[@name='searchbar']")
        self.driver.find_element_by_xpath("//input[@name='searchbar']").click()
        clear_field(self.driver.find_element_by_xpath("//input[@name='searchbar']"))
        self.driver.find_element_by_xpath("//input[@name='searchbar']").send_keys(ioc_type)
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'" + ioc_type + "')]/ancestor::div[1]")
        sleep(5)
        self.driver.find_element_by_xpath("//div[contains(text(),'" + ioc_type + "')]/div[1]/div").click()
        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(name)
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").send_keys(ioc_value)
        fprint(self, "Clicking on Create Intel for data created")
        waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Create Intel')]")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Create Intel')]").click()
        if Build_Version.__contains__("3."):
            verify_success(self, "You can view the created intel as a report object in the Threat Data module")
        else:
            verify_success(self, "You will be notified once the STIX package is created")
        fprint(self, "[Passed] Request for Create Intel sent successfully")
        fprint(self, "Waiting for intel to be with Created Status")
        repeat = 1
        while repeat <= 6:
            if waitfor(self, 10, By.XPATH,
                       "//span[contains(text(),'" + name + "')]/ancestor::td/following-sibling::td[3]//span[contains(text(),'Created')]",
                       False):
                fprint(self, "[Passed] Created Status of intel is visible - " + name)
                self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
                break
            else:
                fprint(self, "Created Status of intel is not visible, Clicking on the Refresh Button")
                sleep(20)
                self.driver.find_element_by_xpath("//button[contains(text(),'Refresh')]").click()
                fprint(self, "Clicked on the Refresh Button")
                if repeat == 6:
                    fprint(self, "going to quick add history")
                    self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
                    fprint(self, "[Failed] Intel is not found with Created Status")
                repeat = repeat + 1
                sleep(30)
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def create_domain_object(self, type, title, value):
        fprint(self, "Creating " + type + ", through quick add intel")
        quick_add_domain_object(self, type, title, value)
        fprint(self, type + " Created.")

    def validate_action_taken_third_party_rule(self, ioc, rule_name):
        """
            Function to validate if rule is populated under actions taken
            args:
                ioc: IOC on which the rule was run
                rule_name: Name of the rule that was expected to be run on IOC
            returns:
                None
        """
        if Build_Version.__contains__("3."):
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                        "/ancestor::tr/td[3]//span[contains(text(),'" + ioc + "')]")
            sleep(2)
            _ele = self.driver.find_elements_by_xpath(
                "//span[contains(text(), '" + ioc + "')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            fprint(self, "Clicking on Actions Taken")
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Action Taken')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Action Taken')]").click()
            waitfor(self, 20, By.XPATH, "//div[@id='tab-third_party']")
            self.driver.find_element_by_xpath("//div[@id='tab-third_party']").click()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), '"+rule_name+"')]")
        else:
            waitfor(self, 20, By.XPATH, "//div[div/div/span[contains(text(), '" + ioc + "')]]")
            self.driver.find_element_by_xpath(
                "//div[div/div/span[contains(text(), '" + ioc + "')]]").click()
            waitfor(self, 20, By.XPATH, "//li[a/span[contains(text(), 'Activity Timeline')]]")
            self.driver.find_element_by_xpath("//li[a/span[contains(text(), 'Activity Timeline')]]").click()
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+ rule_name +"')]")

    def test_01_rule_page_loading(self):
        fprint(self, "TC_ID: 98450 - rule - test_01_rule_page_loading")
        nav_menu_main(self, "Rules")
        fprint(self, "[Passed] - Successfully navigate to rule listing")
        process_console_logs(self)
        fprint(self, "Rule - Page Load Successfully")

    def test_02_rule_add(self):
        fprint(self, "TC_ID: 98451 - rule - test_02_rule_add")
        nav_menu_main(self, "Rules")
        waitfor(self, 15, By.XPATH, "//button[contains(text(),'New Rule')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'New Rule')]").click()
        fprint(self, "[Passed] - Clicked on Add rule button")
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Skip')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Skip')]").click()
        fprint(self, "[Passed] - Clicked on skip button for walkthrough window")
        waitfor(self, 15, By.XPATH, "(//input[@aria-placeholder='Rule Name *'])[2]")
        self.driver.find_element_by_xpath("(//input[@aria-placeholder='Rule Name *'])[2]").click()
        self.driver.find_element_by_xpath("(//input[@aria-placeholder='Rule Name *'])[2]").send_keys("Rule" + uniquestr)
        fprint(self, "[Passed] - Rule title given")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description']").click()
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description']").send_keys(
            "Rule" + " " + "Desription" + "" + uniquestr)
        fprint(self, "[Passed] - Rule Description given")
        self.driver.find_element_by_xpath("//button[contains(text(),'Submit')]").click()
        waitfor(self, 15, By.XPATH, "//button[text()='Save']")
        self.driver.find_element_by_xpath("//button[text()='Save as Draft']").click()
        sleep(1)
        verify_success(self, "Rule created successfully")
        fprint(self, "[Passed] - Rule Created successfully")
        process_console_logs(self)
        fprint(self, "Rule - Added Successfully")

    def rule_search_functionality(self):
        fprint(self, "TC_ID: 98452 - rule - rule_search_functionality")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
        fprint(self, "[Passed] - clearing existing search filter data")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(
            "Rule" + uniquestr)
        # self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("Rule1622705842915")
        fprint(self, "[Passed] - Provided search data")
        waitfor(self, 15, By.XPATH, "//span[contains(text(),'Press enter or click to search')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Press enter or click to search')]").click()
        fprint(self, "[Passed] - Search successfully ")
        waitfor(self, 15, By.XPATH, "//span[contains(text(),'Rule" + uniquestr + "')]")
        # waitfor(self, 15, By.XPATH, "//span[contains(text(),'Rule1622705842915')]")
        self.driver.find_element_by_xpath("//button[@data-testid='action']").click()
        fprint(self, "[Passed] - Clicked on action button")

    def test_03_rule_update(self):
        fprint(self, "TC_ID: 98453 - rule - test_03_rule_update")
        nav_menu_main(self, "Rules")
        waitfor(self, 15, By.XPATH, "//input[@placeholder='Search or filter results']")
        self.rule_search_functionality()
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Edit')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Edit')]").click()
        fprint(self, "[Passed] - Select Edit option from action dropdown")
        waitfor(self, 15, By.XPATH, "//button[text()='Save']")

        # --------------- Rule data provided-----------
        # Rule_option = ['Allow all Sources','Allow all Feeds','Triggers On Update']
        for option in range(1, 5):
            if option != 3:
                self.driver.find_element_by_xpath("(//span[@class='cy-checkbox__style'])[" + str(option) + "]").click()
                sleep(4)
                self.driver.find_element_by_xpath("//button[contains(text(),'Yes, Remove')]").click()
                sleep(4)

            # self.driver.find_element_by_xpath("//span[contains(text(),'"+option+"')]").click()
            # waitfor(self, 15, By.XPATH, "//button[@class='text-capitalize cy-button cy-button--danger cy-button--md']")
            # self.driver.find_element_by_xpath("//button[@class='text-capitalize cy-button cy-button--danger cy-button--md']").click()
            # sleep(1)
            # fprint(self, "[Passed] - Clicked on '" + option + "' option of indicator ")
        self.driver.find_element_by_xpath("//span[@class='flex-grow-1'][contains(text(),'Actions')]").click()

        rule_Action = ['Send E-Mail']
        for _action in rule_Action:
            self.driver.find_element_by_xpath("//a[contains(text(),'" + _action + "')]").click()
        fprint(self, "[Passed] - Clicked on '" + _action + "' action ")
        send_email_option = ['Application', 'Account', 'Users']
        for _options in send_email_option:
            waitfor(self, 5, By.XPATH, "//span[contains(text(),'Application')]/ancestor::*[@tabindex]")
            self.driver.find_element_by_xpath(
                "//span[contains(text(),'" + _options + "')]/ancestor::*[@tabindex]").click()
            sleep(1)
            self.driver.find_element_by_xpath("(//div[@class='cy-select-menu-option-label-main'])[1]").click()

        # --------------- Rule data provided-----------

        self.driver.find_element_by_xpath("//button[text()='Save as Draft']").click()
        verify_success(self, "Rule updated succesfully")
        fprint(self, "[Passed] - Rule Updated successfully")
        process_console_logs(self)
        fprint(self, "Rule updated successfully!")

    def test_04_rule_delete(self):
        fprint(self, "TC_ID: 98454 - rule - test_04_rule_delete")
        nav_menu_main(self, "Rules")
        self.rule_search_functionality()
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Delete')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Delete')]").click()
        fprint(self, "[Passed] - select Delete option")
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Delete')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Delete')]").click()
        fprint(self, "[Passed] - Clicked on Delete confirmation")
        verify_success(self, "Rule deleted successfully")
        process_console_logs(self)
        clear_console_logs(self)
        fprint(self, "Rule deleted successfully!")

    def test_05_rule_update_tag(self):
        """
        Testcase to validate if update tag action is working
        """
        fprint(self, "TC_ID: 61001 - verify_rule_update_tag")
        _rule_name = "auto_rule_update_tag"
        add_tag(self, rule_tag)
        quick_create_ip(self, update_tag_old_ip, "ip_old_feed_run")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_update_tag(self, tagname=rule_tag)
        add_condition_title(self, value=tag_ip_pattern)
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        sleep(10)

    def test_06_validate_update_tag_old_feed(self):
        """
            Testcase to validate update yag action on old feed
        """
        fprint(self, "TC_ID: 61002 - verify update tag on preexisting data")
        actions = ActionChains(self.driver)
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        self.driver.find_element_by_xpath(rules_main_search).send_keys("auto_rule_update_tag")
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        click_on_actions_item(self, "auto_rule_update_tag", "Run")
        # waitfor(self, 20, By.XPATH, "//div//span[contains(text(), 'auto_rule_update_tag')]")
        # _ele = self.driver.find_element_by_xpath("//div//span[contains(text(), 'auto_rule_update_tag')]")
        # actions.move_to_element(_ele).perform()
        # sleep(10)
        # self.driver.find_element_by_xpath("//button[@data-testid='action']").click()
        # waitfor(self, 20, By.XPATH, "//li[contains(text(), 'Run')]")
        # sleep(2)
        # _ele = self.driver.find_elements_by_xpath("//li[contains(text(), 'Run')]")[1]
        # actions.move_to_element(_ele).perform()
        # actions.click(_ele).perform()
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, update_tag_old_ip, "Import")
        if Build_Version.__contains__("3."):
            verify_data_in_threatdata(self, update_tag_old_ip, "Import")
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                        "/ancestor::tr/td[3]//span[contains(text(),'" + update_tag_old_ip + "')]")
            sleep(2)
            _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '"+update_tag_old_ip+"')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
            validate_tag(self, rule_tag)
        else:
            waitfor(self, 20, By.XPATH, "//div[div/div/span[contains(text(), '"+update_tag_old_ip+"')]]")
            self.driver.find_element_by_xpath("//div[div/div/span[contains(text(), '"+update_tag_old_ip+"')]]").click()
            validate_tag(self, rule_tag)

    def test_07_update_tag_new_feed(self):
        """
            Testing auto update tag on newly received tags
        """
        fprint(self, "TC_ID: 61003 - verify update tag via rules on auto run")
        quick_create_ip(self, update_tag_new_ip, "ip_auto_feed_run")
        sleep(20)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, update_tag_new_ip, "Import")
        if Build_Version.__contains__("3."):
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                        "/ancestor::tr/td[3]//span[contains(text(),'" + update_tag_new_ip + "')]")
            sleep(2)
            _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '"+update_tag_new_ip+"')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            fprint(self, "Clicking on basic details")
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
            validate_tag(self, rule_tag)
        else:
            sleep(2)
            waitfor(self, 20, By.XPATH, "//div[div/div/span[contains(text(), '"+update_tag_new_ip+"')]]")
            self.driver.find_element_by_xpath("//div[div/div/span[contains(text(), '"+update_tag_new_ip+"')]]").click()
            validate_tag(self, rule_tag)

    def test_08_create_intel_and_rule_update_reference_set(self):
        """
            Testcase to update reference set
        """
        fprint(self, "TC_ID: 61004 - verify rule creation for update reference")
        _rule_name = "auto_rule_update_reference_set"
        _refset = "auto"+uniquestr[-4:]
        set_value("REFERENCE_SET_NAME", _refset)
        create_ref_set_qradar(set_name=_refset)
        quick_create_ip(self, update_ref_set_old_ip, "ip_old_ref_set")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_update_ref_set(self, set_name=_refset)
        add_condition_title(self, value=ref_set_ip_pattern)
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        process_console_logs(self)

    def test_09_manual_run_update_reference_set_verify_action_3rdparty(self):
        """
            Validate if rule cam be run on previously existing data
        """
        fprint(self, "TC_ID: 61005 - verify old feeds run for reference set")
        _rule_name = "auto_rule_update_reference_set"
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        fprint(self, "Searching for a rule name")
        self.driver.find_element_by_xpath(rules_main_search).send_keys(_rule_name)
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        sleep(5)
        click_on_actions_item(self, _rule_name, "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, update_ref_set_old_ip, "Import")
        self.validate_action_taken_third_party_rule(ioc=update_ref_set_old_ip, rule_name=_rule_name)

    def test_10_create_intel_for_auto_update_reference_set_verify_action_3rdparty(self):
        """
            Testing if the rule is auto run upon newly added data
        """
        fprint(self, "TC_ID: 61006 - verify auto update reference set via rules")
        _rule_name = "auto_rule_update_reference_set"
        fprint(self, "Creating Data for auto run")
        quick_create_ip(self, update_ref_set_new_ip, "ip_new_ref_set")
        sleep(20)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, update_ref_set_new_ip, "Import")
        self.validate_action_taken_third_party_rule(ioc=update_ref_set_new_ip, rule_name=_rule_name)
        process_console_logs(self)

    def test_11_verify_in_QRADAR_reference_set_data(self):
        """
            Validate if intel is added to selected reference set
        """
        fprint(self, "TC_ID: 61007 - verify_reference set data")
        _fail = False
        try:
            if search_data_in_qradar(get_value("REFERENCE_SET_NAME"), [update_ref_set_old_ip, update_ref_set_new_ip]) is True:
                fprint(self, "All required data is visible in QRADAR")
            else:
                _fail = True
        finally:
            fprint(self, "Deleting reference set ")
            delete_ref_set_qradar(set_name=get_value("REFERENCE_SET_NAME"))
        if _fail is True:
            self.fail("Not all required data is visible in QRADAR")

    def test_12_rule_mark_manual_review(self):
        fprint(self, "TC_ID: 40100- verify_rule_manual_review")
        _rule_name = "auto_rule_manual_review"
        quick_create_ip(self, manual_review_old_ip, "manual_review_old_ip")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_manual_review(self)
        add_condition_title(self, value=manual_ip_pattern)
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        quick_create_ip(self, manual_review_new_ip, "manual_review_new_ip")

    def test_13_verify_rule_mark_manual_review_new_feed(self):
        fprint(self, "TC_ID: 40101 - Verifying 'verify_rule_manual_review_new_feeds'")
        nav_menu_main(self, 'Threat Data')
        if Build_Version.__contains__("3."):
            verify_data_in_threatdata(self, manual_review_new_ip, "Import")
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                        "/ancestor::tr/td[3]//span[contains(text(),'" + manual_review_new_ip + "')]")
            sleep(2)
            _ele = \
                self.driver.find_elements_by_xpath(
                    "//span[contains(text(), '" + manual_review_new_ip + "')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), 'Under Manual Review')]")
            fprint(self, '[Passed] Indicator is marked under manual review')
            fprint(self, 'Checking under Action Taken for rule name')
            fprint(self, "Clicking on Actions Taken")
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Action Taken')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Action Taken')]").click()
            waitfor(self, 20, By.XPATH, "//div[@id='tab-third_party']")
            self.driver.find_element_by_xpath("//div[@id='tab-ctix']").click()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), 'auto_rule_manual_review')]")
            fprint(self, '[Passed] auto_rule_manual_review rule name is visible under action taken.')

    def test_14_verify_rule_mark_manual_review_old_feed(self):
        """
            Testcase to validate update manual review action on old feed
        """
        fprint(self, "TC_ID: 40102 - verify update manual review action on preexisting data")
        #actions = ActionChains(self.driver)
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        self.driver.find_element_by_xpath(rules_main_search).send_keys("auto_rule_manual_review")
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        click_on_actions_item(self, "auto_rule_manual_review", "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        if Build_Version.__contains__("3."):
            verify_data_in_threatdata(self, manual_review_old_ip, "Import")
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                        "/ancestor::tr/td[3]//span[contains(text(),'" + manual_review_old_ip + "')]")
            sleep(2)
            _ele = \
                self.driver.find_elements_by_xpath(
                    "//span[contains(text(), '" + manual_review_old_ip + "')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), 'Under Manual Review')]")
            fprint(self, '[Passed] Indicator is marked under manual review')
            fprint(self, 'Checking under Action Taken for rule name')
            fprint(self, "Clicking on Actions Taken")
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Action Taken')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Action Taken')]").click()
            waitfor(self, 20, By.XPATH, "//div[@id='tab-third_party']")
            self.driver.find_element_by_xpath("//div[@id='tab-ctix']").click()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), 'auto_rule_manual_review')]")
            fprint(self, '[Passed] auto_rule_manual_review rule name is visible under action taken.')

    def test_15_rule_add_to_indicators_allowed(self):
        fprint(self, "TC_ID: 40103- verify_rule_indicators_allowed")
        _rule_name = "auto_rule_indicators_allowed"
        quick_create_ip(self, indicators_allowed_old_ip, "indicators_allowed_old_ip")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_indicators_allowed(self)
        add_condition_title(self, value=allowed_ip_pattern)
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        quick_create_ip(self, indicators_allowed_new_ip, "indicators_allowed_new_ip")

    def test_16_verify_rule_add_to_indicators_allowed_new_feed(self):
        """
            Testcase to validate update indicator allowed action on new feed
        """
        fprint(self, "TC_ID: 40104 - verify update indicator allowed action on new feed")
        nav_menu_main(self, 'Threat Data')
        if Build_Version.__contains__("3."):
            verify_data_in_threatdata(self, indicators_allowed_new_ip, "Import")
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                        "/ancestor::tr/td[3]//span[contains(text(),'" + indicators_allowed_new_ip + "')]")
            sleep(2)
            _ele = \
                self.driver.find_elements_by_xpath(
                    "//span[contains(text(), '" + indicators_allowed_new_ip + "')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), 'Indicator Allowed')]")
            waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Indicator Allowed')]]")
            self.driver.find_element_by_xpath("//div[span[contains(text(), 'Indicator Allowed')]]").click()
            waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Remove from Indicator Allowed')]]")
            fprint(self, '[Passed] Indicator is marked as Indicator Allowed')
            fprint(self, 'Checking under Action Taken for rule name')
            fprint(self, "Clicking on Actions Taken")
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Action Taken')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Action Taken')]").click()
            waitfor(self, 20, By.XPATH, "//div[@id='tab-third_party']")
            self.driver.find_element_by_xpath("//div[@id='tab-ctix']").click()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), 'auto_rule_indicators_allowed')]")
            fprint(self, '[Passed] auto_rule_indicators_allowed rule name is visible under action taken.')

    def test_17_verify_rule_add_to_indicators_allowed_old_feed(self):
        """
            Testcase to validate update indicator allowed action on old feed
        """
        fprint(self, "TC_ID: 40105 - verify update indicator allowed on preexisting data")
        actions = ActionChains(self.driver)
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        self.driver.find_element_by_xpath(rules_main_search).send_keys("auto_rule_indicators_allowed")
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        click_on_actions_item(self, "auto_rule_indicators_allowed", "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        if Build_Version.__contains__("3."):
            verify_data_in_threatdata(self, indicators_allowed_old_ip, "Import")
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                        "/ancestor::tr/td[3]//span[contains(text(),'" + indicators_allowed_old_ip + "')]")
            sleep(2)
            _ele = \
                self.driver.find_elements_by_xpath(
                    "//span[contains(text(), '" + indicators_allowed_old_ip + "')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), 'Indicator Allowed')]")
            waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Indicator Allowed')]]")
            self.driver.find_element_by_xpath("//div[span[contains(text(), 'Indicator Allowed')]]").click()
            waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Remove from Indicator Allowed')]]")
            fprint(self, '[Passed] Indicator is marked as Indicator Allowed')
            fprint(self, 'Checking under Action Taken for rule name')
            fprint(self, "Clicking on Actions Taken")
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Action Taken')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Action Taken')]").click()
            waitfor(self, 20, By.XPATH, "//div[@id='tab-third_party']")
            self.driver.find_element_by_xpath("//div[@id='tab-ctix']").click()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), 'auto_rule_indicators_allowed')]")
            fprint(self, '[Passed] auto_rule_indicators_allowed rule name is visible under action taken.')

    def test_18_rule_update_false_positive(self):
        """
        Testcase to validate if update false positive action is working
        """
        fprint(self, "TC_ID: 40106 - verify_rule_update_false_positive")
        quick_create_ip(self, update_fp_old_ip, "update_fp_old_ip")
        _rule_name = "auto_rule_update_false-positive"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_update_false_positive(self)
        add_condition_title(self, value=fp_ip_pattern)
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        quick_create_ip(self, update_fp_new_ip, "update_fp_new_ip")

    def test_19_verify_update_false_positive_new_feed(self):
        """
            Testcase to validate update false positive action on new feed
        """
        fprint(self, "TC_ID: 40107 - verify update false positive on new data")
        nav_menu_main(self, 'Threat Data')
        if Build_Version.__contains__("3."):
            verify_data_in_threatdata(self, update_fp_new_ip, "Import")
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                        "/ancestor::tr/td[3]//span[contains(text(),'" + update_fp_new_ip + "')]")
            sleep(2)
            _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '" + update_fp_new_ip + "')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), 'Marked False Positive')]")
            fprint(self, '[Passed] Indicator is marked as False Positive')
            fprint(self, 'Checking under Action Taken for rule name')
            fprint(self, "Clicking on Actions Taken")
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Action Taken')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Action Taken')]").click()
            waitfor(self, 20, By.XPATH, "//div[@id='tab-third_party']")
            self.driver.find_element_by_xpath("//div[@id='tab-ctix']").click()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), 'auto_rule_update_false-positive')]")
            fprint(self, '[Passed] auto_rule_update_false_positive rule name is visible under action taken.')

    def test_20_verify_update_false_positive_old_feed(self):
        """
            Testcase to validate update false positive action on old feed
        """
        fprint(self, "TC_ID: 40108 - verify update false positive on preexisting data")
        actions = ActionChains(self.driver)
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        self.driver.find_element_by_xpath(rules_main_search).send_keys("auto_rule_update_false-positive")
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        click_on_actions_item(self, "auto_rule_update_false-positive", "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        if Build_Version.__contains__("3."):
            verify_data_in_threatdata(self, update_fp_old_ip, "Import")
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                        "/ancestor::tr/td[3]//span[contains(text(),'" + update_fp_old_ip + "')]")
            sleep(2)
            _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '" + update_fp_old_ip + "')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), 'Marked False Positive')]")
            fprint(self, '[Passed] Indicator is marked as False Positive')
            fprint(self, 'Checking under Action Taken for rule name')
            fprint(self, "Clicking on Actions Taken")
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Action Taken')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Action Taken')]").click()
            waitfor(self, 20, By.XPATH, "//div[@id='tab-third_party']")
            self.driver.find_element_by_xpath("//div[@id='tab-ctix']").click()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), 'auto_rule_update_false-positive')]")
            fprint(self, '[Passed] auto_rule_update_false_positive rule name is visible under action taken.')

    def test_21_create_rule_save_result_set(self):
        """
        Testcase to verify action save result set
        """
        fprint(self, "TC_ID: 40108 verify rule save result set.")
        self.quick_create_intel("save_result_set_old_domain", "Domain", save_result_set_old_domain)
        _rule_name = "auto_rule_save_result_set"
        _rule_tag_to_save_result_set = "saveresultset"
        add_tag(self, _rule_tag_to_save_result_set)
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_save_result_set(self, _rule_tag_to_save_result_set, "indicators")
        add_condition_indicators(self, 'DOMAIN')
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        nav_menu_main(self, "Dashboards")
        self.quick_create_intel("save_result_set_new_domain", "Domain", save_result_set_new_domain)


    def test_22_verify_rule_save_result_set_new_feed(self):
        """
            Testcase to validate save result set action on new feed
        """
        fprint(self, "TC_ID: 40109 - verify save result set on new data")
        nav_menu_main(self, 'Threat Data')
        if Build_Version.__contains__("3."):
            verify_data_in_threatdata(self, save_result_set_new_domain, "Import")
            waitfor(self, 5, By.XPATH, "//span[contains(text(),'Import')]"
                                       "/ancestor::tr/td[3]//span[contains(text(),'" + save_result_set_new_domain + "')]")
            sleep(2)
            _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '" + save_result_set_new_domain + "')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            fprint(self, 'Checking under Action Taken for rule name')
            fprint(self, "Clicking on Actions Taken")
            waitfor(self, 5, By.XPATH, "//div[contains(text(), 'Action Taken')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Action Taken')]").click()
            waitfor(self, 5, By.XPATH, "//div[@id='tab-third_party']")
            self.driver.find_element_by_xpath("//div[@id='tab-ctix']").click()
            waitfor(self, 5, By.XPATH, "//span[contains(text(), 'auto_rule_save_result_set')]")
            fprint(self, '[Passed] auto_rule_save_result_set rule name is visible under action taken.')

    def test_23_verify_update_save_result_set_old_feed(self):
        """
            Testcase to validate save result set action on old feed
        """
        fprint(self, "TC_ID: 40110 - verify save result set on preexisting data")
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        self.driver.find_element_by_xpath(rules_main_search).send_keys("auto_rule_save_result_set")
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        fprint(self, "Running rule manually for previous data")
        click_on_actions_item(self, "auto_rule_save_result_set", "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        if Build_Version.__contains__("3."):
            verify_data_in_threatdata(self, save_result_set_old_domain, "Import")
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                        "/ancestor::tr/td[3]//span[contains(text(),'" + save_result_set_old_domain + "')]")
            sleep(2)
            _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '" + save_result_set_old_domain + "')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            fprint(self, "Clicking on Actions Taken")
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Action Taken')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Action Taken')]").click()
            waitfor(self, 20, By.XPATH, "//div[@id='tab-third_party']")
            self.driver.find_element_by_xpath("//div[@id='tab-ctix']").click()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), 'auto_rule_save_result_set')]")
            fprint(self, '[Passed] auto_rule_save_result_set rule name is visible under action taken.')
            disable_rule(self, "auto_rule_save_result_set")

    def test_24_create_rule_save_result_set_V3(self):
        """
        Testcase to verify action save result set V3
        """
        fprint(self, "TC_ID: 40112 verify rule save result set V3.")
        self.quick_create_intel("save_result_setV3_old_domain", "Domain", save_result_setV3_old_domain)
        _rule_name = "auto_rule_save_setV3"
        _rule_tag_to_save_result_setV3 = "savesetV3"
        add_tag(self, _rule_tag_to_save_result_setV3)
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_save_result_setV3(self, _rule_tag_to_save_result_setV3)
        add_condition_indicators(self, 'DOMAIN')
        waitfor(self, 10, By.XPATH, "//button[text()='Save']")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully", 15)
        fprint(self, "Clicked on Save- Rule Saved")
        nav_menu_main(self, "Dashboards")
        self.quick_create_intel("save_result_set_new_domainV3", "Domain", save_result_setV3_new_domain)

    def test_25_verify_rule_save_result_set_V3_new_feed(self):
        """
            Testcase to validate save result set V3 action on new feed
        """
        fprint(self, "TC_ID: 40113 - verify save result set V3 on new data")
        nav_menu_main(self, 'Threat Data')
        if Build_Version.__contains__("3."):
            verify_data_in_threatdata(self, save_result_setV3_new_domain, "Import")
            waitfor(self, 5, By.XPATH, "//span[contains(text(),'Import')]"
                                       "/ancestor::tr/td[3]//span[contains(text(),'" + save_result_setV3_new_domain + "')]")
            sleep(2)
            _ele = \
                self.driver.find_elements_by_xpath(
                    "//span[contains(text(), '" + save_result_setV3_new_domain + "')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            fprint(self, 'Checking under Action Taken for rule name')
            fprint(self, "Clicking on Actions Taken")
            waitfor(self, 5, By.XPATH, "//div[contains(text(), 'Action Taken')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Action Taken')]").click()
            waitfor(self, 5, By.XPATH, "//div[@id='tab-third_party']")
            self.driver.find_element_by_xpath("//div[@id='tab-ctix']").click()
            waitfor(self, 5, By.XPATH, "//span[contains(text(), 'auto_rule_save_setV3')]")
            fprint(self, '[Passed] auto_rule_save_setV3 rule name is visible under action taken.')

    def test_26_verify_update_save_result_set_V3_old_feed(self):
        """
            Testcase to validate save result set V3 action on old feed
        """
        fprint(self, "TC_ID: 40114 - verify save result set V3 on preexisting data")
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        self.driver.find_element_by_xpath(rules_main_search).send_keys("auto_rule_save_setV3")
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        fprint(self, "Running rule manually for previous data")
        click_on_actions_item(self, "auto_rule_save_setV3", "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        if Build_Version.__contains__("3."):
            verify_data_in_threatdata(self, save_result_setV3_old_domain, "Import")
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                        "/ancestor::tr/td[3]//span[contains(text(),'" + save_result_setV3_old_domain + "')]")
            _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '" + save_result_setV3_old_domain + "')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            fprint(self, "Clicking on Actions Taken")
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Action Taken')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Action Taken')]").click()
            waitfor(self, 20, By.XPATH, "//div[@id='tab-third_party']")
            self.driver.find_element_by_xpath("//div[@id='tab-ctix']").click()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), 'auto_rule_save_setV3')]")
            fprint(self, '[Passed] auto_rule_save_setV3 rule name is visible under action taken.')
            disable_rule(self,"auto_rule_save_setV3")

    def test_27_update_tag_for_threat_actor(self):
        """
        Validate if update tag action is working for intent type: Threat Actors
        """
        fprint(self, "TC_ID: 40122 - verify_rule_update_tag for intent type: Threat Actor")
        _rule_name = "auto_rule_update_tag_threat_actor"
        add_tag(self, rule_tag)
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        if Build_Version.__contains__("3."):
            add_action_update_tag(self, tagname=rule_tag)
            add_condition_domain_objects(self, 'Threat Actor')
        else:
            add_action_update_tag(self, tagname=rule_tag)
            add_condition_title(self, value=rule_ip_pattern)
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        quick_add_domain_object(self, 'Threat Actor', 'TA:00:00:00', threat_actor)

    def test_28_verify_update_tag_threat_actor_new_feed(self):
        """
        Testing auto update tag on newly received tags
        """
        fprint(self, "TC_ID: 40123 - verify update tag via rules on auto run")
        nav_menu_main(self, 'Threat Data')
        if Build_Version.__contains__("3."):
            verify_data_in_threatdata(self, threat_actor, "Import")
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                        "/ancestor::tr/td[3]//span[contains(text(), '" + threat_actor + "')]")
            _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '" + threat_actor + "')]//ancestor::tr")[
                1]
            ActionChains(self.driver).click(_ele).perform()
            fprint(self, "Clicking on basic details")
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
            validate_tag(self, rule_tag)
        else:
            sleep(2)
            waitfor(self, 20, By.XPATH, "//div[div/div/span[contains(text(), '" + threat_actor + "')]]")
            self.driver.find_element_by_xpath("//div[div/div/span[contains(text(), '" + threat_actor + "')]]").click()
            validate_tag(self, rule_tag)

    def test_29_update_tag_for_course_of_action(self):
        """
        Validate if update tag action is working for intent type: COA
        """
        fprint(self, "TC_ID: 40124 - verify_rule_update_tag for intent type: COA")
        _rule_name = "auto_rule_update_tag_coa"
        add_tag(self, rule_tag)
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_update_tag(self, tagname=rule_tag)
        add_condition_domain_objects(self, 'Course Of Action')
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        quick_add_domain_object(self, 'Course of Action',"coa_value", coa_value)


    def test_30_verify_update_tag_course_of_action_new_feed(self):
        """
        Testing auto update tag on newly received tags : Course of action
        """
        fprint(self, "TC_ID: 40125 - verify update tag via rules on auto run")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, coa_value, "Import")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]/ancestor::tr/td[3]//span[contains(text(),'"+coa_value+"')]")
        _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '"+coa_value+"')]//ancestor::tr")[1]
        ActionChains(self.driver).click(_ele).perform()
        fprint(self, "Clicking on basic details")
        waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
        self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
        validate_tag(self, rule_tag)

    def test_31_update_tag_for_campaign(self):
        """
        Validate if update tag action is working for intent type: Campaign
        """
        fprint(self, "TC_ID: 40126 - verify_rule_update_tag for intent type: Campaign")
        _rule_name = "auto_rule_update_tag_campaign"
        add_tag(self, rule_tag)
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_update_tag(self, tagname=rule_tag)
        add_condition_domain_objects(self, 'Campaign')
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        quick_add_domain_object(self, 'Campaign', 'campaign_value', campaign_value)

    def test_32_verify_update_tag_campaign_new_feed(self):
        """
        Testing auto update tag on newly received tags : Campaign
        """
        fprint(self, "TC_ID: 40127 - verify update tag via rules on auto run")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, campaign_value, "Import")
        waitfor(self, 20, By.XPATH,"//span[contains(text(),'Import')]/ancestor::tr/td[3]//span[contains(text(),'" + campaign_value + "')]")
        _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '" + campaign_value + "')]//ancestor::tr")[1]
        ActionChains(self.driver).click(_ele).perform()
        fprint(self, "Clicking on basic details")
        waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
        self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
        validate_tag(self, rule_tag)

    def test_33_update_tag_for_intrusion_set(self):
        """
        Validate if update tag action is working for intent type: Intrusion Set
        """
        fprint(self, "TC_ID: 40128 - verify_rule_update_tag for intent type: Intrusion set")
        _rule_name = "auto_rule_update_tag_intrusionSet"
        add_tag(self, rule_tag)
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_update_tag(self, tagname=rule_tag)
        add_condition_domain_objects(self, 'Intrusion Set')
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        quick_add_domain_object(self, 'Intrusion Set', 'intrusion_set_value', intrusion_set_value)

    def test_34_verify_update_tag_intrusion_set(self):
        """
        Testing auto update tag on newly received tags : Intrusion set
        """
        fprint(self, "TC_ID: 40129 - verify update tag via rules on auto run")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, intrusion_set_value, "Import")
        waitfor(self, 20, By.XPATH,"//span[contains(text(),'Import')]/ancestor::tr/td[3]//span[contains(text(),'" + intrusion_set_value + "')]")
        _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '" + intrusion_set_value + "')]//ancestor::tr")[1]
        ActionChains(self.driver).click(_ele).perform()
        fprint(self, "Clicking on basic details")
        waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
        self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
        validate_tag(self, rule_tag)

    def test_35_update_tag_for_malware(self):
        """
        Validate if update tag action is working for intent type: Malware
        """
        fprint(self, "TC_ID: 40130 - verify_rule_update_tag for intent type: Malware")
        _rule_name = "auto_rule_update_tag_Malware"
        add_tag(self, rule_tag)
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_update_tag(self, tagname=rule_tag)
        add_condition_domain_objects(self, 'Malware')
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        quick_add_domain_object(self, 'Malware', 'malware_value', malware_value)

    def test_36_verify_update_tag_malware(self):
        """
        Testing auto update tag on newly received tags : Malware
        """
        fprint(self, "TC_ID: 40131 - verify update tag via rules on auto run")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, malware_value, "Import")
        waitfor(self, 20, By.XPATH,"//span[contains(text(),'Import')]/ancestor::tr/td[3]//span[contains(text(),'" + malware_value + "')]")
        sleep(2)
        _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '" + malware_value + "')]//ancestor::tr")[1]
        ActionChains(self.driver).click(_ele).perform()
        fprint(self, "Clicking on basic details")
        waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
        self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
        validate_tag(self, rule_tag)

    def test_37_update_tag_for_tool(self):
        """
        Validate if update tag action is working for intent type: tool
        """
        fprint(self, "TC_ID: 40132 - verify_rule_update_tag for intent type: tool")
        _rule_name = "auto_rule_update_tag_tool"
        add_tag(self, rule_tag)
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_update_tag(self, tagname=rule_tag)
        add_condition_domain_objects(self, 'Tool')
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        quick_add_domain_object(self, 'Tool', 'tool_value', tool_value)

    def test_38_verify_update_tag_tool(self):
        """
        Testing auto update tag on newly received tags : tool
        """
        fprint(self, "TC_ID: 40133 - verify update tag via rules on auto run")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, tool_value, "Import")
        waitfor(self, 20, By.XPATH,"//span[contains(text(),'Import')]/ancestor::tr/td[3]//span[contains(text(),'" + tool_value + "')]")
        _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '" + tool_value + "')]//ancestor::tr")[1]
        ActionChains(self.driver).click(_ele).perform()
        fprint(self, "Clicking on basic details")
        waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
        self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
        validate_tag(self, rule_tag)

    def test_39_update_tag_for_vulnerability(self):
        """
        Validate if update tag action is working for intent type: vulnerability
        """
        fprint(self, "TC_ID: 40134 - verify_rule_update_tag for intent type: vulnerability")
        _rule_name = "auto_rule_update_tag_vulnerability"
        add_tag(self, rule_tag)
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_update_tag(self, tagname=rule_tag)
        add_condition_domain_objects(self, 'Vulnerability')
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        quick_add_domain_object(self, 'Vulnerability', 'vulnerability_value', vulnerability_value)

    def test_40_verify_update_vulnerability(self):
        """
        Testing auto update tag on newly received tags : vulnerability
        """
        fprint(self, "TC_ID: 40135 - verify update tag via rules on auto run")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, vulnerability_value, "Import")
        waitfor(self, 20, By.XPATH,"//span[contains(text(),'Import')]/ancestor::tr/td[3]//span[contains(text(),'" + vulnerability_value + "')]")
        _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '" + vulnerability_value + "')]//ancestor::tr")[1]
        ActionChains(self.driver).click(_ele).perform()
        fprint(self, "Clicking on basic details")
        waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
        self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
        validate_tag(self, rule_tag)

    def test_41_update_tag_for_attack_pattern(self):
        """
        Validate if update tag action is working for intent type: attack_pattern
        """
        fprint(self, "TC_ID: 40136 - verify_rule_update_tag for intent type: attack_pattern")
        _rule_name = "auto_rule_update_tag_attack_pattern"
        add_tag(self, rule_tag)
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_update_tag(self, tagname=rule_tag)
        add_condition_domain_objects(self, 'Attack-Pattern')
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        quick_add_domain_object(self, 'Attack Pattern', 'attack_pattern_value', attack_pattern_value)

    def test_42_verify_update_tag_attack_pattern(self):
        """
        Testing auto update tag on newly received tags : attack_pattern
        """
        fprint(self, "TC_ID: 40137 - verify update tag via rules on auto run")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, attack_pattern_value, "Import")
        waitfor(self, 20, By.XPATH,"//span[contains(text(),'Import')]/ancestor::tr/td[3]//span[contains(text(),'" + attack_pattern_value + "')]")
        _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '" + attack_pattern_value + "')]//ancestor::tr")[1]
        ActionChains(self.driver).click(_ele).perform()
        fprint(self, "Clicking on basic details")
        waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
        self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
        validate_tag(self, rule_tag)

    def test_43_update_tag_for_identity(self):
        """
        Validate if update tag action is working for intent type: identity
        """
        fprint(self, "TC_ID: 40138 - verify_rule_update_tag for intent type: identity")
        _rule_name = "auto_rule_update_tag_identity"
        add_tag(self, rule_tag)
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_update_tag(self, tagname=rule_tag)
        add_condition_domain_objects(self, 'Identity')
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        quick_add_domain_object(self, 'Identity', 'identity_value', identity_value)

    def test_44_verify_update_tag_identity(self):
        """
        Testing auto update tag on newly received tags : identity
        """
        fprint(self, "TC_ID: 40139 - verify update tag via rules on auto run")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, identity_value, "Import")
        waitfor(self, 20, By.XPATH,"//span[contains(text(),'Import')]/ancestor::tr/td[3]//span[contains(text(),'" + identity_value + "')]")
        _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '" + identity_value + "')]//ancestor::tr")[1]
        ActionChains(self.driver).click(_ele).perform()
        fprint(self, "Clicking on basic details")
        waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
        self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
        validate_tag(self, rule_tag)

    def test_45_update_tag_for_location(self):
        """
        Validate if update tag action is working for intent type: location
        """
        fprint(self, "TC_ID: 40140 - verify_rule_update_tag for intent type: location")
        _rule_name = "auto_rule_update_tag_location"
        add_tag(self, rule_tag)
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_update_tag(self, tagname=rule_tag)
        add_condition_domain_objects(self, 'Location')
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        quick_add_domain_object(self, 'Location', 'location_value', location_value)

    def test_46_verify_update_tag_location(self):
        """
        Testing auto update tag on newly received tags : location
        """
        fprint(self, "TC_ID: 40141 - verify update tag via rules on auto run")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, location_value, "Import")
        waitfor(self, 20, By.XPATH,"//span[contains(text(),'Import')]/ancestor::tr/td[3]//span[contains(text(),'" + location_value + "')]")
        _ele = self.driver.find_elements_by_xpath("//span[contains(text(),'Import')]/ancestor::tr/td[3]//span[contains(text(),'" + location_value + "')]")[1]
        ActionChains(self.driver).click(_ele).perform()
        fprint(self, "Clicking on basic details")
        waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
        self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
        validate_tag(self, rule_tag)

    def test_47_update_tag_for_infrastructure(self):
        """
        Validate if update tag action is working for intent type: Infrastructure
        """
        fprint(self, "TC_ID: 40142 - verify_rule_update_tag for intent type: Infrastructure")
        _rule_name = "auto_rule_update_tag_Infrastructure"
        add_tag(self, rule_tag)
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_update_tag(self, tagname=rule_tag)
        add_condition_domain_objects(self, 'Infrastructure')
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        quick_add_domain_object(self, 'Infrastructure', 'infra_value', infra_value)

    def test_48_verify_update_tag_infrastructure(self):
        """
        Testing auto update tag on newly received tags : Infrastructure
        """
        fprint(self, "TC_ID: 40143 - verify update tag via rules on auto run")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, infra_value, "Import")
        waitfor(self, 20, By.XPATH,
                "//span[contains(text(),'Import')]/ancestor::tr/td[3]//span[contains(text(),'" + infra_value + "')]")
        _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '" + infra_value + "')]//ancestor::tr")[1]
        ActionChains(self.driver).click(_ele).perform()
        fprint(self, "Clicking on basic details")
        waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
        self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
        validate_tag(self, rule_tag)

    def test_49_create_rule_splunk_lookup_table(self):
        """
            Testcase to create a rule to Update lookup Table
        """
        fprint(self, "TC_ID: 61049 - Verify if rule to update Lookup table can be created")
        _rule_name = "auto_rule_splunk_lookup"
        quick_create_ip(self, update_splunk_lookup_old_ip, "splunk_lookup_old_ip")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_update_lookup_table(self, table_name=get_value("Splunk Lookup"))
        add_condition_title(self, value=splunk_ip_pattern)
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")

    def test_50_manual_run_update_lookup_table_verify_action_3rdparty(self):
        """
            Testcase to validate if rule for update lookup run successfully on old feed
        """
        fprint(self, "TC_ID: 61050 - verify old feeds run for lookup table")
        _rule_name = "auto_rule_splunk_lookup"
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        fprint(self, "Searching for a rule name")
        self.driver.find_element_by_xpath(rules_main_search).send_keys(_rule_name)
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        sleep(5)
        click_on_actions_item(self, _rule_name, "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, update_splunk_lookup_old_ip, "Import")
        self.validate_action_taken_third_party_rule(ioc=update_splunk_lookup_old_ip, rule_name=_rule_name)
        process_console_logs(self)

    def test_51_create_intel_for_auto_update_lookup_table_verify_action_3rdparty(self):
        """
            Testing if rule for auto execution of update lookup table is run successfully
        """
        fprint(self, "TC_ID - 61051 - verify if update lookup rule can be autorun")
        _rule_name = "auto_rule_splunk_lookup"
        quick_create_ip(self, update_splunk_lookup_new_ip, "splunk_lookup_new_ip")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, update_splunk_lookup_new_ip, "Import")
        self.validate_action_taken_third_party_rule(ioc=update_splunk_lookup_new_ip, rule_name=_rule_name)
        process_console_logs(self)

    def test_52_verify_splunk_lookup_table_old_feed(self):
        """
            Testcase to validate if manual data run upon lookup table is now added in splunk
        """
        fprint(self, "TC_ID - 61052 - verify if data is visible in splunk")
        main_driver = launch_splunk(self)
        try:
            fails = check_splunk_fields(self, tlp='RED', type='ipv4-addr',value=update_splunk_lookup_old_ip)
        finally:
            main_driver.quit()
        if len(fails):
            fprint(self, "Lookup table values not updated for")
        self.assert_(fails == [], str(fails))

    def test_53_verify_splunk_lookup_table_auto_feed(self):
        """
            Testcase to validate if auto data run upon lookup table is now added in splunk
        """
        fprint(self, "TC_ID - 61053 - verify if data is visible in splunk")
        main_driver = launch_splunk(self)
        try:
            fails = check_splunk_fields(self, tlp='RED', type='ipv4-addr',value=update_splunk_lookup_new_ip)
        finally:
            main_driver.quit()
        if len(fails):
            fprint(self, "Lookup table values not updated for")
        self.assert_(fails == [], str(fails))

    def test_54_publishing_add_publishToCollection_rule_Ip(self):
        """
        Testcase to verify action Publish to collection for intent type : IP
        """
        fprint(self, "TC_ID: 41054 verify rule PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_IP"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        # add_condition_indicators(self, 'IP')
        add_action_publish_collection(self)
        add_condition_title(self, publish_ip)
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self, _rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : "+_rule_name+" visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        create_intel(self, 'IP', "publish_ip", publish_ip)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_55_publishing_add_publishToCollection_rule_Url(self):
        """
        Testcase to verify action Publish to collection for intent type : URL
        """
        fprint(self, "TC_ID: 41055 verify rule PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_url"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_indicators(self, 'URL')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self,_rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : "+_rule_name+" visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        create_intel(self, 'URL', 'publish_url', publish_url)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_56_publishing_add_publishToCollection_rule_Md5(self):
        """
        Testcase to verify action Publish to collection for intent type : MD5
        """
        fprint(self, "TC_ID: 41056 verify rule PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_MD5"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_indicators(self, 'MD5')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self,_rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : "+_rule_name+" visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        create_intel(self, 'MD5', 'publish_md5', publish_md5)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_57_publishing_add_publishToCollection_rule_SHA224(self):
        """
        Testcase to verify action Publish to collection for intent type : SHA224
        """
        fprint(self, "TC_ID: 41057 verify rule PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_sha224"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_indicators(self, 'SHA224')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self, _rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : "+_rule_name+" visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        create_intel(self, 'SHA224', 'publish_sha224', publish_sha224)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_58_publishing_add_publishToCollection_rule_SHA256(self):
        """
        Testcase to verify action Publish to collection for intent type : SHA256
        """
        fprint(self, "TC_ID: 41058 verify rule PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_sha256"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_indicators(self, 'SHA256')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self, _rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : "+_rule_name+" visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        create_intel(self, 'SHA256', 'publish_sha256', publish_sha256)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_59_publishing_add_publishToCollection_rule_SHA384(self):
        """
        Testcase to verify action Publish to collection for intent type : SHA384
        """
        fprint(self, "TC_ID: 41059 verify rule PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_sha384"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_indicators(self, 'SHA384')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self, _rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : "+_rule_name+" visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        create_intel(self, 'SHA384', 'publish_sha384', publish_sha384)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_60_publishing_add_publishToCollection_rule_SHA512(self):
        """
        Testcase to verify action Publish to collection for intent type : SHA512
        """
        fprint(self, "TC_ID: 41060 verify rule PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_sha512"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_indicators(self, 'SHA512')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self, _rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : "+_rule_name+" visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        create_intel(self, 'SHA512', 'publish_sha512', publish_sha512)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_61_publishing_add_publishToCollection_rule_SSDEEP(self):
        """
        Testcase to verify action Publish to collection for intent type : SSDEEP
        """
        fprint(self, "TC_ID: 41061 verify rule PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_SSDEEP"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_indicators(self, 'SSDEEP')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self, _rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : "+_rule_name+" visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        create_intel(self, 'SSDEEP', 'publish_SSDEEP', publish_ssdeep)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_62_publishing_add_publishToCollection_rule_Threat_Actor(self):
        """
        Testcase to verify action Publish to collection for intent type : Threat Actor
        """
        fprint(self, "TC_ID: 41062 verify rule PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_threat_actor"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_domain_objects(self, "Threat Actor")
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self,_rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : "+_rule_name+" visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        self.create_domain_object("Threat Actor", "title_ta", threat_actor)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_63_publishing_add_publishToCollection_rule_COA(self):
        """
        Testcase to verify action Publish to collection for intent type : Course Of Action
        """
        fprint(self, "TC_ID: 41063 verify rule PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_COA"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_domain_objects(self, 'Course Of Action')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self,_rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : "+_rule_name+" visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        self.create_domain_object("Course of Action", "title_coa", coa)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_64_publishing_add_publishToCollection_rule_Campaign(self):
        """
        Testcase to verify action Publish to collection for intent type : Campaign
        """
        fprint(self, "TC_ID: 41064 verify rule PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_Campaign"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_domain_objects(self, 'Campaign')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self,_rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : "+_rule_name+" visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        self.create_domain_object("Campaign", "title_campaign", campaign)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_65_publishing_add_publishToCollection_rule_Intrusion_set(self):
        """
        Testcase to verify action Publish to collection for intent type : Intrusion_set
        """
        fprint(self, "TC_ID: 41065 verify rule PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_intrusion_set"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_domain_objects(self, 'Intrusion Set')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self,_rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : "+_rule_name+" visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        self.create_domain_object("Intrusion Set", "title_intrusion_set", intrusion_set)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_66_publishing_add_publishToCollection_rule_Malware(self):
        """
        Testcase to verify action Publish to collection for intent type : Malware
        """
        fprint(self, "TC_ID: 41066 verify rule PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_malware"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_domain_objects(self, 'Malware')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self,_rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : " + _rule_name + " visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        self.create_domain_object("Malware", "title_malware", malware)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_67_publishing_add_publishToCollection_rule_Tool(self):
        """
        Testcase to verify action Publish to collection for intent type : Tool
        """
        fprint(self, "TC_ID: 41067 verify PUBLISH TO COLLECTION")
        _rule_name = "auto_rule_publish_tool"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_domain_objects(self, 'Tool')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self,_rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : " + _rule_name + " visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        self.create_domain_object("Tool", "title_tool", tool)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_68_publishing_add_publishToCollection_rule_Attack_Pattern(self):
        """
        Testcase to verify action Publish to collection for intent type : Attack_Pattern
        """
        fprint(self, "TC_ID: 41068 verify PUBLISH TO COLLECTION")
        _rule_name = "auto_rule_publish_attack_pattern"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_domain_objects(self, 'Attack-Pattern')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self,_rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : " + _rule_name + " visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        self.create_domain_object("Attack Pattern", "title_AP", attack_pattern)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_69_publishing_add_publishToCollection_rule_Identity(self):
        """
        Testcase to verify action Publish to collection for intent type : Identity
        """
        fprint(self, "TC_ID: 41069 verify PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_identity"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_domain_objects(self, 'Identity')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self,_rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : " + _rule_name + " visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        self.create_domain_object("Identity", "title_identity", identity)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_70_publishing_add_publishToCollection_rule_Location(self):
        """
        Testcase to verify action Publish to collection for intent type : Location
        """
        fprint(self, "TC_ID: 41070 PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_location"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_domain_objects(self, 'Location')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self,_rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : " + _rule_name + " visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        self.create_domain_object("Location", "title_location", location)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_71_publishing_add_publishToCollection_rule_Infrastructure(self):
        """
        Testcase to verify action Publish to collection for intent type : Infrastructure
        """
        fprint(self, "TC_ID: 41071 verify PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_infrastructure"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_domain_objects(self, 'Infrastructure')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self,_rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : " + _rule_name + " visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        self.create_domain_object("Infrastructure", "title_infra", infra)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_72_publishing_add_publishToCollection_rule_Report(self):
        """
        Testcase to verify action Publish to collection for intent type : Report
        """
        fprint(self, "TC_ID: 40172 verify PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_report"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_domain_objects(self, 'Report')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self,_rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+_rule_name+"')]")
        fprint(self, "Rule name : " + _rule_name + " visible.")
        nav_menu_main(self, "Threat Data")
        create_intel(self, 'URL', 'publish_report', publish_report)
        fprint(self, "[PASSED] Rule: "+_rule_name+" created succesfully.")

    def test_83_publishing_add_publishToCollection_rule_Vulnerability(self):
        """
        Testcase to verify action Publish to collection for intent type : Vulnerability
        """
        fprint(self, "TC_ID: 41083 verify rule PUBLISH TO COLLECTION.")
        _rule_name = "auto_rule_publish_vulnerability"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_publish_collection(self)
        add_condition_domain_objects(self, 'Vulnerability')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        search(self, _rule_name)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'" + _rule_name + "')]")
        fprint(self, "Rule name : " + _rule_name + " visible.")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        self.create_domain_object("Vulnerability", "title_vulnerability", vulnerability)
        fprint(self, "[PASSED] Rule: " + _rule_name + " created succesfully.")

    def test_73_create_rule_cortex_trigger_playbook(self):
        """
            Testcase for creating a rule to Trigger Playbook action on CORTEX SOAR
        """
        _ip = generate_random_ip()
        set_value("cortex_playbook_ip", _ip[0:int(_ip.rfind('.'))])
        cortex_pattern = get_value("cortex_playbook_ip")
        fprint(self, "TC_ID - 61073 - verify if trigger playbook rule is created successfully")
        _rule_name = "auto_rule_cortex_playbook"
        quick_create_ip(self, cortex_pattern+".1", "cortex_playbook_old_ip")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_cortex_trigger_playbook(self)
        add_condition_title(self, value=cortex_pattern)
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")

    def test_74_manual_run_cortex_playbook_action_3rdparty(self):
        """
            Testcase to run Trigger Playbook Action on CORTEX-XSOAR
        """
        fprint(self, "TC_ID: 61074 - verify old feeds run for trigger playbook")
        cortex_pattern = get_value("cortex_playbook_ip")
        _rule_name = "auto_rule_cortex_playbook"
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        fprint(self, "Searching for a rule name")
        self.driver.find_element_by_xpath(rules_main_search).send_keys(_rule_name)
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        sleep(5)
        click_on_actions_item(self, _rule_name, "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, cortex_pattern+".1", "Import")
        self.validate_action_taken_third_party_rule(ioc=cortex_pattern+".1", rule_name=_rule_name)
        process_console_logs(self)

    def test_75_create_intel_for_auto_cortex_trigger_playbook_verify_action_3rdparty(self):
        """
            Testing if rule for auto execution of update lookup table is run successfully
        """
        fprint(self, "TC_ID - 61075 - verify if cortex trigger playbook rule can be autorun")
        cortex_pattern = get_value("cortex_playbook_ip")
        _rule_name = "auto_rule_cortex_playbook"
        quick_create_ip(self, cortex_pattern+".2", "cortex_playbook_new_ip")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, cortex_pattern+".2", "Import")
        self.validate_action_taken_third_party_rule(ioc=cortex_pattern+".2", rule_name=_rule_name)
        process_console_logs(self)

    def test_76_verify_trigger_playbook_old_ip(self):
        """
            Testcase to validate if intel is visible in CORTEX-XSOAR
        """
        fprint(self, "TC_ID - 61076 - verify if IOC entry is now present in CORTEX-XSOAR")
        cortex_pattern = get_value("cortex_playbook_ip")
        launch_cortex_soar(self)
        cortex_search_and_delete(self, cortex_intel=cortex_pattern+".1")

    def test_77_verify_trigger_playbook_new_ip(self):
        """
            Testcase to validate if intel is visible in CORTEX-XSOAR
        """
        fprint(self, "TC_ID - 61077 - verify if IOC entry is now present in CORTEX-XSOAR")
        cortex_pattern = get_value("cortex_playbook_ip")
        launch_cortex_soar(self)
        cortex_search_and_delete(self, cortex_intel=cortex_pattern+".2")

    def test_78_create_rule_cortex_trigger_playbook_v3(self):
        """
            Testcase for creating a rule to Trigger Playbook V3 action on CORTEX SOAR
        """
        fprint(self, "TC_ID - 61078 - verify if trigger playbook v3 rule is created successfully")
        _ip = generate_random_ip()
        set_value("cortex_v3_playbook_ip", _ip[0:int(_ip.rfind('.'))])
        cortex_v3_pattern = get_value("cortex_v3_playbook_ip")
        _rule_name = "auto_rule_cortex_playbook_v3"
        quick_create_ip(self, cortex_v3_pattern+".1", "cortex_playbook_v3_old_ip")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_cortex_trigger_playbook(self, v3=True)
        add_condition_title(self, value=cortex_v3_pattern)
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")

    def test_79_manual_run_cortex_playbook_v3_action_3rdparty(self):
        """
            Testcase to run Trigger Playbook V3 Action on CORTEX-XSOAR
        """
        fprint(self, "TC_ID: 61079 - verify old feeds run for trigger playbook v3")
        cortex_v3_pattern = get_value("cortex_v3_playbook_ip")
        _rule_name = "auto_rule_cortex_playbook_v3"
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        fprint(self, "Searching for a rule name")
        self.driver.find_element_by_xpath(rules_main_search).send_keys(_rule_name)
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        sleep(5)
        click_on_actions_item(self, _rule_name, "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, cortex_v3_pattern+".1", "Import")
        self.validate_action_taken_third_party_rule(ioc=cortex_v3_pattern+".1", rule_name=_rule_name)
        process_console_logs(self)

    def test_80_create_intel_for_auto_cortex_trigger_playbook_v3_verify_action_3rdparty(self):
        """
            Testing if rule for auto execution of update lookup table is run successfully
        """
        fprint(self, "TC_ID - 61080 - verify if cortex trigger playbook rule can be autorun")
        cortex_v3_pattern = get_value("cortex_v3_playbook_ip")
        _rule_name = "auto_rule_cortex_playbook_v3"
        quick_create_ip(self, cortex_v3_pattern+".2", "cortex_playbook_v3_new_ip")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, cortex_v3_pattern+".2", "Import")
        self.validate_action_taken_third_party_rule(ioc=cortex_v3_pattern+".2", rule_name=_rule_name)
        process_console_logs(self)

    def test_81_verify_trigger_playbook_v3_old_ip(self):
        """
            Testcase to validate if intel is visible in CORTEX-XSOAR
        """
        fprint(self, "TC_ID - 61081 - verify if IOC entry is now present in CORTEX-XSOAR")
        cortex_v3_pattern = get_value("cortex_v3_playbook_ip")
        launch_cortex_soar(self)
        cortex_search_and_delete(self, cortex_intel=cortex_v3_pattern+".1")

    def test_82_verify_trigger_playbook_v3_new_ip(self):
        """
            Testcase to validate if intel is visible in CORTEX-XSOAR
        """
        fprint(self, "TC_ID - 61082 - verify if IOC entry is now present in CORTEX-XSOAR")
        cortex_v3_pattern = get_value("cortex_v3_playbook_ip")
        launch_cortex_soar(self)
        cortex_search_and_delete(self, cortex_intel=cortex_v3_pattern+".2")

    def test_83_create_rule_zscaler_update_whitelist(self):
        """
            Testcase to validate if intel can be whitelisted in ZScaler
        """
        fprint(self, "TC_ID - 61083 - verify if rule to update whitelist in ZScaler can be created")
        set_value("zscaler_old_whitelist", zscaler_whitelist_url_pattern.format(uniquestr[-4:]))
        _rule_name = 'rule_zscaler_whitelist'
        create_intel(self, "URL", "zsc_old_white", get_value("zscaler_old_whitelist"))
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_zscaler(self, action="whitelist")
        add_condition_title(self, value="demae")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")

    def test_84_manual_run_zscaler_whitelist_verify_3rd_party(self):
        """
            Testcase to run Update Whitelist in Zscaler on old feed
        """
        fprint(self, "TC_ID: 61084 - verify old feeds run for update whhitelist Zscaler")
        _rule_name = "rule_zscaler_whitelist"
        _old_feed = get_value("zscaler_old_whitelist")
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        fprint(self, "Searching for a rule name")
        self.driver.find_element_by_xpath(rules_main_search).send_keys(_rule_name)
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        sleep(5)
        click_on_actions_item(self, _rule_name, "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, _old_feed, "Import")
        self.validate_action_taken_third_party_rule(ioc=_old_feed, rule_name=_rule_name)
        process_console_logs(self)

    def test_85_auto_run_zscaler_whitelist_verify_3rd_party(self):
        """
            Testcase to autorun Update Whitelist Zscaler rule on feeds
        """
        fprint(self, "TC_ID - 61085 - verify if Update Whitelist Zscaler rule can be autorun")
        set_value("zscaler_new_whitelist", zscaler_whitelist_url_pattern.format(uniquestr[-4:]))
        _rule_name = "rule_zscaler_whitelist"
        create_intel(self, "URL", "zsc_new_white", get_value("zscaler_new_whitelist"))
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, get_value("zscaler_new_whitelist"), "Import")
        self.validate_action_taken_third_party_rule(ioc=get_value("zscaler_new_whitelist"), rule_name=_rule_name)
        process_console_logs(self)

    def test_86_verify_zscaler_whitelist_old_feed(self):
        """
            Testcase to verify if old feed run by rule is added into Zscaler
        """
        fprint(self, "TC_ID - 61086 - verify if old feed is whitelisted in ZScaler")
        _intel = get_value("zscaler_old_whitelist")[8:]
        launch_zscaler(self)
        self.driver.find_element_by_xpath("//div[@data-item='policy']").click()
        waitfor(self, 20, By.XPATH, "//li[span[text()='Advanced Threat Protection']]")
        fprint(self, "Clicking on Advanced Threat Protection")
        self.driver.find_element_by_xpath("//li[span[text()='Advanced Threat Protection']]").click()
        waitfor(self, 20, By.XPATH, "//div[@class='page-title ']/span[text()='Advanced Threat Protection']")
        sleep(5)    #required
        fprint(self, "Clicking on Security Exceptions")
        self.driver.find_element_by_xpath("//li[span[text()='Security Exceptions']]").click()
        table_ele = self.driver.find_element_by_xpath("//div[@data-help-property='bypassUrls']/following-sibling::span")
        waitfor(self, 20, By.XPATH,
                "//div[@data-help-property='bypassUrls']/following-sibling::span//"
                "input[@class='search-input-text']")
        fprint(self, "Searching for "+_intel)
        table_ele.find_element_by_xpath(".//input[@class='search-input-text']").send_keys(_intel)
        table_ele.find_element_by_xpath(".//span[contains(@class,'search-icon')]").click()
        waitfor(self, 20, By.XPATH, "//div[contains(text(), '"+_intel+"')]")
        fprint(self, _intel +" is successfully added to Zscaler whitelist")
        fprint(self, "Deleting "+_intel+" from Zscaler")
        sleep(5)    # required
        table_ele.find_element_by_xpath(".//span[text()='Remove']").click()
        waitfor(self, 20, By.XPATH, "//div[@data-help-property='bypassUrls']/following-sibling::span//"
                                    "li[text()='Remove Page']")
        fprint(self, "Clicking on remove page")
        table_ele.find_element_by_xpath(".//li[@data-id='REMOVE_PAGE']").click()
        waitfor(self, 20, By.XPATH, "//span[text()='Confirmation: Remove Page']")
        sleep(2)    # required
        self.driver.find_element_by_xpath("//span[text()='Confirm']").click()
        if waitfor(self, 20, By.XPATH, "//div[text()='No matching items found']"):
            fprint(self, "Whitelisted entry "+_intel+" is deleted successfully")

    def test_87_verify_zscaler_whitelist_new_feed(self):
        """
            Testcase to verify if new feed run by rule is added into Zscaler
        """
        fprint(self, "TC_ID - 61087 - verify if old feed is whitelisted in ZScaler")
        _intel = get_value("zscaler_new_whitelist")[8:]
        launch_zscaler(self)
        self.driver.find_element_by_xpath("//div[@data-item='policy']").click()
        waitfor(self, 20, By.XPATH, "//li[span[text()='Advanced Threat Protection']]")
        fprint(self, "Clicking on Advanced Threat Protection")
        self.driver.find_element_by_xpath("//li[span[text()='Advanced Threat Protection']]").click()
        waitfor(self, 20, By.XPATH, "//div[@class='page-title ']/span[text()='Advanced Threat Protection']")
        sleep(5)    #required
        fprint(self, "Clicking on Security Exceptions")
        self.driver.find_element_by_xpath("//li[span[text()='Security Exceptions']]").click()
        table_ele = self.driver.find_element_by_xpath("//div[@data-help-property='bypassUrls']/following-sibling::span")
        waitfor(self, 20, By.XPATH,
                "//div[@data-help-property='bypassUrls']/following-sibling::span//"
                "input[@class='search-input-text']")
        fprint(self, "Searching for "+_intel)
        table_ele.find_element_by_xpath(".//input[@class='search-input-text']").send_keys(_intel)
        table_ele.find_element_by_xpath(".//span[contains(@class,'search-icon')]").click()
        waitfor(self, 20, By.XPATH, "//div[contains(text(), '"+_intel+"')]")
        fprint(self, _intel +" is successfully added to Zscaler whitelist")
        fprint(self, "Deleting "+_intel+" from Zscaler")
        sleep(5)    # required
        table_ele.find_element_by_xpath(".//span[text()='Remove']").click()
        waitfor(self, 20, By.XPATH, "//div[@data-help-property='bypassUrls']/following-sibling::span//"
                                    "li[text()='Remove Page']")
        fprint(self, "Clicking on remove page")
        table_ele.find_element_by_xpath(".//li[@data-id='REMOVE_PAGE']").click()
        waitfor(self, 20, By.XPATH, "//span[text()='Confirmation: Remove Page']")
        sleep(2)    # required
        self.driver.find_element_by_xpath("//span[text()='Confirm']").click()
        if waitfor(self, 20, By.XPATH, "//div[text()='No matching items found']"):
            fprint(self, "Whitelisted entry "+_intel+" is deleted successfully")

    def test_88_create_rule_zscaler_update_blacklist(self):
        """
            Testcase to validate if intel can be blacklisted in ZScaler
        """
        fprint(self, "TC_ID - 61088 - verify if rule to update blacklist in ZScaler can be created")
        set_value("zscaler_old_blacklist", zscaler_blacklist_url_pattern.format(uniquestr[-4:]))
        _rule_name = 'rule_zscaler_blacklist'
        create_intel(self, "URL", "zsc_old_black", get_value("zscaler_old_blacklist"))
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_zscaler(self, action="blacklist")
        add_condition_title(self, value="fiverr")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")

    def test_89_manual_run_zscaler_blacklist_verify_3rd_party(self):
        """
            Testcase to run Update Blacklist in Zscaler on old feed
        """
        fprint(self, "TC_ID: 61089 - verify old feeds run for update blacklist Zscaler")
        _rule_name = "rule_zscaler_blacklist"
        _old_feed = get_value("zscaler_old_blacklist")
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        fprint(self, "Searching for a rule name")
        self.driver.find_element_by_xpath(rules_main_search).send_keys(_rule_name)
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        sleep(5)
        click_on_actions_item(self, _rule_name, "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, _old_feed, "Import")
        self.validate_action_taken_third_party_rule(ioc=_old_feed, rule_name=_rule_name)
        process_console_logs(self)

    def test_90_auto_run_zscaler_blacklist_verify_3rd_party(self):
        """
            Testcase to autorun Update Blacklist Zscaler rule on feeds
        """
        fprint(self, "TC_ID - 61090 - verify if update blacklist zscaler rule can be autorun")
        set_value("zscaler_new_blacklist", zscaler_blacklist_url_pattern.format(uniquestr[-4:]))
        _intel = get_value("zscaler_new_blacklist")
        _rule_name = "rule_zscaler_blacklist"
        create_intel(self, "URL", "zsc_new_black", _intel)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, _intel, "Import")
        self.validate_action_taken_third_party_rule(ioc=_intel, rule_name=_rule_name)
        process_console_logs(self)

    def test_91_verify_zscaler_blacklist_old_feed(self):
        """
            Testcase to verify if old feed run by rule is added into Zscaler
        """
        fprint(self, "TC_ID - 61091 - verify if old feed is blacklisted in ZScaler")
        _intel = get_value("zscaler_old_blacklist")[7:]
        launch_zscaler(self)
        self.driver.find_element_by_xpath("//div[@data-item='policy']").click()
        waitfor(self, 20, By.XPATH, "//li[span[text()='Advanced Threat Protection']]")
        fprint(self, "Clicking on advanced threat protection")
        self.driver.find_element_by_xpath("//li[span[text()='Advanced Threat Protection']]").click()
        waitfor(self, 20, By.XPATH, "//div[@class='page-title ']/span[text()='Advanced Threat Protection']")
        sleep(5)    # required
        fprint(self, "Clicking om Advanced Threats Policy")
        self.driver.find_element_by_xpath("//li[span[text()='Advanced Threats Policy']]").click()
        table_ele = self.driver.find_element_by_xpath("//div[@data-help-property='maliciousUrls']/following-sibling::span")
        waitfor(self, 20, By.XPATH,"//div[@data-help-property='maliciousUrls']/following-sibling::span//"
                "input[@class='search-input-text']")
        fprint(self, "Searching for "+_intel)
        table_ele.find_element_by_xpath(".//input[@class='search-input-text']").send_keys(_intel)
        table_ele.find_element_by_xpath(".//span[contains(@class,'search-icon')]").click()
        waitfor(self, 20, By.XPATH, "//div[contains(text(), '"+_intel+"')]")
        fprint(self, _intel + " is successfully added to Zscaler whitelist")
        fprint(self, "Deleting "+_intel+" from Zscaler")
        sleep(5)    # required
        self.driver.find_element_by_xpath("//div[text()='Fraud Protection']").click()
        table_ele.find_element_by_xpath(".//span[text()='Remove']").click()
        waitfor(self, 20, By.XPATH, "//div[@data-help-property='maliciousUrls']/following-sibling::span//"
                                    "li[text()='Remove Page']")
        fprint(self, "Clicking on remove page")
        table_ele.find_element_by_xpath(".//li[@data-id='REMOVE_PAGE']").click()
        waitfor(self, 20, By.XPATH, "//span[text()='Confirmation: Remove Page']")
        sleep(2)    # required
        self.driver.find_element_by_xpath("//span[text()='Confirm']").click()
        if waitfor(self, 20, By.XPATH, "//div[text()='No matching items found']"):
            fprint(self, "Whitelisted entry "+_intel+" is deleted successfully")

    def test_92_verify_zscaler_blacklist_new_feed(self):
        """
            Testcase to verify if new feed run by rule is added into Zscaler
        """
        fprint(self, "TC_ID - 61092 - verify if new feed is blacklisted in ZScaler")
        _intel = get_value("zscaler_new_blacklist")[7:]
        launch_zscaler(self)
        self.driver.find_element_by_xpath("//div[@data-item='policy']").click()
        waitfor(self, 20, By.XPATH, "//li[span[text()='Advanced Threat Protection']]")
        fprint(self, "Clicking on advanced threat protection")
        self.driver.find_element_by_xpath("//li[span[text()='Advanced Threat Protection']]").click()
        waitfor(self, 20, By.XPATH, "//div[@class='page-title ']/span[text()='Advanced Threat Protection']")
        sleep(5)    # required
        fprint(self, "Clicking om Advanced Threats Policy")
        self.driver.find_element_by_xpath("//li[span[text()='Advanced Threats Policy']]").click()
        table_ele = self.driver.find_element_by_xpath("//div[@data-help-property='maliciousUrls']/following-sibling::span")
        waitfor(self, 20, By.XPATH, "//div[@data-help-property='maliciousUrls']/following-sibling::span//"
                                    "input[@class='search-input-text']")
        fprint(self, "Searching for "+_intel)
        table_ele.find_element_by_xpath(".//input[@class='search-input-text']").send_keys(_intel)
        table_ele.find_element_by_xpath(".//span[contains(@class,'search-icon')]").click()
        waitfor(self, 20, By.XPATH, "//div[contains(text(), '"+_intel+"')]")
        fprint(self, _intel + " is successfully added to Zscaler whitelist")
        fprint(self, "Deleting "+_intel+" from Zscaler")
        sleep(5)    # required
        self.driver.find_element_by_xpath("//div[text()='Fraud Protection']").click()
        table_ele.find_element_by_xpath(".//span[text()='Remove']").click()
        waitfor(self, 20, By.XPATH, "//div[@data-help-property='maliciousUrls']/following-sibling::span//"
                                    "li[text()='Remove Page']")
        fprint(self, "Clicking on remove page")
        table_ele.find_element_by_xpath(".//li[@data-id='REMOVE_PAGE']").click()
        waitfor(self, 20, By.XPATH, "//span[text()='Confirmation: Remove Page']")
        sleep(2)    # required
        self.driver.find_element_by_xpath("//span[text()='Confirm']").click()
        if waitfor(self, 20, By.XPATH, "//div[text()='No matching items found']"):
            fprint(self, "Whitelisted entry "+_intel+" is deleted successfully")

    def test_93_create_rule_exabeam_update_context(self):
        """
            Testcase to create a rule to perform Update Context Table in EXABEAM
        """
        fprint(self, "TC_ID: 61093 - testcase for rule creation for update context table action")
        set_value("exa_context_old", exabeam_context_pattern+"."+str(random.randint(1, 124)))
        _intel = get_value("exa_context_old")
        _rule_name = 'rule_exabeam_context_table'
        quick_create_ip(self, _intel, "exa_content_old")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_exabeam(self)
        add_condition_title(self, value=exabeam_context_pattern)
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")

    def test_94_manual_run_exabeam_update_context_3rd_party(self):
        """
            Testcase to validate if rule run manually for update context table
        """
        fprint(self, "TC_ID: 61094 - Testing for manual rule run for update context table")
        _rule_name = 'rule_exabeam_context_table'
        _old_feed = get_value("exa_context_old")
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        fprint(self, "Searching for a rule name")
        self.driver.find_element_by_xpath(rules_main_search).send_keys(_rule_name)
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        sleep(5)
        click_on_actions_item(self, _rule_name, "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, _old_feed, "Import")
        self.validate_action_taken_third_party_rule(ioc=_old_feed, rule_name=_rule_name)
        process_console_logs(self)

    def test_95_auto_run_exabeam_update_context_3rd_party(self):
        """
            Testcase to autorun Update Context Table Exabeam on feeds
        """
        fprint(self, "TC_ID - 61095 - verify if update context exabeam rule can be autorun")
        set_value("exa_context_new", exabeam_context_pattern+"."+str(random.randint(125, 255)))
        _intel = get_value("exa_context_new")
        _rule_name = 'rule_exabeam_context_table'
        quick_create_ip(self, _intel, "exa_content_new")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, _intel, "Import")
        self.validate_action_taken_third_party_rule(ioc=_intel, rule_name=_rule_name)
        process_console_logs(self)

    def test_96_verify_context_table_manual_run(self):
        """
            Testcase to validate if intel from manual run is visible in Exabeam
        """
        fprint(self, "TC_ID: 61096 - validating if manual run intel is present in context table")
        _table_name = get_value("ex_context_table")
        _intel = get_value("exa_context_old")
        launch_exabeam(self)
        self.driver.find_element_by_xpath("//div[i[text()='search']]").click()
        waitfor(self, 20, By.XPATH, "//input[@placeholder='Search context tables']")
        sleep(2)    # needed
        fprint(self, "Searching for the created table name")
        self.driver.find_element_by_xpath("//input[@placeholder='Search context tables']").send_keys(_table_name)
        waitfor(self, 20, By.XPATH, "//span[text()='"+_table_name+"']")
        self.driver.find_element_by_xpath("//span[text()='"+_table_name+"']").click()
        if waitfor(self, 20, By.XPATH, "//div[text()='"+_intel+"']"):
            fprint(self, f"Intel {_intel} found in Context table ")
            waitfor(self, 20, By.XPATH, "//div[div[text()='"+_intel+"']]/div/label/span")
            self.driver.find_element_by_xpath("//div[div[text()='"+_intel+"']]/div/label/span").click()
            sleep(2)    # needed
            self.driver.find_element_by_xpath("//div[@id='remove_selected']/span/i[text()='delete']").click()
        waitfor(self, 20, By.XPATH, "//span[text()='DELETE']")
        self.driver.find_element_by_xpath("//span[text()='DELETE']").click()
        sleep(2)

    def test_97_verify_context_table_auto_run(self):
        """
            Testcase to validate if intel from auto run is visible in Exabeam
        """
        fprint(self, "TC_ID: 61097 - validating if auto run intel is present in context table")
        _table_name = get_value("ex_context_table")
        _intel = get_value("exa_context_new")
        launch_exabeam(self)
        self.driver.find_element_by_xpath("//div[i[text()='search']]").click()
        waitfor(self, 20, By.XPATH, "//input[@placeholder='Search context tables']")
        sleep(2)    # needed
        self.driver.find_element_by_xpath("//input[@placeholder='Search context tables']").send_keys(_table_name)
        fprint(self, "Clicking on the created context table")
        waitfor(self, 20, By.XPATH, "//span[text()='"+_table_name+"']")
        self.driver.find_element_by_xpath("//span[text()='"+_table_name+"']").click()
        if waitfor(self, 20, By.XPATH, "//div[text()='"+_intel+"']"):
            fprint(self, f"Intel {_intel} found in Context table ")
            waitfor(self, 20, By.XPATH, "//div[div[text()='"+_intel+"']]/div/label/span")
            self.driver.find_element_by_xpath("//div[div[text()='"+_intel+"']]/div/label/span").click()
            sleep(2)    # needed
            self.driver.find_element_by_xpath("//div[@id='remove_selected']/span/i[text()='delete']").click()
        waitfor(self, 20, By.XPATH, "//span[text()='DELETE']")
        self.driver.find_element_by_xpath("//span[text()='DELETE']").click()
        sleep(2)

    def test_98_create_rule_phantom_trigger_playbook(self):
        """
            Testcase to create rule to trigger playbook on splunk phantom
        """
        fprint(self, "TC_ID: 61098 - testcase to create rule for splunk phantom trigger playbook")
        _rule_name = "auto_rule_phantom_playbook"
        set_value("phantom_old_ip", phantom_playbook_pattern + "." + str(random.randint(1, 124)))
        _intel = get_value("phantom_old_ip")
        quick_create_ip(self, _intel, "phantom_playbook_old_ip")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_splunk_phantom(self)
        add_condition_title(self, value=phantom_playbook_pattern)
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")

    def test_99_manual_run_phantom_trigger_playbook(self):
        """
            Testcase to validate if rule run manually for phantom trigger playbook
        """
        fprint(self, "TC_ID: 61099 - Testing for manual rule run for phantom trigger playbook")
        _rule_name = 'auto_rule_phantom_playbook'
        _old_feed = get_value("phantom_old_ip")
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        fprint(self, "Searching for a rule name")
        self.driver.find_element_by_xpath(rules_main_search).send_keys(_rule_name)
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        sleep(5)
        click_on_actions_item(self, _rule_name, "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, _old_feed, "Import")
        self.validate_action_taken_third_party_rule(ioc=_old_feed, rule_name=_rule_name)
        process_console_logs(self)

    def test_100_auto_run_phantom_playbook(self):
        """
            Testcase to autorun Trigger Playbook Splunk Phantom on feeds
        """
        fprint(self, "TC_ID - 61100 - verify if trigger playbook phantom rule can be autorun")
        set_value("phantom_new_ip", phantom_playbook_pattern + "." + str(random.randint(125, 255)))
        _intel = get_value("phantom_new_ip")
        _rule_name = 'auto_rule_phantom_playbook'
        quick_create_ip(self, _intel, "phantom_new_ip")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, _intel, "Import")
        self.validate_action_taken_third_party_rule(ioc=_intel, rule_name=_rule_name)
        process_console_logs(self)

    def test_101_create_rule_phantom_trigger_playbook_v3(self):
        """
            Testcase to create rule to trigger playbook v3 on splunk phantom
        """
        fprint(self, "TC_ID: 61101 - testcase to create rule for splunk phantom trigger playbook v3")
        _rule_name = "auto_rule_phantom_playbook_v3"
        set_value("phantom_v3_old_ip", phantom_playbook_v3_pattern + "." + str(random.randint(1, 124)))
        _intel = get_value("phantom_v3_old_ip")
        quick_create_ip(self, _intel, "phantom_playbook_v3_old_ip")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_splunk_phantom(self)
        add_condition_title(self, value=phantom_playbook_v3_pattern)
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")

    def test_102_manual_run_phantom_trigger_playbook_v3(self):
        """
            Testcase to validate if rule run manually for phantom trigger playbook
        """
        fprint(self, "TC_ID: 61102 - Testing for manual rule run for phantom trigger playbook")
        _rule_name = 'auto_rule_phantom_playbook_v3'
        _old_feed = get_value("phantom_v3_old_ip")
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        fprint(self, "Searching for a rule name")
        self.driver.find_element_by_xpath(rules_main_search).send_keys(_rule_name)
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        sleep(5)
        click_on_actions_item(self, _rule_name, "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, _old_feed, "Import")
        self.validate_action_taken_third_party_rule(ioc=_old_feed, rule_name=_rule_name)
        process_console_logs(self)

    def test_103_auto_run_phantom_playbook_v3(self):
        """
            Testcase to autorun Trigger Playbook Splunk Phantom on feeds
        """
        fprint(self, "TC_ID - 61103 - verify if trigger playbook phantom rule can be autorun")
        set_value("phantom_v3_new_ip", phantom_playbook_v3_pattern + "." + str(random.randint(125, 255)))
        _intel = get_value("phantom_v3_new_ip")
        _rule_name = 'auto_rule_phantom_playbook_v3'
        quick_create_ip(self, _intel, "phantom_v3_new_ip")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, _intel, "Import")
        self.validate_action_taken_third_party_rule(ioc=_intel, rule_name=_rule_name)
        process_console_logs(self)

    def test_104_validate_phantom_trigger_manual_3rd_party(self):
        """
            Testcase to validate third party phantom trigger playbook
        """
        fprint(self, "TC_ID: 61104 - verify trigger playbook manual run in splunk phantom")
        package_name = "phantom_old_ip"
        intel = get_value(package_name)
        launch_splunk_phantom(self)
        verify_data_in_phantom(self, intel, package_name)

    def test_105_validate_phantom_trigger_auto_3rd_party(self):
        """
            Testcase to validate third party phantom trigger playbook
        """
        fprint(self, "TC_ID: 61105 - verify trigger playbook auto run in splunk phantom")
        package_name = "phantom_new_ip"
        intel = get_value(package_name)
        launch_splunk_phantom(self)
        verify_data_in_phantom(self, intel, package_name)

    def test_106_validate_phantom_trigger_v3_manual_3rd_party(self):
        """
            Testcase to validate third party phantom trigger playbook v3
        """
        fprint(self, "TC_ID: 61106 - verify trigger playbook v3 manual run in splunk phantom")
        package_name = "phantom_v3_old_ip"
        intel = get_value(package_name)
        launch_splunk_phantom(self)
        verify_data_in_phantom(self, intel, package_name)

    def test_107_validate_phantom_trigger_v3_auto_3rd_party(self):
        """
            Testcase to validate third party phantom trigger playbook v3
        """
        fprint(self, "TC_ID: 61107 - verify trigger playbook v3 auto run in splunk phantom")
        package_name = "phantom_v3_new_ip"
        intel = get_value(package_name)
        launch_splunk_phantom(self)
        verify_data_in_phantom(self, intel, package_name)

    def test_108_create_rule_csap_alert_draft(self):
        """
            Tewstcase to create a rule to Create CSAP alert in draft mode
        """
        fprint(self, "TC_ID: 61108 - verify rule creation to send alert to CSAP")
        set_value("csap_old_draft_domain", csap_draft_pattern.format(uniquestr[-4:]))
        _rule_name = 'auto_rule_csap_alert_draft'
        create_intel(self, "Domain", "csap_old_draft_domain"+get_value("tstamp"), get_value("csap_old_draft_domain"),
                     description="csap_old_draft_description")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_csap(self, action="Draft")
        add_condition_report_title(self, report_title="csap")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")

    def test_109_manual_run_rule_csap_alert_draft(self):
        """
            Testcase to run rule for create CSAP alert on old feeds
        """
        fprint(self, "TC_ID: 61109 - verify manual CSAP alert published rule creation")
        _rule_name = 'auto_rule_csap_alert_draft'
        _old_feed = get_value("csap_old_draft_domain")
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        fprint(self, "Searching for a rule name")
        self.driver.find_element_by_xpath(rules_main_search).send_keys(_rule_name)
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        sleep(5)
        click_on_actions_item(self, _rule_name, "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, _old_feed, "Import")
        self.validate_action_taken_third_party_rule(ioc=_old_feed, rule_name=_rule_name)
        process_console_logs(self)

    def test_110_auto_run_rule_csap_alert_draft(self):
        """
            Testcase to auto run rule for CSAP alert draft upon new intel added
        """
        fprint(self, "TC_ID: 61110 - verify auto csap alert creation as draft")
        set_value("csap_new_draft_domain", csap_draft_pattern.format(uniquestr[-4:]))
        _new_feed = get_value("csap_new_draft_domain")
        _rule_name = 'auto_rule_csap_alert_draft'
        create_intel(self, "Domain", "csap_new_draft_domain"+get_value("tstamp"), _new_feed,
                     description="csap_new_draft_description")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, _new_feed, "Import")
        self.validate_action_taken_third_party_rule(ioc=_new_feed, rule_name=_rule_name)
        process_console_logs(self)

    def test_111_create_rule_csap_alert_published(self):
        """
            Tewstcase to create a rule to Create CSAP alert in published mode
        """
        fprint(self, "TC_ID: 61111 - verify create CSAP alert published rule creation")
        set_value("csap_old_publish_domain", csap_publish_pattern.format(uniquestr[-4:]))
        _rule_name = 'auto_rule_csap_alert_publish'
        create_intel(self, "Domain", "csap_old_publish_domain"+get_value("tstamp"), get_value("csap_old_publish_domain"),
                     description="csap_old_publish_description")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source="Import", collection='Select All')
        add_action_csap(self, action="Published")
        add_condition_report_title(self, report_title="csap")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")

    def test_112_manual_run_rule_csap_alert_draft(self):
        """
            Testcase to run rule for create CSAP alert on old feeds
        """
        fprint(self, "TC_ID: 61112 - verify create CSAP alert published rule creation")
        _rule_name = 'auto_rule_csap_alert_publish'
        _old_feed = get_value("csap_old_publish_domain")
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        fprint(self, "Searching for a rule name")
        self.driver.find_element_by_xpath(rules_main_search).send_keys(_rule_name)
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        sleep(5)
        click_on_actions_item(self, _rule_name, "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, _old_feed, "Import")
        self.validate_action_taken_third_party_rule(ioc=_old_feed, rule_name=_rule_name)
        process_console_logs(self)

    def test_113_auto_run_rule_csap_alert_draft(self):
        """
            Testcase to auto run rule for CSAP alert published upon new intel added
        """
        fprint(self, "TC_ID: 61113 - verify CSAP alert published rule on new intel creation")
        set_value("csap_new_publish_domain", csap_publish_pattern.format(uniquestr[-4:]))
        _new_feed = get_value("csap_new_publish_domain")
        _rule_name = 'auto_rule_csap_alert_publish'
        create_intel(self, "Domain", "csap_new_publish_domain"+get_value("tstamp"), _new_feed,
                     description="csap_new_publish_description")
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, _new_feed, "Import")
        self.validate_action_taken_third_party_rule(ioc=_new_feed, rule_name=_rule_name)
        process_console_logs(self)

    def test_114_create_rule_inbox_1dotx(self):
        """
        Tescase to create rule with action send inbox for 1.x
        """
        fprint(self, "TC_ID: 61114 - verify rule creation - send inbox 1.x")
        _rule_name = "auto_rule_inbox_1dotx"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_send_inbox(self, 'subs_1dotx', 'inbox_1.x')
        add_condition_indicators(self, 'IP')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        quick_create_ip(self, send_inbox_1dotx_new_ip, 'send_inbox_1dotx_new_ip')

    def test_115_create_rule_inbox_2dot0(self):
        """
        Tescase to create rule with action send inbox for 2.0
        """
        fprint(self, "TC_ID: 61115 - verify rule creation - send inbox 2.0")
        _rule_name = "auto_rule_inbox_2dot0"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_send_inbox(self, 'subs_2dot0', 'inbox_2.0')
        add_condition_indicators(self, 'DOMAIN')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        create_intel(self, 'Domain', 'send_inbox_2dot0_new_domain', send_inbox_2dot0_new_domain)

    def test_116_create_rule_inbox_2dot1(self):
        """
        Tescase to create rule with action send inbox for 2.1
        """
        fprint(self, "TC_ID: 61116 - verify rule creation - send inbox 2.1")
        _rule_name = "auto_rule_inbox_2dot1"
        nav_menu_main(self, "Rules")
        create_basic_rule(self, _rule_name)
        add_source(self, source='Import', collection='Select All')
        add_action_send_inbox(self, 'subs_2dot1', 'inbox_2.1')
        add_condition_indicators(self, 'IP')
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Save')])[2]").click()
        verify_success(self, "Rule created successfully")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Adding object via quick add.")
        quick_create_ip(self, send_inbox_2dot1_new_ip, 'send_inbox_2dot1_new_ip')

    def test_117_cc_create_trigger_rule_confidence_csol(self):
        """
            Testcase for client confidence score
        """
        fprint(self, "TC_ID: 61117 - test_117_cc_create_trigger_rule_confidence_csol ")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, "Rule_cc_CSOL_conf_playbook")
        add_source(self, source="Recorded Future", collection='Select All')
        add_action_csol(self, type='Trigger Playbook V3', event="RULE_confscore"+get_value("csol_timestamp"))
        add_condition_confidence_score(self, comparator="GREATER", value='70')
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        disable_rule_api("Rule_cc_CSOL_conf_playbook")

    def test_118_cc_add_update_tag_rule(self):
        fprint(self, "TC_ID: 61118 - test_118_cc_add_update_tag_rule")
        add_tag(self, "Devo24")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, "CSOL_updateTag_rule")
        add_source(self, source="Recorded Future", collection="Select All")
        add_action_update_tag(self, "Devo24")
        add_condition_domain_objects(self, "Indicator")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        run_rule_delta("CSOL_updateTag_rule", delta=2)

    # After polling RF call the below function
    def test_119_cc_create_rule_tags_triggerPlaybookV3_csol(self):
        fprint(self, "TC_ID: 61117 - test_119_cc_create_rule_tags_triggerPlaybookV3_csol")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, "Rule_cc_CSOL_tags")
        add_source(self, source="Recorded Future", collection='Select All')
        add_action_csol(self, type="Trigger Playbook V3", event="RULE_tags"+get_value("csol_timestamp"))
        add_condition_tag(self, "Devo24")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        disable_rule_api("Rule_cc_CSOL_tags")

    def test_120_cc_create_trigger_rule_domainAll_csol(self):
        """
            Testcase for client domain ALL condition
        """
        fprint(self, "TC_ID: 61120 - test_118_cc_create_trigger_rule_domainAll_csol")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, "Rule_cc_CSOL_domainAll_playbook")
        add_source(self, source="Recorded Future", collection='Select All')
        add_action_csol(self, type="Trigger Playbook V3", event="RULE_domainAll" + get_value("csol_timestamp"))
        add_condition_ioc_All(self, ioc_type="DOMAIN")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        disable_rule_api("Rule_cc_CSOL_domainAll_playbook")

    def test_121_cc_create_publish_to_collection_rule_Indicator_All(self):
        """
            Testcase for client Indicator ALL Publish condition
        """
        fprint(self, "TC_ID: 61121 - test_121_cc_create_publish_to_collection_rule_Indicator_All")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, "Rule_cc_IndicatorAll_publish")
        add_source(self, source="Mandiant Threat Intelligence", collection='Select All')
        add_action_publish_collection(self)
        add_condition_indicator_all(self)
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        disable_rule_api("Rule_cc_IndicatorAll_publish")

    def test_122_cc_updateRefSet_and_updateTag_on_url_and_domain(self):
        """
            Testcase -  type: url and domain, any source, action: update reference set, update tag
        """
        fprint(self, "TC_ID: 61122 - test_122_cc_updateRefSet_and_updateTag_on_url_and_domain")
        # add_tag(self, "update_tag_refset")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, "updateRefSet_and_updateTag_on_url_and_domain")
        add_source(self, source="Import", collection='Select All')
        add_action_update_tag(self, "update_tag_refset")
        add_action_update_ref_set(self, get_value("REFERENCE_SET_NAME"))
        add_condition_ioc_All(self, ioc_type="URL")
        select_operator(self, operator="OR")
        add_condition_ioc_All(self, ioc_type="DOMAIN")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        disable_rule_api("updateRefSet_and_updateTag_on_url_and_domain")

    def test_123_cc_verify_in_QRADAR_reference_set_count(self):
        fprint(self, "TC_ID: 61123 - test_123_cc_verify_in_QRADAR_reference_set_count")
        verify_in_qradar(self, refset_name=get_value("REFERENCE_SET_NAME"))
        waitfor(self, 20, By.XPATH, "//td[@colid='elem_count' and contains(text(),'2')]")
        fprint(self, "Verified, Expected count is visible - 2")

    def test_124_cc_create_rule_publishToCol_UpdateRefSet_for_allHashes(self):
        fprint(self, "TC_ID: 61124 - test_124_cc_create_rule_publishToCol_UpdateRefSet_for_allHashes")
        create_ref_set_qradar(set_name="REFERENCE_SET_124")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, "Rule_cc_updateRefSet_PublishToCol_allHashes")
        add_source(self, source="Recorded Future", collection="Select All")
        add_action_publish_collection(self)
        add_action_update_ref_set(self, "REFERENCE_SET_124")
        add_condition_ioc_All(self, ioc_type="ALL HASH TYPES")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        disable_rule_api("Rule_cc_updateRefSet_PublishToCol_allHashes")

    def test_125_cc_create_rule_publishToCol_UpdateRefSet_for_allDomains(self):
        fprint(self, "TC_ID: 61125 - test_125_cc_create_rule_publishToCol_UpdateRefSet_for_allDomains")
        create_ref_set_qradar(set_name="REFERENCE_SET_125")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, "Rule_cc_updateRefSet_PublishToCol_allDomains")
        add_source(self, source="Recorded Future", collection="Select All")
        add_action_publish_collection(self)
        add_action_update_ref_set(self, "REFERENCE_SET_125")
        add_condition_ioc_All(self, ioc_type="DOMAIN")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        disable_rule_api("Rule_cc_updateRefSet_PublishToCol_allDomains")

    def test_126_cc_create_rule_publishToCol_UpdateRefSet_for_allIPs(self):
        fprint(self, "TC_ID: 61126 - test_126_cc_create_rule_publishToCol_UpdateRefSet_for_allIPs")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, "Rule_cc_updateRefSet_PublishToCol_allIPs")
        add_source(self, source="Recorded Future", collection="Select All")
        add_action_publish_collection(self)
        add_action_update_ref_set(self, "REFERENCE_SET_126")
        add_condition_ioc_All(self, ioc_type="IP")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        disable_rule_api("Rule_cc_updateRefSet_PublishToCol_allIPs")

    def test_127_cc_create_rule_publishToCol_UpdateRefSet_for_allURL(self):
        fprint(self, "TC_ID: 61127 - test_127_cc_create_rule_publishToCol_UpdateRefSet_for_allURL")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, "Rule_cc_updateRefSet_PublishToCol_allUrl")
        add_source(self, source="Recorded Future", collection="Select All")
        add_action_publish_collection(self)
        add_action_update_ref_set(self, "REFERENCE_SET_127")
        add_condition_ioc_All(self, ioc_type="URL")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")
        disable_rule_api("Rule_cc_updateRefSet_PublishToCol_allUrl")

    def test_128_create_rule_publish_intel_to_misp(self):
        """
            Testcase to send data from CTIX to MISP
        """
        set_value("ctom_stamp", uniquestr[-4:])
        nav_menu_main(self, "Threat Data")
        create_intel(self, type='Domain', title="ctom_old_"+get_value("ctom_stamp"), value="getmyjio.com")
        fprint(self, "TC_ID: 61128 - Testcase to send data from CTIX to MISP")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, "Rule_publish_intel_to_MISP")
        add_source(self, source="Import", collection="Select All")
        add_action_publish_collection(self, collection_list=["misp_coll"])
        add_condition_report_title(self, report_title="ctom")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "Rule created successfully")

    def test_139_manual_run_misp_rule(self):
        """
            Testcase to run Publish to collection action on MISP collection
        """
        fprint(self, "TC_ID: 61139 - Publish to collection action on MISP collection")
        _rule_name = "Rule_publish_intel_to_MISP"
        nav_menu_main(self, "Rules")
        waitfor(self, 20, By.XPATH, "//div[input[@id='main-input']]")
        self.driver.find_element_by_xpath("//div[input[@id='main-input']]").click()
        sleep(2)
        fprint(self, "Searching for a rule name")
        self.driver.find_element_by_xpath(rules_main_search).send_keys(_rule_name)
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        sleep(5)
        click_on_actions_item(self, _rule_name, "Run")
        run_rule_for_previous_feeds(self)
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, f"ctom_old_{get_value('ctom_stamp')}", "Import")
        validate_actioned_by_rule(self, intel=f"ctom_old_{get_value('ctom_stamp')}", rule_name=_rule_name)

    def test_140_auto_run_misp_rule(self):
        """
            Testcase to run Publish to collection action to MISP collection for new data
        """
        fprint(self, "TC_ID: 61140 - Publish to collection action on MISP collection on new data")
        _rule_name = "Rule_publish_intel_to_MISP"
        create_intel(self, type='Domain', title="ctom_new_"+get_value("ctom_stamp"), value="getmyairtel.com")
        sleep(30)   # waiting for rule to be actioned
        nav_menu_main(self, 'Threat Data')
        verify_data_in_threatdata(self, f"ctom_new_{get_value('ctom_stamp')}", "Import")
        validate_actioned_by_rule(self, intel=f"ctom_new_{get_value('ctom_stamp')}", rule_name=_rule_name)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
