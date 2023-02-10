import unittest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lib.ui.nav_tableview import click_on_actions_item
from lib.ui.rules import *
from lib.ui.stix_collections import create_collection
from lib.ui.subscribers import create_subscriber


failures = []
ioc_type = "Domain"
ioc_value = "testabc.com"
name = "subs_domain"
collection = ["col_1.x", "col_2.0", "col_2.1", "inbox_1.x", "inbox_2.0", "inbox_2.1"]
stix_source = ["subs_1dotx", "subs_2dot0", "subs_2dot1"]
threat_actor = "TA:00:02_publish"
vulnerability = "CVE-2022-publish"
coa = "coa_publish"
campaign = "campaign_publish"
intrusion_set = "intrusion_set_publish"
malware = "bitcoin_publish"
tool = "tool_publish"
attack_pattern = "ap_publish"
identity = "identity_publish"
location = 'Algeria'
infra = 'infra_publish'
publish_ip = "221.221.221.22"
publish_url = "https://www.systemtem.com"
publish_report = "https://www.sys123.com"
publish_md5 = "a18ca4003deb042bbee7a40f15e1970b"
publish_sha224 = "90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809"
publish_sha256 = "755738e1051d65e3374bd38bad04f1de6cda492c6d516c61a64efc4164588ba3"
publish_sha384 = "fdbd8e75a67f29f701a4e040385e2e23986303ea10239211af907fcbb83578b3e417cb71ce646efd0819dd8c088de1bd"
publish_sha512 = "aed7ed7a5a0778659577e7dcf560b78a97435226bbb9e91efa7835f5e72d0d3059f3badef52ca83bbee8ec96926b02f97ad10cc722f6278e465a323c45806262"
publish_ssdeep = "24:ol9rfbzwjx5zkvbbi8rum4pp6rg5yg+q8wixhmc:qrfbzkx5l8sm4grq8wixht"


