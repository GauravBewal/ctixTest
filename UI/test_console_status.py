import unittest
from lib.ui.nav_app import *
from lib.common_functions import *


class ConsoleStatus(unittest.TestCase):

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

    def test_01_Navigate_Console_Status(self):
        """
        This test case checks if all the services are working fine or not.
        """
        fprint(self, "TC_ID: 60 - Check Console status page errors")
        nav_menu_admin(self, "Console Status")

    def test_02_Elastic_Search_status(self):
        fprint(self, "TC_ID: 61 - Check if Elastic Search is Active")
        waitfor(self, 2, By.XPATH, "//div[p[contains(text(),'Elasticsearch')]]//p[contains(text(),'Active')]")
        fprint(self, "[Passed] Elastic Search found Active")

    def test_03_MySQL_status(self):
        fprint(self, "TC_ID: 62 - Check if My SQL is Active")
        waitfor(self, 2, By.XPATH, "//div[p[contains(text(),'My SQL')]]//p[contains(text(),'Active')]")
        fprint(self, "[Passed] My SQL found Active")

    def test_04_Redis_status(self):
        fprint(self, "TC_ID: 63 - Check if Redis is Active")
        waitfor(self, 2, By.XPATH, "//div[p[contains(text(),'Redis')]]//p[contains(text(),'Active')]")
        fprint(self, "[Passed] Redis found Active")

    def test_05_Celery_status(self):
        fprint(self, "TC_ID: 64 - Check if Celery is Active")
        waitfor(self, 2, By.XPATH, "//div[p[contains(text(),'Celery')]]//p[contains(text(),'Active')]")
        fprint(self, "[Passed] Celery found Active")

    def test_06_Gunicorn_status(self):
        fprint(self, "TC_ID: 65 - Check if Gunicorn is Active")
        waitfor(self, 2, By.XPATH, "//div[p[contains(text(),'Gunicorn')]]//p[contains(text(),'Active')]")
        fprint(self, "[Passed] Gunicorn found Active")

    def test_07_Nginx_status(self):
        fprint(self, "TC_ID: 66 - Check if Nginx is Active")
        waitfor(self, 2, By.XPATH, "//div[p[contains(text(),'Nginx')]]//p[contains(text(),'Active')]")
        fprint(self, "[Passed] Nginx found Active")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
