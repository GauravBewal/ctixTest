import unittest
from lib.ui.nav_app import *
from lib.ui.smtp import *

edit_button = "//h4[contains(text(),'Configure Email Server')]/ancestor::div[2]//button[contains(text(),'Edit')]"
host_server_id = "//span[contains(text(),'Host Server ID')]/ancestor::span[2]//input[@placeholder='Enter Value']"
server_port = "//span[contains(text(),'Server Port')]/ancestor::span[2]//input[@placeholder='Enter Value']"
host_user = "//span[contains(text(),'Host User')]/ancestor::span[2]//input[@placeholder='Enter Value']"
host_user_password = "//span[contains(text(),'Host User Password')]/ancestor::span[2]//input[@placeholder='Enter Value']"
ctix_communication_mail = "//span[contains(text(),'CTIX Communication Mail')]/ancestor::span[2]//input[@placeholder='Enter Value']"
sender_name = "//span[contains(text(),'Sender Name')]/ancestor::span[2]//input[@placeholder='Enter Value']"


class SMTP(unittest.TestCase):
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

    def enable_smtp(self):
        if waitfor(self, 1, By.XPATH, "//span[contains(text(),'SMTP Over TLS')]/ancestor::div[1]//input[@value='true']", False):
            fprint(self, "Found SMTP Over TLS checkbox already enabled")
        else:
            fprint(self, "Enabling SMTP Over TLS checkbox")
            self.driver.find_element_by_xpath("//span[contains(text(),'SMTP Over TLS')]").click()
        fprint(self, "Putting values into the fields")
        clear_field(self.driver.find_element_by_xpath(host_server_id))
        self.driver.find_element_by_xpath(host_server_id).send_keys("email-smtp.us-east-1.amazonaws.com")
        clear_field(self.driver.find_element_by_xpath(server_port))
        self.driver.find_element_by_xpath(server_port).send_keys("587")
        clear_field(self.driver.find_element_by_xpath(host_user))
        self.driver.find_element_by_xpath(host_user).send_keys("AKIAUH7P5UIABF5K4ZOJ")
        clear_field(self.driver.find_element_by_xpath(host_user_password))
        self.driver.find_element_by_xpath(host_user_password).send_keys("BLj3524L7DMgYEp/s/BioaT8hSY9vpeBiD1QowSExMOF")
        clear_field(self.driver.find_element_by_xpath(ctix_communication_mail))
        self.driver.find_element_by_xpath(ctix_communication_mail).send_keys("noreply@cyware.com")
        clear_field(self.driver.find_element_by_xpath(sender_name))
        self.driver.find_element_by_xpath(sender_name).send_keys("CTIX")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "Clicked on the Save button")
        waitfor(self, 10, By.XPATH, "//input[@placeholder='Enter Email address']")
        self.driver.find_element_by_xpath("//input[@placeholder='Enter Email address']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Enter Email address']").send_keys("system.default@cyware.com")
        self.driver.find_element_by_xpath("//button[contains(text(),'Send Test Mail')]").click()
        verify_success(self, "General settings saved successfully")

    # def test_01_smtp_configuration(self):
    #     fprint(self, "TC_ID: 1 - SMTP Configuration" + uniquestr)
    #     nav_menu_admin(self, "Configuration")
    #     waitfor(self, 5, By.XPATH, "//span[contains(text(),'SMTP')]")
    #     fprint(self, "SMTP - SMTP Tab is visible")
    #     self.driver.find_element_by_xpath("//span[contains(text(),'SMTP')]").click()
    #     fprint(self, "SMTP - SMTP Tab is clicked")
    #     process_console_logs(self)
    #     if waitfor(self, 5, By.XPATH, "//input[@name='email_host']", False):
    #         fprint(self, "SMTP basic settings is visible, Putting values into the fields")
    #         enable_smtp(self)
    #     else:
    #         fprint(self, "SMTP found Disabled")
    #         waitfor(self, 5, By.XPATH, "(//span[contains(@class,'cy-switch-btn__icon pl-0 pr-2 cyicon-cross-lg')])[1]")
    #         self.driver.find_element_by_xpath("(//span[contains(@class,'cy-switch-btn__icon pl-0 pr-2 cyicon-cross-lg')])[1]").click()
    #         fprint(self, "SMTP is Enabled now")
    #         waitfor(self, 5, By.XPATH, "//input[@name='email_host']")
    #         fprint(self, "SMTP basic settings is visible now")
    #         enable_smtp(self)

    def test_01_enable_smtp(self):
        fprint(self, "TC_ID: 223301 - SMTP Configuration")
        nav_menu_admin(self, "Configuration")
        fprint(self, "Going down on - Configure Email Server")
        self.driver.find_element_by_xpath("//h4[contains(text(),'Configure Email Server')]").click()
        fprint(self, "Reached to Configure Email Server")
        waitfor(self, 10, By.XPATH, edit_button)
        self.driver.find_element_by_xpath(edit_button).click()
        self.enable_smtp()

    def test_02_disable_smtp(self):
        fprint(self, "TC_ID: 223302 - SMTP Configuration")
        nav_menu_admin(self, "Configuration")
        fprint(self, "Going down on - Configure Email Server")
        self.driver.find_element_by_xpath("//h4[contains(text(),'Configure Email Server')]").click()
        fprint(self, "Reached to Configure Email Server")
        waitfor(self, 10, By.XPATH, edit_button)
        self.driver.find_element_by_xpath(edit_button).click()
        if waitfor(self, 5, By.XPATH, "//div[@name='is_active' and contains(@class,'enabled')]", False):
            self.driver.find_element_by_xpath("//div[@name='is_active' and contains(@class,'enabled')]").click()
        else:
            self.driver.find_element_by_xpath("//span[@name='is_active' and contains(@class,'active')]").click()
        fprint(self, "SMTP Disabled")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "Clicked on the Save button")
        verify_success(self, "General settings saved successfully")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
