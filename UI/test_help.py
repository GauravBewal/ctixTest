import unittest
from lib.ui.nav_app import *
from lib.common_functions import *


class HelpDocumentation(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.driver = initialize_browser(self)
        login(self, Admin_Email, Admin_Password)
        clear_console_logs(self)

    def tearDown(self):
        self.driver.quit()

    def test_01_Help_Documentation(self):
        """
        This test case checks whether the documentation loads or not. After navigating to documentation it checks for
        header 'Knowledge Base - CTIX' and pass the case if it appears to be ok.
        """
        fprint(self, "TC_ID: 81 - Verify if the Help Documentation link parks us to the documentation")
        self.driver.find_element_by_xpath("//i[@class='cyicon-question-active']").click()
        fprint(self, "Clicked on Help icon")
        waitfor(self, 4, By.XPATH, "//li[contains(text(),'Help Documentation')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Help Documentation')]").click()
        fprint(self, "[Passed] Clicked on Help Documentation")
        sleep(5)    # Waiting for the 5 seconds to page get load properly
        win_handles = len(self.driver.window_handles)
        if win_handles > 1:
            fprint(self, "[Passed] A new browser tab seems to have opened")
        else:
            fprint(self, "[Failed] The browser tab didn't seem to open")
        win_instance = self.driver.window_handles[win_handles - 1]
        self.driver.switch_to.window(win_instance)
        fprint(self, "[Passed] Successfully took control of new browser tab")
        fprint(self, "Verifying if the browser tab loaded documentation")
        if waitfor(self, 20, By.XPATH, "//h2[contains(text(),'Cyware Threat Intelligence eXchange (CTIX)')]") \
                or waitfor(self, 1, By.XPATH, "//h1[contains(text(),'How can we help you today?')]"):
            fprint(self, "[Passed] Help Documents appeared successfully")
        else:
            fprint(self, "[Failed] No help document page was found")
            self.fail("[Failed] No help document page was found")

    def test_02_Contact_Support(self):
        fprint(self, "TC_ID: 82 - Verify if Contact Support page is loading")
        self.driver.find_element_by_xpath("//i[@class='cyicon-question-active']").click()
        fprint(self, "Clicked on Help icon")
        waitfor(self, 4, By.XPATH, "//li[contains(text(),'Contact Support')]")
        sleep(1)
        self.driver.find_element_by_xpath("//li[contains(text(),'Contact Support')]").click()
        waitfor(self, 3, By.XPATH, "//span[contains(text(),'Contact Support')]")
        fprint(self, "[Passed] Title Contact Support is visible")
        waitfor(self, 3, By.XPATH, "//input[@aria-placeholder='Subject *']")
        fprint(self, "Subject Field is visible")
        waitfor(self, 3, By.XPATH, "//textarea[@aria-placeholder='Email Body *']")
        fprint(self, "[Passed] Email Body field is visible")
        waitfor(self, 3, By.XPATH, "//button[text() = 'Send Email']")
        fprint(self, "[Passed] Send Email button is visible")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
