import unittest
from lib.ui.nav_tags import *
from lib.ui.nav_tableview import *
from lib.ui.nav_threat_data import verify_data_in_threatdata, click_on_intel


class Tags(unittest.TestCase):

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

    def test_01_tags_add(self):
        # Test Case to add a Tag in CTIX V3
        fprint(self, "TC_ID: 1 - Tags - Add Tag")
        add_tag(self, "test_tag_auto")
        fprint(self, "TC_ID: 1 - Tag added")

    def test_02_tags_search(self):
        # Test case to verify whether a tag is added
        fprint(self, "TC_ID: 2 - Tags - search test_tag_auto")
        nav_menu_main(self, "Tags")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        fprint(self, "[Passed] - Clicked on Search field")
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("test_tag_auto")
        fprint(self, "[Passed] - Provided search data to  Search field")
        self.driver.find_element_by_xpath("//span[contains(text(),'Press enter or click to search')]").click()
        fprint(self, "[Passed] - Search action performed")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        waitfor(self,10,By.XPATH,"(//span[contains(text(),'test_tag_auto')])[1]")
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'Clear All')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Clear All')]").click()
        fprint(self, "TC_ID: 2 - Tag searched")

    def test_03_Verify_Duplicate_tags_Cannot_be_added(self):
        fprint(self, "TC_ID: 3 - Try to create Duplicate Tag")
        nav_menu_main(self, "Tags")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add')]").click()
        fprint(self, "[Passed]- Clicked on  Add Tag Button")
        waitfor(self, 5, By.XPATH, "//input[contains(@aria-placeholder,'Tag Name*')]")
        fprint(self, "[Passed] -Adding the tag name")
        self.driver.find_element_by_xpath("//input[contains(@aria-placeholder,'Tag Name*')]").send_keys("test_tag_auto")
        fprint(self, "[Passed] -Selecting the color for the tag")
        if waitfor(self, 10, By.XPATH, "//div[contains( @style,'--color: #5236E2')]"):
            # writing this to handle the case in firefox
            self.driver.find_element_by_xpath("//div[contains( @style,'--color: #5236E2')]").click()
        elif waitfor(self, 10, By.XPATH, "//div[contains( @style,'color:#5236E2')]"):
            # writing this to handle the case in chrome
            self.driver.find_element_by_xpath("//div[contains( @style,'color:#5236E2')]").click()
        else:
            fprint(self, "[Failed]- Color element for tag not found")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "[Passed] - Clicked on Save")
        verify_success(self, "Value provided for the field already exists")
        fprint(self, "TC_ID: 1 - Test Duplicate Tags")

    def test_04_Verify_Tag_in_Threat_Data(self):
        fprint(self, "TC_ID: 4 - Check whether the tag test_tag_auto reflects in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, "12.12.12.43", "Import")
        # fprint(self, "[Passed]-Clicked on the threat Data ")
        # self.driver.find_element_by_xpath("(//input[contains(@placeholder,'Search')])[4]").send_keys("12.12.12.43")
        # fprint(self, "[Passed]-Clicking on the search button")
        # self.driver.find_element_by_xpath("//*[@data-testaction='search-icon']").click()
        # fprint(self, 'Search button is clicked')
        # waitfor(self, 20, By.XPATH, "(//span[contains(text(),'12.12.12.43')])[1]")
        # fprint(self, "[Passed] -Waitfor Ran succesfully")
        # ele = self.driver.find_element_by_xpath("(//span[contains(text(),'12.12.12.43')])[1]")
        # action = ActionChains(self.driver).move_to_element(ele)
        # action.click()
        # action.perform()
        click_on_intel(self, "Import", "12.12.12.43")
        fprint(self, "Checking for the overview page is being loaded or not")
        waitfor(self, 10, By.XPATH, "//div[normalize-space()='Overview']")
        fprint(self, "[Passed]- Basic details page is loaded")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),' Add Tag')]")
        self.driver.find_element_by_xpath("//span[contains(text(),' Add Tag')]").click()
        fprint(self, "[Passed]- Clicked on Add Tag")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),' Add Tag')]")
        self.driver.find_element_by_xpath("//input[@placeholder='Search Tags']").send_keys("test_tag_auto")
        fprint(self, "[Passed]- Searched for the test_tag_auto")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'test_tag_auto')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'test_tag_auto')]").click()
        self.driver.refresh()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'test_tag_auto')]")
        fprint(self, "[Passed]- Tag is visible in threat data")

    def test_05_tags_edit(self):
        fprint(self, "TC_ID: 5- Tags - edit Functionality")
        nav_menu_main(self, "Tags")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        fprint(self, "[Passed] - Clicked on Search field")
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("test_tag_auto")
        fprint(self, "[Passed] - Provided search data to  Search field")
        self.driver.find_element_by_xpath("//*[@data-testid='filter-search-icon']").click()
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'test_tag_auto')])[1]")
        fprint(self, "[Passed]-clicking on the edit button in the action tab")
        fprint(self, "[Passed] - Clicked on Action dropdown")
        ele= self.driver.find_element_by_xpath("(//span[@data-testid='name' and contains(text(),test_tag_auto)])[1]")
        ActionChains(self.driver).move_by_offset(1,1).perform()
        ActionChains(self.driver).move_to_element(ele).perform()
        sleep(2)
        fprint(self, "Waiting fot the channel - test_tag_auto")
        self.driver.find_element_by_xpath("(//span[contains(text(), 'test_tag_auto')])[1]/ancestor::tr//button[@data-testid='action']").click()
        fprint(self, "[Passed]-Waiting for the Action button to load ")
        waitfor(self, 10, By.XPATH, "(//span[contains(text(), 'test_tag_auto')])[1]/ancestor::tr//button[@data-testid='action']")
        self.driver.find_element_by_xpath("//div[contains(text(),'Edit')]").click()
        fprint(self, "[Passed]- Clicked on edit Button")
        waitfor(self, 5, By.XPATH, "//input[contains(@aria-placeholder,'Tag Name*')]")
        self.driver.find_element_by_xpath("//input[contains(@aria-placeholder,'Tag Name*')]").send_keys("test_tag_auto_1")
        self.driver.find_element_by_xpath("//div[contains( @style,'--color: #EB9C00')]").click()
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "[Passed] - Clicked on Save")
        verify_success(self, "Tag updated successfully")
        fprint(self, "[Passed] - Edit action performed")

    def test_06_tags_delete(self):
        fprint(self, "TC_ID: 6 - Tags - delete test_tag_autotest_tag_auto_1")
        self.driver.refresh()
        sleep(5)
        nav_menu_main(self, "Tags")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        fprint(self, "[Passed] - Clicked on Search field")
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("test_tag_autotest_tag_auto_1")
        fprint(self, "[Passed] - Provided search data to  Search field")
        self.driver.find_element_by_xpath("//*[@data-testid='filter-search-icon']").click()
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'test_tag_autotest_tag_auto_1')])[1]")
        fprint(self, "[Passed]-clicking on the edit button in the action tab")
        fprint(self, "[Passed] - Clicked on Action dropdown")
        ele = self.driver.find_element_by_xpath("(//span[@data-testid='name' and contains(text(),test_tag_autotest_tag_auto_1)])[1]")
        ActionChains(self.driver).move_by_offset(1, 1).perform()
        ActionChains(self.driver).move_to_element(ele).perform()
        sleep(2)
        fprint(self, "Waiting fot the channel - test_tag_autotest_tag_auto_1")
        self.driver.find_element_by_xpath("(//span[contains(text(), 'test_tag_autotest_tag_auto_1')])[1]/ancestor::tr//button[@data-testid='action']").click()
        fprint(self, "[Passed]-Waiting for the Action button to load ")
        waitfor(self, 10, By.XPATH, "(//span[contains(text(), 'test_tag_autotest_tag_auto_1')])[1]/ancestor::tr//button[@data-testid='action']")
        self.driver.find_element_by_xpath("//div[contains(text(),'Delete')]").click()
        fprint(self, "[Passed]- Clicked on Delete Button")
        sleep(10)
        self.driver.find_element_by_xpath("//button[contains(text(),'Delete')]").click()
        fprint(self, "[Passed]- Clicked on  Yes Delete Button")
        verify_success(self, "Custom created tags deleted successfully")
        fprint(self, "TC_ID: 6 - Tag delete")

    def test_07_verify_Name_is_required(self):
        fprint(self, "TC_ID: 7 - Tags - Verify that the name is the required field")
        self.driver.refresh()
        sleep(5)
        nav_menu_main(self, "Tags")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add')]").click()
        fprint(self, "[Passed]- Clicked on  Add Tag Button")
        waitfor(self, 5, By.XPATH, "//input[contains(@aria-placeholder,'Tag Name*')]")
        if waitfor(self, 10, By.XPATH, "//div[contains( @style,'--color: #5236E2')]"):
            # writing this to handle the case in firefox
            self.driver.find_element_by_xpath("//div[contains( @style,'--color: #5236E2')]").click()
        elif waitfor(self, 10, By.XPATH, "//div[contains( @style,'color:#5236E2')]"):
            # writing this to handle the case in chrome
            self.driver.find_element_by_xpath("//div[contains( @style,'color:#5236E2')]").click()
        else:
            fprint(self, "[Failed]- Color element for tag not found")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "[Passed] - Clicked on Save")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Tag name is required')]")
        fprint(self, "[Passed] -Tag cannot be saved without Name")

    def test_08_Verify_Color_is_required(self):
        fprint(self, "TC_ID: 8 - Tags - Verify that the Color is the required field")
        self.driver.refresh()
        sleep(5)
        nav_menu_main(self, "Tags")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add')]").click()
        fprint(self, "[Passed]- Clicked on  Add Tag Button")
        if waitfor(self, 5, By.XPATH, "//div[contains(@class,'cy-color-dot--selected')]", False):
            self.driver.find_element_by_xpath("//button[contains(text(),'Clear')]").click()
        self.driver.find_element_by_xpath("//input[contains(@aria-placeholder,'Tag Name*')]").send_keys("Test_Without_Color")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "[Passed] - Clicked on Save")
        waitfor(self, 10, By.XPATH, "//div[contains( text(), 'You must choose a Color code')]")
        fprint(self, "[Passed] -Tag cannot be saved without Color")

    def test_09_Verify_Tag_Visible_from_threat_data(self):
        fprint(self, "TC_ID: 8 - Tags - Verify that the Tags created in threat data are visible")
        self.driver.refresh()
        sleep(5)
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, "12.12.12.43", "Import")
        # fprint(self, "[Passed]-Send the value of Ip value to be searched in the test case")
        # self.driver.find_element_by_xpath("(//input[contains(@placeholder,'Search')])[4]").send_keys('12.12.12.43')
        # fprint(self, "[Passed]-Clicking on the search button")
        # sleep(4)
        # fprint(self, "[Passed]-Clicking on the indicator that needs to be searched")
        # waitfor(self, 10, By.XPATH, "(//span[contains(text(),'12.12.12.43')])[1]")
        # ele = self.driver.find_element_by_xpath("(//span[contains(text(),'12.12.12.43')])[1]")
        # action = ActionChains(self.driver).move_to_element(ele)
        # action.click()
        # action.perform()
        click_on_intel(self, "Import", "12.12.12.43")
        fprint(self, "[Passed]-Checking for the overview page is being loaded or not")
        waitfor(self, 10, By.XPATH, "//div[normalize-space()='Overview']")
        fprint(self, "[Passed]-Clicking Add tag to add the Tag")
        self.driver.find_element_by_xpath("//span[contains(text(),'Add Tag')]").click()
        waitfor(self, 10, By.XPATH, "//input[@placeholder='Search Tags']")
        fprint(self, "[Passed]- sending values to the Search Tag")
        self.driver.find_element_by_xpath("//input[@placeholder='Search Tags']").send_keys("sau_tag_test")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(),'+ Add Tag')]").click()
        fprint(self, "[Passed]-Clicked the Add tag Button")
        sleep(10)
        self.driver.refresh()
        sleep(5)
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'sau_tag_test')]")
        fprint(self, "[Passed] - The Tag is present in the Threat data Basic details page")
        nav_menu_main(self, "Tags")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        fprint(self, "[Passed] - Clicked on Search field")
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("sau_tag_test")
        fprint(self, "[Passed] - Provided search data to  Search field")
        self.driver.find_element_by_xpath("//span[contains(text(),'Press enter or click to search')]").click()
        fprint(self, "[Passed] - Search action performed")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'sau_tag_test')])[1]")
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'Clear All')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Clear All')]").click()
        fprint(self, "TC_ID: 9- Tag searched in Tags")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
