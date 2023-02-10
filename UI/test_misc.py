import unittest
from lib.ui.smtp import *

def_users = ['sanjai@cyware.com',
             'anushka.bajaj@cyware.com',
             'madhuri.karanth@cyware.com',
             'sharada.jayaprakash@cyware.com',
             'aniket.bhardwaj@cyware.com',
             'vishwendra.chauhan@cyware.com',
             'mridhula.shetty@cyware.com',
             'jyothi@cyware.com',
             'smsanjai@cyware.com']


class Misc(unittest.TestCase):

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

    def test_01_add_default_users(self):
        """
        Verify if My Profile page is loading
        """
        fprint(self, "----------- TC_ID: 1311 Verifying if my profile page is loading ----------")
        fprint(self, "User Not Found, Disabling SMTP")
        fprint(self, "Switching to Configuration page")
        nav_menu_admin(self, "Configuration")
        waitfor(self, 5, By.XPATH, "//div[h4[normalize-space(text())='Configure Email Server']]"
                                   "/following-sibling::div//button[text()='Edit']")
        self.driver.find_element_by_xpath("//div[h4[normalize-space(text())='Configure Email Server']]"
                                          "/following-sibling::div//button[text()='Edit']").click()
        fprint(self, "Enabling SMTP")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'SMTP Over TLS')]")
        fprint(self, "Enabled state is visible, filling up the credentials")
        fprint(self, "Clicking on the SMTP Tab")
        self.driver.find_element_by_xpath("//span[contains(text(),'SMTP')]").click()
        fprint(self, "Waiting for the Enable/Disable Toggle Button")
        enable_smtp(self)
        fprint(self, "Switching back to User Management page")
        nav_menu_admin(self, "User Management")
        for i in def_users:
            if waitfor(self, 2, By.XPATH, "//div[span[contains(text(), 'Users not found')]]", False):
                self.driver.find_element_by_xpath(
                    "//div[span[contains(text(), 'Users not found')]]/following-sibling::div/"
                    "button[normalize-space(text())='Add User']").click()
            else:
                self.driver.find_element_by_xpath("//button[@data-testid='new-user']").click()
            fprint(self, "Creating a new user - " + i.split('@')[0])
            waitfor(self, 20, By.XPATH, "//input[@name='first_name']")
            sleep(2)
            fprint(self, "Putting values into the fields")
            self.driver.find_element_by_xpath("//input[@name='first_name']").send_keys(i.split('@')[0].split(".")[0])
            self.driver.find_element_by_xpath("//input[@name='last_name']").send_keys("Temp")
            if waitfor(self, 5, By.XPATH, "//input[@name='username']", False):
                self.driver.find_element_by_xpath("//input[@name='username']").send_keys(i.split('@')[0].split(".")[0])
            self.driver.find_element_by_xpath("//input[@name='email']").send_keys(i)
            self.driver.find_element_by_xpath("(//div[@name='groups'])[1]").click()
            waitfor(self, 5, By.XPATH, "//div/div[text()='Admin']")
            self.driver.find_element_by_xpath("//div/div[text()='Admin']").click()
            self.driver.find_element_by_xpath("//button[@data-testid='save-users']").click()
            verify_success(self, "User created successfully")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
