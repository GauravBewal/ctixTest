import unittest
from lib.ui.nav_app import *


class MyProfile(unittest.TestCase):

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

    new_first_name = 'NewSystem'
    new_last_name = 'NewDefault'

    def load_profile(self):
        nav_menu_main(self, "Dashboards")
        waitfor(self, 2, By.XPATH, "//a[@href='/ctix/profile']/div/span")
        self.driver.find_element_by_xpath("//a[@href='/ctix/profile']/div/span").click()
        waitfor(self, 2, By.XPATH, "//h1[contains(text(),'My Profile')]")
        fprint(self, "[PASSED] My Profile page loaded successfully")

    def test_01_my_profile_loading(self):
        """
        Verify if My Profile page is loading
        """
        fprint(self, "----------- TC_ID: 1311 Verifying if my profile page is loading ----------")
        self.load_profile()
        process_console_logs(self)

    def test_02_notification_settings(self):
        """
        Verify if notification settings are available
        """
        fprint(self, "----------- TC_ID: 1312 Verifying if notification settings are avaliable----------")
        self.load_profile()
        waitfor(self, 2, By.XPATH, "//span[contains(text(), 'Notification  Settings')]")
        self.driver.find_element_by_xpath("//span[contains(text(), 'Notification  Settings')]").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(), 'Email Notification')]/preceding-sibling::div")
        waitfor(self, 2, By.XPATH, "//div[contains(text(), 'Application Notification')]/preceding-sibling::div")
        fprint(self, "[PASSED] Notification settings loaded successfully")
        process_console_logs(self)

    def test_03_other_settings(self):
        """
        Verify if other settings are available
        """
        fprint(self, "----------- TC_ID: 1313 Verifying if other settings are avaliable----------")
        self.load_profile()
        waitfor(self, 2, By.XPATH, "//span[text()='Other Settings']")
        self.driver.find_element_by_xpath("//span[text()='Other Settings']").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(), 'Two Factor Authentication')]")
        fprint(self, "[PASSED] Other Settings loaded successfully")
        process_console_logs(self)

    def test_04_pagination_setting(self):
        ''' Test case to change the pagination setting'''
        fprint(self, "----------- TC_ID: 1314 Verifying if Pagination settings can be changed---------")
        self.load_profile()
        waitfor(self, 10, By.XPATH, "//div[@aria-label='Default Page Limit']")
        self.driver.find_element_by_xpath("//div[contains(@data-testaction,'close')]//span").click()
        fprint(self, "[Passed]-clicked on the drop down menu")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'100')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'100')]").click()
        fprint(self, "[Passed]- clicked on 100 pagination")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//div[contains(@name,'data-value') and contains(text(),'100')]")
        fprint(self, "[Passed]-set the page limit to 100 for the user")

    def test_05_verify_pagination_setting(self):
        '''Test case to verify that the pagination ios working fine '''
        fprint(self, "----------- TC_ID: 1315 Verifying if the pagination is updated successfully----------")
        nav_menu_main(self, "Threat Data")
        fprint(self, "[Passed]-clicked on the Threat data")
        elem =(self.driver.find_element_by_xpath("//input[@placeholder='Select']")).get_attribute("value")
        if elem == '100/page':
            fprint(self, "[Passed]-verified that the page limit is set successfully")
        else:
            fprint(self, "[Failed]-value is not updated successfully")
            self.fail("[Failed]-value is not updated successfully")

    def test_06_view_activity_logs(self):
        ''' Test case to verify that we are able to access the user activity logs'''
        fprint(self, "----------- TC_ID: 1316 Verifying if view activity logs is working fine----------")
        self.load_profile()
        self.driver.find_element_by_xpath(
            "//div[@data-testaction='dropdown-link']/button[contains(@class,'cyicon-more')]").click()
        fprint(self, "[Passed]-clicked on the action button")
        waitfor(self, 10, By.XPATH, "//li[normalize-space()='View Activity Logs']")
        self.driver.find_element_by_xpath("//li[normalize-space()='View Activity Logs']").click()
        fprint(self, "[Passed]-clicked on the Activity logs")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'My Activity Logs')]")
        search(self, "/ctixapi/rest-auth/user-details/")
        waitfor(self, 10, By.XPATH, "(//div[contains(text(),'/ctixapi/rest-auth/user-details/')]/span)[1]")
        fprint(self, "[Passed]-Activity logs are opened successfully")

    def test_07_change_first_name(self):
        ''' Test case to change the first name in my profile '''
        fprint(self, "----------- TC_ID: 1317 Verifying if change first name is working fine----------")
        self.load_profile()
        self.driver.find_element_by_xpath("//div[contains(text(),'System')]//div//span").click()
        fprint(self, "[Passed]-clicked on the edit button")
        waitfor(self, 10, By.XPATH, "//input[contains(@aria-placeholder,'First Name')]")
        val = self.driver.find_element_by_xpath("//input[contains(@aria-placeholder,'First Name')]")
        clear_field(val)
        self.driver.find_element_by_xpath("//input[contains(@aria-placeholder,'First Name')]").send_keys(self.new_first_name)
        fprint(self, "[Passed]-Entered the new first Name")
        self.driver.find_element_by_xpath("//button[normalize-space()='Update']").click()
        fprint(self, "[Passed]-clicked on the update")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'"+self.new_first_name+"')]")
        fprint(self, "[Passed]-First Name Updated Successfully")

    def test_08_change_last_name(self):
        ''' Test case to verify that the last name can be updated'''
        fprint(self, "----------- TC_ID: 1318 Verifying if change last name is working fine----------")
        self.load_profile()
        self.driver.find_element_by_xpath("//div[contains(text(),'"+self.new_first_name+"')]//div//span").click()
        fprint(self, "[Passed]-clicked on the edit button")
        waitfor(self, 10, By.XPATH, "//input[contains(@aria-placeholder,'Last Name')]")
        val1 = self.driver.find_element_by_xpath("//input[contains(@aria-placeholder,'Last Name')]")
        clear_field(val1)
        self.driver.find_element_by_xpath("//input[contains(@aria-placeholder,'Last Name')]").send_keys(self.new_last_name)
        fprint(self, "[Passed]-Entered the new Last Name")
        self.driver.find_element_by_xpath("//button[normalize-space()='Update']").click()
        fprint(self, "[Passed]-clicked on the update")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'"+self.new_last_name+"')]")
        fprint(self, "[Passed]-Last Name Updated Successfully")

    def test_09_verify_only_alphabet_can_be_added(self):
        ''' Test case to verify that only alphabet can be added in the name'''
        fprint(self, "----------- TC_ID: 1319 Verifying that only alphabet can be added in the name----------")
        self.load_profile()
        self.driver.find_element_by_xpath("//div[contains(text(),'"+self.new_first_name+"')]//div//span").click()
        fprint(self, "[Passed]-clicked on the edit button")
        waitfor(self, 10, By.XPATH, "(//div[contains(text(),'Edit Profile')])[2]")
        val1 = self.driver.find_element_by_xpath("//input[contains(@aria-placeholder,'First Name')]")
        clear_field(val1)
        self.driver.find_element_by_xpath("//input[contains(@aria-placeholder,'First Name')]").send_keys("System3")
        fprint(self, "[Passed]-Entered the new Last Name")
        self.driver.find_element_by_xpath("//button[normalize-space()='Update']").click()
        fprint(self, "[Passed]-clicked on the update")
        verify_success(self, "Please provide alphabets only", timeout=30)
        fprint(self, "[Passed]-Verified that only alphabets acn be added")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
