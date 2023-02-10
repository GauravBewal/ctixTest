import unittest
from lib.ui.nav_app import *
from lib.ui.nav_tableview import *
from lib.ui.nav_create_intel_package import *


class CreateIntelPackage(unittest.TestCase):

    # --------------- Test Data -----------------
    # Write
    cip_domain = "domain" + uniquestr + ".com"
    set_value("cip_domain", cip_domain)
    # Read
    stix_collection = get_value("stix_collection")
    # -------------------------------------------

    #@classmethod
    #def setUpClass(self):
    #    self.driver = initialize_browser(self)
    #    login(self, Admin_Email, Admin_Password)

    #@classmethod
    #def tearDownClass(self):
    #    self.driver.quit()

    @classmethod
    def setUp(self):
        self.driver = initialize_browser(self)
        login(self, Admin_Email, Admin_Password)
        clear_console_logs(self)

    @classmethod
    def tearDown(self):
        self.driver.quit()

    def test_01_create_intel_package_indicator(self):
        fprint(self, "TC_ID: 52 - Create Intel Package - Indicator - STIX: " + "IntelPackage_"+uniquestr)
        nav_menu_main(self, "Create Intel Package")
        fprint(self, "Clicking on Add New button")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add New')]/span").click()
        sleep(1)  # Static wait is important here.
        waitfor(self, 2, By.XPATH, "//li[text()='Detailed Submission']")
        fprint(self, "[Passed] Found Detailed Submission in drop down menu, Clicking on it")
        self.driver.find_element_by_xpath("//li[text()='Detailed Submission']").click()
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Title*']")
        fprint(self, "[Passed] Reached on Detailed Submission Page, Entering Details")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys("IntelPackage_"+uniquestr)
        sleep(1)
        fprint(self, "Clicking on Indicator checkbox")
        self.driver.find_element_by_xpath("//div[@class ='cy-page__body w-100']//span[contains(text(), 'Indicator')]").click()
        cip_left_submenu(self, "Indicator")
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Name*']")
        fprint(self, "[Passed] Indicator Detailed page is visible, Entering details")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name*']").send_keys("IndicatorName_"+uniquestr)
        sleep(1)
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description']").send_keys("Basic Intel Description")
        fprint(self, "Choosing Pattern Type as STIX")
        self.driver.find_element_by_name("pattern_type").click()
        sleep(2)
        self.driver.find_element_by_xpath("//div[@name='pattern_type']/descendant-or-self::div[contains(text(),'STIX')]").click()
        fprint(self, "Clicking on Valid From Calendar and Choosing today as the date")
        waitfor(self, 5, By.XPATH, "//input[@name='valid_from']")
        self.driver.find_element_by_xpath("//input[@name='valid_from']").click()
        sleep(2)
        self.driver.find_element_by_xpath("//td[@class='available today']").click()
        sleep(2)
        fprint(self, "Clicking on Valid To Calendar and Choosing next month as the date")
        self.driver.find_element_by_xpath("//input[@name='valid_until']").click()
        sleep(2)
        self.driver.find_element_by_xpath("//td[@class='next-month'][1]").click()
        sleep(2)
        cip_navigate_tabs(self, "Common Fields")
        sleep(2)
        fprint(self, "Selecting TLP as Red")
        self.driver.find_element_by_xpath("//div[@name='tlp']").click()
        sleep(2)
        self.driver.find_element_by_xpath("//div[@name='tlp']/descendant-or-self::div[contains(text(),'Red')]").click()
        sleep(2)
        cip_navigate_tabs(self, "STIX")
        sleep(2)
        fprint(self, "Adding Observable Expression")
        self.driver.find_element_by_xpath("//div[@name='type']").click()
        sleep(2)
        self.driver.find_element_by_xpath("//div[@name='type']/descendant-or-self::div[contains(text(),'Domain')]").click()
        fprint(self, "[Passed] Added Domain as type")
        sleep(1)
        self.driver.find_element_by_xpath("//div[@name='id']").click()
        sleep(2)
        fprint(self, "Adding a new Domain value")
        self.driver.find_element_by_xpath("//div[@name='id']/descendant-or-self::button[contains(text(),'+ Add New')]").click()
        sleep(2)
        waitfor(self, 5, By.XPATH, "//div[text()='Add New']")
        sleep(1)
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Value']").send_keys(self.cip_domain)
        sleep(1)
        fprint(self, "Clicking on Save Button while adding Domain")
        self.driver.find_element_by_xpath("//div[@class='cy-right-modal cy-right-modal__show']//button[contains(text(),'Save')]").click()
        sleep(2)
        fprint(self, "Verifying if the domain is added successfully")
        waitfor(self, 5, By.XPATH, "//div[@name='id']")
        domaintext = str(self.driver.find_element_by_xpath("//div[@name='id']").get_attribute("innerHTML"))
        if domaintext.__contains__(self.cip_domain):
            fprint(self, "[Passed] Domain is added successfully")
        else:
            fprint(self, "[Failed] to add domain")
            self.fail("[Failed] to add domain")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        # waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']") # UI Changed
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'Select All')]")
        fprint(self, "[Passed] Clicked on Save Button")
        sleep(2)
        cip_left_menu(self, "Publish")
        sleep(1)
        cip_select_collection(self, self.stix_collection)  # Select Collection which was created earlier
        sleep(5)
        fprint(self, "Clicking on Publish Button")
        self.driver.find_element_by_xpath("//button[contains(text(),'Publish')]").click()
        verify_success(self, "Package published successfully")
        process_console_logs(self)

    def test_02_check_navigation_intel_package_leftmenu_items(self):
        fprint(self, "TC_ID: 53 - Check navigation and items in intel package")
        nav_menu_main(self, "Create Intel Package")
        fprint(self, "Clicking on Add New button")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add New')]/span").click()
        sleep(1)  # Static wait is important here.
        waitfor(self, 2, By.XPATH, "//li[text()='Detailed Submission']")
        fprint(self, "[Passed] Found Detailed Submission in drop down menu, Clicking on it")
        self.driver.find_element_by_xpath("//li[text()='Detailed Submission']").click()
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Title*']")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys("IP_1" + uniquestr)
        sleep(1)
        cip_left_menu(self, 'STIX Components')
        waitfor(self, 5, By.XPATH, "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Attack Pattern')]")
        fprint(self, "[Passed] Attack Pattern is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Campaign')]")
        fprint(self, "[Passed] Campaign is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Course of action')]")
        fprint(self, "[Passed] Course of action is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Grouping')]")
        fprint(self, "[Passed] Grouping is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Identity')]")
        fprint(self, "[Passed] Identity is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Indicator')]")
        fprint(self, "[Passed] Indicator is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Infrastructure')]")
        fprint(self, "[Passed] Infrastructure is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Intrusion Set')]")
        fprint(self, "[Passed] Intrusion Set is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Location')]")
        fprint(self, "[Passed] Location is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Malware')]")
        fprint(self, "[Passed] Malware is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Malware Analysis')]")
        fprint(self, "[Passed] Malware Analysis is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Note')]")
        fprint(self, "[Passed] Note is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Observed Data')]")
        fprint(self, "[Passed] Observed Data is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Opinion')]")
        fprint(self, "[Passed] Opinion is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Report')]")
        fprint(self, "[Passed] Report is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Threat Actor')]")
        fprint(self, "[Passed] Threat Actor is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Tool')]")
        fprint(self, "[Passed] Tool is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Vulnerability')]")
        fprint(self, "[Passed] Vulnerability is visible]")
        cip_left_menu(self, 'Relations')
        fprint(self, "[Passed] Expand Relations to verify items]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Relationship')]")
        fprint(self, "[Passed] Relationship is visible]")
        waitfor(self, 2, By.XPATH,
                "//div[@class='create-intel-packages__form-step-bar']//span[contains(text(),'Sighting')]")
        fprint(self, "[Passed] Sighting is visible]")

    def test_03_discard_draft(self):
        fprint(self, "TC_ID: 54 - Check if Discard Drafts removes the Intel Package")
        nav_menu_main(self, "Create Intel Package")
        fprint(self, "Clicking on Add New button")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add New')]/span").click()
        sleep(1)  # Static wait is important here.
        waitfor(self, 2, By.XPATH, "//li[text()='Detailed Submission']")
        fprint(self, "[Passed] Found Detailed Submission in drop down menu, Clicking on it")
        self.driver.find_element_by_xpath("//li[text()='Detailed Submission']").click()
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Title*']")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys("IP_1" + uniquestr)
        sleep(1)
        fprint(self, "Clicking on Indicator checkbox to add into the process")
        self.driver.find_element_by_xpath(
            "//div[@class ='cy-page__body w-100']//span[contains(text(), 'Indicator')]").click()
        fprint(self, "[Passed] Clicked on Indicator, Waiting to appear in the step process")
        waitfor(self, 10, By.XPATH, "//div[@class='create-intel-packages__form-step-bar__step-tab-0']//span[contains(text(),'Indicator')]")
        fprint(self, "[Passed] Indicator appeared in the step process, Clicking on back button")
        self.driver.find_element_by_xpath("//i[@class='cyicon-chevron-left']").click()
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Create Intel Package')]")
        fprint(self, "[Passed] Reached at the main Create Intel Package")
        self.driver.find_element_by_xpath("//input[@placeholder = 'Search or filter results']").send_keys("IP_1" + uniquestr)
        self.driver.find_element_by_xpath("//i[@data-testid='filter-search-icon']").click()
        click_on_actions_item(self, "IP_1" + uniquestr, "Discard")
        waitfor(self, 3, By.XPATH, "//button[text()='Proceed']")
        fprint(self, "[Passed] Proceed button appeared successfully, Clicking on it.")
        self.driver.find_element_by_xpath("//button[text()='Proceed']").click()
        fprint(self, "Proceed button is clicked")
        verify_success(self, 'Draft Intel Package discarded successfully')


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
