import unittest
from selenium.common.exceptions import ElementClickInterceptedException
from lib.ui.nav_tableview import click_on_actions_item
from lib.ui.nav_threat_data import *

webscrapper_title = "test_automation_title"


class IntegrationWebScraper(unittest.TestCase):

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

    def add_webscraper_url(self):
        if Build_Version.__contains__("3."):
            waitfor(self, 5, By.XPATH, "//button[contains(text(),'Add Web Scraper')]")
            self.driver.find_element_by_xpath("//button[contains(text(),'Add Web Scraper')]").click()
            fprint(self, "Clicked on the 'Add Web Scraper' Button")
        else:
            waitfor(self, 5, By.XPATH, "//button[contains(text(),'Add New')]")
            self.driver.find_element_by_xpath("//button[contains(text(),'Add New')]").click()
            fprint(self, "Clicked on the 'Add New' Button")
            waitfor(self, 5, By.XPATH, "//li[contains(text(),'URL')]")
            self.driver.find_element_by_xpath("//li[contains(text(),'URL')]").click()
            fprint(self, "Clicked on the URL option")
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Web URL *']")
        fprint(self, "Adding new URL now")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Web URL *']").send_keys("https://orion.cywareqa.com/webscrapper/ip-addresses.txt")
        fprint(self, "Web URL - https://orion.cywareqa.com/webscrapper/ip-addresses.txt")
        self.driver.find_element_by_xpath("//div[contains(text(),'Text')]").click()
        sleep(1)  # This sleep is required
        self.driver.find_element_by_xpath("//button[contains(text(),'Add Attribute(s)')]").click()
        fprint(self, "Clicked on the Add Attribute button")
        if Build_Version.__contains__("3."):
            waitfor(self, 10, By.XPATH, "//span[contains(text(),'ipv4')]")
            self.driver.find_element_by_xpath("//span[contains(text(),'ipv4')]").click()
        else:
            waitfor(self, 10, By.XPATH, "//span[contains(text(),'ipv4')]//preceding::div[1]")
            self.driver.find_element_by_xpath("//span[contains(text(),'ipv4')]//preceding::div[1]").click()
        fprint(self, "Selected checkbox - ipv4")
        self.driver.find_element_by_xpath("//button[@data-testid='add-attributes']").click()
        fprint(self, "Clicked on the Add button")
        waitfor(self, 5, By.XPATH, "//span[contains(text(),' Select Type ')]//ancestor::div[3]")
        self.driver.find_element_by_xpath("//span[contains(text(),' Select Type ')]//ancestor::div[3]").click()
        fprint(self, "Clicked on the Select Type Dropdown")
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'IPV4')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'IPV4')]").click()
        fprint(self, "Selected - IPV4")
        self.driver.find_element_by_xpath("//div[contains(text(),'Once')]").click()
        fprint(self, "Selected Polling - Once")
        self.driver.find_element_by_xpath("//span[contains(text(),' Start Date & Time ')]//ancestor::div[2]").click()
        fprint(self, "Calender is visible")
        waitfor(self, 5, By.XPATH, "(//td[@class='available today'])[1]")
        self.driver.find_element_by_xpath("(//td[@class='available today'])[1]").click()
        fprint(self, "Selected today's date")
        try:
            self.driver.find_element_by_xpath("//span[contains(text(),' Select TLP * ')]//ancestor::div[4]").click()
        except ElementClickInterceptedException:
            self.driver.find_element_by_xpath("//h4[contains(text(),'Polling Cron Schedule *')]").click()
            sleep(2)
            self.driver.find_element_by_xpath("//span[contains(text(),' Select TLP * ')]//ancestor::div[4]").click()
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'RED')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'RED')]").click()
        fprint(self, "Selected TLP  - RED")
        self.driver.find_element_by_xpath("//span[contains(text(),' Select URL Confidence * ')]//ancestor::div[4]").click()
        if waitfor(self, 5, By.XPATH, "//div[contains(text(),'High')]", False):
            self.driver.find_element_by_xpath("//div[contains(text(),'High')]").click()
        else:
            self.driver.find_element_by_xpath("//div[contains(text(),'HIGH')]").click()
        fprint(self, "Selected URL Confidence - HIGH")
        if Build_Version.__contains__("3."):
            self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys(webscrapper_title)
            fprint(self, "Title - "+webscrapper_title)
            self.driver.find_element_by_xpath("//button[@data-testid='save-webscrapper']").click()
            fprint(self, "Clicked on the Add Web Scraper Button")
        else:
            self.driver.find_element_by_xpath("(//div[@name='source'])[1]").click()
            sleep(1)
            self.driver.find_element_by_xpath("//input[@placeholder='Search']").send_keys("wsSource")
            waitfor(self, 5, By.XPATH, "//div[contains(text(),'wsSource')]")
            self.driver.find_element_by_xpath("//div[contains(text(),'wsSource')]").click()
            fprint(self, "Selected 'Select Source' - wsSource")
            waitfor(self, 5, By.XPATH, "(//div[@name='collection'])[1]")
            self.driver.find_element_by_xpath("(//div[@name='collection'])[1]").click()
            waitfor(self, 5, By.XPATH, "//div[contains(text(),'- wsSource')]")
            self.driver.find_element_by_xpath("//div[contains(text(),'- wsSource')]").click()
            fprint(self, "Selected Collection - 'Collection-wsSource'")
            self.driver.find_element_by_xpath("//input[@aria-placeholder='Title *']").send_keys(webscrapper_title)
            fprint(self, "Title - "+webscrapper_title)
            self.driver.find_element_by_xpath("//button[@data-testid='save-webscrapper']").click()
            fprint(self, "Clicked on the Add Web Scraper Button")
        verify_success(self, "URL created successfully")
        fprint(self, "Searching newly added Web Scraper URL")
        search(self, webscrapper_title)
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+webscrapper_title+"')]")
        fprint(self, "Newly added Web Scraper URL is visible")

    def poll_webscraper(self):
        click_on_actions_item(self, rowtitle=webscrapper_title, item="Poll Now")
        fprint(self, "Clicked on the Poll Now")

    def test_01_verify_addNew_webScraper(self):
        fprint(self, "TC_ID: 6001 - verify_addNew_webScraper")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to Web Scraper Feed Source")
        self.driver.find_element_by_xpath("//a/span[contains(text(),'Web Scraper')]").click()
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Add New')]")
        fprint(self, "Clicked on the 'Add New' Button")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add New')]").click()

        # Adding Web Scraper Source
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Source')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Source')]").click()
        fprint(self, "Clicked on the Source option")
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Source Name *']")
        fprint(self, "Adding Web Scraper source now")
        set_value("source_name", "wsSource")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Source Name *']").send_keys("wsSource")
        fprint(self, "Source Name - wsSource")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description *']").send_keys("test_description")
        fprint(self, "Description - test_description")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Confidence *']").send_keys("70")
        fprint(self, "Confidence score - 70")
        self.driver.find_element_by_xpath("//div[@name='category']").click()
        # self.driver.find_element_by_xpath("//input[@placeholder='Search']").send_keys("test_automation_category")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Community Feeds')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Community Feeds')]").click()
        fprint(self, "Selected Community Feeds")
        # if waitfor(self, 3, By.XPATH, "//div[contains(text(),'test_automation_category')]", False):
        #     self.driver.find_element_by_xpath("//div[contains(text(),'test_automation_category')]").click()
        #     fprint(self, "Found Category already exist - test_automation_category")
        # else:
        #     self.driver.find_element_by_xpath("//button[contains(text(),'+ Add Category')]").click()
        #     fprint(self, "Added new Category - test_automation_category")
        #     self.driver.find_element_by_xpath("//div[@name='category']").click()
        #     self.driver.find_element_by_xpath("//input[@placeholder='Search']").send_keys("test_automation_category")
        #     waitfor(self, 5, By.XPATH, "//div[contains(text(),'test_automation_category')]")
        #     self.driver.find_element_by_xpath("//div[contains(text(),'test_automation_category')]").click()
        #     fprint(self, "Category selected - test_automation_category")
        self.driver.find_element_by_xpath("//button[@data-testid='save-sources']").click()
        fprint(self, "Clicked on the Add button")
        verify_success(self, "Source created successfully")
        process_console_logs(self)
        # Adding Web Scraper URL
        self.add_webscraper_url()

    # Only for CTIX Version 3.0
    def test_02_v3_verify_addNew_webScraper(self):
        fprint(self, "TC_ID: 6002 - v3_verify_addNew_webScraper")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to Web Scraper Feed Source")
        self.driver.find_element_by_xpath("//a/span[contains(text(),'Web Scraper')]").click()
        # Adding Web Scraper URL
        self.add_webscraper_url()
        self.poll_webscraper()

    # Worked for both CTIX Version 3.0 and previous versions
    def test_03_verify_webscraper_polledData(self):
        fprint(self, "TC_ID: 6003 - verify_webscraper_polledData")
        fprint(self, "Waiting for the 5 minutes to data get polled")
        sleep(300)
        fprint(self, "Navigating to the Threat Data")
        nav_menu_main(self, "Threat Data")
        if Build_Version.__contains__("3."):
            verify_polleddata_in_threatdata(self, webscrapper_title, "webscraper_data.csv")
        else:
            verify_polleddata_in_threatdata(self, get_value("source_name"), "webscraper_data.csv")
        fprint(self, "[Passed] Found all the Web Scraper data")

    def test_04_verify_edit_webscraper(self):
        fprint(self, "TC_ID: 6004 - verify_edit_webscraper")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to Web Scraper Feed Source")
        self.driver.find_element_by_xpath("//a/span[contains(text(),'Web Scraper')]").click()
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        fprint(self, "Searching Web Scraper URL - "+webscrapper_title)
        search(self, webscrapper_title)
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+webscrapper_title+"')]")
        fprint(self, "Web Scraper URL is visible")
        self.driver.find_element_by_xpath("//span[contains(text(),'"+webscrapper_title+"')]/ancestor::td/following-sibling::td[4]/div/div").click()
        fprint(self, "Clicked on the Action menu")
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Edit')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Edit')]").click()
        fprint(self, "Clicked on the Edit option")
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Title *']")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title *']").send_keys("_edit")
        fprint(self, "Appended test in title - _edit")
        self.driver.find_element_by_xpath("//button[@data-testid='update-webscrapper']").click()
        fprint(self, "Clicked on the Update Web Scrapper button")
        verify_success(self, "updated successfully")
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'"+webscrapper_title+"_edit')]")
        fprint(self, "Edited Title is visible - "+webscrapper_title+"_edit")

    def test_05_verify_delete_webscraper(self):
        fprint(self, "TC_ID: 6005 - verify_delete_webscraper")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to Web Scraper Feed Source")
        self.driver.find_element_by_xpath("//a/span[contains(text(),'Web Scraper')]").click()
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        fprint(self, "Searching Web Scraper URL - "+webscrapper_title)
        search(self, webscrapper_title)
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+webscrapper_title+"')]")
        fprint(self, "Web Scraper URL is visible")
        self.driver.find_element_by_xpath("//span[contains(text(),'"+webscrapper_title+"')]/ancestor::td/following-sibling::td[4]/div/div").click()
        fprint(self, "Clicked on the Action menu")
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Delete')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Delete')]").click()
        fprint(self, "Clicked on the Delete option")
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Delete')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Delete')]").click()
        fprint(self, "Clicked on the Delete button in the Confirmation popup")
        verify_success(self, "Selected URL deleted successfully")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(),'No results found!')]")
        fprint(self, "Web Scraper URL Deleted successfully")
        process_console_logs(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
