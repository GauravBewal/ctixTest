import unittest
from lib.ui.nav_app import *
from selenium.webdriver import ActionChains


class QuickAddSliders(unittest.TestCase):

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

    def test_01_quick_add_rule(self):
        """
        Verify if Quick Add Rule slider is working
        """
        nav_menu_main(self, "Dashboards")
        fprint(self, "----------- TC_ID 1: Verifying Quick Add Rule slider is working ----------")
        waitfor(self, 2, By.XPATH, "//button[text()=' New']")
        self.driver.find_element_by_xpath("//button[text()=' New']").click()
        waitfor(self, 2, By.XPATH, "//li/*[contains(text(), 'Rule')]")
        self.driver.find_element_by_xpath("//li/*[contains(text(), 'Rule')]").click()
        if waitfor(self, 2, By.XPATH, "//button[text()='Skip']", False):
            fprint(self, "[PASSED] Redirection to rules working walk through presented")
            self.driver.find_element_by_xpath("//button[text()='Skip']").click()
        waitfor(self, 2, By.XPATH, "//div[text()='Add Rule']")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        fprint(self, "[PASSED] Quick Add Rule slider is working")
        process_console_logs(self)

    def test_02_quick_add_stix_source(self):
        """
        Verify if Quick Add STIX Source slider is working
        """
        nav_menu_main(self, "Dashboards")
        actions = ActionChains(self.driver)
        fprint(self, "----------- TC_ID 2: Verifying Quick Add STIX Source slider is working ----------")
        waitfor(self, 2, By.XPATH, "//button[text()=' New']")
        self.driver.find_element_by_xpath("//button[text()=' New']").click()
        waitfor(self, 2, By.XPATH, "//a[contains(text(), 'STIX Source')]")
        ele = self.driver.find_element_by_xpath("//a[contains(text(), 'STIX Source')]")
        actions.move_to_element(ele).click().perform()
        waitfor(self, 5, By.XPATH, "//div[contains(text(), 'Add  STIX Source')]")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        fprint(self, "[PASSED] Quick add STIX source slider is working")
        process_console_logs(self)

    def test_03_quick_add_user(self):
        """
        Verify if quick add user slider is working
        """
        nav_menu_main(self, "Dashboards")
        actions = ActionChains(self.driver)
        fprint(self, "----------- TC_ID 3: Verifying Quick Add User slider is working ----------")
        waitfor(self, 2, By.XPATH, "//button[text()=' New']")
        self.driver.find_element_by_xpath("//button[text()=' New']").click()
        waitfor(self, 2, By.XPATH, "//a[text()='User']")
        ele = self.driver.find_element_by_xpath("//a[text()='User']")
        actions.move_to_element(ele).click().perform()
        waitfor(self, 5, By.XPATH, "//div[contains(text(), 'New User')]")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        fprint(self, "[PASSED] Quick add User slider is working")
        process_console_logs(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())