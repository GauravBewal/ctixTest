import unittest
from lib.ui.nav_app import *

name = "integratorName"
description = "integratorDescription"
doc_url = "https://ctixapiv3.cyware.com/"


class CTIXIntegrator(unittest.TestCase):

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

    def test_01_verify_addNew_ctix_integrator(self):
        fprint(self, "TC_ID: 122331 - test_01_verify_addNew_ctix_integrator")
        nav_menu_admin(self, "Integration Management")
        waitfor(self, 20, By.XPATH, "//span[text()='CTIX Integrators ']/parent::a")
        self.driver.find_element_by_xpath("//span[text()='CTIX Integrators ']/parent::a").click()
        fprint(self, "Clicked on the CTIX Integrator tab")
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'Add New')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add New')]").click()
        fprint(self, "Clicked on the Add New Button")
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Name *']")
        fprint(self, "Entering credentials now")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys(name)
        waitfor(self, 5, By.XPATH, "//textarea[@aria-placeholder='Description *']")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description *']").send_keys(description)
        waitfor(self, 5, By.XPATH, "//input[@name='expiry_date']")
        self.driver.find_element_by_xpath("//input[@name='expiry_date']").click()
        try:
            waitfor(self, 5, By.XPATH, "//td[@class='available today']/following-sibling::td")
            self.driver.find_element_by_xpath("//td[@class='available today']/following-sibling::td").click()
        except:
            waitfor(self, 5, By.XPATH, "(//td[@class='next-month'])[1]")
            self.driver.find_element_by_xpath("(//td[@class='next-month'])[1]").click()
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Generate')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Generate')]").click()
        fprint(self, "Clicked on the Generate button")
        verify_success(self, "CTIX Integrator created successfully")
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Open API Credentials')]")
        fprint(self, "Credentials slider is visible, Storing credentials now")
        waitfor(self, 20, By.XPATH, "//p[contains(text(),'Access ID')]")
        waitfor(self, 20, By.XPATH, "//p[contains(text(),'Secret Key')]")
        waitfor(self, 20, By.XPATH, "//p[contains(text(),'Endpoint URL')]")
        access_id = self.driver.find_element_by_xpath("//p[contains(text(),'Access ID')]/parent::div/div/p").text
        secret_key = self.driver.find_element_by_xpath("//p[contains(text(),'Secret Key')]/parent::div/div/p").text
        endpoint = self.driver.find_element_by_xpath("//p[contains(text(),'Endpoint URL')]/parent::div/div/p").text
        set_credentials("ctix", "base_url",  endpoint)
        set_credentials("ctix", "access_id", access_id)
        set_credentials("ctix", "secret_key", secret_key)
        fprint(self, "access ID - "+access_id)
        fprint(self, "secret key - "+secret_key)
        fprint(self, "endpoint - "+endpoint)
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        fprint(self, "Verifying added Integrator is visible in the Listing or not")
        search(self, name)
        waitfor(self, 20, By.XPATH, "//span[@data-testid='name' and contains(text(),'"+name+"')]")
        fprint(self, "Added CTIX Integrator is visible")

    def test_02_verify_enable_disable_ctix_integrator(self):
        fprint(self, "TC_ID: 122332 - test_02_verify_enable_disable_ctix_integrator")
        nav_menu_admin(self, "Integration Management")
        waitfor(self, 20, By.XPATH, "//span[text()='CTIX Integrators ']/parent::a")
        self.driver.find_element_by_xpath("//span[text()='CTIX Integrators ']/parent::a").click()
        fprint(self, "Clicked on the CTIX Integrator tab, searching Integrator - "+name)
        search(self, name)
        waitfor(self, 20, By.XPATH, "//span[@data-testid='name' and contains(text(),'" + name + "')]")
        fprint(self, "CTIX Integrator is visible - "+name)
        self.driver.find_element_by_xpath("//div[contains(@class,'cyicon-add-active')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Last Accessed Date')]/i")
        self.driver.find_element_by_xpath("//span[contains(text(),'Last Accessed Date')]/i").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Created by')]/i").click()
        try:
            self.driver.find_element_by_xpath("//span[contains(text(),'Created on')]/i").click()
        except:
            self.driver.find_element_by_xpath("//span[contains(text(),'Created Date')]/i").click()
        self.driver.find_element_by_xpath("//div[contains(@class,'cyicon-add-active')]").click()
        waitfor(self, 20, By.XPATH, "//div[@data-testid='is_active']")
        self.driver.find_element_by_xpath("//div[@data-testid='is_active']").click()
        # verify_success(self, "")
        fprint(self, "Integrator Disabled - "+name)
        self.driver.find_element_by_xpath("//div[@data-testid='is_active']").click()
        # verify_success(self, "")
        fprint(self, "Integrator Enabled - "+description)

    def test_03_verify_API_Doc_button_redirection(self):
        fprint(self, "TC_ID: 122333 - test_03_verify_API_Doc_button_redirection")
        nav_menu_admin(self, "Integration Management")
        waitfor(self, 20, By.XPATH, "//span[text()='CTIX Integrators ']/parent::a")
        self.driver.find_element_by_xpath("//span[text()='CTIX Integrators ']/parent::a").click()
        fprint(self, "Navigated to the CTIX Integrator page")
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'CTIX REST API Doc')]")
        fprint(self, "CTIX REST API Doc button is visible clicking on it")
        self.driver.find_element_by_xpath("//button[contains(text(),'CTIX REST API Doc')]").click()
        fprint(self, "Button clicked")
        sleep(10)   # Required
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        fprint(self, "Navigated to the second tab")
        waitfor(self, 60, By.XPATH, "//span[@data-testid=“aether-text”]")
        fprint(self, "CTIX API Reference doc is visible")
        url = self.driver.current_url
        if url == doc_url:
            fprint(self, "[Passed] Expected API Doc URL is found - "+url)
        else:
            fprint(self, "[Failed] Expected API Doc URL is not found")
            self.fail("Expected API Doc URL is not found")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
