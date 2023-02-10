import unittest
from lib.ui.nav_app import *

class Dashboard_Export(unittest.TestCase):

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

    def test_01_Dashboard_Export_PNG(self):
        fprint(self, "TC_ID: 2100 - Dashboards - Export PNG")
        # First Check if this instance supports fusion export , support was added in 2.9 dev builds
        if not waitfor(self, 5, By.XPATH, "//*[@data-testid='Analyst Dashboard']/..//button", False):
            fprint(self, "This instance doesn't support fusion export")
            exit()
        fprint(self, "Navigate to Background Tasks and keep note of last dashboard export job")
        nav_menu_main(self, "Background Tasks")
        fprint(self, "Filter table results with Dashboard Export keywords")
        self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys("Dashboard Export")
        fprint(self, "Click on filter search icon")
        sleep(2)
        self.driver.find_element_by_xpath("//i[@data-testid='filter-search-icon']").click()
        sleep(4)
        if waitfor(self, 5, By.XPATH, "//*[@data-testid='task_title']", False):
            previous_bt = self.driver.find_element_by_xpath("//*[@data-testid='task_title']").text
            fprint(self, "Previous Background task: " + previous_bt)
        else:
            fprint(self, "There is no previous background task which is present")

        fprint(self, "Navigate to Dashboards")
        nav_menu_main(self, "Dashboards")
        fprint(self, "Click on Analyst Dashboard's options button")
        self.driver.find_element_by_xpath("//*[@data-testid='Analyst Dashboard']/..//button").click()
        fprint(self, "Click on the export button in the Analyst Dashboard's options menu")
        self.driver.find_element_by_xpath("//*[@data-testaction='export-dashboard']").click()
        sleep(2)
        fprint(self, "Check if the slide window appeared")
        waitfor(self, 5, By.XPATH, "//*[@class='cy-right-modal-content']//div[contains(text(),'PNG')]")
        fprint(self, "Click on the PNG option")
        self.driver.find_element_by_xpath(self, "//*[@class='cy-right-modal-content']//div[contains(text(),'PNG')]").click()
        sleep(1)
        fprint(self, "Click on the Export Button")
        self.driver.find_element_by_xpath(self, "//*[@class='cy-right-modal-content']//button[contains(text(),'Export')]").click()
        verify_success(self, "Your dashboard will be available in ‘Notifications’ under Topbar section")




        #fprint(self, "TC_ID: 1 - Dashboards - Default Analyst Dashboards is visible")
        #self.driver.find_element_by_xpath("//input[@id='main-input']").click()
        #sleep(2)
        #process_console_logs(self)
        #fprint(self, "TC_ID: 1 - Dashboards - Default Analyst Dashboards is clicked")
        #waitfor(self, 5, By.XPATH, "//span[@data-testid='Feeds ROI']")
        #fprint(self, "TC_ID: 1 - Dashboards - Default Feeds ROI Dashboards is visible")
        #self.driver.find_element_by_xpath("//span[@data-testid='Feeds ROI']").click()
        #sleep(2)
        #process_console_logs(self)
        #fprint(self, "TC_ID: 1 - Dashboards - Default Feeds ROI Dashboards is clicked")
        #fprint(self, "TC_ID: 1 - Dashboards - DefaultDashboards are available")



if __name__ == '__main__':
    unittest.main(testRunner=reporting())
