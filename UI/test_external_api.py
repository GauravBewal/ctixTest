import unittest
from lib.ui.external_api import *

MISP_URL = "https://misp-v3.stegnophora.in/"
MISP_USERNAME = "admin@admin.test"
MISP_PASSWORD = "h2CpdGi8_cVuRbhizk3D"


class ExternalAPI(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.driver = initialize_browser(self)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    @classmethod
    def setUp(self):
        clear_console_logs(self)

    def test_01_add_misp_event(self):
        """
            Testcase to add a new event in MISP
        """
        fprint(self, "TC_ID: 91801 - Testcase to add a new event in MISP")
        misp_stamp = uniquestr[-4:]
        set_value("misp_stamp", misp_stamp)
        login_misp(self)
        add_event(self, title="mtoc"+get_value("misp_stamp"))
        filename = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds", "misp_to_ctix.csv")
        with open(filename, 'r') as obj:
            row = csv.reader(obj)
            for data in row:
                add_attribute(self, data=data)
        fprint(self, "Clicking on Publish Event")
        waitfor(self, 20, By.XPATH, "//li[a[text()='Publish Event']]")
        self.driver.find_element_by_xpath("//li[a[text()='Publish Event']]").click()
        waitfor(self, 10, By.XPATH, "//legend[text()='Publish Event']")
        fprint(self, "Clicking on Submit")
        self.driver.find_element_by_xpath("//span[@id='PromptYesButton']").click()

    def test_02_add_ctix_server_on_misp(self):
        """
            Testcase to add ctix server into MISP portal
        """
        fprint(self, "TC_ID: 91802 - Testcase to add ctix server into MISP portal")
        login_misp(self)
        creds = get_value("misp_creds")
        add_ctix_server_in_misp(self, misp_auth=creds[5], misp_url=creds[6])

    def test_03_delete_ctix_server_on_misp(self):
        """
            Testcase to delete the created CTIX Server from MISP portal
        """
        fprint(self, "TC_ID: 91803 - Testcase to delete the created CTIX Server from MISP portal")
        login_misp(self)
        creds = get_value("misp_creds")
        delete_ctix_server_in_misp(self, misp_url=creds[6])

    def test_04_validate_manual_run_ctix_to_misp(self):
        """
            Testcase to validate if data sent from CTIX is being received on MISP
        """
        fprint(self, "TC_ID: 91804 - Testcase to validate if data sent from CTIX is being received on MISP")
        login_misp(self)
        creds = get_value("misp_creds")
        pull_data_from_ctix_server(self, misp_url=creds[6])
        open_event_in_misp(self, title=f"ctom_old_{get_value('ctom_stamp')}")
        search_attribute_in_misp_event(self, attribute="getmyjio.com")

    def test_05_validate_auto_run_ctix_to_misp(self):
        """
            Testcase to validate if data sent from CTIX is received in MISP
        """
        fprint(self, "TC_ID: 91805 - Testcase to validate if data sent from CTIX is received in MISP")
        login_misp(self)
        creds = get_value("misp_creds")
        pull_data_from_ctix_server(self, misp_url=creds[6])
        open_event_in_misp(self, title=f"ctom_new_{get_value('ctom_stamp')}")
        search_attribute_in_misp_event(self, attribute="getmyairtel.com")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