class StixSubscriber(unittest.TestCase):

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

    def adding_STIXSource(self, sourcename, url, username, password):
        fprint(self, "Checking for the 'Add Stix Source' button")
        if Build_Version.__contains__("3."):
            waitfor(self, 20, By.XPATH, "(//button[contains(text(),'STIX Source')])[1]")
            fprint(self, "Button found, now clicking on it")
            self.driver.find_element_by_xpath("(//button[contains(text(),'STIX Source')])[1]").click()
        else:
            waitfor(self, 20, By.XPATH, "//button[contains(text(),'Add STIX Source')]")
            fprint(self, "Button found, now clicking on it")
            self.driver.find_element_by_xpath("//button[contains(text(),'Add STIX Source')]").click()
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Source Name *']")
        fprint(self, "Adding Configuration Details : ")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Source Name *']").send_keys(sourcename)
        fprint(self, "Source Name - "+sourcename)
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description *']").send_keys("test_STIX_Description")
        fprint(self, "Source Description - test_STIX_Description")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Discovery Service URL *']").send_keys(url)
        fprint(self, "Discovery Service URL - "+url)
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Confidence *']").send_keys("70")
        fprint(self, "Confidence Score - 70")
        self.driver.find_element_by_xpath("(//div[@name='taxii_option'])[1]").click()
        if sourcename == "subs_2dot1":
            waitfor(self, 5, By.XPATH, "//div[text()='STIX 2.1']")
            self.driver.find_element_by_xpath("//div[text()='STIX 2.1']").click()
        elif sourcename == "subs_2dot0":
            waitfor(self, 5, By.XPATH, "//div[text()='STIX 2.0']")
            self.driver.find_element_by_xpath("//div[text()='STIX 2.0']").click()
        else:
            waitfor(self, 5, By.XPATH, "//div[text()='STIX 1.x']")
            self.driver.find_element_by_xpath("//div[text()='STIX 1.x']").click()
        fprint(self, "STIX version - STIX 2.0")
        self.driver.find_element_by_xpath("(//div[@name='category'])[1]").click()
        waitfor(self, 20, By.XPATH, "//div[text()='Community Feeds']")
        sleep(2)
        self.driver.find_element_by_xpath("//div[text()='Community Feeds']").click()
        fprint(self, "Category - Community Feeds")
        self.driver.find_element_by_xpath("(//div[@name='authentication_type'])[1]").click()
        waitfor(self, 5, By.XPATH, "//div[text()='Basic']")
        self.driver.find_element_by_xpath("//div[text()='Basic']").click()
        fprint(self, "Authentication Tyoe - Basic")
        waitfor(self, 5, By.XPATH, "//input[@name='username']")
        self.driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
        fprint(self, "Entered Username")
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
        fprint(self, "Entered Password")
        if Build_Version.__contains__("3."):
            self.driver.find_element_by_xpath("//button[@data-testid='save-custom-sources']").click()
        else:
            self.driver.find_element_by_xpath("//button[@data-testid='save-sources']").click()
        fprint(self, "Clicked on the Save Source Button")
        verify_success(self, "Source created successfully")
        # process_console_logs(self)

    def enable_manual_poll(self, source_name):
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        fprint(self, "Searching the STIX Source - "+source_name)
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(source_name)
        self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
        waitfor(self, 5, By.XPATH, "//p[contains(text(),'"+source_name+"')]")
        fprint(self, "Getting the added STIX Source - "+source_name)
        self.driver.find_element_by_xpath(
            "//p[contains(text(),'" + source_name + "')]").click()
        waitfor(self, 5, By.XPATH, "//button[@data-testid='action']")
        fprint(self, "Inside of - Collections of "+source_name)
        # Need to implement particular collection enable
        if source_name == "subs_1dotx":
            click_on_actions_item(self, "col_1.x", "Edit Poll Configuration")
        elif source_name == "subs_2dot0":
            click_on_actions_item(self, "col_2.0", "Edit Poll Configuration")
        else:
            click_on_actions_item(self, "col_2.1", "Edit Poll Configuration")
        fprint(self, "Clicked on the Edit Poll Configuration option")
        waitfor(self, 5, By.XPATH, "//button[text()='Update']")
        self.driver.find_element_by_xpath("//button[text()='Update']").click()
        fprint(self, "Clicked on the Update Button")
        verify_success(self, "updated successfully!", 30)
        # process_console_logs(self)
        sleep(2)

    def poll_now(self, source_name):
        waitfor(self, 10, By.XPATH, "//input[@placeholder='Search or filter results']")
        fprint(self, "Searching the STIX Source - " + source_name)
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(source_name)
        self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
        waitfor(self, 5, By.XPATH, "//p[contains(text(),'" + source_name + "')]")
        self.driver.find_element_by_xpath(
            "//p[contains(text(),'" + source_name + "')]").click()
        # Clicked on the action menu
        if source_name == "subs_1dotx":
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys('col_1.x')
            self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
            click_on_actions_item(self, "col_1.x", "Poll Now")
        elif source_name == "subs_2dot0":
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys('col_2.0')
            self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
            click_on_actions_item(self, "col_2.0", "Poll Now")
        else:
            waitfor(self, 10, By.XPATH, "//input[@placeholder='Search or filter results']")
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("col_2.1")
            self.driver.find_element_by_xpath("//span[contains(text(),'Press enter or click to search')]/parent::div/parent::a").click()
            click_on_actions_item(self, "col_2.1", "Poll Now")
        fprint(self, "Clicked on the Poll Now option")
        #verify_success_alert(self, "Collection is updated successfully!")
        verify_success(self, "updated successfully")
        # process_console_logs(self)

    def enable_subsribed_status(self, source_name):
        if source_name == "subs_1dotx":
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'inbox_1.x')]//following::div[@data-testid='subscribed']")
            self.driver.find_element_by_xpath("//span[contains(text(),'inbox_1.x')]//following::div[@data-testid='subscribed']").click()
        elif source_name == "subs_2dot0":
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'inbox_2.0')]//following::div[@data-testid='subscribed']")
            self.driver.find_element_by_xpath("//span[contains(text(),'inbox_2.0')]//following::div[@data-testid='subscribed']").click()
        else:
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'inbox_2.1')]//following::div[@data-testid='subscribed']")
            self.driver.find_element_by_xpath("//span[contains(text(),'inbox_2.1')]//following::div[@data-testid='subscribed']").click()
        verify_success(self, "updated successfully")

    def create_intel(self):
        textis = ""
        fprint(self, "Waiting for the New Button...")
        self.driver.find_element_by_xpath("//button[contains(text(),'New')]").click()
        fprint(self, "Clicked on the New Button")
        waitfor(self, 5, By.XPATH, "//li/div[contains(text(),'Quick Add Intel')]")
        self.driver.find_element_by_xpath("//li/div[contains(text(),'Quick Add Intel')]").click()
        fprint(self, "Clicked on the 'Quick Add Intel' option")
        waitfor(self, 10, By.XPATH, qai_ioc_type_search)
        sleep(5)
        fprint(self, "Searching - Domain")
        self.driver.find_element_by_xpath(qai_ioc_type_search).click()
        clear_field(self.driver.find_element_by_xpath(qai_ioc_type_search))
        self.driver.find_element_by_xpath(qai_ioc_type_search).send_keys(ioc_type)
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Domain')]/ancestor::div[1]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Domain')]/div[1]/div").click()
        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(name)
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").send_keys(ioc_value)
        self.driver.find_element_by_xpath("//button[contains(text(),'Create Intel')]").click()
        if waitfor(self, 30, By.XPATH, "//i[@class = 'cyicon-check-o-active']", False):
            sleep(1)
            textis = self.driver.find_element_by_xpath("//div[contains(@class, 'cy-message__text')]").text
            if textis == "You can view the created intel as a report object in the Threat Data module.":
                fprint(self, "[Passed] Expected message is found, " + str(textis))
                self.driver.find_element_by_xpath("//div[@class='el-notification__closeBtn el-icon-close']").click()
                repeat = 1
                while repeat <= 3:
                    if waitfor(self, 40, By.XPATH, "//span[contains(text(),'"+name+"')]/ancestor::td/following-sibling::td[3]//span[contains(text(),'Created')]", False):
                        fprint(self, "Created Status of intel is visible - "+name)
                        self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
                        break
                    else:
                        self.driver.find_element_by_xpath("//button[contains(text(),'Refresh')]").click()
                        fprint(self, "Created Status of intel is not visible, Clicked on the Refresh Button")
                        if repeat == 3:
                            failures.append("Created Status of intel is not visible - "+name)
                            self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
                        repeat = repeat + 1
            else:
                fprint(self,
                       "[Failed] Alert found with different msg. Found: " + str(
                           textis) + "Expected:" + "You will be notified once the STIX package is created!")
                self.driver.find_element_by_xpath("//div[contains(text(),'"+ioc_type+"')]/div[1]/div").click()
                failures.append("Case Status: [Failed] Alert found but expected message is not found -" + textis)
        else:
            fprint(self, "Getting some error in adding - "+ioc_type)
            self.driver.find_element_by_xpath("//div[contains(text(),'"+ioc_type+"')]/div[1]/div").click()
            failures.append("Expected message is not found - " + textis)
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        self.assert_(failures == [], str(failures))
        sleep(20)

    def verify_under_feed(self, value, section=1, object_value=ioc_value):
        waitfor(self, 5, By.XPATH, threat_data_main_search_field)
        self.driver.find_element_by_xpath(threat_data_main_search_field).click()
        fprint(self, "Clicked on the search field")
        clear_field(self.driver.find_element_by_xpath(threat_data_main_search_field))
        self.driver.find_element_by_xpath(threat_data_main_search_field).send_keys(object_value)
        fprint(self, "Searching - "+object_value)
        waitfor(self, 10, By.XPATH,
                "//span[contains(text(),'Import')]/ancestor::tr/td[3]//span[contains(text(),'" + object_value + "')]")
        fprint(self, "Feed Visible - " + object_value)
        wait = WebDriverWait(self.driver, 10)
        ele = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'Import')]/ancestor::tr/td[3]//span[contains(text(),'" + object_value + "')]")))
        self.driver.execute_script("arguments[0].click();", ele)
        sleep(2)
        fprint(self, "Clicked on - "+object_value)
        if section == 1:
            fprint(self, "Verifying Published Collection Section")
            if value == "col_2.1":
                waitfor(self, 20, By.XPATH, "//span[contains(text(),'col_2.1')]")
                fprint(self, "Collection visible - col_2.1")
            elif value == "col_2.0":
                waitfor(self, 20, By.XPATH, "//span[contains(text(),'col_2.0')]")
                fprint(self, "Collection visible - col_2.0")
            else:
                waitfor(self, 20, By.XPATH, "//span[contains(text(),'col_1.x')]")
                fprint(self, "Collection visible - col_1.x")
        if section == 2:
            fprint(self, "Verifying Sources Section")
            #   Expected sources should be visible under 3 sources - "Reported By Sources", "custom attributes table"
            #   and "Sources table"
            if value == "subs_2dot1":
                waitfor(self, 20, By.XPATH, "//span[contains(text(),'subs_2dot1')]")
                fprint(self, "Source Visible - subs_2dot1")
            elif value == "subs_2dot0":
                waitfor(self, 20, By.XPATH, "//span[contains(text(),'subs_2dot0')]")
                fprint(self, "Source Visible - subs_2dot0")
            else:
                waitfor(self, 20, By.XPATH, "//span[contains(text(),'subs_1dotx')]")
                fprint(self, "Source Visible - subs_1dotx")
        if section == 3:
            fprint(self, "Veriying Subscriber name under Source Section")
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'subscriber_name')]")
            fprint(self, "Subscriber visible - subscriber_name")

    def test_01_publishing_create_STIXCollection(self):
        fprint(self, "TC_ID: 55101 - test_01_publishing_create_STIXCollection")
        nav_menu_admin(self, "STIX Collections")
        for col in collection:
            fprint(self, "Waiting for the Add Button")
            waitfor(self, 10, By.XPATH, "//button[contains(text(),'Add')]")
            self.driver.find_element_by_xpath("//button[contains(text(),'Add')]").click()
            fprint(self, "Clicked on the Add Button")
            waitfor(self, 10, By.XPATH, "//input[@aria-placeholder='Collection Name *']")
            self.driver.find_element_by_xpath("//input[@aria-placeholder='Collection Name *']").click()
            self.driver.find_element_by_xpath("//input[@aria-placeholder='Collection Name *']").send_keys(col)
            fprint(self, "Collection name - " + col)
            waitfor(self, 10, By.XPATH, "//textarea[@aria-placeholder='Description *']")
            self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description *']").click()
            self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description *']").send_keys(
                col + "_description")
            fprint(self, "Description - " + col + "_description")
            if col == "col_1.x" or col == "col_2.0" or col == "col_2.1":
                self.driver.find_element_by_xpath("//span[contains(text(),'Polling')]/parent::div").click()
                fprint(self, "Selected - Polling")
            self.driver.find_element_by_xpath("//span[contains(text(),'Inbox')]/parent::div").click()
            fprint(self, "Selected - Inbox")
            self.driver.find_element_by_xpath("//button[contains(text(),'Save Collection')]").click()
            fprint(self, "Clicked on the Saved Button")
            #verify_success_alert(self, "STIX Collection created successfully!")
            verify_success(self, "STIX Collection created successfully")
            fprint(self, "Verifying added collection is visible or not...")
            waitfor(self, 10, By.XPATH, "//span[contains(text(),'" + col + "')]")
            fprint(self, "Collection Visible - " + col)

    def test_02_publishing_add_subscriber(self):
        fprint(self, "TC_ID: 55102 - test_02_publishing_add_subscriber")
        nav_menu_admin(self, "Integration Management")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Subscribers ')]/parent::a")
        self.driver.find_element_by_xpath("//span[contains(text(),'Subscribers ')]/parent::a").click()
        waitfor(self, 2, By.XPATH, "//button[contains(text(),'Add Subscriber')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add Subscriber')]").click()
        waitfor(self, 10, By.XPATH, "//input[@aria-placeholder='Subscriber Name *']")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Subscriber Name *']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Subscriber Name *']").send_keys("subscriber_name")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name*']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name*']").send_keys("automation_name")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Email *']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Email *']").send_keys("automation@cyware.com")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Confidence *']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Confidence *']").send_keys("90")
        self.driver.find_element_by_xpath("(//div[@name='collections'])[1]").click()
        for col in collection:
            waitfor(self, 10, By.XPATH, "//div[contains(text(),'" + col + "')]/parent::div")
            self.driver.find_element_by_xpath("//div[contains(text(),'" + col + "')]/parent::div").click()
        self.driver.find_element_by_xpath("//button[@data-testid='save-subscribers']").click()
        verify_success(self, "Subscriber created successfully")
        waitfor(self, 10, By.XPATH, "//p[contains(text(),'Username')]/parent::div/div/p")
        username = self.driver.find_element_by_xpath("//p[contains(text(),'Username')]/parent::div/div/p").text
        password = self.driver.find_element_by_xpath("//p[contains(text(),'Password')]/parent::div/div/p").text
        url_1dotx = self.driver.find_element_by_xpath("//p[contains(text(),'TAXII-1 URL')]/parent::div/div/p").text
        url_2dot0 = self.driver.find_element_by_xpath("//p[contains(text(),'TAXII-2 URL')]/parent::div/div/p").text
        url_2dot1 = self.driver.find_element_by_xpath("//p[contains(text(),'TAXII-2.1 URL')]/parent::div/div/p").text
        fprint(self, "username - " + username + " password - " + password)
        fprint(self, "url_2dot1 - " + url_2dot1)
        fprint(self, "url_2dot0 - " + url_2dot0)
        fprint(self, "url_1dotx - " + url_1dotx)
        set_value("username", username)
        set_value("password", password)
        set_value("url_1dotx", url_1dotx)
        set_value("url_2dot0", url_2dot0)
        set_value("url_2dot1", url_2dot1)
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        fprint(self, "Credentials Slider close")
        self.driver.find_element_by_xpath("(//a[@href='/ctix/sources/custom'])[2]")
        sleep(2)  # wait required here

    def test_03_publishing_add_stixSource_manual_2dot1(self):
        fprint(self, "TC_ID: 55122 - test_03_publishing_add_stixSource_manual_2dot1")
        nav_menu_admin(self, "Integration Management")
        self.adding_STIXSource("subs_2dot1", get_value("url_2dot1"), get_value("username"), get_value("password"))
        self.enable_manual_poll("subs_2dot1")
        self.enable_subsribed_status("subs_2dot1")

    def test_04_publishing_add_stixSource_manual_2dot0(self):
        fprint(self, "TC_ID: 55123 - test_04_publishing_add_stixSource_manual_2dot0")
        nav_menu_admin(self, "Integration Management")
        self.adding_STIXSource("subs_2dot0", get_value("url_2dot0"), get_value("username"), get_value("password"))
        self.enable_manual_poll("subs_2dot0")
        self.enable_subsribed_status("subs_2dot0")

    def test_05_publishing_add_stixSource_manual_1dotx(self):
        fprint(self, "TC_ID: 55124 - test_05_publishing_add_stixSource_manual_1dotx")
        nav_menu_admin(self, "Integration Management")
        self.adding_STIXSource("subs_1dotx", get_value("url_1dotx"), get_value("username"), get_value("password"))
        self.enable_manual_poll("subs_1dotx")
        self.enable_subsribed_status("subs_1dotx")

    def test_06_publishing_add_publishToCollection_rule(self):
        fprint(self, "TC_ID: 55104 - test_04_publishing_add_publishToCollection_rule")
        fprint(self, "Navigating to the Rules page")
        nav_menu_main(self, "Rules")
        create_basic_rule(self, 'Rule1')
        fprint(self, "Clicked on the Submit button, now adding source...")
        add_source(self, source="Import", collection="Select All")
        fprint(self, "Adding condition...")
        fprint(self, "Adding action...")
        add_action_publish_collection(self)
        add_condition_title(self, value="testabc")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        # verify_success_alert(self, "Rule created successfully!")
        verify_success(self, "Rule created successfully")

    def test_07_publishing_createIntel(self):
        fprint(self, "TC_ID: 55105 - test_05_publishing_createIntel")
        # creating intel
        fprint(self, "Creating Intel now, through quick add intel")
        self.create_intel()

    def test_08_publishing_verifying_2dot1_collection_under_PublishedCollectionSection(self):
        fprint(self, "TC_ID: 55106 - test_06_publishing_verifying_2dot1_collection_PublishedCollectionSection")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1")
        fprint(self, "Verifying 2dot1 collection, Test Case Passed")

    def test_09_publishing_verifying_2dot0_collection_under_PublishedCollectionSection(self):
        fprint(self, "TC_ID: 55107 - test_07_publishing_verifying_2dot0_collection_PublishedCollectionSection")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.0")
        fprint(self, "Verifying 2dot0 Collection, Test Case Passed")

    def test_10_publishing_verifying_1dotx_collection_under_PublishedCollectionSection(self):
        fprint(self, "TC_ID: 55108 - test_08_publishing_verifying_1dotx_collection_PublishedCollectionSection")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_1.x")
        fprint(self, "Verifying 1dotx Collection, Test Case Passed")

    def test_11_publishing_polling_each_stixSource(self):
        fprint(self, "TC_ID: 55109 - test_09_publishing_polling_each_stixSource")
        nav_menu_admin(self, "Integration Management")
        self.poll_now("subs_2dot1")
        self.driver.find_element_by_xpath("//div[@class='cy-page__back-button']/i").click()
        self.poll_now("subs_2dot0")
        self.driver.find_element_by_xpath("//div[@class='cy-page__back-button']/i").click()
        self.poll_now("subs_1dotx")

    def test_12_publishing_verifying_2dot1_under_sourcesSection(self):
        fprint(self, "TC_ID: 55110 - test_10_publishing_verifying_2dot1_sourcesSection")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("subs_2dot1", 2)
        fprint(self, "Verifying 2dot1 source, Test Case Passed")

    def test_13_publishing_verifying_2dot0_under_sourcesSection(self):
        fprint(self, "TC_ID: 55111 - test_11_publishing_verifying_2dot0_sourcesSection")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("subs_2dot0", 2)
        fprint(self, "Verifying 2dot0 source, Test Case Passed")

    def test_14_publishing_verifying_1dotx_under_sourcesSection(self):
        fprint(self, "TC_ID: 55112 - test_12_publishing_verifying_1dotx_sourcesSection")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("subs_1dotx", 2)
        fprint(self, "Verifying 1dotx source, Test Case Passed")

    def test_15_publishing_verifying_collection_under_PublishedCollectionSection_IP(self):
        fprint(self, "TC_ID: 41115 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : IP")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, publish_ip)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_16_publishing_verifying_collection_under_PublishedCollectionSection_URL(self):
        fprint(self, "TC_ID: 41116 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : URL")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, publish_url)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_17_publishing_verifying_collection_under_PublishedCollectionSection_MD5(self):
        fprint(self, "TC_ID: 41117 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : MD5")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, publish_md5)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_18_publishing_verifying_collection_under_PublishedCollectionSection_SHA224(self):
        fprint(self, "TC_ID: 41118 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : SHA224")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, publish_sha224)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_19_publishing_verifying_collection_under_PublishedCollectionSection_SHA384(self):
        fprint(self, "TC_ID: 41119 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : SHA384")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, publish_sha384)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_20_publishing_verifying_collection_under_PublishedCollectionSection_SHA256(self):
        fprint(self, "TC_ID: 41120 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : SHA256")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, publish_sha256)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_21_publishing_verifying_collection_under_PublishedCollectionSection_SHA512(self):
        fprint(self, "TC_ID: 41121 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : SHA512")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, publish_sha512)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_22_publishing_verifying_collection_under_PublishedCollectionSection_SSDEEP(self):
        fprint(self, "TC_ID: 41122 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : SSDEEP")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, publish_ssdeep)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_23_publishing_verifying_collection_under_PublishedCollectionSection_Threat_Actor(self):
        fprint(self, "TC_ID: 41123 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : Threat Actor")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, threat_actor)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_24_publishing_verifying_collection_under_PublishedCollectionSection_Course_Of_Action(self):
        fprint(self, "TC_ID: 41124 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : Course_Of_Action")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, coa)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_25_publishing_verifying_collection_under_PublishedCollectionSection_Campaign(self):
        fprint(self, "TC_ID: 41125 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : Campaign")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, campaign)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_26_publishing_verifying_collection_under_PublishedCollectionSection_Intrusion_set(self):
        fprint(self, "TC_ID: 41126 - test_publishing_verifying_collection_PublishedCollectionSection : Intrusion_set")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, intrusion_set)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_27_publishing_verifying_collection_under_PublishedCollectionSection_Malware(self):
        fprint(self, "TC_ID: 41127 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : Malware")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, malware)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_28_publishing_verifying_collection_under_PublishedCollectionSection_Tool(self):
        fprint(self, "TC_ID: 41128 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : Tool")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, tool)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_29_publishing_verifying_collection_under_PublishedCollectionSection_Attack_Pattern(self):
        fprint(self, "TC_ID: 41129 - test_publishing_verifying_collection_PublishedCollectionSection : Attack_Pattern")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, attack_pattern)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_30_publishing_verifying_collection_under_PublishedCollectionSection_Identity(self):
        fprint(self, "TC_ID: 41130 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : Identity")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, identity)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_31_publishing_verifying_collection_under_PublishedCollectionSection_Location(self):
        fprint(self, "TC_ID: 41131 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : Location")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, location)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_32_publishing_verifying_collection_under_PublishedCollectionSection_Infrastructure(self):
        fprint(self, "TC_ID: 41132 - test_publishing_verifying_collection_PublishedCollectionSection : Infrastructure")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, infra)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_33_publishing_verifying_collection_under_PublishedCollectionSection_Report(self):
        fprint(self, "TC_ID: 41133 - test_publishing_verifying_2dot1_collection_PublishedCollectionSection : Report")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, publish_report)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_34_publishing_verifying_collection_under_PublishedCollectionSection_Vulnerability(self):
        fprint(self, "TC_ID: 41134 - test_publishing_verifying_collection_PublishedCollectionSection : Vulnerability")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("col_2.1", 1, vulnerability)
        fprint(self, "Verifying collection : collection is visible, object is published")
        fprint(self, "[PASSED] publishing_verifying_collection_under_PublishedCollectionSection")

    def test_35_inbox_1dotx_verify_subscriber_name_under_subscriberSection(self):
        fprint(self, "TC_ID: 41135 - verifying subscriber name under source/subscriber section for version 1.x")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("subscriber_name", 3, send_inbox_1dotx_new_ip)
        fprint(self, "[PASSED] subscriber name is visible under source/subscriber section for version 1.x")

    def test_36_inbox_2dot1_verify_subscriber_name_under_subscriberSection(self):
        fprint(self, "TC_ID: 41136 - verifying subscriber name under source/subscriber section for version 2.1")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("subscriber_name", 3, send_inbox_2dot1_new_ip)
        fprint(self, "[PASSED] subscriber name is visible under source/subscriber section for version 2.1")

    def test_37_inbox_2dot0_verify_subscriber_name_under_subscriberSection(self):
        fprint(self, "TC_ID: 41137 - verifying subscriber name under source/subscriber section for version 2.0")
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
        self.verify_under_feed("subscriber_name", 3, send_inbox_2dot0_new_domain)
        fprint(self, "[PASSED] subscriber name is visible under source/subscriber section for version 2.0")

    def test_38_setup_misp_subscriber(self):
        """
            Testcase to setup subscriber to test MISP flow
        """
        fprint(self, "TC_ID: 41138 - Testcase to setup subscriber to test MISP flow")
        create_collection(self, title="misp_coll")
        misp_creds = create_subscriber(self, name="misp_subscriber", collections=["misp_coll"])
        fprint(self, ", ".join(misp_creds))
        set_value("misp_creds", misp_creds)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())


