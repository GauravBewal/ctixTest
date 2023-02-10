import unittest
from lib.ui.nav_app import *
from lib.ui.quick_add import quick_create_ip


class Notifications(unittest.TestCase):

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

    def test_01_notification_load(self):
        """
        Validate if notifications page is loading
        """
        fprint(self, "\n----------- TC_ID 1: Testing if notifications slider is loading properly")
        nav_menu_main(self, "Dashboards")
        waitfor(self, 5, By.XPATH, "//a[@aria-current='page']/i[contains(@class,'notification')]")
        self.driver.find_element_by_xpath("//a[@aria-current='page']/i[contains(@class,'notification')]").click()
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'Notifications')]/following-sibling::span/i[2]")
        if waitfor(self, 2, By.XPATH, "//div[span[contains(text(),'Notifications')]]/following-sibling::div/div", False):
            fprint(self, "[PASSED] Notifications found in notifications slider")
        else:
            fprint(self, "[PASSED] No Notifications found in the slider")
        fprint(self, "[PASSED] Notifications slider is working as expected")
        process_console_logs(self)

    def test_02_mark_all_as_read(self):
        """
        Validate if notifications page is loading
        """
        self.driver.refresh()
        sleep(5)
        if Build_Version.__contains__("2."):
            fprint(self, "\n----------- TC_ID 2: Testing if mark all as read working properly")
            fprint(self, "Adding a intel via quick add for getting a notification")
            quick_create_ip(self, "131.159.198.10", "HS_AUTOMATE")
            nav_menu_main(self, "Dashboards")
            waitfor(self, 5, By.XPATH, "//a[@aria-current='page']/i[contains(@class,'notification')]")
            self.driver.find_element_by_xpath("//a[@aria-current='page']/i[contains(@class,'notification')]").click()
            waitfor(self, 5, By.XPATH, "//span[contains(text(),'Notifications')]/following-sibling::span/i[2]")
            self.driver.find_element_by_xpath("//span[contains(text(),'Notifications')]/following-sibling::span/i[2]").click()
            sleep(2)
            self.driver.refresh()
            sleep(4)
            waitfor(self, 5, By.XPATH, "//a[@aria-current='page']/i[contains(@class,'notification')]")
            after_val = ""
            if waitfor(self, 5, By.XPATH, "//i[@class='cyicon-notification-active']/following-sibling::span", False):
                after_val = self.driver.find_element_by_xpath("//i[@class='cyicon-notification-active']/following-sibling::span").text
            else:
                pass
            if after_val == "":
                fprint(self, "[PASSED] Mark all as read is working correctly")
            else:
                fprint(self, "[FAILED] Mark all as read is not working as expected")
            process_console_logs(self)
        else:
            # For V3QA the notification icon is not present as of now
            pass

if __name__ == '__main__':
    unittest.main(testRunner=reporting())


