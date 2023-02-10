import unittest
from lib.ui.nav_app import *


class LiveActivity(unittest.TestCase):

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

    def test_01_ActivityTimeline_SourceFilter(self):
        fprint(self, "TC_ID: 1 - Live Activity - SourceFilter" + uniquestr)
        nav_menu_main(self, "Live Activity")
        waitfor(self, 5, By.XPATH, "//i[@class='cyicon-department']")
        self.driver.find_element_by_xpath("//i[@class='cyicon-department']").click()
        fprint(self, "TC_ID: 1 - Live Activity - Source Filter opened")
        waitfor(self, 5, By.XPATH, "//div[@class='d-flex w-100 align-items-center']")
        self.driver.find_element_by_xpath("//div[@class='d-flex w-100 align-items-center']").click()
        self.driver.find_element_by_xpath(live_activity_search).send_keys("import")
        fprint(self, "TC_ID: 1 - Live Activity - Source Filter Text is entered")
        waitfor(self, 5, By.XPATH, "//li[@id='list-item-0']")
        self.driver.find_element_by_xpath("//li[@id='list-item-0']").click()
        process_console_logs(self)
        fprint(self, "TC_ID: 1 - Live Activity - Source Filter verified")

    def test_02_ActivityTimeline_CountryFilter(self):
        fprint(self, "TC_ID: 2 - Live Activity - CountryFilter" + uniquestr)
        nav_menu_main(self, "Live Activity")
        waitfor(self, 5, By.XPATH, "//i[@class='cyicon-globe']")
        self.driver.find_element_by_xpath("//i[@class='cyicon-globe']").click()
        fprint(self, "TC_ID: 1 - Live Activity - Country Filter Opened")
        waitfor(self, 5, By.XPATH, "//div[@class='d-flex w-100 align-items-center']")
        self.driver.find_element_by_xpath("//div[@class='d-flex w-100 align-items-center']").click()
        waitfor(self, 5, By.XPATH, live_activity_search)
        self.driver.find_element_by_xpath(live_activity_search).send_keys("United States")
        fprint(self, "TC_ID: 1 - Live Activity - Country Filter text is entered")
        waitfor(self, 5, By.XPATH, "//li[@id='list-item-0']")
        self.driver.find_element_by_xpath("//li[@id='list-item-0']").click()
        process_console_logs(self)
        fprint(self, "TC_ID: 2 - Live Activity - Country Filter verified")

    def test_03_ActivityTimeline_TTPFilter(self):
        fprint(self, "TC_ID: 3 - Live Activity - TTPFilter" + uniquestr)
        nav_menu_main(self, "Live Activity")
        waitfor(self, 5, By.XPATH, "//i[@class='cyicon-ttp']")
        self.driver.find_element_by_xpath("//i[@class='cyicon-ttp']").click()
        fprint(self, "TC_ID: 1 - Live Activity - TTP Filter is opened")
        waitfor(self, 5, By.XPATH, "//div[@class='d-flex w-100 align-items-center']")
        self.driver.find_element_by_xpath("//div[@class='d-flex w-100 align-items-center']").click()
        waitfor(self, 5, By.XPATH, live_activity_search)
        self.driver.find_element_by_xpath(live_activity_search).send_keys("werdc")
        fprint(self, "TC_ID: 1 - Live Activity - TTP Filter text is entered")
        waitfor(self, 5, By.XPATH, "//div[@class='cy-select__menu---expanded d-flex flex-column']//div//div")
        ttptextbox = self.driver.find_element_by_xpath("//div[@class='cy-select__menu---expanded d-flex flex-column']//div//div").text
        assert ttptextbox == 'No results found'
        process_console_logs(self)
        fprint(self, "TC_ID: 3 - Live Activity - TTP Filter verified")

    def test_04_ActivityTimeline_ClearFilter(self):
        fprint(self, "TC_ID: 4 - Live Activity - ClearFilter" + uniquestr)
        nav_menu_main(self, "Live Activity")
        waitfor(self, 5, By.XPATH, "//a[contains(text(),'Clear Filter')]")
        self.driver.find_element_by_xpath("//a[contains(text(),'Clear Filter')]").click()
        fprint(self, "TC_ID: 4 - Live Activity - clicked on clear filter")
        time.sleep(2)
        #clearfilter = self.driver.find_element_by_xpath("//a[@class='cy-text-primary applied cy-border-primary']").get_attribute("border-color")
        process_console_logs(self)
        fprint(self, "TC_ID: 4 - Live Activity - clear filter verified")

    def test_05_ActivityTimeline_ActivityLogs(self):
        fprint(self, "TC_ID: 5 - Live Activity - ActivityLogs" + uniquestr)
        nav_menu_main(self, "Live Activity")
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Activity Logs')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Activity Logs')]").click()
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Activity Logs')]")
        fprint(self, "TC_ID: 5 - Live Activity - ActivityLogs Slider is opened")
        headertext = self.driver.find_element_by_xpath("//div[contains(text(),'Activity Logs')]").text
        assert headertext == 'Activity Logs'
        process_console_logs(self)
        waitfor(self, 5, By.XPATH, "//span[@data-testaction='slider-close']")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        process_console_logs(self)
        fprint(self, "TC_ID: 5 - Live Activity - ActivityLogs verified")

    def test_06_ActivityTimeline_SelectDateRange(self):
        fprint(self, "TC_ID: 6 - Live Activity - SelectDateRange" + uniquestr)
        nav_menu_main(self, "Live Activity")
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Activity Logs')]")
        self.driver.find_element_by_xpath("//div[div[span[contains(text(),'Start Date & Time')]]]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//td[@class='available today']").click()
        fprint(self, "TC_ID: 6 - Live Activity - Start Date & Time is selected")
        fprint(self, "TC_ID: 6 - Live Activity - Calender - Start date selected")
        self.driver.find_element_by_xpath("//div[div[span[contains(text(),'End Date & Time')]]]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//td[@class='available today']").click()
        fprint(self, "TC_ID: 6 - Live Activity - End Date & Time is selected")
        self.driver.find_element_by_xpath("//button[contains(text(),'Apply')]").click()
        process_console_logs(self)
        fprint(self, "TC_ID: 6 - Live Activity - Date filter verified")

if __name__ == '__main__':
    unittest.main(testRunner=reporting())
