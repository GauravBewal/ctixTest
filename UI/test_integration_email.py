import unittest
from lib.ui.nav_app import *
from lib.ui.threat_mailbox import *


class IntegrationEmail(unittest.TestCase):

    TITLE = "TESTINAUTO9"
    USERNAME = "testin.auto9@gmail.com"
    PASSWORD = "oawcueontwaedtnj"
    DOMAIN = "pop.gmail.com"

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

    def perform_action(self, **kwargs):
        action = kwargs.get('action')
        fprint(self, "Searching for the created source")
        waitfor(self, 5, By.XPATH, "//div/input[@placeholder='Search or filter results']")
        self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']").click()
        clear_field(self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']"))
        sleep(1)
        self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']").send_keys(self.TITLE)
        self.driver.find_element_by_xpath("//i[@data-testid='filter-search-icon']").click()
        if waitfor(self, 20, By.XPATH, "//div/p[contains(text(), '"+self.TITLE+"')]"):
            sleep(1)
            if str(action) == "View Collections":
                fprint(self, "Click on " + self.TITLE)
                if Build_Version.__contains__("3."):
                    self.driver.find_element_by_xpath("//div[p[contains(text(), '" + self.TITLE + "')]]").click()
                else:
                    self.driver.find_element_by_xpath("//button[@data-testid='action']").click()
                    waitfor(self, 10, By.XPATH, "//li[contains(text(),'View Collections')]")
                    self.driver.find_element_by_xpath("//li[contains(text(),'View Collections')]").click()
            else:
                fprint(self, "Click on Options Menu")
                self.driver.find_element_by_xpath("//div[p[contains(text(), '" + self.TITLE + "')]]//button[span]").click()
                waitfor(self, 2, By.XPATH, "//li[contains(text(), '"+action+"')]")
                fprint(self, "Click on Menu item: " + action)
                self.driver.find_element_by_xpath("//li[contains(text(), '"+action+"')]").click()

    def test_01_load_email(self):
        """
        Checking if Email sources pages are loading

        returns: None
        """
        add_source_button = "//button[contains(text(),'Email')]"
        nav_menu_admin(self, "Integration Management")
        fprint(self, "\n----------- TC_ID 1: Checking load screen of Email sources -----------")
        fprint(self, "Clicking on Email under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Email')]").click()
        fprint(self, "Validating if 'Add Email Source button is present'")
        if waitfor(self, 2, By.XPATH, add_source_button):
            fprint(self, "[Passed] Page for Email Source is loading as expected")
        sleep(2)
        process_console_logs(self)

    def test_02_add_account(self):
        """
        Checking if email account can be added successfully

        returns: None
        """
        fprint(self, "TC_ID: 5500290 - test_02_add_account")
        add_source_button = "//button[contains(text(),'Email')]"
        nav_menu_admin(self, "Integration Management")
        fprint(self, "Clicking on Email under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Email')]").click()
        fprint(self, "Searching if source already exists")
        if waitfor(self, 10, By.XPATH, "//div/input[@placeholder='Search or filter results']", False):
            self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']").click()
            clear_field(self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']"))
            sleep(1)
            self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']").send_keys(self.TITLE)
            self.driver.find_element_by_xpath("//i[@data-testid='filter-search-icon']").click()
        if waitfor(self, 10, By.XPATH, "//div/p[contains(text(), '"+self.TITLE+"')]", False):
            fprint(self, "Deleting the source that is already present")
            self.perform_action(action='Delete')
            waitfor(self, 10, By.XPATH, "//button[@name='Delete']")
            self.driver.find_element_by_xpath("//button[@name='Delete']").click()
            verify_success(self, "Selected Source deleted successfully")
            fprint(self, "[Passed] Existing source has been deleted successfully")
            process_console_logs(self)
        fprint(self, "Validating if 'Add Email Source button is present'")
        waitfor(self, 10, By.XPATH, add_source_button)
        self.driver.find_element_by_xpath(add_source_button).click()
        add_email_source(self, title=self.TITLE, username=self.USERNAME, password=self.PASSWORD, domain=self.DOMAIN,
                         type="POP 3", auto_create=False)
        waitfor(self, 10, By.XPATH, "//div/input[@placeholder='Search or filter results']")
        self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']").click()
        clear_field(self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']"))
        fprint(self, "Searching for the Email source added")
        self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']").send_keys(self.TITLE)
        self.driver.find_element_by_xpath("//i[@data-testid='filter-search-icon']").click()
        if waitfor(self, 10, By.XPATH, "//div/p[contains(text(), '"+self.TITLE+"')]", False):
            fprint(self, "[Passed] Email Source added successfully!")
        sleep(2)
        process_console_logs(self)

    def test_03_email_collections(self):
        """
        Checking for collections in the mailbox created

        returns: None
        """
        nav_menu_admin(self, "Integration Management")
        fprint(self, "\n-------------- TC-ID 3: Checking if email source collections page is loading -------------")
        fprint(self, "Clicking on Email under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Email')]").click()
        sleep(2)
        fprint(self, "Selecting View Collections from the action menu for "+self.TITLE)
        self.perform_action(action='View Collections')
        waitfor(self, 5, By.XPATH, "//h1[contains(text(),'Collections of "+self.TITLE+"')]")
        fprint(self, "Collections page for "+self.TITLE+" loaded successfully")
        sleep(2)
        process_console_logs(self)

    def test_04_email_follow(self):
        """
        Checking if email source can be followed

        returns: None
        """
        nav_menu_admin(self, "Integration Management")
        fprint(self, "\n-------------- TC-ID 4: Checking if email source can be followed -------------")
        fprint(self, "Clicking on Email under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Email')]").click()
        sleep(2)
        fprint(self, "Selecting Follow from the action menu")
        self.perform_action(action='Follow')
        verify_success(self, 'Email Source followed successfully')
        fprint(self, "[Passed] Selected source is being followed successfully")
        sleep(2)
        process_console_logs(self)

    def test_05_email_unfollow(self):
        """
        Checking if email source can be followed

        returns: None
        """
        nav_menu_admin(self, "Integration Management")
        fprint(self, "\n-------------- TC-ID 5: Checking if email source can be unfollowed -------------")
        fprint(self, "Clicking on Email under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Email')]").click()
        sleep(2)
        fprint(self, "Selecting Unfollow from the action menu")
        self.perform_action(action='Unfollow')
        verify_success(self, 'Email Source Unfollowed successfully')
        fprint(self, '[Passed] Selected source is unfollowed successfully')
        sleep(2)
        process_console_logs(self)

    def test_06_email_delete(self):
        nav_menu_admin(self, "Integration Management")
        fprint(self, "\n-------------- TC-ID 6: Checking if email source can be deleted -------------")
        fprint(self, "Clicking on Email under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Email')]").click()
        sleep(2)
        fprint(self, "Selecting Delete from the action menu")
        self.perform_action(action='Delete')
        waitfor(self, 2, By.XPATH, "//button[@name='Delete']")
        sleep(2)
        fprint(self, "Selecting delete from the displayed popup")
        self.driver.find_element_by_xpath("//button[@name='Delete']").click()
        verify_success(self, "Selected Source deleted successfully")
        sleep(1)
        self.driver.refresh()
        if waitfor(self, 2, By.XPATH, "//div/p[contains(text(), '"+self.TITLE+"')]", False):
            raise Exception("[Failed] Email Source is not deleted")
        else:
            fprint(self, "[Passed] Source is deleted successfully")
        sleep(2)
        process_console_logs(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
