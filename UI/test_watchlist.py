import unittest
from lib.ui.nav_app import *
from lib.ui.nav_tableview import click_on_actions_item
from lib.ui.quick_add import quick_create_ip
from selenium.webdriver.common.action_chains import ActionChains

class Watchlist(unittest.TestCase):

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

    name = "First_Watchlist"
    sau = "tu"
    ip = "11.216.88.107"
    mail ="hh852856@gmail.com"

    def test_01_Verify_Page_Load_Watchlist(self):
        """ Test case to verify that watchlist page load successfully"""
        fprint(self, "TC_ID: 8901 - Verify that the page load successfully")
        nav_menu_main(self, "Watchlist")
        fprint(self, "[Passed]-Clicked on Watchlist in main menu")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(), 'Watchlist')]")
        fprint(self, "[Passed]-The watchlist page loaded successfully")

    def test_02_Verify_Add_Watchlist(self):
        """ Test Case to verify that the watchlist are added successfully"""
        fprint(self, "TC_ID: 8902 - To verify that the watchlist are added successfully")
        nav_menu_main(self, "Watchlist")
        fprint(self, "[Passed]-Clicked on Watchlist in main menu")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(), 'Watchlist')]")
        fprint(self, "[Passed]-The watchlist page loaded successfully")
        if waitfor(self, 10, By.XPATH, "//button[@data-testid='new-watchlist']", False):
            self.driver.find_element_by_xpath("//button[@data-testid='new-watchlist']").click()
            fprint(self, "[Passed]-clicked on the button Add to watchlist")
            waitfor(self, 10, By.XPATH, "//div[contains(text(), 'Watchlist')]")
            fprint(self, "[Passed]-Add to watchlist pop up loaded successfully")
            self.driver.find_element_by_xpath("//input[@aria-placeholder='Add Keyword *']").send_keys(self.name)
            fprint(self, "[Passed]-Entered the value for the watchlist")
            self.driver.find_element_by_xpath(
                "(//button[contains(text(),'Add')])[2]").click()
            fprint(self, "Passed]-clicked on add Button")
            verify_success(self, "Keyword added to watchlist successfully.")
            fprint(self, "[Passed]-Added the keyword in Watchlist")
        else:
            waitfor(self, 10, By.XPATH, "//div[contains(text(), 'Watchlist')]")
            fprint(self, "[Passed]-Add to watchlist pop up loaded successfully")
            self.driver.find_element_by_xpath("//input[@aria-placeholder='Add Keyword *']").send_keys(self.name)
            fprint(self, "[Passed]-Entered the value for the watchlist")
            self.driver.find_element_by_xpath("//button[contains(text(),'Add')]").click()
            fprint(self, "Passed]-clicked on add Button")
            verify_success(self, "Keyword added to watchlist successfully.")
            fprint(self, "[Passed]-Added the keyword in Watchlist")


    def test_03_Verify_Added_Successfully(self):
        """ Test case to verify that the keyword was added successfully"""
        fprint(self, "TC_ID: 8903 - To verify that the keyword is added successfully in the watchlist module ")
        nav_menu_main(self, "Watchlist")
        fprint(self, "[Passed]-Clicked on Watchlist in main menu")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(), 'Watchlist')]")
        fprint(self, "[Passed]-The watchlist page loaded successfully")
        self.driver.find_element_by_xpath("//button[@data-testid='new-watchlist']").click()
        search(self, self.name)
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'"+self.name+"')])[2]")
        fprint(self, "[Passed]-Verified that the name added successfully")

    def test_04_Verify_That_Minimum_Length_Keyword(self):
        """ Test case to verify that the minimum length is 3"""
        fprint(self, "TC_ID: 8904 - To verify that minimum length of the keyword that is added is 3")
        nav_menu_main(self, "Watchlist")
        fprint(self, "[Passed]-Clicked on Watchlist in main menu")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(), 'Watchlist')]")
        fprint(self, "[Passed]-The watchlist page loaded successfully")
        self.driver.find_element_by_xpath("//button[@data-testid='new-watchlist']").click()
        fprint(self, "[Passed]-clicked on the button Add to watchlist")
        waitfor(self, 10, By.XPATH, "//div[contains(text(), 'Watchlist')]")
        fprint(self, "[Passed]-Add to watchlist pop up loaded successfully")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Add Keyword *']").send_keys(self.sau)
        fprint(self, "[Passed]-Entered the value for the watchlist")
        self.driver.find_element_by_xpath(
            "(//button[contains(text(),'Add')])[2]").click()
        fprint(self, "Passed]-clicked on add Button")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Enter at least 3 characters')]")
        fprint(self, "[Passed]-Verified that the length cannot be less than 3")

    def test_05_Verify_that_Keyword_Is_Mandatory(self):
        """ Test Case to verify that the keyword is mandatory field"""
        fprint(self, "TC_ID: 8905 - Test Case to verify that the keyword is mandatory field")
        nav_menu_main(self, "Watchlist")
        fprint(self, "[Passed]-Clicked on Watchlist in main menu")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(), 'Watchlist')]")
        fprint(self, "[Passed]-The watchlist page loaded successfully")
        self.driver.find_element_by_xpath("//button[@data-testid='new-watchlist']").click()
        fprint(self, "[Passed]-clicked on the button Add to watchlist")
        waitfor(self, 10, By.XPATH, "//div[contains(text(), 'Watchlist')]")
        fprint(self, "[Passed]-Add to watchlist pop up loaded successfully")
        self.driver.find_element_by_xpath(
            "(//button[contains(text(),'Add')])[2]").click()
        fprint(self, "Passed]-clicked on add Button")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Keyword is required')]")
        fprint(self, "[Passed]-Verified that the keyword is mandatory field")

    def test_06_Verify_Same_Name_Cannot_Be_Added_Again(self):
        """ Test Case to verify that same name cannot be added again"""
        fprint(self, "TC_ID: 8906 - Test Case to verify that the same name cannot be added again")
        nav_menu_main(self, "Watchlist")
        fprint(self, "[Passed]-Clicked on Watchlist in main menu")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(), 'Watchlist')]")
        fprint(self, "[Passed]-The watchlist page loaded successfully")
        self.driver.find_element_by_xpath("//button[@data-testid='new-watchlist']").click()
        fprint(self, "[Passed]-clicked on the button Add to watchlist")
        waitfor(self, 10, By.XPATH, "//div[contains(text(), 'Watchlist')]")
        fprint(self, "[Passed]-Add to watchlist pop up loaded successfully")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Add Keyword *']").send_keys(self.name)
        fprint(self, "[Passed]-Entered the value for the watchlist")
        self.driver.find_element_by_xpath(
            "(//button[contains(text(),'Add')])[2]").click()
        fprint(self, "Passed]-clicked on add Button")
        verify_success(self, "Watchlist with this name already exists !")
        fprint(self, "[Passed]-Added the keyword in Watchlist")

    def test_07_Verify_Occurences_increases(self):
        """Test case to verify that the occurences of watchlist increases"""
        fprint(self, "TC_ID: 8907 - To verify that occurances increases")
        nav_menu_main(self, "Watchlist")
        fprint(self, "[Passed]-Clicked on Watchlist in main menu")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(), 'Watchlist')]")
        fprint(self, "[Passed]-The watchlist page loaded successfully")
        self.driver.find_element_by_xpath("//button[@data-testid='new-watchlist']").click()
        fprint(self, "[Passed]-clicked on the button Add to watchlist")
        waitfor(self, 10, By.XPATH, "//div[contains(text(), 'Watchlist')]")
        fprint(self, "[Passed]-Add to watchlist pop up loaded successfully")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Add Keyword *']").send_keys(self.ip)
        fprint(self, "[Passed]-Entered the value for the watchlist")
        self.driver.find_element_by_xpath(
            "(//button[contains(text(),'Add')])[2]").click()
        fprint(self, "Passed]-clicked on add Button")
        verify_success(self, "Keyword added to watchlist successfully.")
        fprint(self, "[Passed]-Added the keyword in Watchlist")
        quick_create_ip(self, self.ip, self.ip)
        nav_menu_main(self, "Watchlist")
        search(self, self.ip)
        sleep(5)#mandatory
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'3')]/ancestor::div[@class ='cy-ellipsis'])[1]")
        fprint(self, "[Passed] Verified that the occurences are increasing")

    def test_08_Verify_Email_is_Mandatory(self):
        """ Test case to verify that email is mandatory field"""
        fprint(self, "TC_ID: 8908 - To verify that emails are the mandatory field")
        nav_menu_main(self, "Watchlist")
        fprint(self, "[Passed]-Clicked on Watchlist in main menu")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(), 'Watchlist')]")
        fprint(self, "[Passed]-The watchlist page loaded successfully")
        search(self, self.name)
        click_on_actions_item(self, self.name, 'Edit', 'Watchlist')
        fprint(self, "[Passed]-Clicked on edit successfully")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Watchlist')]")
        fprint(self, "[Passed]-Edit section loaded successfully")
        self.driver.find_element_by_xpath(
            "//span[contains(@class, 'cy-checkbox')]//following::span[contains(text(),'Enable Email Alert')]").click()
        fprint(self, "[Passed]-clicked on enable email alert")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'CTIX users')]")
        self.driver.find_element_by_xpath("(//button[contains(text(),'Update')])[2]").click()
        waitfor(self, 10, By.XPATH ,"//div[contains(text(),'Enter either a CTIX or a Non-CTIX email address to receive email notifications')]")
        fprint(self, "[Passed]-Verified that the emails are mandatory field")

    def test_09_Verify_Watchlist_Edit(self):
        """ Test case to verify that watchlist can be Edited successfully"""
        fprint(self, "TC_ID: 8909 - To verify that watchlist are Edited successfully")
        nav_menu_main(self, "Watchlist")
        fprint(self, "[Passed]-Clicked on Watchlist in main menu")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(), 'Watchlist')]")
        fprint(self, "[Passed]-The watchlist page loaded successfully")
        search(self, self.name)
        click_on_actions_item(self, self.name, 'Edit', 'Watchlist')
        fprint(self, "[Passed]-Clicked on edit successfully")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Watchlist')]")
        fprint(self, "[Passed]-Edit section loaded successfully")
        self.driver.find_element_by_xpath("//span[contains(@class, 'cy-checkbox')]//following::span[contains(text(),'Enable Email Alert')]").click()
        fprint(self, "[Passed]-clicked on enable email alert")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'CTIX users')]")
        ele = self.driver.find_element_by_xpath("//span[contains(text(),'Enter Email Addresses *')]")
        action = ActionChains(self.driver).move_to_element(ele)
        action.click()
        #action.send_keys(self.mail)
        action.perform()
        self.driver.find_element_by_xpath("//div[@class='cy-select-search multiple']//input[@type='text']").send_keys(self.mail)
        sleep(5)#mandatory
        fprint(self, "[Passed]-email value is sent successfully")
        waitfor(self, 10, By.XPATH, "(//button[contains(text(),'Update')])[2]")
        self.driver.find_element_by_xpath("(//button[contains(text(),'Update')])[2]").click()
        self.driver.find_element_by_xpath("(//button[contains(text(),'Update')])[2]").click()
        verify_success(self, "updated successfully.")
        fprint(self, "[Passed]-edit option is working fine")

    def test_10_Verify_watchlist_Deleted(self):
        """
        Test case to verify that watchlist is deleted successful.

        """
        fprint(self, "TC_ID: 8910 - To verify that watchlist are Deleted successfully")
        nav_menu_main(self, "Watchlist")
        fprint(self, "[Passed]-Clicked on Watchlist in main menu")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(), 'Watchlist')]")
        fprint(self, "[Passed]-The watchlist page loaded successfully")
        search(self, self.name)
        click_on_actions_item(self, self.name, 'Delete', 'Watchlist')
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'You will no longer be notified about any occurrences of this keyword. To confirm, click Delete.')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Delete')]").click()
        fprint(self, "[Passed]-clicked on Delete button")
        verify_success(self, "Keywords deleted from watchlist successfully.")
        fprint(self, "[Passed]-The keyword deletion test case is run succesfully")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
