import unittest
from lib.ui.nav_threat_data import *

organizationType_name = "test_orgtype"
collection_name = "col_2.1"
organizationType_name_edit = "test_orgtype_edit"
collection_name2 = "col_2.0"
subscriber_name = "org_subscriber_name"


class OrganizationType(unittest.TestCase):

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

    def click_on_action_menu(self):
        waitfor(self, 10, By.XPATH, "//span[@data-testid='name']")
        ele = self.driver.find_element_by_xpath("//span[@data-testid='name']")
        ActionChains(self.driver).move_to_element(ele).perform()
        sleep(1)
        ele = self.driver.find_element_by_xpath("//button[@data-testid='action']")
        self.driver.execute_script("arguments[0].click();", ele)
        fprint(self, "Clicked on the Action menu")

    def subscriber_edit(self, subs_name):
        nav_menu_admin(self, "Integration Management")
        fprint(self, "Waiting for the Subscriber tab")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Subscribers')]/parent::a")
        self.driver.find_element_by_xpath("//span[contains(text(),'Subscribers')]/parent::a").click()
        fprint(self, "Clicked on the Subscriber tab")
        search(self, subs_name)
        self.click_on_action_menu()
        waitfor(self, 10, By.XPATH, "(//li[@name='select-option' and contains(text(),'Edit')])[2]")
        self.driver.find_element_by_xpath("(//li[@name='select-option' and contains(text(),'Edit')])[2]").click()

    def test_01_verify_add_organizationType(self):
        fprint(self, "TC_ID: 700801- test_01_verify_add_organizationType")
        nav_menu_admin(self, "Organization Type")
        fprint(self, "Waiting for the Collection Dropdown")
        waitfor(self, 20, By.XPATH, "//div[@name='collections']")
        self.driver.find_element_by_xpath("//div[@name='collections']").click()
        fprint(self, "Visible, clicked on the Collection Dropdown")
        self.driver.find_element_by_xpath("//input[@name='search-input']").send_keys(collection_name)
        waitfor(self, 10, By.XPATH, "//div[@name='text' and contains(text(),'" + collection_name + "')]")
        self.driver.find_element_by_xpath("//div[@name='text' and contains(text(),'" + collection_name + "')]").click()
        fprint(self, "Selected Collection - "+collection_name)
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys(organizationType_name)
        fprint(self, "Organization Type name set to - "+organizationType_name)
        self.driver.find_element_by_xpath("//button[@data-testaction='save-organization-type']").click()
        fprint(self, "Clicked on the Save the button")
        verify_success(self, "Organization Type created successfully")
        search(self, organizationType_name)
        waitfor(self, 20, By.XPATH, "//span[@data-testid='name']/ancestor::td/following-sibling::td[2]//span[contains(text(),'col_2.1')]")
        fprint(self, "[Passed] Organization Type Successfully Added")

    def test_02_verify_orgType_while_adding_subscriber(self):
        fprint(self, "TC_ID: 700802- test_02_verify_orgType_while_adding_subscriber")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "Waiting for the Subscriber tab")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Subscribers')]/parent::a")
        self.driver.find_element_by_xpath("//span[contains(text(),'Subscribers')]/parent::a").click()
        fprint(self, "Clicked on the Subscriber tab")
        waitfor(self, 2, By.XPATH, "//button[contains(text(),'Add Subscriber')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add Subscriber')]").click()
        fprint(self, "Clicked on the add Subscriber button")
        waitfor(self, 10, By.XPATH, "//input[@aria-placeholder='Subscriber Name *']")
        fprint(self, "Filling Subscriber details -")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Subscriber Name *']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Subscriber Name *']").send_keys(subscriber_name)
        fprint(self, "Subscriber Name - "+subscriber_name)
        self.driver.find_element_by_xpath("//div[@name='organization_types']").click()
        self.driver.find_element_by_xpath("//input[@name='search-input']").send_keys(organizationType_name)
        waitfor(self, 10, By.XPATH, "//div[@name='text' and contains(text(),'"+organizationType_name+"')]")
        self.driver.find_element_by_xpath("//div[@name='text' and contains(text(),'"+organizationType_name+"')]").click()
        fprint(self, "Selected Organization type - "+organizationType_name)
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name*']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name*']").send_keys("org_automation_name")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Email *']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Email *']").send_keys("automation@cyware.com")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Confidence *']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Confidence *']").send_keys("90")
        fprint(self, "Name, email and confidence score is filled up now")
        waitfor(self, 10, By.XPATH, "//div[@name='data-value-0' and contains(text(),'"+collection_name+"')]")
        fprint(self, "[Passed] Respective Organization Type collection is visible - "+collection_name)
        self.driver.find_element_by_xpath("//button[@data-testid='save-subscribers']").click()
        verify_success(self, "Subscriber created successfully")
        waitfor(self, 10, By.XPATH, "//span[@data-testaction='slider-close']")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        nav_menu_admin(self, "Organization Type")
        search(self, organizationType_name)
        waitfor(self, 10, By.XPATH, "//div[contains(@class,'cy-data-renderer__value')]//span[normalize-space()='1']")
        fprint(self, "[Passed] Subscriber count is increased by 1")

    def test_03_verify_edit_organizationType(self):
        fprint(self, "TC_ID: 700803- test_03_verify_edit_organizationType")
        nav_menu_admin(self, "Organization Type")
        search(self, organizationType_name)
        self.click_on_action_menu()
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Edit')]/parent::div")
        self.driver.find_element_by_xpath("//div[contains(text(),'Edit')]/parent::div").click()
        fprint(self, "Clicked on the Edit option")
        waitfor(self, 20, By.XPATH, "//div[@name='collections']")
        self.driver.find_element_by_xpath("//div[@name='collections']").click()
        fprint(self, "Clicked on the Collection Dropdown")
        self.driver.find_element_by_xpath("//input[@name='search-input']").send_keys(collection_name2)
        waitfor(self, 10, By.XPATH, "//div[@name='text' and contains(text(),'" + collection_name2 + "')]")
        self.driver.find_element_by_xpath("//div[@name='text' and contains(text(),'" + collection_name2 + "')]").click()
        fprint(self, "Selected Collection - " + collection_name2 + " and " + collection_name)
        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']"))
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys(organizationType_name_edit)
        fprint(self, "Organization Type name set to - " + organizationType_name_edit)
        self.driver.find_element_by_xpath("//button[@data-testaction='update-organization-type']").click()
        fprint(self, "Clicked on the Update button")

    def test_04_verify_edit_orgType_in_subscriber(self):
        fprint(self, "TC_ID: 700804- test_04_verify_edit_orgType_in_subscriber")
        self.subscriber_edit(subscriber_name)
        waitfor(self, 10, By.XPATH, "//div[@name='data-value-0' and contains(text(),'"+organizationType_name_edit+"')]")
        fprint(self, "[Passed] Updated Organization Type name is visible - "+organizationType_name_edit)
        waitfor(self, 10, By.XPATH, "//div[@name='data-value']//div[contains(text(),'"+collection_name2+"')]")
        fprint(self, "[Passed] Updated Organization Type collection is visible - "+collection_name2)

    def test_05_verify_disabling_linked_orgType(self):
        fprint(self, "TC_ID: 700805- test_05_verify_enable_disable_toggleButton")
        nav_menu_admin(self, "Organization Type")
        search(self, organizationType_name)
        if waitfor(self, 5, By.XPATH, "//span[contains(@class,'active')]/input[@value='true']", False):
            self.driver.find_element_by_xpath("//span[contains(@class,'active')]/input[@value='true']").click()
        else:
            self.driver.find_element_by_xpath("//span[@class='cy-switch-btn__icon']").click()
        fprint(self, "Clicked on the Toggle button")
        verify_success(self, "This Organization cannot be disabled as it has at least one subscriber associated with it")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())