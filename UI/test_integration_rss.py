import csv
import unittest
from lib.ui.nav_app import *
from lib.ui.rss_feeds import *

RSS_NAME = "Talos"
EDITED_NAME = "Talos_edited"


class IntegrationRSS(unittest.TestCase):

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

    def test_01_load_rss(self):
        """
        Checking if RSS sources pages are loading

        returns: None
        """
        fprint(self, "TC_ID: 8001 - verify_load_rss")
        add_source_button = "//button[contains(text(),'RSS')]"
        nav_menu_admin(self, "Integration Management")
        fprint(self, "\n----------- TC_ID 1: Checking load screen of RSS sources -----------")
        fprint(self, "Clicking on RSS under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'RSS')]").click()
        fprint(self, "Validating if 'Add RSS Source button is present'")
        if waitfor(self, 5, By.XPATH, add_source_button):
            fprint(self, "[Passed] Page for RSS Source is loading as expected")
        sleep(2)
        process_console_logs(self)

    def test_02_add_csv_rss_sources(self):
        """
        Testcase to add RSS Sources from rss_feeds.csv

        :return: None
        """
        fprint(self, "TC_ID: 8002 - verify_add_rss_source")
        add_source_button = "//button[contains(text(),'RSS')]"
        nav_menu_admin(self, "Integration Management")
        fprint(self, "\n---------------------- TC_ID 2 RSS Feeds addition from CSV --------------------")
        fprint(self, "Clicking on RSS under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'RSS')]").click()
        fprint(self, "Validating if 'Add RSS Source button is present'")
        if waitfor(self, 5, By.XPATH, add_source_button):
            fprint(self, "[Passed] Page for RSS Source is loading as expected")
        filename = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds", "rss_feeds.csv")
        with open(filename, 'r') as obj:
            data = csv.reader(obj)
            for rssFeeds in data:
                if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
                    self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
                create_source(self, name=rssFeeds[0], url=rssFeeds[1])
        process_console_logs(self)

    def test_03_rss_collections(self):
        """
        Checking for collections in the rss source created

        returns: None
        """
        fprint(self, "TC_ID: 8003 - verify_rss_collections")
        if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        nav_menu_admin(self, "Integration Management")
        fprint(self, "\n-------------- TC-ID 3: Checking if RSS Source collections are visible -------------")
        fprint(self, "Clicking on RSS under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'RSS')]").click()
        sleep(2)
        fprint(self, "Selecting View Collections from the action menu")
        perform_action(self, name=RSS_NAME, action='View Collections')
        waitfor(self, 5, By.XPATH, "//h1[contains(text(),'Collections of "+RSS_NAME+"')]")
        fprint(self, "Collections page for "+RSS_NAME+" loaded successfully")
        sleep(2)
        process_console_logs(self)

    def test_04_edit_rss(self):
        """
        Checking for rss source name can be edited

        returns: None
        """
        global RSS_NAME
        fprint(self, "TC_ID: 8004 - verify_edit_rss_source")
        if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        nav_menu_admin(self, "Integration Management")
        fprint(self, "\n-------------- TC-ID 4: Checking if RSS Source details can be edited-------------")
        fprint(self, "Clicking on RSS under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'RSS')]").click()
        sleep(2)
        fprint(self, "Selecting View Collections from the action menu")
        perform_action(self, name=RSS_NAME, action='Edit')
        waitfor(self, 2, By.XPATH, "//div[text()='Update Source']")
        sleep(1)
        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Source Name*']"))
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Source Name*']"). \
            send_keys(EDITED_NAME)
        sleep(1)
        self.driver.find_element_by_xpath("//button[text()='Update']").click()
        fprint(self, "[Passed] Clicked on Update")
        verify_success(self, "updated successfully")
        RSS_NAME = EDITED_NAME
        process_console_logs(self)

    def test_05_disable_rss_source(self):
        """
        Checking for rss source name can be disabled

        returns: None
        """
        fprint(self, "TC_ID: 8005 - verify_disable_rss_source")
        if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        nav_menu_admin(self, "Integration Management")
        fprint(self, "\n-------------- TC-ID 5: Checking if RSS Source can be disabled -------------")
        fprint(self, "Clicking on RSS under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'RSS')]").click()
        sleep(2)     # required
        self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']").click()
        clear_field(self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']"))
        sleep(1)
        fprint(self, "Searching for the RSS Source that is disabled")
        self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']").send_keys(RSS_NAME)
        self.driver.find_element_by_xpath("//i[@data-testid='filter-search-icon']").click()
        if waitfor(self, 7, By.XPATH, "//div/p[contains(text(), '"+RSS_NAME+"')]"):
            waitfor(self, 2, By.XPATH, "//div/p[contains(text(), '"+RSS_NAME+"')]/following-sibling::div/div/div")
            self.driver.find_element_by_xpath\
                ("//div/p[contains(text(), '"+RSS_NAME+"')]/following-sibling::div/div/div").click()
        else:
            raise Exception("Requested source not found")
        process_console_logs(self)

    def test_06_enable_rss_source(self):
        """
        Checking for rss source name can be enabled

        returns: None
        """
        fprint(self, "TC_ID: 8006 - verify_enable_rss_source")
        if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        nav_menu_admin(self, "Integration Management")
        fprint(self, "\n-------------- TC-ID 6: Checking if RSS Source can be enabled -------------")
        fprint(self, "Clicking on RSS under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'RSS')]").click()
        sleep(2)    # required
        self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']").click()
        clear_field(self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']"))
        sleep(1)
        fprint(self, "Searching selected RSS Source that was enabled")
        self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']").send_keys(RSS_NAME)
        self.driver.find_element_by_xpath("//i[@data-testid='filter-search-icon']").click()
        if waitfor(self, 7, By.XPATH, "//div/p[contains(text(), '"+RSS_NAME+"')]"):
            waitfor(self, 2, By.XPATH, "//div/p[contains(text(), '"+RSS_NAME+"')]/following-sibling::div/div/div")
            self.driver.find_element_by_xpath\
                ("//div/p[contains(text(), '"+RSS_NAME+"')]/following-sibling::div/div/div").click()
        else:
            raise Exception("Requested source not found")
        process_console_logs(self)

    def test_07_delete_rss_source(self):
        """
        Checking for rss source name can be deleted

        returns: None
        """
        fprint(self, "TC_ID: 8007 - verify_delete_rss_source")
        if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        nav_menu_admin(self, "Integration Management")
        fprint(self, "\n-------------- TC-ID 7: Checking if RSS source can be deleted -------------")
        fprint(self, "Clicking on RSS under feed sources")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'RSS')]").click()
        sleep(2)
        perform_action(self, name=RSS_NAME, action="Delete")
        if waitfor(self, 5, By.XPATH, "//button[@data-testalert='confirm-delete']", False):
            self.driver.find_element_by_xpath("//button[@data-testalert='confirm-delete']").click()
        else:
            self.driver.find_element_by_xpath("//button[@data-testalert='confirm-remove']").click()
        verify_success(self, "Selected Source deleted successfully")
        sleep(2)    # required
        self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']").click()
        clear_field(self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']"))
        sleep(1)
        fprint(self, "Searching for the deleted RSS Source")
        self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']").send_keys(RSS_NAME)
        self.driver.find_element_by_xpath("//i[@data-testid='filter-search-icon']").click()
        if not waitfor(self, 7, By.XPATH, "//div/p[contains(text(), '"+RSS_NAME+"')]", False):
            fprint(self, "[Passed] "+RSS_NAME+" RSS Source is deleted successfully")
        else:
            raise Exception("[Failed] Failed to delete the selected RSS Source")
        process_console_logs(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
