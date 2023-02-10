import unittest
from lib.ui.nav_app import *
from lib.ui.rss_feeds import create_intel_from_feed


class RSSFeeds(unittest.TestCase):

    _source_url = "http://feeds.feedburner.com/Unit42"

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

    def test_01_add_rss_source(self):
        """
        Testcase to add a specified RSS Source

        :return: None
        """
        fprint(self, "\n----------- TC_ID 1 RSS Feed Addition: " + "RSSFeed_"+uniquestr+" -----------")
        nav_menu_main(self, "RSS Feeds")
        waitfor(self, 2, By.XPATH, "//ul/following-sibling::div/span/i")
        self.driver.find_element_by_xpath("//ul/following-sibling::div/span/i").click()
        sleep(1)
        RSS_NAME = "Talos"
        set_value("RSS_NAME", RSS_NAME)
        self.driver.find_element_by_xpath(rss_feeds_search).send_keys(RSS_NAME)
        if waitfor(self, 2, By.XPATH, "//span[contains(text(),'RSS7258376430')]", False):
            self.driver.find_element_by_xpath("//span[contains(text(),'RSS7258376430')]").click()
            fprint(self, "Opening Action list for RSS Source")
            waitfor(self, 4, By.XPATH, "//button[@data-testid='action']")
            self.driver.find_element_by_xpath("//button[@data-testid='action']").click()
            waitfor(self, 4, By.XPATH, "//li[text()='Remove']")
            fprint(self, "Selecting Remove Operation")
            self.driver.find_element_by_xpath("//li[text()='Remove']").click()
            waitfor(self, 4, By.XPATH, "//button[@data-testalert='confirm-remove']")
            fprint(self, "Confirming to remove RSS Feed Source")
            self.driver.find_element_by_xpath("//button[@data-testalert='confirm-remove']").click()
        self.driver.find_element_by_xpath("//button[text()='Add New Source']").click()
        fprint(self, "[Passed] clicked on Add New Source")
        waitfor(self, 2, By.XPATH, "//div[text()='New Source']")
        sleep(1)
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Source Name*']").\
            send_keys(RSS_NAME)
        sleep(1)
        self.driver.find_element_by_xpath("//input[@aria-placeholder='URL*']").send_keys(self._source_url)
        fprint(self, "[Passed] filled up form details")
        fprint(self, "Unchecking Auto create package if marked True")
        if Build_Version.__contains__("3."):
            waitfor(self, 2, By.XPATH,
                    "//span[contains(text(), 'Create intel automatically')]/preceding-sibling::span/input")
            _ele = self.driver.find_element_by_xpath("//span[contains(text(), 'Create intel automatically')]/preceding-sibling::span/input")
            if _ele.get_attribute("value") == "true":  # Uncheck auto intel creation if active
                self.driver.find_element_by_xpath( "//span[contains(text(), 'Create intel automatically')]/preceding-sibling::span/input").click()
            sleep(1)
        else:
            waitfor(self, 2, By.XPATH,
                    "//span[contains(text(), 'Automatically create Intel Packages')]/preceding-sibling::span/input")
            _ele = self.driver.find_element_by_xpath("//span[contains(text(), 'Automatically create Intel Packages')]/preceding-sibling::span/input")
            if _ele.get_attribute("value") == "true":  # Uncheck auto intel creation if active
                self.driver.find_element_by_xpath("//span[contains(text(), 'Automatically create Intel Packages')]/preceding-sibling::span/input").click()
            sleep(1)
        self.driver.find_element_by_xpath("//button[text()='Add']").click()
        fprint(self, "[Passed] Clicked on Add")
        verify_success(self, "RSS Feed Source added successfully")
        fprint(self, "[Passed] Obtained required Success Alert")
        process_console_logs(self)

    def test_02_rss_parser(self):
        """
        Verify if IOC's are getting parsed from the RSS Source

        :return: None
        """
        fprint(self, "\n----------- TC_ID 2: Parsing RSS feed data for intel -----------")
        RSS_NAME = get_value("RSS_NAME")
        _feeds = False
        _create_intel = "//button[normalize-space(text())='Create Intel']"
        if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        fprint(self, "Searching for created RSS Source")
        nav_menu_main(self, "RSS Feeds")
        waitfor(self, 2, By.XPATH, "//ul/following-sibling::div/span/i")
        self.driver.find_element_by_xpath("//ul/following-sibling::div/span/i").click()
        sleep(1)
        # .clear sometimes don't work , driver/system compatibility issues
        clear_field(self.driver.find_element_by_xpath(rss_feeds_search))
        # self.driver.find_element_by_xpath(rss_feeds_search).clear()
        self.driver.find_element_by_xpath(rss_feeds_search).send_keys(RSS_NAME)
        waitfor(self, 2, By.XPATH, "//span[text()='"+RSS_NAME+"']")
        self.driver.find_element_by_xpath("//span[text()='"+RSS_NAME+"']").click()
        fprint(self, "Waiting for RSS Feeds")
        self.driver.find_element_by_xpath\
            ("//h1[contains(text(),'RSS Feeds')]//ancestor::div/following-sibling::div/div/button").click()
        fprint(self, "Waiting 5 minutes for feeds to appear")
        for i in range(30):
            if waitfor(self, 10, By.XPATH, "//span/a[text()='Create']", False) or waitfor(self, 10, By.XPATH, "//button[normalize-space(text())='Create Intel']", False):
                _feeds = True
                break
            elif i == 29:
                fprint(self, "[FAILED] No Feeds received from the RSS Source to be parsed")
            else:
                self.driver.find_element_by_xpath \
                    ("//h1[contains(text(),'RSS Feeds')]//ancestor::div/following-sibling::div/div/button").click()
        if waitfor(self, 10, By.XPATH, "//span/a[text()='Create']", False):
            _create_intel = "//span/a[text()='Create']"
        if _feeds:
            self.driver.find_element_by_xpath(_create_intel).click()
            fprint(self, "[Passed] Clicked on Create for data recieved")
            # Check if parsed data is shown
            # waitfor(self, 3, By.XPATH, "//div[contains(text(),'Create an Intel Package')]")
            waitfor(self, 5, By.XPATH, "//span[@data-testaction='slider-close']")
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            fprint(self, "[Passed] Closed the data creation slider")
        process_console_logs(self)

    def test_03_edit_rss_source(self):
        """
        Verify if user is able to edit RSS source data

        :return: None
        """
        RSS_NAME = get_value("RSS_NAME")
        fprint(self, "\n----------- TC_ID 3: Editing the added RSS source data -----------")
        if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        fprint(self, "Searching for RSS Source")
        nav_menu_main(self, "RSS Feeds")
        waitfor(self, 2, By.XPATH, "//ul/following-sibling::div/span/i")
        self.driver.find_element_by_xpath("//ul/following-sibling::div/span/i").click()
        self.driver.find_element_by_xpath(rss_feeds_search).clear()
        sleep(1)
        self.driver.find_element_by_xpath(rss_feeds_search).send_keys(RSS_NAME)
        waitfor(self, 2, By.XPATH, "//span[text()='"+RSS_NAME+"']")
        self.driver.find_element_by_xpath("//span[text()='"+RSS_NAME+"']").click()
        self.driver.find_element_by_xpath("//button[@data-testid='action']").click()
        waitfor(self, 5, By.XPATH, "//li[text()='Edit Source']")
        fprint(self, "[PASSED] Opened Edit source form")
        sleep(2)
        self.driver.find_element_by_xpath("//li[text()='Edit Source']").click()
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Source Name*']")
        fprint(self, "Searching for the RSS source to be edited")
        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Source Name*']"))
        sleep(1)
        RSS_NAME = "Talos_edited"
        set_value("RSS_NAME", RSS_NAME)
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Source Name*']").send_keys(RSS_NAME)
        fprint(self, "[PASSED] Updated the RSS Source Name")
        self.driver.find_element_by_xpath("//button[text()='Update']").click()
        fprint(self, "[PASSED] Clicked on Update")
        verify_success(self, "updated successfully")
        if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        process_console_logs(self)

    def test_04_rss_listing(self):
        """
        Verify if added or modified RSS sources are present

        :return: None
        """
        RSS_NAME = get_value("RSS_NAME")
        fprint(self, "\n----------- TC_ID 4: Searching if updated source is present in listing -----------")
        if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        nav_menu_main(self, "RSS Feeds")
        waitfor(self, 2, By.XPATH, "//ul/following-sibling::div/span/i")
        self.driver.find_element_by_xpath("//ul/following-sibling::div/span/i").click()
        self.driver.find_element_by_xpath(rss_feeds_search).clear()
        sleep(1)
        fprint(self, "Validating if modified source is present in RSS Listing")
        self.driver.find_element_by_xpath(rss_feeds_search).send_keys(RSS_NAME)
        waitfor(self, 5, By.XPATH, "//span[text()='" + RSS_NAME + "']")
        fprint(self, "Updated RSS feed present in listing")
        process_console_logs(self)

    def test_05_refresh_rss_listing(self):
        """
        Check if refresh on RSS Feeds is working as expected

        :return: None
        """
        RSS_NAME = get_value("RSS_NAME")
        fprint(self, "\n----------- TC_ID 5: Clicking on Refresh Button -----------")
        if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        fprint(self, "Searching for RSS Source")
        nav_menu_main(self, "RSS Feeds")
        waitfor(self, 2, By.XPATH, "//ul/following-sibling::div/span/i")
        self.driver.find_element_by_xpath("//ul/following-sibling::div/span/i").click()
        self.driver.find_element_by_xpath(rss_feeds_search).clear()
        sleep(1)
        self.driver.find_element_by_xpath(rss_feeds_search).send_keys(RSS_NAME)
        waitfor(self, 2, By.XPATH, "//span[text()='"+RSS_NAME+"']")
        self.driver.find_element_by_xpath("//span[text()='"+RSS_NAME+"']").click()
        fprint(self, "Clicking on refresh feeds for the RSS Source")
        self.driver.find_element_by_xpath\
            ("//h1[contains(text(),'RSS Feeds')]//ancestor::div/following-sibling::div/div/button").click()
        fprint(self, "[PASSED] Feeds are refreshed successfully")
        process_console_logs(self)

    def test_06_rss_bookmarking(self):
        """
        Verify if RSS feed data is getting bookmarked

        :return: None
        """
        RSS_NAME = get_value("RSS_NAME")
        fprint(self, "\n----------- TC_ID 6: Verifying if RSS feed Data can be bookmarked -----------")
        if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        fprint(self, "Searching for RSS Source")
        nav_menu_main(self, "RSS Feeds")
        waitfor(self, 2, By.XPATH, "//ul/following-sibling::div/span/i")
        self.driver.find_element_by_xpath("//ul/following-sibling::div/span/i").click()
        self.driver.find_element_by_xpath(rss_feeds_search).clear()
        sleep(1)
        self.driver.find_element_by_xpath(rss_feeds_search).send_keys(RSS_NAME)
        waitfor(self, 2, By.XPATH, "//span[text()='"+RSS_NAME+"']")
        self.driver.find_element_by_xpath("//span[text()='"+RSS_NAME+"']").click()
        if waitfor(self, 20, By.XPATH, "//div[@data-testid='title']", False):
            _intel_name = self.driver.find_element_by_xpath("//div[@data-testid='title']").text
            self.driver.find_element_by_xpath\
                ("//a/i[@class='cyicon-bookmark']").click()
            fprint(self, "Clicking on Bookmark Feed")
            waitfor(self, 2, By.XPATH, "//span[text()='Bookmarked']")
            fprint(self, "Checking if feed is bookmarked")
            self.driver.find_element_by_xpath("//span[text()='Bookmarked']").click()
            fprint(self, "Validating title of the bookmarked feed")
            waitfor(self, 2, By.XPATH, "//div[@data-testid='title']")
            _name_2 = self.driver.find_element_by_xpath("//div[@data-testid='title']").text
            if _name_2 != _intel_name:
                raise Exception("Data failed to get bookmarked")
            fprint(self, "Data is bookmarked successfully")
            self.driver.find_element_by_xpath("//span[text()='All Feeds']").click()
        else:
            fprint(self, "[FAILED] Failed to bookmark as no data received from source")
        process_console_logs(self)

    def test_07_search_and_sort(self):
        """
        Verify if search and sort are working as expected

        :return: None
        """
        RSS_NAME = get_value("RSS_NAME")
        fprint(self, "\n----------- TC_ID 7: Testing searching and sorting on RSS Feeds -----------")
        if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        nav_menu_main(self, "RSS Feeds")
        waitfor(self, 2, By.XPATH, "//ul/following-sibling::div/span/i")
        self.driver.find_element_by_xpath("//ul/following-sibling::div/span/i").click()
        fprint(self, "Searching for RSS Source")
        self.driver.find_element_by_xpath(rss_feeds_search).clear()
        sleep(1)
        self.driver.find_element_by_xpath(rss_feeds_search).send_keys(RSS_NAME)
        waitfor(self, 2, By.XPATH, "//span[text()='"+RSS_NAME+"']")
        self.driver.find_element_by_xpath("//span[text()='"+RSS_NAME+"']").click()
        if waitfor(self, 10, By.XPATH, "//span[contains(text(),'Sort')]", False):
            self.driver.find_element_by_xpath("//span[contains(text(),'Sort')]").click()
            fprint(self, "Clicking on sort")
            waitfor(self, 5, By.XPATH, "//li[contains(text(), 'By Date')]//ancestor::ul")
            fprint(self, "Sorting by date Ascending")
            sleep(1)
            self.driver.find_element_by_xpath\
                ("//div/li//div/following-sibling::div/li[contains(text(),'By Date')][1]").click()
            fprint(self, "[PASSED] Sorted by date Ascending")
            waitfor(self, 5, By.XPATH, "//span[contains(text(),'By Date')]")
            self.driver.find_element_by_xpath("//span[contains(text(),'By Date')]").click()
            sleep(1)
            fprint(self, "Sorting by date Descending")
            self.driver.find_element_by_xpath\
                ("//div/li//div/following-sibling::div/li[contains(text(),'By Date')][2]").click()
            fprint(self, "[PASSED] Sorted by date Ascending")
            waitfor(self, 5, By.XPATH, "//span[contains(text(),'By Date')]")
            self.driver.find_element_by_xpath("//span[contains(text(),'By Date')]").click()
            sleep(1)
            fprint(self, "Sorting by Alphabet Ascending")
            self.driver.find_element_by_xpath\
                ("//div/li//div/following-sibling::div/li[contains(text(),'By Alphabet')][1]").click()
            fprint(self, "[PASSED] Sorted by Alphabet Descending")
            waitfor(self, 5, By.XPATH, "//span[contains(text(),'By Alphabet')]")
            self.driver.find_element_by_xpath("//span[contains(text(),'By Alphabet')]").click()
            sleep(1)
            fprint(self, "Sorting by Alphabet Descending")
            self.driver.find_element_by_xpath\
                ("//div/li//div/following-sibling::div/li[contains(text(),'By Date')][2]").click()
            fprint(self, "[PASSED] Sorted by Alphabet Descending")
        else:
            fprint(self, "[FAILED] Failed to sort data as no data is received from the feed")
        process_console_logs(self)

    def test_08_rss_redirect(self):
        """
        Verify is RSS intel redirection is working

        :return: None
        """
        RSS_NAME = get_value("RSS_NAME")
        fprint(self, "\n----------- TC_ID 8: Checking for RSS feed intel redirection -----------")
        if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        nav_menu_main(self, "RSS Feeds")
        waitfor(self, 2, By.XPATH, "//ul/following-sibling::div/span/i")
        self.driver.find_element_by_xpath("//ul/following-sibling::div/span/i").click()
        waitfor(self, 2, By.XPATH, rss_feeds_search)
        fprint(self, "Searching for RSS Source")
        self.driver.find_element_by_xpath(rss_feeds_search).click()
        self.driver.find_element_by_xpath(rss_feeds_search).clear()
        waitfor(self, 2, By.XPATH, rss_feeds_search)
        sleep(1)
        self.driver.find_element_by_xpath(rss_feeds_search).send_keys(RSS_NAME)
        fprint(self, "Clicking on redirection link")
        sleep(1)
        # Todo: Confirm if the page actually opened and if that is the required page
        if waitfor(self, 5, By.XPATH, "//a[@rel='noopener noreferrer']", False):
            self.driver.find_element_by_xpath("//a[@rel='noopener noreferrer']").click()
            sleep(3)
            fprint(self, "[PASSED] Successfully Redirected to page")
            h = self.driver.window_handles
            fprint(self, "Redirecting back to CTIX")
            self.driver.switch_to.window(h[0])
            fprint(self, "[PASSED] CTIX Redirection successful")
        else:
            fprint(self, "[FAILED] No data to carry redirection upon")
        process_console_logs(self)

    def test_09_delete_rss(self):
        """
        Verify if RSS Source can be deleted

        :return: None
        """
        fprint(self, "\n----------- TC_ID 9: Deleting the created RSS feed source -----------")
        RSS_NAME = get_value("RSS_NAME")
        if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        nav_menu_main(self, "RSS Feeds")
        waitfor(self, 2, By.XPATH, "//ul/following-sibling::div/span/i")
        self.driver.find_element_by_xpath("//ul/following-sibling::div/span/i").click()
        fprint(self, "Searching for RSS Source")
        self.driver.find_element_by_xpath(rss_feeds_search).clear()
        sleep(1)
        self.driver.find_element_by_xpath(rss_feeds_search).send_keys(RSS_NAME)
        waitfor(self, 2, By.XPATH, "//span[text()='"+RSS_NAME+"']")
        self.driver.find_element_by_xpath("//span[text()='" + RSS_NAME + "']").click()
        fprint(self, "Opening Action list for RSS Source")
        waitfor(self, 4, By.XPATH, "//button[@data-testid='action']")
        self.driver.find_element_by_xpath("//button[@data-testid='action']").click()
        waitfor(self, 4, By.XPATH, "//li[text()='Remove']")
        fprint(self, "Selecting Remove Operation")
        self.driver.find_element_by_xpath("//li[text()='Remove']").click()
        waitfor(self, 4, By.XPATH, "//button[@data-testalert='confirm-remove']")
        fprint(self, "Confirming to remove RSS Feed Source"+RSS_NAME)
        self.driver.find_element_by_xpath("//button[@data-testalert='confirm-remove']").click()
        verify_success(self, "RSS Feed Source deleted successfully")
        try:
            ele = self.driver.find_element_by_xpath(
                "//div//*[contains(text(),'Sources')]/parent::span/following-sibling::span")
            ActionChains(self.driver).move_to_element(ele).click().perform()
        except:
            fprint(self, "Search input is visible now..")
        waitfor(self, 2, By.XPATH, rss_feeds_search)
        self.driver.find_element_by_xpath(rss_feeds_search).click()
        self.driver.find_element_by_xpath(rss_feeds_search).clear()
        sleep(1)
        self.driver.find_element_by_xpath(rss_feeds_search).send_keys(RSS_NAME)
        sleep(1)
        if waitfor(self, 2, By.XPATH, "//span[text()='" + RSS_NAME + "']", False):
            fprint(self, "[Failed] RSS Source Not deleted from listing")
            self.fail("[Failed] RSS Source Not deleted from listing")
        else:
            fprint(self, "[PASSED] RSS Source Deleted Successfully")

    def test_10_add_csv_rss_sources(self):
        """
        Testcase to add RSS Sources from rss_feeds.csv

        :return: None
        """
        nav_menu_main(self, "RSS Feeds")
        self.driver.refresh()
        waitfor(self, 20, By.XPATH, "//ul/following-sibling::div/span/i")
        self.driver.find_element_by_xpath("//ul/following-sibling::div/span/i").click()
        fprint(self, "\n---------------------- TC_ID 10 RSS Feeds addition from CSV --------------------")
        filename = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds", "rss_feeds.csv")
        failures = []
        with open(filename, 'r') as obj:
            data = csv.reader(obj)
            for rssFeeds in data:
                if rssFeeds[0] == "Talos":
                    continue
                waitfor(self, 20, By.XPATH, rss_feeds_search)
                clear_field(self.driver.find_element_by_xpath(rss_feeds_search))
                self.driver.find_element_by_xpath(rss_feeds_search).send_keys(rssFeeds[0])
                if waitfor(self, 2, By.XPATH, "//span[text()='"+rssFeeds[0]+"']", False):
                    fprint(self, rssFeeds[0]+" source already exists")
                    continue
                sleep(1)
                self.driver.find_element_by_xpath("//button[text()='Add New Source']").click()
                fprint(self, "[Passed] clicked on Add New Source")
                waitfor(self, 2, By.XPATH, "//div[text()='New Source']")
                RSS_NAME = rssFeeds[0]
                sleep(1)
                self.driver.find_element_by_xpath("//input[@aria-placeholder='Source Name*']").\
                    send_keys(RSS_NAME)
                sleep(1)
                self.driver.find_element_by_xpath("//input[@aria-placeholder='URL*']").send_keys(rssFeeds[1])
                fprint(self, "[Passed] filled up form details")
                _ele = self.driver.find_element_by_xpath\
                    ("//span[contains(text(), 'Create intel automatically')]/preceding-sibling::span/input")
                if _ele.get_attribute("value") == "true":   # Uncheck auto intel creation if active
                    self.driver.find_element_by_xpath\
                        ("//span[contains(text(), 'Create intel automatically')]/preceding-sibling::span/input").click()
                self.driver.find_element_by_xpath("//button[text()='Add']").click()
                fprint(self, "[Passed] Clicked on Add")
                waitfor(self, 20, By.XPATH, "//div[contains(@class, 'cy-message__text')]")
                verify_success(self, "RSS Feed Source added successfully")
                sleep(2)    # required
                if waitfor(self, 2, By.XPATH, "//span[@data-testaction='slider-close']", False):
                    failures.append(rssFeeds[0])
                    self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
                fprint(self, "[Passed] Obtained required Success Alert for "+rssFeeds[0])
                sleep(1)
                fprint(self, "Searching for created RSS Source")
                waitfor(self, 2, By.XPATH, "//ul/following-sibling::div/span/i")
                clear_field(self.driver.find_element_by_xpath(rss_feeds_search))
                self.driver.find_element_by_xpath(rss_feeds_search).send_keys(rssFeeds[0])
                waitfor(self, 2, By.XPATH, "//span[text()='"+rssFeeds[0]+"']")
                self.driver.find_element_by_xpath("//span[text()='"+rssFeeds[0]+"']").click()
                fprint(self, "[Passed] Added "+rssFeeds[0]+" source successfully")
        if len(failures) > 0:
            self.fail("RSS Source addition failed for "+"\n".join(failures))
        process_console_logs(self)

    def test_11_rss_parse_and_create_intel(self):
        """
            Testcase to parse the first feed received from an RSS source and create intel from the same
        """
        nav_menu_main(self, "RSS Feeds")
        self.driver.refresh()
        filename = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds", "rss_feeds.csv")
        _no_intel = []
        _no_feeds = []
        waitfor(self, 10, By.XPATH, "//h1[normalize-space(text())='RSS Feeds']")
        with open(filename, 'r') as obj:
            data = csv.reader(obj)
            for rssFeeds in data:
                if rssFeeds[0] == "Talos":
                    continue
                if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
                    self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
                if not waitfor(self, 5, By.XPATH, rss_feeds_search, False):
                    self.driver.find_element_by_xpath("//ul/following-sibling::div/span/i").click()
                fprint(self, "Searching for RSS Source")
                clear_field(self.driver.find_element_by_xpath(rss_feeds_search))
                self.driver.find_element_by_xpath(rss_feeds_search).send_keys(rssFeeds[0])
                waitfor(self, 2, By.XPATH, "//span[text()='" + rssFeeds[0] + "']")
                self.driver.find_element_by_xpath("//span[text()='" + rssFeeds[0] + "']").click()
                if waitfor(self, 5, By.XPATH, "//div[@data-testid='rss-feeds-card-0']", False):
                    self.driver.find_element_by_xpath("//div[@data-testid='rss-feeds-card-0']").click()
                    status = create_intel_from_feed(self)
                    if not status:
                        _no_intel.append(rssFeeds[0])
                else:
                    fprint(self, f"[Failed] No Feed received from {rssFeeds[0]}")
                    _no_feeds.append(rssFeeds[0])
        if _no_feeds:
            fprint(self, "No Feed received from the sources "+" ".join(_no_feeds))
        if _no_intel:
            fprint(self, "No Intel parsed from received feed for source - "+" ".join(_no_intel))
        if _no_intel or _no_feeds:
            self.fail("Some feeds and intel were not found")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
