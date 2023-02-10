import unittest
from lib.ui.nav_app import *
from lib.ui.nav_threat_data import verify_data_in_threatdata
from lib.ui.saved_search import *

ip = "67.55.71.97"  # Taken from the confidence score properties file
ss_title = "ss_automation"

failures = []


class SavedSearches(unittest.TestCase):

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

    set_value("SavedSearchName", "SavedSearch" + uniquestr)
    set_value("EditSavedSearchName", "EditSavedSearch" + uniquestr)

    def test_01_SavedSearches_PageLoad(self):
        fprint(self, "TC_ID: 1 - SavedSearches" + uniquestr)
        nav_menu_main(self, "Saved Searches")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(),'Saved Searches')]")
        process_console_logs(self)
        fprint(self, "TC_ID: 1 - Saved Searches - Saved Searches Page Load is verified")

    def test_02_SavedSearches_Add(self):
        fprint(self, "TC_ID: 2 - SavedSearches Add" + uniquestr)
        nav_menu_main(self, "Saved Searches")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add Saved Search')]").click()
        fprint(self, "TC_ID: 2 - Clicked on Add Button")
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Enter Name*']")
        fprint(self, "TC_ID: 2 - Add Saved Search slider is opened")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter Name*']").send_keys(get_value("SavedSearchName"))
        self.driver.find_element_by_xpath("(//button[contains(text(),'Save')])[1]").click()
        fprint(self, "TC_ID: 2 - Clicked on Save Button")
        verify_success(self, "Saved Search created successfully")
        process_console_logs(self)
        fprint(self, "TC_ID: 2 - Add Saved Search verified")

    def test_03_SavedSearches_Edit(self):
        fprint(self, "TC_ID: 3 - SavedSearches Edit " + uniquestr)
        nav_menu_main(self, "Saved Searches")
        self.driver.find_element_by_xpath("//input[@id='main-input']").click()
        self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys("" + get_value("SavedSearchName") + "")
        self.driver.find_element_by_xpath("//i[@data-testid='filter-search-icon']").click()
        fprint(self, "TC_ID: 3 - SavedSearches Edit: Entered search value and clicked on search icon")
        sleep(1)
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'" + get_value("SavedSearchName") + "')]/ancestor::a//button//i")
        self.driver.find_element_by_xpath("//span[contains(text(),'" + get_value("SavedSearchName") + "')]/ancestor::a//button//i").click()
        waitfor(self, 5, By.XPATH,"(//li[contains(text(),'Edit')])")
        self.driver.find_element_by_xpath("(//li[contains(text(),'Edit')])").click()
        fprint(self, "TC_ID: 3 - SavedSearches Edit: Clicked on Edit button")

        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Enter Name*']")
        fprint(self, "TC_ID: 3 - SavedSearches Edit: Edit Slider is opened")
        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter Name*']"))
        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter Name*']"))
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter Name*']").send_keys(get_value("EditSavedSearchName"))
        self.driver.find_element_by_xpath("(//button[contains(text(),'Save')])[1]").click()
        verify_success(self, "updated successfully")
        process_console_logs(self)

        self.driver.find_element_by_xpath("//i[@class='cyicon-cross-o-active cy-filters__icon']").click()
        sleep(0.5)
        self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys("" + get_value("EditSavedSearchName") + "")
        self.driver.find_element_by_xpath("//i[@data-testid='filter-search-icon']").click()
        waitfor(self, 5, By.XPATH,"//div[contains(text(),'" + get_value("EditSavedSearchName") + "')]")
        fprint(self, "TC_ID: 2 - Edit Saved Search verified")

    def test_04_SavedSearches_Delete(self):
        fprint(self, "TC_ID: 4 - SavedSearches Delete " + uniquestr)
        nav_menu_main(self, "Saved Searches")
        if self.driver.find_element_by_xpath("//i[@class='cyicon-cross-o-active cy-filters__icon']").is_displayed():
            self.driver.find_element_by_xpath("//i[@class='cyicon-cross-o-active cy-filters__icon']").click()
        self.driver.find_element_by_xpath("//input[@id='main-input']").click()
        self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys("" + get_value("EditSavedSearchName") + "")
        waitfor(self, 5, By.XPATH, "//i[@data-testid='filter-search-icon']")
        self.driver.find_element_by_xpath("//i[@data-testid='filter-search-icon']").click()
        fprint(self, "TC_ID: 3 - SavedSearches Delete: Entered search value and clicked on search icon")
        self.driver.find_element_by_xpath("//i[@class='cyicon-more-vertical']").click()
        waitfor(self, 5, By.XPATH, "(//li[contains(text(),'Delete')])")
        self.driver.find_element_by_xpath("(//li[contains(text(),'Delete')])").click()
        fprint(self, "TC_ID: 3 - SavedSearches Delete: Clicked on Delete button")

        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Are you sure you want to delete this ')]")
        fprint(self, "TC_ID: 3 - SavedSearches Delete: Edit pop up is opened")
        self.driver.find_element_by_xpath("//button[contains(text(),'Delete')]").click()
        verify_success(self, "Saved Search deleted successfully")
        process_console_logs(self)

        self.driver.find_element_by_xpath("//input[@id='main-input']").click()
        self.driver.find_element_by_xpath("//i[@data-testid='filter-search-icon']").click()
        waitfor(self, 5, By.XPATH, "//h1[contains(text(),'No Saved Search found!')]")
        fprint(self, "TC_ID: 2 - Delete Saved Search verified")

    def test_05_add_saved_search(self):
        fprint(self, "TC_ID: 4012585 - test_05_add_saved_search")
        nav_menu_main(self, "Threat Data")
        click_on_saved_search_link(self)
        verify_data_in_threatdata(self, value=ip, source="Import")
        save_search(self, title=ss_title)

    def test_06_verify_added_saved_search(self):
        fprint(self, "TC_ID: 4012586 - test_06_verify_added_saved_search")
        nav_menu_main(self, "Threat Data")
        click_on_saved_search_link(self)
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'"+ss_title+"')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'"+ss_title+"')]").click()
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'Import')]/ancestor::tr/td[3]//span[contains(text(),'"+ip+"')]")
        fprint(self, "[Passed] - Newly added saved search is visible")

    def test_07_verify_global_sharing(self):
        fprint(self, "TC_ID: 4012587 - test_07_verify_global_sharing")
        nav_menu_main(self, "Threat Data")
        click_on_saved_search_link(self)
        click_and_choose_from_dropdown_option(self, title=ss_title, option="Share it globally")
        waitfor(self, 2, By.XPATH, "//span[contains(text(),'"+ss_title+"')]/parent::span//span[contains(@class,'cyicon-user-unfilled')]")
        fprint(self, "Saved Search become private")
        #   Closing the dropdown
        self.driver.find_element_by_xpath("//span[contains(text(),'"+ss_title+"')]/ancestor::div[contains(@class,'cy-flex-between-center')]//div[@data-testaction='dropdown-link']").click()
        click_and_choose_from_dropdown_option(self, title=ss_title, option="Share it globally")
        waitfor(self, 2, By.XPATH, "//span[contains(text(),'"+ss_title+"')]/parent::span//span[contains(@class,'cyicon-world')]")
        fprint(self, "Saved Search become Globally available again")

    def test_08_verify_pin_unpin(self):
        fprint(self, "TC_ID: 4012588 - test_08_verify_pin_unpin")
        nav_menu_main(self, "Threat Data")
        click_on_saved_search_link(self)
        element = self.driver.find_element_by_xpath("//span[contains(text(),'"+ss_title+"')]")
        ActionChains(self.driver).move_to_element(element).perform()
        sleep(2)
        elements = self.driver.find_elements(By.XPATH, "//span[contains(@class,'cyicon-pin')]/parent::button")
        for element in elements:
            if element.is_displayed():
                element.click()
        fprint(self, "Clicked on the Pin Icon")
        waitfor(self, 2, By.XPATH, "//span[contains(text(),'"+ss_title+"')]/parent::span/following-sibling::div//span[contains(@class,'cyicon-unpin')]/parent::button")
        fprint(self, "Unpin Icon is visible")
        self.driver.find_element_by_xpath("//span[contains(text(),'"+ss_title+"')]/parent::span/following-sibling::div//span[contains(@class,'cyicon-unpin')]/parent::button").click()
        fprint(self, "Clicked on the Unpin Icon")
        waitfor(self, 2, By.XPATH, "//span[contains(text(),'"+ss_title+"')]/parent::span/following-sibling::div//span[contains(@class,'cyicon-pin')]/parent::button")
        fprint(self, "Pin Icon is visible")

    def test_09_verify_rename(self):
        fprint(self, "TC_ID: 4012589 - test_09_verify_rename")
        nav_menu_main(self, "Threat Data")
        click_on_saved_search_link(self)
        click_and_choose_from_dropdown_option(self, title=ss_title, option="Rename")
        waitfor(self, 5, By.XPATH, "//input[@placeholder='"+ss_title+"']")
        self.driver.find_element_by_xpath("//input[@placeholder='"+ss_title+"']").send_keys(ss_title+"_edit")
        self.driver.find_element_by_xpath("//input[@placeholder='"+ss_title+"']/ancestor::div[contains(@class,'cy-flex-between-center')]//button").click()
        fprint(self, "Clicked on the Save button")
        self.driver.refresh()
        fprint(self, "Browser refreshed, waiting for the Switch to saved search button...")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Saved Search')]")
        fprint(self, "Visible now")
        click_on_saved_search_link(self)
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'"+ss_title+"_edit')]")
        fprint(self, "[Passed] Rename functionality is working")

    def test_10_verify_remove(self):
        fprint(self, "TC_ID: 4012590 - test_10_verify_remove")
        nav_menu_main(self, "Threat Data")
        click_on_saved_search_link(self)
        click_and_choose_from_dropdown_option(self, title=ss_title+"_edit", option="Remove")
        verify_success(self, "Saved Search deleted successfully")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
