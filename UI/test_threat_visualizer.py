import unittest
from lib.ui.nav_app import *


class ThreatVisualizer(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.driver = initialize_browser(self)
        login(self, Admin_Email, Admin_Password)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    @classmethod
    def setUp(self):
        process_console_logs(self)

    def test_threat_visualizer_loading(self):
        fprint(self, "TC_ID: 1 - Page load")
        nav_menu_main(self, "Threat Visualizer")
        waitfor(self, 2, By.XPATH, "//h1[contains(text(),'Threat Visualizer')]/ancestor::div[@class='d-flex align-items-center cy-page__header']")
        fprint(self, "Page loaded successfully !")
        process_console_logs(self)


if __name__ == '__main__':
    unittest.main()
