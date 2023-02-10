import unittest
from lib.ui.nav_app import *


class CreateThreatBulletin(unittest.TestCase):

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

    def test_01_CreateThreatBulletin_DefaultPageLoad(self):
        fprint(self, "TC_ID: 1 - CreateThreatBulletin - Default PageLoad" + uniquestr)
        nav_menu_main(self, "Create Threat Bulletin")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(),'Create Threat Bulletin')]")
        fprint(self, "TC_ID: 1 - CreateThreatBulletin - Default Page Load is verified")

    def test_02_CreateThreatBulletin_Export(self):
        fprint(self, "TC_ID: 2 - CreateThreatBulletin - Export ThreatSpec" + uniquestr)
        nav_menu_main(self, "Create Threat Bulletin")
        waitfor(self, 5, By.XPATH, "//button[@data-testaction='open-export']")
        self.driver.find_element_by_xpath("//button[@data-testaction='open-export']").click()
        fprint(self, "TC_ID: 2 - CreateThreatBulletin - clicked on export button successfully")
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'THREAT SPEC')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'THREAT SPEC')]").click()
        fprint(self, "TC_ID: 2 - CreateThreatBulletin - clicked on 'THREAT SPEC' option successfully")
        verify_success(self, "Your file will be downloaded in a moment")
        process_console_logs(self)
        fprint(self, "TC_ID: 2 - CreateThreatBulletin - Export ThreatSpec is verified")

if __name__ == '__main__':
    unittest.main(testRunner=reporting())
