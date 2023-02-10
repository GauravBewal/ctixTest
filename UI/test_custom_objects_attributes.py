import unittest
from lib.ui.nav_app import *
from lib.ui.nav_tableview import click_on_actions_item


class CustomObjects(unittest.TestCase):

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

    kill_name = "test-kill"
    phase_name = "test-phase"

    def Click_Custom_Object(self):
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        self.driver.find_element_by_xpath("//div[normalize-space()='Custom Object']").click()
        fprint(self, "[Passed]-Clicked on the custom objects")
        waitfor(self, 10, By.XPATH, "//button[contains(text(),'Custom Object')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Custom Object')]").click()
        fprint(self, "[Passed]-clicked on the button to add custom objects")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Add')]")

    def Add_Custom_kill_Chain(self, name, phase):
        """
        case to add elements in the custom kill chain module
        """
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the integration management on custom object entities")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom Entities Management')]")
        fprint(self, "[Passed]-Page loaded successfully")
        self.driver.find_element_by_xpath("//div[contains(text(),'Custom Kill Chain')]").click()
        fprint(self, "[Passed]-clicked on the custom kill chain")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Custom Kill Chain')]")
        fprint(self, "[Passed]-custom kill chain loaded successfully")
        self.driver.find_element_by_xpath("//button[contains(text(),'Custom Kill Chain')]").click()
        fprint(self, "[Passed]-clicked on the add button")
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'Custom Kill Chain')])[2]")
        fprint(self, "[Passed]-Added button loaded successfully")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Kill Chain Name *']").send_keys(name)
        fprint(self, "[Passed]-Added the name of the kill chain")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Kill Chain Phase 1 *']").send_keys(
            phase)
        fprint(self, "[Passed]- Entered the name for the phase in the kill chain module")


    def test_01_Verify_Page_load(self):
        fprint(self, "TC_ID: 1561 Verify that the custom Attributes page load successfully")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")

    def test_02_Verify_Add_Custom_Attribute_Boolean(self):
        fprint(self, "TC_ID: 1562 Verify that we are able to add custom attribute of boolean type")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Custom Attribute')]").click()
        fprint(self, "[Passed]-Clicked on the add custom Attributes Button")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Custom Attribute')]/ancestor::span")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys("sm_02")
        fprint(self, "[Passed]-Added the Name of the Custom Attribute")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder,'Description')]").send_keys("Testing_Boolean")
        fprint(self, "[Passed]- Entered The description of the Custom Attribute")
        self.driver.find_element_by_xpath("//div[@name='header']").click()
        fprint(self, "[Passed]-Clicked on the Field")
        self.driver.find_element_by_xpath("//div[contains(text(),'Input (Boolean)')]").click()
        fprint(self, "[Passed]-Selected the field type-(Boolean)")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        verify_success(self, "Custom Attribute created successfully")
        fprint(self, "[Passed]-Custom Attribute of Boolean type created Successfully")

    def test_03_Verify_Add_Custom_Attribute_Integer(self):
        fprint(self, "TC_ID: 1563 Verify that we are able to add custom attribute of Integer type")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Custom Attribute')]").click()
        fprint(self, "[Passed]-Clicked on the add custom Attributes Button")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Custom Attribute')]/ancestor::span")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys("sm_03")
        fprint(self, "[Passed]-Added the Name of the Custom Attribute")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder,'Description')]").send_keys("Testing_Integer")
        fprint(self, "[Passed]- Entered The description of the Custom Attribute")
        self.driver.find_element_by_xpath("//div[@name='header']").click()
        fprint(self, "[Passed]-Clicked on the Field")
        self.driver.find_element_by_xpath("//div[contains(text(),'Input (Integer)')]").click()
        fprint(self, "[Passed]-Selected the field type-(Integer)")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        verify_success(self, "Custom Attribute created successfully")
        fprint(self, "[Passed]-Custom Attributes of Boolean type created Successfully")

    def test_04_Verify_Add_Custom_Attribute_String(self):
        fprint(self, "TC_ID: 1564 Verify that we are able to add custom attribute of String type")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Custom Attribute')]").click()
        fprint(self, "[Passed]-Clicked on the add custom Attributes Button")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Custom Attribute')]/ancestor::span")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys("sm_04")
        fprint(self, "[Passed]-Added the Name of the Custom Attribute")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder,'Description')]").send_keys("Testing_String")
        fprint(self, "[Passed]- Entered The description of the Custom Attribute")
        self.driver.find_element_by_xpath("//div[@name='header']").click()
        fprint(self, "[Passed]-Clicked on the Field")
        self.driver.find_element_by_xpath("//div[contains(text(),'Input (String)')]").click()
        fprint(self, "[Passed]-Selected the field type-(string)")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        verify_success(self, "Custom Attribute created successfully")
        fprint(self, "[Passed]-Custom Attributes of Boolean type created Successfully")

    def test_05_Verify_Add_Custom_Attribute_Single_Select(self):
        fprint(self, "TC_ID: 1565 Verify that we are able to add custom attribute of Single Select type")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Custom Attribute')]").click()
        fprint(self, "[Passed]-Clicked on the add custom Attributes Button")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Custom Attribute')]/ancestor::span")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys("sm_05")
        fprint(self, "[Passed]-Added the Name of the Custom Attribute")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder,'Description')]").send_keys(
            "Testing_Single_Select")
        fprint(self, "[Passed]- Entered The description of the Custom Attribute")
        self.driver.find_element_by_xpath("//div[@name='header']").click()
        fprint(self, "[Passed]-Clicked on the Field")
        self.driver.find_element_by_xpath("//div[contains(text(),'Single Select')]").click()
        fprint(self, "[Passed]-Selected the field type-(single select )")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Value 1']").send_keys("Val_1")
        fprint(self, "[Passed]-Entered the value of Value1")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Value 2']").send_keys("Val_2")
        fprint(self, "[Passed]-Entered the value of Value2")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        verify_success(self, "Custom Attribute created successfully")
        fprint(self, "[Passed]-Custom Attributes of Boolean type created Successfully")

    def test_06_Verify_Add_Custom_Attribute_Date(self):
        fprint(self, "TC_ID: 1566 Verify that we are able to add custom attribute of Date type")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Custom Attribute')]").click()
        fprint(self, "[Passed]-Clicked on the add custom Attributes Button")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Custom Attribute')]/ancestor::span")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys("sm_06")
        fprint(self, "[Passed]-Added the Name of the Custom Attribute")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder,'Description')]").send_keys("Testing_Date")
        fprint(self, "[Passed]- Entered The description of the Custom Attribute")
        self.driver.find_element_by_xpath("//div[@name='header']").click()
        fprint(self, "[Passed]-Clicked on the Field")
        self.driver.find_element_by_xpath("//div[contains(text(),'Date')]").click()
        fprint(self, "[Passed]-Selected the field type-(Date)")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        verify_success(self, "Custom Attribute created successfully")
        fprint(self, "[Passed]-Custom Attributes of Boolean type created Successfully")

    def test_07_Verify_Add_Custom_Attribute_JSON(self):
        fprint(self, "TC_ID: 1567 Verify that we are able to add custom attribute of JSON type")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Custom Attribute')]").click()
        fprint(self, "[Passed]-Clicked on the add custom Attributes Button")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Custom Attribute')]/ancestor::span")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys("sm_07")
        fprint(self, "[Passed]-Added the Name of the Custom Attribute")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder,'Description')]").send_keys("Testing_JSON")
        fprint(self, "[Passed]- Entered The description of the Custom Attribute")
        self.driver.find_element_by_xpath("//div[@name='header']").click()
        fprint(self, "[Passed]-Clicked on the Field")
        self.driver.find_element_by_xpath("//div[contains(text(),'JSON')]").click()
        fprint(self, "[Passed]-Selected the field type-(JSON)")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        verify_success(self, "Custom Attribute created successfully")
        fprint(self, "[Passed]-Custom Attributes of Boolean type created Successfully")

    def test_08_Verify_Same_Name_Cannot_Be_Added(self):
        fprint(self, "TC_ID: 1568 Verify we are not able to add the same name")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Custom Attribute')]").click()
        fprint(self, "[Passed]-Clicked on the add custom Attributes Button")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Custom Attribute')]/ancestor::span")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys("sm_07")
        fprint(self, "[Passed]-Added the Name of the Custom Attribute")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder,'Description')]").send_keys("Testing_JSON")
        fprint(self, "[Passed]- Entered The description of the Custom Attribute")
        self.driver.find_element_by_xpath("//div[@name='header']").click()
        fprint(self, "[Passed]-Clicked on the Field")
        self.driver.find_element_by_xpath("//div[contains(text(),'JSON')]").click()
        fprint(self, "[Passed]-Selected the field type-(JSON)")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        verify_success(self, "Value provided for the field already exists")
        fprint(self, "[Passed]-Same Name Cannot Be added")

    def test_09_Verify_Name_Is_Mandatory_field(self):
        fprint(self, "TC_ID: 1569 To verify that name is the mandatory field")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Custom Attribute')]").click()
        fprint(self, "[Passed]-Clicked on the add custom Attributes Button")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Custom Attribute')]/ancestor::span")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder,'Description')]").send_keys("Testing_JSON")
        fprint(self, "[Passed]- Entered The description of the Custom Attribute")
        self.driver.find_element_by_xpath("//div[@name='header']").click()
        fprint(self, "[Passed]-Clicked on the Field")
        self.driver.find_element_by_xpath("//div[contains(text(),'JSON')]").click()
        fprint(self, "[Passed]-Selected the field type-(JSON)")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        waitfor(self, 10, By.XPATH, "//div[normalize-space()='Name is required']")
        fprint(self, "[Passed]-Custom attribute cannot be added without adding the name")

    def test_10_Verify_Field_Is_Mandatory_Field(self):
        fprint(self, "TC_ID: 15610 to verify that field is the mandatory field")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Custom Attribute')]").click()
        fprint(self, "[Passed]-Clicked on the add custom Attributes Button")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Custom Attribute')]/ancestor::span")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys("sm_07")
        fprint(self, "[Passed]-Added the Name of the Custom Attribute")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder,'Description')]").send_keys("Testing_JSON")
        fprint(self, "[Passed]- Entered The description of the Custom Attribute")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        waitfor(self, 10, By.XPATH, "//div[normalize-space()='Field Type is required']")
        fprint(self, "[Passed]-verified that field is a mandatory field.")

    def test_11_Verify_Boolean_Custom_Attribute_Is_Present(self):
        fprint(self, "TC_ID:15611 To verify that the custom attribute is present")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        search(self, "sm_02")
        waitfor(self, 10, By.XPATH, "(//span[contains(@data-testid,'name')][normalize-space()='sm_02'])[2]")
        fprint(self, "[Passed]-Attribute is present in the list")

    def test_12_Verify_Custom_Object_can_Be_Added(self):
        fprint(self, "TC_ID: 15612 To verify that the custom object can be added successfully")
        self.Click_Custom_Object()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title *']").send_keys("first")
        fprint(self, "[Passed]-entered the title of the custom object")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description']").send_keys("thisisfirst")
        fprint(self, "[Passed]-entered the description")
        self.driver.find_element_by_xpath("//input[@name='search-input']").send_keys("sm_02")
        waitfor(self, 10, By.XPATH, "//div[@name='text']")
        self.driver.find_element_by_xpath("//div[@name='text']").click()
        self.driver.find_element_by_xpath("//input[@name='primary_attribute']").click()
        fprint(self, "[Passed]-clicked on the primary attribute")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        verify_success(self, "Custom Object created successfully")
        fprint(self, "[Passed]-custom object created successfully")

    def test_13_Verify_Same_Name_Cannot_Be_Added(self):
        fprint(self, "TC_ID: 15613 To verify that the custom object of the same name cannot be added")
        self.Click_Custom_Object()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title *']").send_keys("first")
        fprint(self, "[Passed]-entered the title of the custom object")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description']").send_keys("thisisfirst")
        fprint(self, "[Passed]-entered the description")
        self.driver.find_element_by_xpath("//input[@name='search-input']").send_keys("sm_02")
        waitfor(self, 10, By.XPATH, "//div[@name='text']")
        self.driver.find_element_by_xpath("//div[@name='text']").click()
        self.driver.find_element_by_xpath("//input[@name='primary_attribute']").click()
        fprint(self, "[Passed]-clicked on the primary attribute")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        verify_success(self, "Value provided for the field already exists")
        fprint(self, "[Passed]-custom object with same name cannot be created")

    def test_14_Verify_title_As_Mandatory(self):
        fprint(self, "TC_ID:15614 To verify that the custom object of the same name cannot be added")
        self.Click_Custom_Object()
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description']").send_keys("Title_is_mand")
        fprint(self, "[Passed]-entered the description")
        self.driver.find_element_by_xpath("//input[@name='search-input']").send_keys("sm_02")
        waitfor(self, 10, By.XPATH, "//div[@name='text']")
        self.driver.find_element_by_xpath("//div[@name='text']").click()
        self.driver.find_element_by_xpath("//input[@name='primary_attribute']").click()
        fprint(self, "[Passed]-clicked on the primary attribute")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        waitfor(self, 10, By.XPATH, "//div[normalize-space()='Title is required']")
        fprint(self, "[Passed]-Title is mandatory field")

    def test_15_Verify_Custom_As_Mandatory(self):
        fprint(self, "TC_ID: 15615 To verify that the custom object without custom attribute cannot be created")
        self.Click_Custom_Object()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title *']").send_keys("first")
        fprint(self, "[Passed]-entered the title of the custom object")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description']").send_keys("Title_is_mand")
        fprint(self, "[Passed]-entered the description")
        self.driver.find_element_by_xpath("//input[@name='search-input']").send_keys("sm_02")
        waitfor(self, 10, By.XPATH, "//div[@name='text']")
        self.driver.find_element_by_xpath("//div[@name='text']").click()
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        waitfor(self, 10, By.XPATH, "//div[normalize-space()='Mark one attribute as primary attribute']")
        fprint(self, "[Passed]-Custom attribute should be marked as primary attribute")

    def test_16_Verify_That_Attribute_Should_Marked_As_Primary(self):
        fprint(self, "TC_ID: 15616 To verify that the custom object cannot be created is the custom attribute is not marked as primary attribue")
        self.Click_Custom_Object()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title *']").send_keys("first")
        fprint(self, "[Passed]-entered the title of the custom object")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description']").send_keys("Title_is_mand")
        fprint(self, "[Passed]-entered the description")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        waitfor(self, 10, By.XPATH, "//div[normalize-space()='Custom Attribute(s) is required']")
        fprint(self, "[Passed]-Custom attribute is the mandatory field")

    def test_17_Custom_Object_Is_Present_In_Quick_Add(self):
        fprint(self, "TC_ID: 15617 - to verify that the custom object is present in the quick add")
        nav_menu_main(self, "Threat Data")
        fprint(self, "[Passed]-clicked on threat data in main menu")
        waitfor(self, 20, By.XPATH, "//button[text()=' New']")
        self.driver.find_element_by_xpath("//button[text()=' New']").click()
        fprint(self, "[Passed]-clicked on the new button")
        waitfor(self, 20, By.XPATH, "//li/*[contains(text(), 'Quick Add Intel')]")
        self.driver.find_element_by_xpath("//li/*[contains(text(), 'Quick Add Intel')]").click()
        fprint(self, "[Passed]- Clicked on the Quick add intel")
        waitfor(self, 10, By.XPATH, "(//div[contains(text(),'Quick Add Intel')])[1]")
        self.driver.find_element_by_xpath("//span[normalize-space()='Custom Objects']").click()
        fprint(self, "[Passed]-Clicked on the custom object")
        self.driver.find_element_by_xpath(
         "//div[contains(@data-testid,'quickadd-search')]//input[contains(@placeholder,'Search')]").send_keys("first")
        fprint(self, "[Passed]-entered the value for search")
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'first')]")
        fprint(self, "[Passed]-Custom object is present in the quick add ")

    def test_18_Verify_Clone_Working(self):
        fprint(self, "TC_ID: 15618 - To verify that the custom Attribute can be cloned")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        search(self, "sm_07")
        fprint(self, "[Passed]-searched for the attribute")
        click_on_actions_item(self, 'sm_07', 'Clone')
        fprint(self, "[Passed]-clicked on the clone")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Custom Attribute')]")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        fprint(self, "[Passed]-clicked on the save button")
        verify_success(self, "Custom Attribute created successfully")
        fprint(self, "[Passed]- Got the success alert for the clone")

    def test_19_Verify_Disable_Attribute(self):
        fprint(self, "TC_ID: 15619- To verify that the disable functionality is working fine")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        search(self, "sm_05")
        fprint(self, "[Passed]-searched for the attribute")
        click_on_actions_item(self, 'sm_05', 'Disable')
        fprint(self, "[Passed]-clicked on the disabled")
        verify_success(self, "Custom Attribute Status updated successfully")
        fprint(self, "[Passed]-Custom attribute can be disabled easily.")

    def test_20_Verify_Status_Inactive(self):
        fprint(self, "TC_ID: 15620- To verify that the filter verify status inactive is working fin")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        waitfor(self, 10, By.XPATH, "//span[normalize-space()='Status']")
        self.driver.find_element_by_xpath("//span[normalize-space()='Status']").click()
        fprint(self, "[Passed]-clicked on the status")
        waitfor(self, 10, By.XPATH, "//span[normalize-space()='Inactive']")
        self.driver.find_element_by_xpath("//span[normalize-space()='Inactive']").click()
        fprint(self, "[Passed]-clicked on Inactive")
        self.driver.find_element_by_xpath("//span[contains(text(),'Press enter or click to search')]").click()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'sm_05')]")
        fprint(self, "[Passed]-Status inactive filter is working fine")

    def test_21_Verify_Status_Active(self):
        fprint(self, "TC_ID: 15621- To verify that the filter staus active is working fine")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        waitfor(self, 10, By.XPATH, "//span[normalize-space()='Status']")
        self.driver.find_element_by_xpath("//span[normalize-space()='Status']").click()
        fprint(self, "[Passed]-clicked on the status")
        waitfor(self, 10, By.XPATH, "//span[normalize-space()='Active']")
        self.driver.find_element_by_xpath("//span[normalize-space()='Active']").click()
        fprint(self, "[Passed]-clicked on Active")
        sleep(3)
        self.driver.find_element_by_xpath("//div[@data-testid='filters']//div//div//div//input[@autocomplete='off']").send_keys("sm_02")
        fprint(self, "[Passed]-Send the name of the indicator")
        self.driver.find_element_by_xpath("//span[contains(text(),'Press enter or click to search')]").click()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'sm_02')]")
        fprint(self, "[Passed]-Status active filter is working fine")

    def test_22_Verify_Enable(self):
        fprint(self, "TC_ID: 15622- To verify that the enable functionality is working fine")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        search(self, "sm_05")
        fprint(self, "[Passed]-searched for the attribute")
        click_on_actions_item(self, 'sm_05', 'Enable')
        fprint(self, "[Passed]-clicked on the Enable")
        verify_success(self, "Custom Attribute Status updated successfully")
        fprint(self, "[Passed]-Custom attribute can be Enabled easily.")

    def test_23_Verify_Clone_created(self):
        """ Test case to verify that the clone is created successfully"""
        fprint(self, "TC_ID: 15623- Test case to verify that the clone is created successfully")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the main menu for custom Attributes")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom')]")
        fprint(self, "[Passed]-Page Successfully Loaded")
        search(self, "sm_07_cloned")
        fprint(self, "[Passed]-searched for the attribute")
        waitfor(self, 20, By.XPATH, "(//span[contains(text(),'sm_07_cloned')])[2]")
        fprint(self, "[Passed]-Custom object that is cloned is added successfully")

    def test_24_Verify_Custom_kill_Chain_created(self):
        """
        test case to create custom kill chain
        """
        fprint(self, "TC_ID: 15624- Test case to verify that the custom kill  chain can be created ")
        self.Add_Custom_kill_Chain(self.kill_name, self.phase_name)
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "[Passed]-clicked on the save button successfully")
        verify_success(self, "Custom Kill Chain created successfully")
        fprint(self, "[Passed]-clicked on the save button")

    def test_25_Verify_That_Same_Name_Cannot_Be_Created(self):
        """
        Test case to verify that the same name kill chain cannot be created
        """
        fprint(self, "TC_ID: 15625- Test case to verify that the same name cannot be added")
        self.Add_Custom_kill_Chain(self.kill_name, self.phase_name)
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "[Passed]-clicked on the save button successfully")
        verify_success(self, "Kill Chain Name already exists.")
        fprint(self, "[Passed]-clicked on the save button")

    def test_26_Verify_Kill_Name_is_required(self):
        """
        Test case to verify that the name is mandatory field
        """
        fprint(self, "TC_ID: 15626- Test case to verify that the name is mandatory field ")
        self.Add_Custom_kill_Chain("", self.phase_name)
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "[Passed]-clicked on the save button successfully")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Kill Chain Name is required')]")
        fprint(self, "[Passed]-clicked on the save button")

    def test_27_Verify_That_The_Phase_is_Required(self):
        """
        Test case to verify that the phase is mandatory field
        """
        fprint(self, "TC_ID: 15627- Test case to verify that the phase is mandatory field")
        self.Add_Custom_kill_Chain(self.kill_name, "")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "[Passed]-clicked on the save button successfully")
        waitfor(self, 10, By.XPATH, "//p[contains(text(),'Kill Chain Phase is Required')]")
        fprint(self, "[Passed]-Phase is the mandatory field")

    def test_28_Verify_That_Same_Phase_Cannot_Be_Added_In_Same_Phase(self):
        """
        test case to verify that the same phase cannot be added in a same kill chain
        """
        fprint(self, "TC_ID: 15628- Test case to verify that the same phase cannot be added in the kill chain")
        self.Add_Custom_kill_Chain(self.kill_name, self.phase_name)
        self.driver.find_element_by_xpath("//span[contains(text(),'Add Phases')]").click()
        fprint(self, "[Passed]-clicked on the add phases successfully")
        waitfor(self, 10, By.XPATH, "//input[@aria-placeholder='Kill Chain Phase 2 ']")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Kill Chain Phase 2 ']").send_keys(
            self.phase_name)
        fprint(self, "[Passed]- Entered the name for the phase in the kill chain module")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "[Passed]-clicked on the save button successfully")
        waitfor(self, 10, By.XPATH, "(//div[contains(text(),'A kill chain phase with the same name exists. Try again with a different name')])[1]")
        fprint(self, "[Passed]-Verified that the same phase connot be added in same kill chain")

    def test_29_Verify_Search_Working_Fine(self):
        """
        test case to verify that the search function is working fine
        """
        fprint(self, "TC_ID: 15629- Test case to verify that the search function is working fine")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the integration management on custom object entities")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom Entities Management')]")
        fprint(self, "[Passed]-Page loaded successfully")
        self.driver.find_element_by_xpath("//div[contains(text(),'Custom Kill Chain')]").click()
        fprint(self, "[Passed]-clicked on the custom kill chain")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Custom Kill Chain')]")
        fprint(self, "[Passed]-custom kill chain loaded successfully")
        search(self, self.kill_name)
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'test-kill')])[1]")
        fprint(self, "[Passed]-search functionality is working fine")

    def test_30_Verify_Edit_Functionality_Working_Fine(self):
        """
        test case to verify that the Edit functionality is working fine
        """
        fprint(self, "TC_ID: 15630- Test case to verify that edit functionality is working fine ")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the integration management on custom object entities")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom Entities Management')]")
        fprint(self, "[Passed]-Page loaded successfully")
        self.driver.find_element_by_xpath("//div[contains(text(),'Custom Kill Chain')]").click()
        fprint(self, "[Passed]-clicked on the custom kill chain")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Custom Kill Chain')]")
        fprint(self, "[Passed]-custom kill chain loaded successfully")
        search(self, self.kill_name)
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'test-kill')])[1]")
        fprint(self, "[Passed]-search functionality is working fine")
        click_on_actions_item(self, self.kill_name, "Edit")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Edit Custom Kill Chain')]")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Kill Chain Name *']").clear()
        fprint(self, "[Passed]-cleared the field")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Kill Chain Name *']").send_keys("kill-modified")
        fprint(self, "[Passed]-sent the modified value")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "[Passed]-clicked on the save button successfully")
        verify_success(self, "Custom Kill Chain updated successfully")

    def test_31_verify_edited_successfully(self):
        """
        test case to verify that the kill chain updated succesfully
        """
        fprint(self, "TC_ID: 15631- test case to verify that the kill chain updated successfully")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the integration management on custom object entities")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom Entities Management')]")
        fprint(self, "[Passed]-Page loaded successfully")
        self.driver.find_element_by_xpath("//div[contains(text(),'Custom Kill Chain')]").click()
        fprint(self, "[Passed]-clicked on the custom kill chain")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Custom Kill Chain')]")
        fprint(self, "[Passed]-custom kill chain loaded successfully")
        search(self, "kill-modified")
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'kill-modified')])[1]")
        fprint(self, "[Passed]-Verified that the kill chain updated successfully")

    def test_32_Verify_kill_Chain_Can_be_Deleted(self):
        """
        test case to verify that the kill chain can be deleted
        """
        fprint(self, "TC_ID: 15632- test case to verify that the kill chain can be deleted successfully")
        nav_menu_admin(self, "Custom")
        fprint(self, "[Passed]-Clicked in the integration management on custom object entities")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Custom Entities Management')]")
        fprint(self, "[Passed]-Page loaded successfully")
        self.driver.find_element_by_xpath("//div[contains(text(),'Custom Kill Chain')]").click()
        fprint(self, "[Passed]-clicked on the custom kill chain")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Custom Kill Chain')]")
        fprint(self, "[Passed]-custom kill chain loaded successfully")
        search(self, "kill-modified")
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'kill-modified')])[1]")
        fprint(self, "[Passed]-Verified that the kill chain updated successfully")
        click_on_actions_item(self, "test-killkill-modified", "Delete")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Are you sure you want to delete this Custom Kill Chain ?')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Delete')]").click()
        verify_success(self, "Custom Kill Chains deleted successfully")
        fprint(self, "[Passed]-Verified custom object deleted successfully")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())




