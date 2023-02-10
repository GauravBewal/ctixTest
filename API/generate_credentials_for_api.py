import json
import unittest
from lib.ui.nav_app import *


class Configuration(unittest.TestCase):

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

    def test_01_generate_creds(self):
        creds = {
            'base_url': '',
            'access_id': '',
            'secret_key': ''}
        print("----- Test Case: test_01_generate_creds -----")
        waitfor(self, 5, By.XPATH, "//i[@class='cyicon-menu-admin']")
        self.driver.find_element_by_xpath("//i[@class='cyicon-menu-admin']").click()
        waitfor(self, 5, By.XPATH, "//a[contains(text(), 'Integration Management')]")
        self.driver.find_element_by_xpath("//a[contains(text(), 'Integration Management')]").click()

        waitfor(self, 5, By.XPATH, "//span[text()='CTIX Integrators ']")
        self.driver.find_element_by_xpath("//span[text()='CTIX Integrators ']").click()
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Add New')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add New')]").click()
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Name *']")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys("HSAutomate")
        waitfor(self, 5, By.XPATH, "(//div[@role='application']/div/div)[1]")
        self.driver.find_element_by_xpath("(//div[@role='application']/div/div)[1]").send_keys("HSAutomate")
        waitfor(self, 5, By.XPATH, "//input[@name='expiry_date']")
        self.driver.find_element_by_xpath("//input[@name='expiry_date']").click()
        try:
            waitfor(self, 5, By.XPATH, "(//td[@class='available'])[1]")
            self.driver.find_element_by_xpath("(//td[@class='available'])[1]").click()
        except :
            waitfor(self, 5, By.XPATH, "(//td[@class='next-month'])[1]")
            self.driver.find_element_by_xpath("(//td[@class='next-month'])[1]").click()
        waitfor(self, 5, By.XPATH, "//button[text()='Generate']")
        self.driver.find_element_by_xpath("//button[text()='Generate']").click()
        waitfor(self, 5, By.XPATH, "//p[text()='Access ID']/following-sibling::div/p")
        element = self.driver.find_element_by_xpath("//p[text()='Access ID']/following-sibling::div/p")
        creds['access_id'] = element.get_attribute('innerHTML').strip()
        waitfor(self, 5, By.XPATH, "//p[text()='Secret Key']/following-sibling::div/p")
        element1 = self.driver.find_element_by_xpath("//p[text()='Secret Key']/following-sibling::div/p")
        creds['secret_key'] = element1.get_attribute('innerHTML').strip()

        waitfor(self, 5, By.XPATH, "//p[text()='Endpoint URL']/following-sibling::div/p")
        element1 = self.driver.find_element_by_xpath("//p[text()='Endpoint URL']/following-sibling::div/p")
        creds['base_url'] = element1.get_attribute('innerHTML').strip()

        fprint(self, f"Acess ID {creds['access_id']} Secret Key {creds['secret_key']} base url {creds['base_url']}")
        json_object = json.dumps(creds, indent=4)

        with open("creds.py", "w") as outfile:
            outfile.write("credentials = "+json_object)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
