import unittest
from lib.ui.nav_app import *


class DomainFuzzer(unittest.TestCase):

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

    def test_01_DomainFuzzer_PageLoad(self):
        fprint(self, "TC_ID: 1 - DomainFuzzer" + uniquestr)
        nav_menu_main(self, "Domain Fuzzer")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(),'Domain Fuzzer')]")
        process_console_logs(self)
        fprint(self, "TC_ID: 1 - Domain Fuzzer - Domain Fuzzer Page Load is verified")

if __name__ == '__main__':
    unittest.main(testRunner=reporting())
