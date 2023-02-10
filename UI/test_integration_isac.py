import unittest
from lib.ui.nav_app import *

isac_list_v3 = ["EASE", "FS-ISAC", "LS-ISAO"]
isac_list_v2 = ["EASE", "FS-ISAC", "LS-ISAO", "H-ISAC", "DNG-ISAC", "MTS ISAC", "A-ISAC"]


class IntegrationISAC(unittest.TestCase):

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

    # Worked for both 3.0 and previous versions
    def test_01_verify_isac_feeds_list(self):
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to ISAC Feed Source")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'ISAC')]").click()
        fprint(self, "Verifying ISAC Feed sources - ")
        if Build_Version.__contains__("3."):
            for isac in isac_list_v3:
                waitfor(self, 5, By.XPATH, "//p[contains(text(),'"+isac+"')]")
                fprint(self, "Visible - "+isac)
        else:
            for isac in isac_list_v2:
                waitfor(self, 5, By.XPATH, "//p[contains(text(),'"+isac+"')]")
                fprint(self, "Visible - "+isac)
        process_console_logs(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
