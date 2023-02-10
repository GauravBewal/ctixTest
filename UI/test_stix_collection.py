import unittest
from lib.ui.nav_app import *


class StixCollections(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.driver = initialize_browser(self)
        login(self, Admin_Email, Admin_Password)
        # Unique Test Data - This will be used in create intel package script
        set_value("stix_collection", "am_coll"+uniquestr)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    @classmethod
    def setUp(self):
        clear_console_logs(self)

    def test_01_create_stix_collection(self):
        fprint(self, "TC_ID: 51 - Create Stix Collection: " + get_value("stix_collection"))
        nav_menu_admin(self, "STIX Collection")
        self.driver.find_element_by_xpath("//button[text()='Add STIX Collection']").click()
        waitfor(self, 3, By.XPATH, "//div[text()='New STIX Collection']")
        fprint(self, "[Passed] - Clicked on Add Stix Collection")
        sleep(1)  # Let the slide open animation complete
        self.driver.find_element_by_name("collection_name").send_keys("am_coll"+uniquestr)
        self.driver.find_element_by_name("description").send_keys("This is create via automation test suite")
        # Checkbox takes the span which is sibling to the input
        self.driver.find_element_by_xpath("//input[@name='polling']/following-sibling::span").click()
        self.driver.find_element_by_xpath("//button[contains(text(),'Save Collection')]").click()
        fprint(self, "[Passed] - Clicked on Save Collection")
        verify_success(self, "STIX Collection created successfully")
        process_console_logs(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
