import unittest
from lib.ui.nav_app import *
from lib.common_functions import *

cert_name = "cert_automation"
cert_file_name = "certificate.txt"
key_file_name = "privatekey.txt"


class Certificate(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.driver = initialize_browser(self)
        login(self, Admin_Email, Admin_Password)
        clear_console_logs(self)

    def tearDown(self):
        self.driver.quit()

    def test_01_add_certificate(self):
        fprint(self, "TC_ID: 84511 - test_01_add_certificate")
        nav_menu_admin(self, "Certificates")
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Add Certificate')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add Certificate')]").click()
        fprint(self, "Clicked on the Add Certificate")
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Name *']")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys(cert_name)
        fprint(self, "Entered Certificate name - "+cert_name)
        self.driver.find_element_by_xpath("//button[contains(text(),'Upload Certificate')]").click()
        file_path = os.path.join(os.environ["PYTHONPATH"], "testdata", "certificates/" + cert_file_name)
        fprint(self, "Uploading certificate file... - " + cert_file_name)
        self.driver.find_element_by_xpath("//button[contains(text(),'Upload Certificate')]/parent::div/input").send_keys(file_path)
        sleep(2)    # Required
        self.driver.find_element_by_xpath("//button[contains(text(),'Upload Private Key')]").click()
        file_path = os.path.join(os.environ["PYTHONPATH"], "testdata", "certificates/" + key_file_name)
        fprint(self, "Uploading key file... - " + key_file_name)
        self.driver.find_element_by_xpath("//button[contains(text(),'Upload Private Key')]/parent::div/input").send_keys(file_path)
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(),'Add  Certificate')]").click()
        fprint(self, "Clicked on the Add Certificate Button")
        verify_success(self, "Certificate created successfully")
        search(self, cert_name)
        waitfor(self, 5, By.XPATH, "//span[@data-testid='certificate_name' and contains(text(),'"+cert_name+"')]")
        fprint(self, "Added Certificate is visible - "+cert_name)
        fprint(self, "[Passed] - Certificate is added successfully")

    def test_02_verify_enable_disable_certificate(self):
        fprint(self, "TC_ID: 84512 - test_02_verify_enable_disable_certificate")
        nav_menu_admin(self, "Certificates")
        search(self, cert_name)
        waitfor(self, 5, By.XPATH, "//span[@data-testid='certificate_name' and contains(text(),'" + cert_name + "')]")
        fprint(self, "Certificate is visible - "+cert_name)
        self.driver.find_element_by_xpath("//input[@type='checkbox' and @value='true']/parent::span").click()
        verify_success(self, "updated successfully")
        fprint(self, "Disabled - " + cert_name)
        self.driver.find_element_by_xpath("//input[@type='checkbox' and @value='false']/parent::span").click()
        verify_success(self, "updated successfully")
        fprint(self, "Enabled - " + cert_name)
        fprint(self, "[Passed] - Enable/Disable functionality of toggle button is working fine.")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
