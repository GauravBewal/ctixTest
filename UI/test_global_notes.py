import unittest
from lib.ui.nav_app import *


class GlobalNotes(unittest.TestCase):

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

    def test_01_my_notes(self):
        """
        Verify if my notes page is loading
        """
        fprint(self, "\n---------- TC_ID 1: Validate if my notes page is loading ------------")
        nav_menu_main(self, "Dashboards")
        self.driver.find_element_by_xpath("//a[@href='/ctix/global-notes']").click()
        waitfor(self, 2, By.XPATH, "//h1[contains(text(),'Global Notes')]")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'My Notes')]").click()
        if waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'My Notes')]", False):
            fprint(self, "[PASSED] Page loading with notes")
        elif waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'No Notes found!')]", False):
            fprint(self, "[PASSED] Page loading but no notes to display")
        else:
            fprint(self, "[FAILED] Page not loading as expected")
            raise WebDriverException("Page Failed to load properly")
        fprint(self, "My Notes page load tested successfully")
        process_console_logs(self)

    def test_02_shared_notes(self):
        """
        Verify if shared notes page is loading
        """
        fprint(self, "\n--------- TC_ID 2: Validate if shared notes page is loading as expected ----------")
        nav_menu_main(self, "Dashboards")
        self.driver.find_element_by_xpath("//a[@href='/ctix/global-notes']").click()
        waitfor(self, 2, By.XPATH, "//h1[contains(text(),'Global Notes')]")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Shared With Me')]").click()
        if waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'Shared With Me')]", False):
            fprint(self, "[PASSED] Page loading with notes")
        elif waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'No Notes found!')]", False):
            fprint(self, "[PASSED] Page loading but no notes to display")
        else:
            fprint(self, "[FAILED] Page not loading as expected")
            raise WebDriverException("Page Failed to load properly")
        fprint(self, "Shared Notes page load tested successfully")
        process_console_logs(self)

    def test_03_all_notes(self):
        """
        Verify if all notes page is loading
        """
        fprint(self, "\n--------- TC_ID 3: Validate if all notes page is loading as expected ----------")
        nav_menu_main(self, "Dashboards")
        self.driver.find_element_by_xpath("//a[@href='/ctix/global-notes']").click()
        waitfor(self, 2, By.XPATH, "//h1[contains(text(),'Global Notes')]")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'All Notes')]").click()
        if waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'All Notes')]", False):
            fprint(self, "[PASSED] Page loading with notes")
        elif waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'No Notes found!')]", False):
            fprint(self, "[PASSED] Page loading but no notes to display")
        else:
            fprint(self, "[FAILED] Page not loading as expected")
            raise WebDriverException("Page Failed to load properly")
        fprint(self, "All Notes page load tested successfully")
        process_console_logs(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
