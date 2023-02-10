import unittest
from lib.ui.nav_app import *


class RevokeIntel(unittest.TestCase):

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

    def test_01_revoke_intel(self):
        """
        Verify if Revoke Intel slider is working
        """
        nav_menu_main(self, "Dashboards")
        fprint(self, "----------- TC_ID 1: Verifying Revoke Intel slider is working ----------")
        waitfor(self, 2, By.XPATH, "//button[text()=' New']")
        self.driver.find_element_by_xpath("//button[text()=' New']").click()
        waitfor(self, 2, By.XPATH, "//li/*[contains(text(), 'Revoke Intel')]")
        self.driver.find_element_by_xpath("//li/*[contains(text(), 'Revoke Intel')]").click()
        waitfor(self, 2, By.XPATH, "//span[contains(text(),'Revoke Intel')]")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        fprint(self, "[PASSED] Revoke Intel slider is loading")
        process_console_logs(self)

    def test_02_revoke_history(self):
        """
        Verify if Revoke History slider is working
        """
        nav_menu_main(self, "Dashboards")
        fprint(self, "----------- TC_ID 1: Verifying Revoke Intel slider is working ----------")
        waitfor(self, 2, By.XPATH, "//button[text()=' New']")
        self.driver.find_element_by_xpath("//button[text()=' New']").click()
        waitfor(self, 2, By.XPATH, "//li/*[contains(text(), 'Revoke Intel')]")
        self.driver.find_element_by_xpath("//li/*[contains(text(), 'Revoke Intel')]").click()
        waitfor(self, 5, By.XPATH, "//button[contains(text(), 'Revoke History')]")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Revoke History')]").click()
        waitfor(self, 4, By.XPATH, "//span[contains(text(), 'Revoke History')]")
        if waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'No Revoke Intel(s) found!')]", False):
            fprint(self, "[PASSED] Revoke History slider working but no intel revoked")
        else:
            fprint(self, "[PASSED] Revoke history slider working as expected")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        process_console_logs(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
