import unittest
from lib.ui.nav_app import *


class Dashboards(unittest.TestCase):

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

    def test_01_Dashboards_DefaultDashboards(self):
        fprint(self, "TC_ID: 1 - Dashboards - DefaultDashboards" + uniquestr)
        waitfor(self, 5, By.XPATH, "//span[@data-testid='Analyst Dashboard']")
        process_console_logs(self)
        fprint(self, "Dashboards - Default Analyst Dashboards is visible")
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'Feeds ROI')]")
        fprint(self, "Dashboards - Default Feeds ROI option is visible")
        self.driver.find_element_by_xpath("//span[contains(text(),'Feeds ROI')]").click()
        fprint(self, "Dashboards - Default Feeds ROI option is clicked")
        sleep(1)
        process_console_logs(self)
        fprint(self, "Dashboards - Default Feeds ROI Dashboards is clicked")
        waitfor(self, 5, By.XPATH, "(//span[text()='Dashboards']//ancestor::span[2]//following-sibling::span)[2]//span[text()='Feeds ROI']")
        fprint(self, "Dashboards - Default Feeds ROI Dashboard is visible")

    def xtest_01_Dashboards_add(self):
        fprint(self, "TC_ID: 2 - Dashboards - Add" + uniquestr)
        nav_menu_admin(self, "Dashboards")
        waitfor(self, 5, By.XPATH, "//button[@data-testid='add-dashboard']")
        self.driver.find_element_by_xpath("//button[@data-testid='add-dashboard']").click()
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Create New Dashboard')]")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Organization Type Name *']").send_keys("Organization"+uniquestr)
        self.driver.find_element_by_xpath("//div[@class='cy-wrapper cy-select__menu cy-wrapper__lg']").click()
        waitfor(self, 5, By.XPATH, "//li[@id='list-item-0']")
        self.driver.find_element_by_xpath("//li[@id='list-item-0']").click()
        self.driver.find_element_by_xpath("//button[contains(text(),'Add  Organization Type')]").click()
        verify_success(self, "Dashboards created successfully")
        process_console_logs(self)
        fprint(self, "Dashboards Type added")




if __name__ == '__main__':
    unittest.main(testRunner=reporting())
