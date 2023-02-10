import unittest
from lib.ui.nav_app import *

HANDLE_NAME = "@kumaryogesh2501"
ACCOUNT_TITLE = "test_twitter"
CONSUMER_KEY = "1RwEiPHlkm34CNX1aEZimqG9S"
CONSUMER_SECRET = "ImwNu94fe05jAuWeQ0iCmxDdVHYdOFiUdUPaMMdjcoibCJ3qhm"
ACCESS_TOKEN = "2901189860-KTATYOhkJMnMuIk4b6r2hAQ8IRKbB6N6UskSxcz"
TOKEN_SECRET = "MJqcx3BomNiGZT8a0JlH8COBg5i52GBbyb4YwNne6WCpw"
UPDATED_ACCOUNT_TITLE = "test_twitter_2"


class IntegrationTwitter(unittest.TestCase):

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

    Name = 'SA_AUT'
    API = '1RwEiPHlkm34CNX1aEZimqG9S'
    API_SECRET = 'ImwNu94fe05jAuWeQ0iCmxDdVHYdOFiUdUPaMMdjcoibCJ3qhm'
    ACCESS_TOKEN = '2901189860-KTATYOhkJMnMuIk4b6r2hAQ8IRKbB6N6UskSxcz'
    SECRET_KEY = 'MJqcx3BomNiGZT8a0JlH8COBg5i52GBbyb4YwNne6WCpw'

    def add_twitter_account_integration(self, name, api, api_secret, access_token, secret_key):
        """ Utiliy function to add the elements"""
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[Passed]-clicked on integration management successfully")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Integration Management')]")
        fprint(self, "[Passed]- Integration management loaded successfully")
        self.driver.find_element_by_xpath("//span[normalize-space()='Twitter']").click()
        fprint(self, "[Passed]-clicked on the twitter successfully")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Integration Management')]/span[contains(text(),'Twitter')]")
        fprint(self, "[Passed]-twitter integration loaded successfully")
        if waitfor(self, 10, By.XPATH, "//button[contains(text(),'Add')]", False):
            self.driver.find_element_by_xpath("//button[contains(text(),'Add')]").click()
        elif waitfor(self, 10, By.XPATH, "//button[@type='button']//span[contains(text(),'Add')]"):
            self.driver.find_element_by_xpath("//button[@type='button']//span[contains(text(),'Add')]").click()
        fprint(self, "[Passed]-clicked on add button successfully")
        waitfor(self, 10, By.XPATH, "//input[@aria-placeholder ='Account Title *']")
        fprint(self, "[Passed]-add page loaded successfully")
        self.driver.find_element_by_xpath("//input[@aria-placeholder ='Account Title *']").send_keys(name)
        fprint(self, "[Passed]-entered the title successfully")
        self.driver.find_element_by_xpath("//input[@aria-placeholder ='Consumer Key *']").send_keys(api)
        fprint(self, "[Passed]-consumer key fed successfully")
        self.driver.find_element_by_xpath("//input[@aria-placeholder ='Consumer Secret *']").send_keys(api_secret)
        fprint(self, "[Passed] entered the cunsomer secret key successfully")
        self.driver.find_element_by_xpath("//input[@aria-placeholder ='Access Token *']").send_keys(access_token)
        fprint(self, "[Passed]-entered th access token successfully")
        self.driver.find_element_by_xpath("//input[@aria-placeholder ='Token Secret *']").send_keys(secret_key)
        fprint(self, "[Passed]-entered the secret key successfully")
        self.driver.find_element_by_xpath("//span[@class='cy-checkbox cy-flex']").click()
        fprint(self, "[Passed]-clicked on the checkbox")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()

    def test_01_load_twitter(self):
        """
        Checking if Twitter sources pages are loading
        """
        nav_menu_admin(self, "Integration Management")
        fprint(self, "\n----------- TC_ID 1: Checking load screen of Twitter sources -----------")
        fprint(self, "Clicking on Twitter under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Twitter')]").click()
        if waitfor(self, 2, By.XPATH, "//button/span[contains(text(), 'Account')]", False):
            fprint(self, "[Passed] Page loading and no twitter account present")
        elif waitfor(self, 2, By.XPATH, "//button[contains(text(), 'Account')]", False):
            fprint(self, "[Passed] Page loading successfully and twitter accounts present")
        else:
            raise Exception("[Failed] Twitter Feed page failed to load")
        process_console_logs(self)

    def test_02_add_account(self):
        """
        Checking if twitter account can be added successfully

        returns: None
        """
        # Account Details
        fprint(self, "\n----------- TC_ID 2: Checking add account for Twitter sources -----------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "Clicking on Twitter under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Twitter')]").click()
        if waitfor(self, 4, By.XPATH, "//div/p[contains(text(), '"+ACCOUNT_TITLE+"')]", False) and \
                waitfor(self, 4, By.XPATH, "//div[div/span[contains(text(),'"+HANDLE_NAME+"')]]", False):
            fprint(self, "Deleting previously existing duplicate account")
            self.driver.find_element_by_xpath("//div[div/span[contains(text(),'"+HANDLE_NAME+"')]]/following-sibling::div/div[2]//button").click()
            fprint(self, "Clicked on Remove")
            waitfor(self, 2, By.XPATH, "//li/span[contains(text(), 'Remove')]")
            self.driver.find_element_by_xpath("//li/span[contains(text(), 'Remove')]").click()
            waitfor(self, 2, By.XPATH, "//button[contains(text(), 'Yes, Remove')]")
            self.driver.find_element_by_xpath("//button[contains(text(), 'Yes, Remove')]").click()
            verify_success(self, "Account removed successfully")
        if waitfor(self, 2, By.XPATH, "//button/span[contains(text(), 'Account')]", False):
            fprint(self, "[Passed] Page loading and no twitter account present")
            self.driver.find_element_by_xpath("//button/span[contains(text(), 'Account')]").click()
        elif waitfor(self, 2, By.XPATH, "//button[contains(text(), 'Account')]", False):
            fprint(self, "[Passed] Page loading successfully and twitter accounts present")
            self.driver.find_element_by_xpath("//button[contains(text(), 'Account')]").click()
        else:
            raise Exception("[Failed] Twitter Integration page failed to load")
        if waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Account Title']"):
            fprint(self, "[Passed] Slider to fill account details is now visible")
        fprint(self, "Filling in details of twitter account in the slider")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Account Title']").send_keys(ACCOUNT_TITLE)
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Consumer Key *']").send_keys(CONSUMER_KEY)
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Consumer Secret *']").send_keys(CONSUMER_SECRET)
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Access Token*']").send_keys(ACCESS_TOKEN)
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Token Secret *']").send_keys(TOKEN_SECRET)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Save')]").click()
        verify_success(self, "Account created successfully")
        if waitfor(self, 4, By.XPATH, "//div/p[contains(text(), '" + ACCOUNT_TITLE + "')]"):
            fprint(self, "[Passed] Account created successfully and verified")
        process_console_logs(self)

    def test_03_edit_twitter_source(self):
        """
        Checking if twitter account details can be edited

        returns: None
        """
        fprint(self, "\n----------- TC_ID 3: Checking edit account for Twitter sources -----------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "Clicking on Twitter under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Twitter')]").click()
        if waitfor(self, 4, By.XPATH, "//div/p[contains(text(), '"+ACCOUNT_TITLE+"')]") and \
                waitfor(self, 4, By.XPATH, "//div[div/span[contains(text(),'"+HANDLE_NAME+"')]]"):
            fprint(self, "Clicking on action menu for the created account")
            self.driver.find_element_by_xpath("//div[div/span[contains(text(),'" + HANDLE_NAME + "')]]/following-sibling::div/div[2]//button").click()
            waitfor(self, 2, By.XPATH, "//li/span[contains(text(), 'Edit')]")
            fprint(self, "Clicking on Edit from the Action menu")
            self.driver.find_element_by_xpath("//li/span[contains(text(), 'Edit')]").click()
        if waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Account Title']"):
            fprint(self, "[Passed] Slider to edit account details is now visible")
        fprint(self, "Updating the title of the twitter account ")
        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Account Title']"))
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Account Title']").send_keys(UPDATED_ACCOUNT_TITLE)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Save')]").click()
        fprint(self, '[Passed] Clicked on save for updated details')
        verify_success(self, "updated successfully")
        if waitfor(self, 4, By.XPATH, "//div/p[contains(text(), '"+UPDATED_ACCOUNT_TITLE+"')]") and \
                waitfor(self, 4, By.XPATH, "//div[div/span[contains(text(),'"+HANDLE_NAME+"')]]"):
            fprint(self, "[Passed] Account name updated successfully")
        process_console_logs(self)

    def test_04_twitter_connectivity(self):
        """
        Checking for twitter account connectivity

        returns: None
        """
        fprint(self, "\n----------- TC_ID 4: Checking for Twitter Account Connectivity -----------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "Clicking on Twitter under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Twitter')]").click()
        if waitfor(self, 4, By.XPATH, "//div/p[contains(text(), '"+UPDATED_ACCOUNT_TITLE+"')]") and \
                waitfor(self, 4, By.XPATH, "//div[div/span[contains(text(),'"+HANDLE_NAME+"')]]"):
            self.driver.find_element_by_xpath("//div/p[contains(text(), '"+UPDATED_ACCOUNT_TITLE+"')]").click()
        waitfor(self, 2, By.XPATH, "//button[contains(text(), 'Test Connectivity')]")
        fprint(self, "Clicking to check for connectivity of twitter account")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Test Connectivity')]").click()
        if waitfor(self, 2, By.XPATH, "//div/p/following-sibling::div//span[contains(text(), 'Working')]", False):
            fprint(self, "[Passed] Connectivity of twitter account is 'Working'")
        else:
            raise Exception("[Failed] Connectivity of twitter account is 'Broken'")
        process_console_logs(self)

    def test_05_disable_twitter(self):
        """
        Checking if account can be disabled successfully

        returns: None
        """
        fprint(self, "\n----------- TC_ID 5: Checking Disable action on created twitter account -----------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "Clicking on Twitter under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Twitter')]").click()
        if waitfor(self, 4, By.XPATH, "//div/p[contains(text(), '"+UPDATED_ACCOUNT_TITLE+"')]") and \
                waitfor(self, 4, By.XPATH, "//div[div/span[contains(text(),'"+HANDLE_NAME+"')]]"):
            fprint(self, "Clicking on action button for the twitter account")
            self.driver.find_element_by_xpath("//div[div/span[contains(text(),'" + HANDLE_NAME + "')]]/following-sibling::div/div[2]//button").click()
            waitfor(self, 2, By.XPATH, "//li[span[contains(text(), 'Disable')]]")
            fprint(self, "Clicking on disable from the action menu")
            self.driver.find_element_by_xpath("//li[span[contains(text(), 'Disable')]]").click()
        verify_success(self, "Account disabled successfully")
        waitfor(self, 5, By.XPATH, "//p[contains(text(), '"+UPDATED_ACCOUNT_TITLE+"')]/following-sibling::p[contains(text(),'Disabled')]")
        fprint(self, "[Passed] Account selected has been successfully disabled")
        process_console_logs(self)

    def test_06_enable_twitter(self):
        """
        Checking if twitter account can be enabled successfully

        returns: None
        """
        fprint(self, "\n----------- TC_ID 6: Checking Enable action on created Twitter Account -----------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "Clicking on Twitter under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Twitter')]").click()
        if waitfor(self, 4, By.XPATH, "//div/p[contains(text(), '"+UPDATED_ACCOUNT_TITLE+"')]") and \
                waitfor(self, 4, By.XPATH, "//div[div/span[contains(text(),'"+HANDLE_NAME+"')]]"):
            fprint(self, "Clicking in the action menu for the created account")
            self.driver.find_element_by_xpath("//div[div/span[contains(text(),'" + HANDLE_NAME + "')]]/following-sibling::div/div[2]//button").click()
            waitfor(self, 2, By.XPATH, "//li[span[contains(text(), 'Enable')]]")
            fprint(self, "Selecting Enable from the action menu")
            self.driver.find_element_by_xpath("//li[span[contains(text(), 'Enable')]]").click()
        verify_success(self, "Account enabled successfully")
        self.driver.find_element_by_xpath("//div[div/span[contains(text(),'" + HANDLE_NAME + "')]]/following-sibling::div/div[2]//button").click()
        waitfor(self, 2, By.XPATH, "//li[span[contains(text(), 'Disable')]]")
        fprint(self, "[Passed] Account selected has been successfully enabled")
        process_console_logs(self)

    def test_07_twitter_profile(self):
        """
        Checking for twitter profile redirection

        returns: None
        """
        fprint(self, "\n----------- TC_ID 7: Checking for twitter account redirection -----------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "Clicking on Twitter under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Twitter')]").click()
        if waitfor(self, 4, By.XPATH, "//div/p[contains(text(), '"+UPDATED_ACCOUNT_TITLE+"')]") and \
                waitfor(self, 4, By.XPATH, "//div[div/span[contains(text(),'"+HANDLE_NAME+"')]]"):
            waitfor(self, 5, By.XPATH, "//div[div/span[contains(text(),'"+HANDLE_NAME+"')]]/following-sibling::div//span/a")
            fprint(self, "Clicking on redirection to twitter account")
            self.driver.find_element_by_xpath\
                ("//div[div/span[contains(text(),'"+HANDLE_NAME+"')]]/following-sibling::div//span/a").click()
            sleep(3)
            fprint(self, "[Passed] Successfully Redirected to twitter account page")
            h = self.driver.window_handles
            fprint(self, "Redirecting back to CTIX")
            self.driver.switch_to.window(h[0])
            fprint(self, "[Passed] CTIX Redirection successful")
        else:
            fprint(self, "[Failed] Redirection to the selected twitter account failed")
        sleep(2)
        waitfor(self, 4, By.XPATH, "//div/p[contains(text(), '"+UPDATED_ACCOUNT_TITLE+"')]")
        fprint(self, "[Passed] Successfully redirected back to CTIX page")
        process_console_logs(self)

    def test_08_twitter_delete(self):
        """
        Checking if created account can be deleted successfully

        returns: None
        """
        fprint(self, "\n----------- TC_ID 8: Checking if created Twitter Account can be deleted -----------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "Clicking on Twitter under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Twitter')]").click()
        if waitfor(self, 4, By.XPATH, "//div/p[contains(text(), '"+ACCOUNT_TITLE+"')]", False) and \
                waitfor(self, 4, By.XPATH, "//div[div/span[contains(text(),'"+HANDLE_NAME+"')]]", False):
            fprint(self, "Clicking on action button for the twitter account")
            self.driver.find_element_by_xpath("//div[div/span[contains(text(),'"+HANDLE_NAME+"')]]/following-sibling::div/div[2]//button").click()
            waitfor(self, 2, By.XPATH, "//li/span[contains(text(), 'Remove')]")
            fprint(self, "Selecting remove operation from the action menu")
            self.driver.find_element_by_xpath("//li/span[contains(text(), 'Remove')]").click()
            waitfor(self, 2, By.XPATH, "//button[contains(text(), 'Yes, Remove')]")
            self.driver.find_element_by_xpath("//button[contains(text(), 'Yes, Remove')]").click()
            fprint(self, "[Passed] Successfully clicked on 'Yes, Remove'")
            verify_success(self, "Account removed successfully")
        sleep(2)
        if not waitfor(self, 4, By.XPATH, "//div/p[contains(text(), '"+UPDATED_ACCOUNT_TITLE+"')]", False):
            fprint(self, "[Passed] Twitter account is deleted successfully")
        else:
            raise Exception("[Failed] Failed to delete the created twitter account")
        process_console_logs(self)

    def test_09_verify_add_account(self):
        """ Test case to verify that the twitter account can be added successfully"""
        fprint(self, "TC_ID:15679 - to verify that the account can be added successfully")
        self.add_twitter_account_integration(self.Name, self.API, self.API_SECRET, self.ACCESS_TOKEN, self.SECRET_KEY)
        verify_success(self, "Account created successfully")
        fprint(self, "[Passed]-Account added successfully")

    def test_10_verify_account_added_successfully(self):
        """ Test case to verify that the account which is added is previous case is added sucessfully"""
        fprint(self, "TC_ID:156710  - to verify that the account added succesfully")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[Passed]-clicked on integration management successfully")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Integration Management')]")
        fprint(self, "[Passed]- Integration management loaded successfully")
        self.driver.find_element_by_xpath("//span[normalize-space()='Twitter']").click()
        fprint(self, "[Passed]-clicked on the twitter successfully")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Integration Management')]/span[contains(text(),'Twitter')]")
        fprint(self, "[Passed]-twitter integration loaded successfully")
        waitfor(self, 10, By.XPATH, "//p[contains(text(),'SA_AUT')]")
        fprint(self, "[Passed]-The account is added successfully")

    def test_11_same_account_cannot_be_addded(self):
        """ Test case to verify that the same account cannot be added"""
        fprint(self, "TC_ID:156711  - To verify that the same account cannot be added again")
        self.add_twitter_account_integration(self.Name, self.API, self.API_SECRET, self.ACCESS_TOKEN, self.SECRET_KEY)
        verify_success(self, "Source with this account handle already exists")
        fprint(self, "[Passed]-same account cannot be added again")

    def test_12_verify_name_is_mandatory(self):
        """
        Test case to verify that the name is mandatory
        """
        fprint(self, "TC_ID:156712  - To verify that the name is mandatory field")
        self.add_twitter_account_integration("", self.API, self.API_SECRET, self.ACCESS_TOKEN, self.SECRET_KEY)
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'This is a mandatory field')]")
        fprint(self, "[Passed]-verified that the name is mandatory field")

    def test_13_verify_consumer_key_is_required(self):
        """ Test case to verify that the keyword is mandatory field"""
        fprint(self, "TC_ID:156713  - To verify that the keyword is mandatory field")
        self.add_twitter_account_integration(self.Name, "", self.API_SECRET, self.ACCESS_TOKEN, self.SECRET_KEY)
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'This is a mandatory field')]")
        fprint(self, "[Passed]- Verified that the consumer feed is mandatory ")

    def test_14_verify_consumer_secret_is_mandatory(self):
        """ Test case to verify that the cosumer secret key is mandatory"""
        fprint(self, "TC_ID:156714  - To verify that the consumer secret key is mandatory")
        self.add_twitter_account_integration(self.Name, self.API, "", self.ACCESS_TOKEN, self.SECRET_KEY)
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'This is a mandatory field')]")
        fprint(self, "[Passed]- Verified that the consumer secret key is mandatory ")

    def test_15_verify_access_token_is_mandatory(self):
        """ test case to verify that the access token is mandatory"""
        fprint(self, "TC_ID:156715  - To verify that the access token is mandatory")
        self.add_twitter_account_integration(self.Name, self.API, self.API_SECRET, "", self.SECRET_KEY)
        waitfor(self, 10, By.XPATH, "///div[contains(text(),'This is a mandatory field')]")
        fprint(self, "[Passed]- Verified that the consumer secret key is mandatory ")

    def test_16_verify_Token_secret_is_mandatory(self):
        """ Test case to verify that the token secret is mandatory"""
        fprint(self, "TC_ID:156716  - To verify that the  token secret is mandatory")
        self.add_twitter_account_integration(self.Name, self.API, self.API_SECRET, self.ACCESS_TOKEN, "")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'This is a mandatory field')]")
        fprint(self, "[Passed]- Verified that the consumer secret key is mandatory ")

    def test_17_verify_that_wrong_cred_cannot_be_added(self):
        """test case to verify that account with wrong credentials cannot be added """
        fprint(self, "TC_ID:156717  - to verify that the wrong credentials cannot be added again")
        self.add_twitter_account_integration("testing", "123456", "78690", "90865", "gufdishjk")
        verify_success(self, "Twitter credentials are invalid. Please try again with valid credentials.")
        fprint(self, "[Passed]-Account added successfully")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
