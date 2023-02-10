import unittest
from lib.ui.nav_app import *


class TwitterFeeds(unittest.TestCase):
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

    def search_twitter(self, ele, aux):
        """ Test case to select the element for search in twitter feeds"""
        nav_menu_main(self, "Twitter Feeds")
        fprint(self, "[Passed]-Clicked on twitter feeds successfully")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Twitter')]")
        fprint(self, "[passed] Page loaded successfully !")
        self.driver.find_element_by_xpath("//input[@id='main-input']").click()
        fprint(self, "[Passed]-clicked on search and filter successfullly")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+ele+"')]")
        fprint(self, '[Passed]-handle loaded successfully')
        self.driver.find_element_by_xpath("//span[contains(text(),'"+ele+"')]").click()
        fprint(self, "[Passed]-clicked on handle successfully")
        self.driver.find_element_by_xpath("//input[@name='search-filters']").send_keys(aux)
        fprint(self, "[Passed]-handle is fed to the search bar")
        self.driver.find_element_by_xpath("//input[@name='search-filters']").send_keys(Keys.ENTER)
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Press enter or click to search')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Press enter or click to search')]").click()
        fprint(self, "[Passed]-clicked on search")

    def test_01_verify_twitter_pageload(self):
        fprint(self, "TC_ID:98751  - to verify that the twitter feeds page loaded successfully")
        nav_menu_main(self, "Twitter Feeds")
        fprint(self, "[Passed]-Clicked on twitter feeds successfully")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Twitter')]")
        fprint(self, "[passed] Page loaded successfully !")
        process_console_logs(self)

    def test_02_verify_that_handle_can_be_searched(self):
        """ Test Case to verify that the handle can be searched"""
        fprint(self, "TC_ID:987502  - to verify that the handle can be searched in the twitter feed")
        self.search_twitter('Handle', 'malwrhunterteam')
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'@malwrhunterteam')])[1]")
        fprint(self, "[Passed]-handle searching is working fine")

    def test_03_verify_that_saved_search_can_be_created(self):
        """ test case to verify that the saved search can be created"""
        fprint(self, "TC_ID:987503  - to verify that the save search can be created")
        self.search_twitter('Handle', 'malwrhunterteam')
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'@malwrhunterteam')])[1]")
        fprint(self, "[Passed]-handle searching is working fine")
        waitfor(self, 10, By.XPATH, "//button[contains(text(),'Save Search')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save Search')]").click()
        waitfor(self, 10, By.XPATH, "//input[@aria-placeholder='Title *']")
        fprint(self, "[Passed]-clicked on the save search")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title *']").send_keys("Testing")
        fprint(self, "[Passed]-Entered the keyword for save search ")
        self.driver.find_element_by_xpath("//button[contains(text(),'Proceed')]").click()
        fprint(self, "[Passed]-clicked on the proceed button")

    def test_04_verify_that_save_search_is_created(self):
        """ Test case to verify that the saved search is created again"""
        fprint(self, "TC_ID:987504  - to verify that the saved search cannot be created again")
        nav_menu_main(self, "Twitter Feeds")
        fprint(self, "[Passed]-Clicked on twitter feeds successfully")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Twitter')]")
        fprint(self, "[Passed]-Twitter feed loaded successfully")
        waitfor(self, 10, By.XPATH,"//span[contains(text(),'Testing')]")
        fprint(self, "[Passed]-saved search created successfully")

    def test_05_verify_same_save_search_cannot_be_created(self):
        """ test case to verify that same saved search cannot be added again"""
        fprint(self, "TC_ID:987505  - to verify that the save search can be created")
        self.search_twitter('Handle', 'malwrhunterteam')
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'@malwrhunterteam')])[1]")
        fprint(self, "[Passed]-handle searching is working fine")
        waitfor(self, 10, By.XPATH, "//button[contains(text(),'Save Search')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save Search')]").click()
        waitfor(self, 10, By.XPATH, "//input[@aria-placeholder='Title *']")
        fprint(self, "[Passed]-clicked on the save search")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title *']").send_keys("Testing")
        fprint(self, "[Passed]-Entered the keyword for save search ")
        self.driver.find_element_by_xpath("//button[contains(text(),'Proceed')]").click()
        fprint(self, "[Passed]-clicked on the proceed button")
        verify_success(self, "Search already exist")
        fprint(self, "[Passed]-Same saved search connot be added again")

    def test_06_verify_saved_search_can_be_pinned(self):
        """ Test case to verify that the saved search can be pinned"""
        fprint(self, "TC_ID:987506  - Test case to verify that save search can be created")
        nav_menu_main(self, "Twitter Feeds")
        fprint(self, "[Passed]-Clicked on twitter feeds successfully")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Twitter')]")
        fprint(self, "[Passed]-Twitter feed loaded successfully")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Testing')]")
        self.driver.find_element_by_xpath("//button[@class='cy-flex-center cy-mr-2 cy-button cy-button--icon cy-button--sm']").click()
        fprint(self, "[Passed]-clicked on the action button")
        waitfor(self, 10, By.XPATH, "//li//span[contains(text(),'Pin')]")
        self.driver.find_element_by_xpath("//li//span[contains(text(),'Pin')]").click()
        fprint(self, "[Passed]-clicked on pin")
        self.driver.find_element_by_xpath(
            "//button[@class='cy-flex-center cy-mr-2 cy-button cy-button--icon cy-button--sm']").click()
        waitfor(self, 10, By.XPATH, "//li//span[contains(text(),'Unpin')]")
        fprint(self, "[Passed]- saved search pinned successfully")

    def test_07_verify_hashtag_search_working_fine(self):
        """
        Test case to verify that hashtag search is working fine
        """
        fprint(self, "TC_ID:987507  - test case to verify that hashtag search is working fine")
        self.search_twitter('Hashtags', 'test')
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'#test')])[1]")
        fprint(self, "[Passed]-Hastag searching is working fine")

    def test_08_verify_keyword_search_working_fine(self):
        """
        Test case to verify that keyword search is working fine
        """
        fprint(self, "TC_ID:987508  - test case to verify that keyword search is not working fine")
        self.search_twitter('Keywords', "https://t.co/fkmhwenI09 https://t.co/peyjm7aUbO")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'https://t.co/fkmhwenI09 https://t.co/peyjm7aUbO')]")
        fprint(self, "[Passed]- Verified that keyword search is working fine")

    def test_09_verify_tweet_can_bookmarked(self):
        """
        test case to verify that the tweet can be bookmarked
        """
        fprint(self, "TC_ID:987509  - Test case to verify that the tweet can be bookmarked")
        self.search_twitter('Keywords', "https://t.co/fkmhwenI09 https://t.co/peyjm7aUbO")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'https://t.co/fkmhwenI09 https://t.co/peyjm7aUbO')]")
        fprint(self, "[Passed]- Verified that keyword search is working fine")
        self.driver.find_element_by_xpath("(//i[@class='cyicon-bookmark'])[1]").click()
        fprint(self, "[Passed]-clicked on bookmarked successfully")

    def test_10_verify_tweet_bookmarked(self):
        """
        test case to verify that the tweet which was bookmarked is kept in bookmarked section
        """
        fprint(self, "TC_ID:987510  - Test case to verify that the tweet is present in the bookmarked section")
        nav_menu_main(self, "Twitter Feeds")
        fprint(self, "[Passed]-Clicked on twitter feeds successfully")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Twitter')]")
        fprint(self, "[passed] Page loaded successfully !")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Bookmarked')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Bookmarked')]").click()
        self.driver.find_element_by_xpath("//i[@class='cyicon-more-vertical']").click()
        fprint(self, "[Passed]-clicked on the action button")
        waitfor(self, 10, By.XPATH, "//span[normalize-space()='Unpin']")
        self.driver.find_element_by_xpath("//span[normalize-space()='Unpin']").click()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'@malwrhunterteam')]")
        fprint(self, "[Passed]-Verified that tweet bookmarked successfully")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())

