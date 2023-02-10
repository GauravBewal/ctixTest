import unittest
from lib.ui.nav_app import *
from lib.common_functions import *
from selenium.webdriver.common.keys import Keys
import pandas as pd


def clear_field(element):
    while len(element.get_attribute("value")) > 0:
        element.send_keys(Keys.BACK_SPACE)


class ExampleSuiteName(unittest.TestCase):


    @classmethod
    def setUpClass(self):
        # Any code written here will get executed at the very beginning in this script (only once)
        print("")

    @classmethod
    def tearDownClass(self):
        # Any code written here gets executed at the end of the whole script. (only once)
        print("")

    @classmethod
    def setUp(self):
        # Any code written here will get executed at the beginning of every test case (before every test case)
        print("")

    def tearDown(self):
        # Any code written here will get executed at the end of every test case (after every test case)
        if hasattr(self, 'driver'):
            self.driver.quit()

    def test_01_write_n_read_a_setting(self):
        """
        This is a non destructive setting, Once set it will remain until updated.
        This can be read in another script as well.
        """
        fprint(self, "TC_ID: 5000 - Check if automation executing user has write access")
        fprint(self, "Checkpoint 1: Writing a value to the settings - color=>red")
        given_value = "red"
        set_value("color", given_value)
        fprint(self, "Checkpoint 2: Reading value from settings - for key color")
        output = get_value("color")
        fprint(self, "Checkpoint 3: Found value of key color=>" + output)
        if output == given_value:
            fprint(self, "Checkpoint 4: Test case is passed")
        else:
            fprint(self, "Checkpoint 4: Failed - Values are not same")

    def test_02_navigate_to_a_menu(self):
        fprint(self, "TC_ID: 5001 - Check if login works and navigate to Threat Mailbox")
        self.driver = initialize_browser(self)
        fprint(self, "Navigating to App URL")
        self.driver.get(APP_URL)
        login(self, Admin_Email, Admin_Password)
        fprint(self, "Checkpoint 1: Passed - Logged in the application, Navigating to Threat Mailbox")
        nav_menu_main(self, "Threat Mailbox")
        fprint(self, "Checkpoint 2: Passed - Threat Mailbox page is visible")

    def test_03_deliberate_fail_login_case(self):
        fprint(self, "TC_ID: 5002 - Negative Test - Check if failure is detected when login doesn't work")
        self.driver = initialize_browser(self)
        fprint(self, "Navigating to App URL")
        self.driver.get(APP_URL)
        login(self, Admin_Email, "This_is_incorrect_password")
        fprint(self, "Checkpoint 1: Passed - Logged in the application, Navigating to Threat Mailbox")
        nav_menu_main(self, "Threat Mailbox")
        fprint(self, "Checkpoint 2: Passed - Threat Mailbox page is visible")

    def test_04_deliberate_fail_page_missing_case(self):
        fprint(self, "TC_ID: 5003 - Negative Test - Check if failure is detected when page doesn't exist")
        self.driver = initialize_browser(self)
        fprint(self, "Navigating to App URL")
        self.driver.get(APP_URL)
        login(self, Admin_Email, Admin_Password)
        fprint(self, "Checkpoint 1: [Passed] - Logged in the application, Negative Case - Navigating to Non Existing Menu item")
        nav_menu_main(self, "Non_Existing_Menu_item")
        fprint(self, "Checkpoint 2: [Passed] - Non Existing Menu item is visible now")

    def xtest_05_override_exception_testing_only(self):
        # Disabled, This case is not implemented yet - We will release it with Selenium 4 release
        fprint(self, "TC_ID: 5004 - Check if we are overriding exceptions and capturing errors")
        self.driver = initialize_browser(self)
        self.driver.get(APP_URL)
        login(self, Admin_Email, Admin_Password)
        # This should throw ElementNotInteractableException exception, Research on custom listener implementation
        self.driver.find_element_by_xpath("//span[contains(text(),'Rules')]/ancestor::a").click()

    def xtest_06_read_csv_file(self):
        # Disabled, Demonstration - How to read a CSV File
        fprint(self, "TC_ID: 5005 - How to read a csv file")
        self.fail("This test case is failed")
        testcaseid = 1212
        known_failures = os.path.join(os.environ["PYTHONPATH"], "jenkins", "known_failures.csv")
        df = pd.read_csv(known_failures)
        comment = None
        for index, row in df.iterrows():
            if row[0] == testcaseid:
                comment = row[1]
                break  # break with the first reason itself.
        print(comment)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
