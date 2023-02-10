import unittest

from lib.ui.nav_app import *
from lib.common_functions import *


class Initial_Change_Password(unittest.TestCase):

    # No class methods will be intentionally executed for this particular case.

    def test_01_First_Login_Change_Password(self):
        """
        This test case checks if the change password screen appears on first login
        """
        fprint(self, "TC_ID: 110 - Verify if the Change Password Screen appears on the first login")
        self.driver = initialize_browser(self)
        #clear_console_logs(self)
        login(self, Admin_Email, First_Password)
        if waitfor(self, 2, By.XPATH, "//p[contains(text(),'Please set your password')]", False) or \
                waitfor(self, 2, By.XPATH, "//p[contains(text(),'Create Password')]", False):
            fprint(self, "Checkpoint 1: [Passed] Change Password Screen appears on First Login")

            if waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='Current Password*']", False):
                self.driver.find_element_by_xpath("//input[@aria-placeholder='Current Password*']").send_keys(First_Password)
            elif waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='Enter Current Password *']"):
                self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter Current Password *']").send_keys(First_Password)

            fprint(self, "Checkpoint 2: [Passed] Entered Current Password in the text field")
            if waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='New Password*']", False):
                self.driver.find_element_by_xpath("//input[@aria-placeholder='New Password*']").send_keys(Admin_Password)
            elif waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='Enter New Password *']"):
                self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter New Password *']").send_keys(Admin_Password)

            fprint(self, "Checkpoint 3: [Passed] Entered New Password in the text field")
            if waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='Confirm your new password*']", False):
                self.driver.find_element_by_xpath("//input[@aria-placeholder='Confirm your new password*']").send_keys(Admin_Password)
            elif waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='Confirm New Password *']"):
                self.driver.find_element_by_xpath("//input[@aria-placeholder='Confirm New Password *']").send_keys(Admin_Password)

            fprint(self, "Checkpoint 4: [Passed] Entered new password in the 'Confirm New Password' text field")
            if waitfor(self, 2, By.XPATH, "//button[contains(text(),'Save & Launch Dashboard')]", False):
                self.driver.find_element_by_xpath("//button[contains(text(),'Save & Launch Dashboard')]").click()
                fprint(self, "Checkpoint 5: Clicked on 'Save & Launch' Dashboard button, waiting for Main screen to load")
            elif waitfor(self, 2, By.XPATH, "//button[contains(text(),'Set Password')]"):
                self.driver.find_element_by_xpath("//button[contains(text(),'Set Password')]").click()
                fprint(self, "Checkpoint 5: Clicked on 'Set Password' button, waiting for License/Main screen to load")
            # Todo: License Keys need to be saved properly in a testdata sheet outside the code, validation is not present for now.
            fprint(self, "Check if Upload license key field is present")
            if waitfor(self, 15, By.XPATH, "//input[@aria-placeholder='Enter License Key*']", False):
                fprint(self, "License Key field is present, Entering License")
                if APP_URL.__contains__("v3qaautomation."):
                    self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter License Key*']").send_keys("9b3b3f77-b957-46d8-a43b-de91d9fe63d5")
                elif APP_URL.__contains__("v3qa."):
                    self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter License Key*']").send_keys("b34cd362-588d-49a9-95f6-85cefc35c003")
                elif APP_URL.__contains__("bugbasket."):
                    self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter License Key*']").send_keys("6acbf04f-d66c-44fb-b0d6-608eaa3b6682")
                elif APP_URL.__contains__("v3qadev."):
                    self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter License Key*']").send_keys("02acea01-f0ef-4c38-8b27-821084c03fc7")
                elif APP_URL.__contains__("uiauto"):
                    self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter License Key*']").send_keys("6acbf04f-d66c-44fb-b0d6-608eaa3b6682")
                elif APP_URL.__contains__("qatest1"):
                    self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter License Key*']").send_keys("e2cc7ae3-f9e0-4ca6-a0f1-2caf667a2c71")
                else:
                    fprint(self, "PLEASE PROVIDE A VALID LICENSE KEY FOR YOUR MACHINE")
                fprint(self,
                       "Checkpoint 7: Entered License Key")
                sleep(1)
                self.driver.find_element_by_xpath("//button[contains(text(),'Save & Launch Dashboard')]").click()
                fprint(self, "Checkpoint 8: Clicked on 'Save & Launch' Dashboard button, waiting for Main screen to load")
                sleep(5)
            waitfor(self, 30, By.XPATH, "//i[@class='cyicon-menu']")
            #process_console_logs(self)
            self.driver.quit()

    def test_02_if_New_Password_Works(self):
        """
        This test case checks if the password was changed properly during the first login.
        """

        fprint(self, "TC_ID: 111 - Verify if the new password works")
        self.driver = initialize_browser(self)
        #clear_console_logs(self)
        fprint(self, "Checkpoint 1: Logging in with new Password")
        login(self, Admin_Email, Admin_Password)
        fprint(self, "Checkpoint 2: [Passed] Logged in successfully")
        #process_console_logs(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
