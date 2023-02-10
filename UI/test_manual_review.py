import unittest
from lib.ui.nav_app import *


class ManualReview(unittest.TestCase):

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

    def test_01_ManualReview_ThreatData_Packages_IntelInbox_PageLoad(self):
        fprint(self, "TC_ID: 1 - ManualReview - ThreatData_Packages_IntelInbox_PageLoad" + uniquestr)
        nav_menu_main(self, "Manual Review")
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Threat Data')]")
        process_console_logs(self)
        fprint(self, "TC_ID: 1 - Manual Review - Threat Data Page Load is verified")

        self.driver.find_element_by_xpath("//span[@class='cy-page-menu__text' and contains(text(),'Packages')]").click()
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Packages')]")
        process_console_logs(self)
        fprint(self, "TC_ID: 1 - Manual Review - Packages Page Load is verified")

        self.driver.find_element_by_xpath("//span[@class='cy-page-menu__text' and contains(text(),'Intel Inbox')]").click()
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Intel Inbox')]")
        process_console_logs(self)
        fprint(self, "TC_ID: 1 - Manual Review - Intel Inbox Page Load is verified")

    #commenting this as Threat visualizer is being renamed to Threat Investigations. We would not need this for production as of now.
    def ctest_02_ManualReview_ThreatData_ViewInThreatVisualizer_PageLoad(self):
        fprint(self, "TC_ID: 2 - ManualReview - ThreatData_View In ThreatVisualizer_PageLoad" + uniquestr)
        nav_menu_main(self, "Manual Review")
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Threat Data')]")
        waitfor(self, 5, By.XPATH, "//*[contains(text(),'View in Threat Visualizer')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'View in Threat Visualizer')]").click()
        fprint(self, "TC_ID: 2 - Manual Review - Clicked on ThreatVisualizer button")
        waitfor(self, 5, By.XPATH, "//*[contains(text(),'Cancel')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Cancel')]").click()
        process_console_logs(self)
        fprint(self, "TC_ID: 2 - Manual Review - ThreatData_View In ThreatVisualizer button click is verified for console errors")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
