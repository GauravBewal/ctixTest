import unittest
from lib.ui.nav_app import *


class IntelPackage(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.driver = initialize_browser(self)
        login(self, Admin_Email, Admin_Password)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    @classmethod
    def setUp(self):
        process_console_logs(self)

    def test_01_intelpackage_importpackage(self):
        fprint(self, "TC_ID: 1 - Import Package")
        nav_menu_main(self, "Intel Package")
        waitfor(self, 2, By.XPATH, "//h1[contains(text(),'Intel Packages')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Refresh')]/ancestor::div[1]/following-sibling::div[1]//button").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(),'Import File')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Select Format*')]/ancestor::div[@tabindex='0']").click()
        self.driver.find_element_by_xpath("//div[contains(text(),'STIX 2.1')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Select Collection *')]/ancestor::div[@tabindex='0']").click()
        sleep(2)
        self.driver.find_element_by_xpath("//div[contains(text(),'Free Text')]").click()
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        process_console_logs(self)

    def test_02_intelpackage_refresh(self):
        fprint(self, "TC_ID: 2 - Refresh Page")
        self.driver.find_element_by_xpath("//button[contains(text(),'Refresh')]").click()
        fprint(self, "Page refreshed successfully !")
        process_console_logs(self)

    def test_03_intelpackage_exportpackage(self):
        fprint(self, "TC_ID: 3 - Export Intel Package")
        self.driver.find_element_by_xpath("//button[contains(text(),'Refresh')]/ancestor::div[1]/following-sibling::div[2]").click()
        waitfor(self, 2, By.XPATH, "//li[contains(text(),'THREAT SPEC')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'THREAT SPEC')]").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(),'Your file will be downloaded in a moment')]")
        process_console_logs(self)
        print("Your file will be downloaded in a moment")


if __name__ == '__main__':
    unittest.main()
