import unittest
from lib.ui.nav_app import *
from lib.ui.nav_tableview import click_on_actions_item
from lib.ui.nav_threat_data import verify_data_in_threatdata
from lib.ui.quick_add import quick_create_ip, quick_add_intel_with_ioc_sdo
from test_stix_subscribers import ioc_value

ipv4 = "44.55.22.11"
title = "deleteAtomic"
malware = "CVE-12345"
published_domain = ioc_value


class AtomicDelete(unittest.TestCase):

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

    def test_01_deleting_object_with_no_relation(self):
        fprint(self, "TC_ID : 2022421 - test_01_deleting_object_with_no_relation")
        quick_create_ip(self, ip=ipv4, title=title)
        verify_data_in_threatdata(self, value=ipv4, source="Import")
        click_on_actions_item(self, rowtitle=ipv4, item="Delete", feature="threatdata")
        waitfor(self, 5, By.XPATH, "//button[@data-testalert='confirm-delete']")
        self.driver.find_element_by_xpath("//button[@data-testalert='confirm-delete']").click()
        verify_success(self, "Object deletion is in progress. Objects that are either published or have a relation with other objects are not deleted. Check your email for details.")
        try:
            verify_data_in_threatdata(self, value=ipv4, source="Import")
            fprint(self, "[Failed] - Object is not Deleted Successfully")
            self.fail("[Failed] - Object is not Deleted Successfully")
        except:
            fprint(self, "[Passed] - Object Deleted Successfully")

    def test_02_deleting_object_with_yes_relation(self):
        fprint(self, "TC_ID : 2022422 - test_02_deleting_object_with_yes_relation")
        quick_add_intel_with_ioc_sdo(self, ioc_type="IPv4", title=title, ioc_value=ipv4, sdo_type="Malware", sdo_value=malware)
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, value=ipv4, source="Import")
        click_on_actions_item(self, rowtitle=ipv4, item="Delete", feature="threatdata")
        waitfor(self, 5, By.XPATH, "//button[@data-testalert='confirm-delete']")
        self.driver.find_element_by_xpath("//button[@data-testalert='confirm-delete']").click()
        verify_success(self, "Cannot delete a threat data object that is either published or has a relation defined with another object")
        try:
            verify_data_in_threatdata(self, value=ipv4, source="Import")
            fprint(self, "[Passed] - Object does not get deleted")
        except:
            fprint(self, "[Failed] - Object get deleted")
            self.fail("[Failed] - Object get deleted")

    def test_03_deleting_object_with_yes_published(self):
        fprint(self, "TC_ID : 2022423 - verify test_03_deleting_object_with_yes_published")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, value=ioc_value, source="Import")
        click_on_actions_item(self, rowtitle=ioc_value, item="Delete", feature="threatdata")
        waitfor(self, 5, By.XPATH, "//button[@data-testalert='confirm-delete']")
        self.driver.find_element_by_xpath("//button[@data-testalert='confirm-delete']").click()
        verify_success(self, "Cannot delete a threat data object that is either published or has a relation defined with another object")
        fprint(self, "[Passed] - Getting an error alert while deleting the object")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())



