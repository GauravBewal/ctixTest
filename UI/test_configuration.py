import unittest
from lib.ui.nav_app import *
from lib.ui.smtp import enable_smtp


class Configuration(unittest.TestCase):

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

    def enable_disable_stixType(self):
        nav_menu_admin(self, "Configuration")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'TAXII Server')]/parent::a")
        self.driver.find_element_by_xpath("//span[contains(text(),'TAXII Server')]/parent::a").click()
        fprint(self, "Clicked on the TAXII Server tab")
        waitfor(self, 20, By.XPATH, "//h4[contains(text(),'STIX Type')]")
        self.driver.find_element_by_xpath(
            "//h4[contains(text(),'STIX Type')]/ancestor::div[2]//button[contains(text(),'Edit')]").click()
        fprint(self, "Clicked on the Edit Option")
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'Save')]")

        try:
            self.driver.find_element_by_xpath("//span[contains(text(),'STIX 2.0')]/parent::span//button").click()
        except:
            self.driver.find_element_by_xpath("//span[contains(text(),'STIX 2.0')]/parent::span//span[@name='stix2']").click()
        if waitfor(self, 2, By.XPATH, "//div[@name='stix2' and contains(@class,'enabled')]", False) or \
                waitfor(self, 1, By.XPATH, "//input[@name='stix2' and @value='true']", False):
            fprint(self, "Enabled STIX-2.0")
        else:
            fprint(self, "Disabled STIX-2.0")

        try:
            self.driver.find_element_by_xpath("//span[contains(text(),'STIX 2.1')]/parent::span//button").click()
        except:
            self.driver.find_element_by_xpath("//span[contains(text(),'STIX 2.1')]/parent::span//span[@name='stix2_v1']").click()
        if waitfor(self, 2, By.XPATH, "//div[@name='stix2_v1' and contains(@class,'enabled')]", False) or \
                waitfor(self, 1, By.XPATH, "//input[@name='stix2_v1' and @value='true']", False):
            fprint(self, "Enabled STIX-2.1")
        else:
            fprint(self, "Disabled STIX-2.1")

        try:
            self.driver.find_element_by_xpath("//span[contains(text(),'STIX 1.2')]/parent::span//button").click()
        except:
            self.driver.find_element_by_xpath("//span[contains(text(),'STIX 1.2')]/parent::span//span[@name='stix1_2']").click()
        if waitfor(self, 2, By.XPATH, "//div[@name='stix1_2' and contains(@class,'enabled')]", False) or \
                waitfor(self, 1, By.XPATH, "//input[@name='stix1_2' and @value='true']", False):
            fprint(self, "Enabled STIX-1.2")
        else:
            fprint(self, "Disabled STIX-1.2")
        try:
            self.driver.find_element_by_xpath("//span[contains(text(),'MISP')]/parent::span//button").click()
        except:
            self.driver.find_element_by_xpath("//span[contains(text(),'MISP')]/parent::span//span[@name='misp']").click()
        if waitfor(self, 2, By.XPATH, "//div[@name='misp' and contains(@class,'enabled')]", False) or \
                waitfor(self, 1, By.XPATH, "//input[@name='misp' and @value='true']", False):
            fprint(self, "Enabled MISP")
        else:
            fprint(self, "Disabled MISP")

        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "Clicked on the Save button")
        verify_success(self, "Settings saved successfully")

    def test_01_load_basic_settings(self):
        """
        Testing if all basic details pages are loading
        """
        fprint(self, "TC_ID 1: Validating Basic Setting pages")
        nav_menu_admin(self, "Configuration")
        waitfor(self, 1, By.XPATH, "//div/span[contains(text(),'General')]", False)
        fprint(self, "Loading General Settings")
        self.driver.find_element_by_xpath("//div/span[contains(text(),'General')]").click()
        waitfor(self, 1, By.XPATH, "//p[contains(text(), 'Minimized Logo')]")
        fprint(self, "[PASSED] General Settings Loaded")
        fprint(self, "Loading TAXII Server Settings")
        self.driver.find_element_by_xpath("//div/span[contains(text(),'TAXII Server')]").click()
        waitfor(self, 1, By.XPATH, "//div[contains(text(), 'Max Polling Time')]")
        fprint(self, "[PASSED] TAXII Server Settings Loaded")
        fprint(self, "Loading Access Restriction Settings")
        self.driver.find_element_by_xpath("//div/span[contains(text(),'Access Restrictions')]").click()
        waitfor(self, 1, By.XPATH, "//div[contains(text(), 'User Access Restrictions')]")
        fprint(self, "[PASSED] Access Restriction Settings Loaded")
        fprint(self, "Loading SMTP Settings")
        self.driver.find_element_by_xpath("//div/span[contains(text(),'SMTP')]").click()
        waitfor(self, 1, By.XPATH, "//div[contains(text(), 'Enable SMTP')]")
        fprint(self, "[PASSED] SMTP Settings Loaded")
        process_console_logs(self)

    def test_02_load_authentication(self):
        """
        Testing if all authentication pages are loading
        """
        fprint(self, "TC_ID 2: Validation Authentication configuration pages")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Authentication')]").click()
        waitfor(self, 1, By.XPATH, "//div/span[contains(text(),'SAML 2.0')]", False)
        fprint(self, "Loading SAML 2.0 Settings")
        self.driver.find_element_by_xpath("//div/span[contains(text(),'SAML 2.0')]").click()
        waitfor(self, 1, By.XPATH, "//div[contains(text(),'Assertion Consumer URL')]")
        fprint(self, "[PASSED] SAML 2.0 Settings Loaded")
        fprint(self, "Loading LDAP Settings")
        self.driver.find_element_by_xpath("//div/span[contains(text(),'LDAP')]").click()
        waitfor(self, 1, By.XPATH, "//input[@aria-placeholder='Domain Name*']")
        fprint(self, "[PASSED] LDAP Settings Loaded")
        fprint(self, "Loading CIAM Settings")
        self.driver.find_element_by_xpath("//div/span[contains(text(),'CIAM')]").click()
        waitfor(self, 1, By.XPATH, "//div[contains(text(), 'Redirect URL')]")
        fprint(self, "[PASSED] CIAM Settings Loaded")
        fprint(self, "Loading Username/Password Settings")
        self.driver.find_element_by_xpath("//div/span[contains(text(),'Username/Password')]").click()
        waitfor(self, 1, By.XPATH, "//div[contains(text(), 'Password Policy')]")
        fprint(self, "[PASSED] Username/Password Settings Loaded")
        process_console_logs(self)

    def test_03_custom_objects_loading(self):
        """
        Testing custom objects page load
        """
        fprint(self, "Validating custom objects page")
        fprint(self, "Loading Custom Objects")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Custom Objects')]").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(), 'Custom Objects')]")
        fprint(self, "[PASSED] Custom Objects Loaded")
        process_console_logs(self)

    def test_04_custom_attributes_loading(self):
        """
        Testing custom attributes page load
        """
        fprint(self, "Validating custom object page")
        fprint(self, "Loading Custom Attributes")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Custom Attributes')]").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(), 'Custom Attributes')]")
        fprint(self, "[PASSED] Custom Attributes Loaded")
        process_console_logs(self)

    def test_05_indicator_action_loading(self):
        """
        Testing indicator action page loading
        """
        fprint(self, "Validating indicator Actions page")
        fprint(self, "Loading Indicator Actions")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Indicator Actions')]").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(), 'Indicator Actions')]")
        fprint(self, "[PASSED] Indicator Actions Loaded")
        process_console_logs(self)

    def test_06_rate_limit_loading(self):
        """
        Testing Rate limit page loading
        """
        fprint(self, "Validating rate limit settings page")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Rate Limit')]").click()
        waitfor(self, 2, By.XPATH, "//div/span[contains(text(),'Open API')]")
        fprint(self, "Loading OPEN API Rate Limit Settings")
        self.driver.find_element_by_xpath("//div/span[contains(text(),'Open API')]").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(),'Per minute rate limit')]")
        fprint(self, "[PASSED] OPEN API Rate Limit Settings Loaded")
        waitfor(self, 2, By.XPATH, "//div/span[contains(text(),'TAXII')]")
        fprint(self, "Loading TAXII Rate Limit Settings")
        self.driver.find_element_by_xpath("//div/span[contains(text(),'TAXII')]").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(),'Per minute rate limit for each subscriber')]")
        fprint(self, "[PASSED] TAXII Rate Limit Settings Loaded")
        process_console_logs(self)

    def test_07_enable_domain_in_General_Settings(self):
        ''' Enabling the threat mailbox and rss feed to parse domain from the url '''
        nav_menu_admin(self, "Configuration")
        waitfor(self, 10, By.XPATH, "//div/span[contains(text(),'General')]", False)
        fprint(self, "Loading General Settings")
        if Build_Version.__contains__("3."):
            self.driver.find_element_by_xpath(
                "//h4[contains(text(),'Parse Domain')]//following::button[contains(text(),'Edit')]").click()
            fprint(self, "[Passed]-clicked on the edit button")
        else:
            self.driver.find_element_by_xpath("//div/span[contains(text(),'General')]").click()

        fprint(self, "Clicking the Url option")
        if waitfor(self, 5, By.XPATH, "//div[@name='parse_domain_from_email_address' and contains(@class,'enabled')]", False) or \
                waitfor(self, 1, By.XPATH, "//input[@name='parse_domain_from_url' and @value='true']", False):
            fprint(self, "Already Enabled")
        else:
            try:
                self.driver.find_element_by_xpath("//div[contains(@name,'parse_domain_from_url')]//div//span//span").click()
            except:
                self.driver.find_element_by_xpath("//span[@name='parse_domain_from_url']").click()

        fprint(self, "Selecting the email")
        if waitfor(self, 5, By.XPATH, "//div[@name='parse_domain_from_email_address' and contains(@class,'enabled')]", False) or \
                waitfor(self, 1, By.XPATH, "//input[@name='parse_domain_from_email_address' and @value='true']", False):
            fprint(self, "Already Enabled")
        else:
            try:
                self.driver.find_element_by_xpath("//div[contains(@name,'parse_domain_from_email_address')]//div//span//span").click()
            except:
                self.driver.find_element_by_xpath("//span[@name='parse_domain_from_email_address']").click()

        fprint(self, "[Passed]-Selecting the parse email through Url ")
        if waitfor(self, 5, By.XPATH, "//div[@name='parse_email_from_url' and contains(@class,'enabled')]", False) or \
                waitfor(self, 1, By.XPATH, "//input[@name='parse_email_from_url' and @value='true']", False):
            fprint(self, "Already exist")
        else:
            try:
                self.driver.find_element_by_xpath("//div[contains(@name,'parse_email_from_url')]//div//span//span").click()
            except:
                self.driver.find_element_by_xpath("//span[@name='parse_email_from_url']").click()

        fprint(self, "Selecting the parse email through Url ")
        if Build_Version.__contains__("3."):
            self.driver.find_element_by_xpath("(//button[normalize-space()='Save'])[1]").click()
            fprint(self, "[Passed]-clicked on save button")
            verify_success(self, "General settings saved successfully")
        else:
            self.driver.find_element_by_xpath("//div[contains(@name,'parse_email_from_url')]//div//span//span").click()
            fprint(self, "Clicking the update configuration Button")
            self.driver.find_element_by_xpath("//button[normalize-space()='Update Configuration']").click()
            verify_success(self, "updated successfully")

    def test_08_disable_domain_in_General_settings(self):
        ''' Disabling the threat mailbox and rss feed to parse domain from the url '''
        nav_menu_admin(self, "Configuration")
        waitfor(self, 10, By.XPATH, "//div/span[contains(text(),'General')]", False)
        fprint(self, "Loading General Settings")
        if Build_Version.__contains__("3."):
            self.driver.find_element_by_xpath(
                "//h4[contains(text(),'Parse Domain')]//following::button[contains(text(),'Edit')]").click()
            fprint(self, "[Passed]-clicked on the edit button")
        else:
            self.driver.find_element_by_xpath("//div/span[contains(text(),'General')]").click()
        fprint(self, "Clicking the Url option")
        if waitfor(self, 5, By.XPATH, "//div[@name='parse_domain_from_email_address' and contains(@class,'disabled')]", False) or \
                waitfor(self, 1, By.XPATH, "//input[@name='parse_domain_from_url' and @value='false']", False):
            fprint(self, "Already Enabled")
        else:
            try:
                self.driver.find_element_by_xpath(
                    "//div[contains(@name,'parse_domain_from_url')]//div//span//span").click()
            except:
                self.driver.find_element_by_xpath("//span[@name='parse_domain_from_url']").click()
        fprint(self, "[Passed]-Unchecked the URL")

        fprint(self, "Selecting the email")
        if waitfor(self, 5, By.XPATH, "//div[@name='parse_domain_from_email_address' and contains(@class,'disabled')]", False) or \
                waitfor(self, 1, By.XPATH, "//input[@name='parse_domain_from_email_address' and @value='false']", False):
            fprint(self, "Already Enabled")
        else:
            try:
                self.driver.find_element_by_xpath(
                    "//div[contains(@name,'parse_domain_from_email_address')]//div//span//span").click()
            except:
                self.driver.find_element_by_xpath("//span[@name='parse_domain_from_email_address']").click()
        fprint(self, "Unchecked the email")

        fprint(self, "Selecting the parse email through Url ")
        if waitfor(self, 5, By.XPATH, "//div[@name='parse_email_from_url' and contains(@class,'disabled')]", False) or \
                waitfor(self, 1, By.XPATH, "//input[@name='parse_email_from_url' and @value='false']", False):
            fprint(self, "Already exist")
        else:
            try:
                self.driver.find_element_by_xpath(
                    "//div[contains(@name,'parse_email_from_url')]//div//span//span").click()
            except:
                self.driver.find_element_by_xpath("//span[@name='parse_email_from_url']").click()
        fprint(self, "[Passed]-Selecting the parse email through Url ")

        if Build_Version.__contains__("3."):
            self.driver.find_element_by_xpath("(//button[normalize-space()='Save'])[1]").click()
            fprint(self, "[Passed]-clicked on save button")
            verify_success(self, "General settings saved successfully")
        else:
            self.driver.find_element_by_xpath(
                    "//div[contains(@name,'parse_email_from_url')]//div//span//span").click()
            fprint(self, "Clicking the update configuration Button")
            self.driver.find_element_by_xpath("//button[normalize-space()='Update Configuration']").click()
            verify_success(self, "updated successfully")

    def test_09_verify_taxiiServer_stixType(self):
        fprint(self, "TC_ID 678009: test_09_verify_taxiiServer_stixType")
        self.enable_disable_stixType()
        fprint(self, "Navigating to the Subscriber page")
        nav_menu_admin(self, "Integration Management")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Subscribers ')]/parent::a")
        self.driver.find_element_by_xpath("//span[contains(text(),'Subscribers ')]/parent::a").click()
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'Add Subscriber')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add Subscriber')]").click()
        fprint(self, "Clicked on the Add Subscriber button")
        waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Subscriber Name *']")
        fprint(self, "Filling up all the mandatory fields")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Subscriber Name *']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Subscriber Name *']").send_keys("taxii_server")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name*']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name*']").send_keys("taxii_server")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Email *']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Email *']").send_keys("taxiiserver@cyware.com")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Confidence *']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Confidence *']").send_keys("90")
        self.driver.find_element_by_xpath("(//div[@name='collections'])[1]").click()
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'col_2.1')]/parent::div")
        self.driver.find_element_by_xpath("//div[contains(text(),'col_2.1')]/parent::div").click()
        self.driver.find_element_by_xpath("//button[@data-testid='save-subscribers']").click()
        fprint(self, "Clicked on the Save Subscriber button")
        verify_success(self, "Subscriber created successfully")
        fprint(self, "Checking TAXII-1 URL is present or not")
        if waitfor(self, 20, By.XPATH, "//p[contains(text(),'TAXII-1 URL')]", False):
            fprint(self, "Found TAXII-1 URL")
        else:
            fprint(self, "[Failed] TAXII-1 URL not found")
            self.fail("TAXII-1 URL not found")

        if not waitfor(self, 0, By.XPATH, "//p[contains(text(),'TAXII-2 URL')]", False):
            fprint(self, "TAXII-2 URL not found")
        else:
            fprint(self, "[Failed] TAXII-2 URL found, which is not expected")
            self.fail("TAXII-2 URL found, which is not expected")

        if not waitfor(self, 0, By.XPATH, "//p[contains(text(),'TAXII-2.1 URL')]", False):
            fprint(self, "TAXII-2.1 URL not found")
        else:
            fprint(self, "[Failed] TAXII-2.1 URL found, which is not expected")
            self.fail("TAXII-2.1 URL found, which is not expected")

        if not waitfor(self, 0, By.XPATH, "//div[@id='tab-misp']", False):
            fprint(self, "MISP Tab not found")
        else:
            fprint(self, "[Failed] MISP Tab found, which is not expected")
            self.fail("MISP Tab found, which is not expected")
        fprint(self, "[Passed] Not Found all the Disabled STIX Type, only Enabled one is visible.")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        fprint(self, "Making all values to there default status again...")
        self.enable_disable_stixType()

    def test_10_verify_taxiiServer_stixVersion(self):
        fprint(self, "TC_ID 678010: test_09_verify_taxiiServer_stixType")
        nav_menu_admin(self, "Configuration")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'TAXII Server')]/parent::a")
        self.driver.find_element_by_xpath("//span[contains(text(),'TAXII Server')]/parent::a").click()
        fprint(self, "Clicked on the TAXII Server tab")
        waitfor(self, 20, By.XPATH, "//h4[contains(text(),'STIX Version for TAXII Server 1.x')]")
        self.driver.find_element_by_xpath(
            "//h4[contains(text(),'STIX Version')]/ancestor::div[2]//button[contains(text(),'Edit')]").click()
        fprint(self, "Clicked on the Edit Option")
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'Save')]")
        self.driver.find_element_by_xpath("//div[@name='header']").click()
        waitfor(self, 20, By.XPATH, "//li[@id='list-item-0']")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        verify_success(self, "Settings saved successfully")

    def test_11_verify_taxiiServer_taxiiURL(self):
        fprint(self, "TC_ID 678011: test_11_verify_taxiiServer_taxiiURL")
        nav_menu_admin(self, "Configuration")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'TAXII Server')]/parent::a")
        self.driver.find_element_by_xpath("//span[contains(text(),'TAXII Server')]/parent::a").click()
        fprint(self, "Clicked on the TAXII Server tab")
        waitfor(self, 20, By.XPATH, "//h4[contains(text(),'STIX Version for TAXII Server 1.x')]")
        self.driver.find_element_by_xpath(
            "//h4[contains(text(),'STIX Version')]/ancestor::div[2]//button[contains(text(),'Edit')]").click()
        fprint(self, "Clicked on the Edit Option")
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'Save')]")
        self.driver.find_element_by_xpath("//div[@name='header']").click()
        waitfor(self, 20, By.XPATH, "//li[@id='list-item-0']")
        self.driver.find_element_by_xpath("//li[@id='list-item-0']").click()
        fprint(self, "Clicked on the Dropdown and selected STIX-1.1.1 option")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "Clicked on the Save button")
        verify_success(self, "Settings saved successfully")

    def test_12_verify_taxiiServer_rateLimit(self):
        fprint(self, "TC_ID 678012: test_12_verify_taxiiServer_rateLimit")
        nav_menu_admin(self, "Configuration")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'TAXII Server')]/parent::a")
        self.driver.find_element_by_xpath("//span[contains(text(),'TAXII Server')]/parent::a").click()
        fprint(self, "Clicked on the TAXII Server tab")
        waitfor(self, 20, By.XPATH, "//h3[contains(text(),'Rate Limit')]")
        self.driver.find_element_by_xpath(
            "//h3[contains(text(),'Rate Limit')]/ancestor::div[2]//button[contains(text(),'Edit')]").click()
        fprint(self, "Clicked on the Edit Option")
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'Save')]")
        self.driver.find_element_by_xpath("//input[@name='subscriber_api_limit_per_minute']").click()
        clear_field(self.driver.find_element_by_xpath("//input[@name='subscriber_api_limit_per_minute']"))
        self.driver.find_element_by_xpath("//input[@name='subscriber_api_limit_per_minute']").send_keys("99")
        fprint(self, "Per minute rate - 99")
        self.driver.find_element_by_xpath("//input[@name='subscriber_api_limit_per_hour']").click()
        clear_field(self.driver.find_element_by_xpath("//input[@name='subscriber_api_limit_per_hour']"))
        self.driver.find_element_by_xpath("//input[@name='subscriber_api_limit_per_hour']").send_keys("99")
        fprint(self, "Per hour rate - 99")
        self.driver.find_element_by_xpath("//input[@name='subscriber_api_limit_per_day']").click()
        clear_field(self.driver.find_element_by_xpath("//input[@name='subscriber_api_limit_per_day']"))
        self.driver.find_element_by_xpath("//input[@name='subscriber_api_limit_per_day']").send_keys("99")
        fprint(self, "Per day rate - 99")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "Clicked on the Save button")
        verify_success(self, "Settings saved successfully")

    def test_13_add_smtp_configuration(self):
        """
        Test case to enable smtp
        """
        fprint(self, "TC_ID 678013: Test case to add smtp setting in configuration")
        nav_menu_admin(self, "Configuration")
        waitfor(self, 10, By.XPATH, "//div/span[contains(text(),'General')]", False)
        fprint(self, "Loading General Settings")
        self.driver.find_element_by_xpath("(//h4[contains(text(),'Configure Email Server')]//following::button[contains(text(),'Edit')])[1]").click()
        fprint(self, "[Passed]-clicked on edit button successfully")
        self.driver.find_element_by_xpath("(//span[@class='cy-checkbox cy-flex'])[1]").click()
        fprint(self, "[Passed]-clicked on the checkbox")
        enable_smtp(self)
        fprint(self, "[Passed]-Test Case executed successfully")

    def test_14_disable_smtp_configuration(self):
        """ Test case to disable th smtp"""
        fprint(self, "TC_ID 678014: test case to disable the smtp in configuration ")
        nav_menu_admin(self, "Configuration")
        waitfor(self, 10, By.XPATH, "//div/span[contains(text(),'General')]", False)
        fprint(self, "Loading General Settings")
        self.driver.find_element_by_xpath(
            "(//h4[contains(text(),'Configure Email Server')]//following::button[contains(text(),'Edit')])[1]").click()
        fprint(self, "[Passed]-clicked on edit button successfully")
        self.driver.find_element_by_xpath("(//p[contains(text(),'All reports, OTP, communications etc. would be sen')]//following::div[contains(@class, 'cy-switch-btn__inner ')])[1]").click()
        fprint(self, "[Passed]-clicked on the toggle")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        fprint(self, "[Passed]-clicked on the save button successfully")
        verify_success(self, "General settings saved successfully")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
