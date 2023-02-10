from lib.ui.nav_app import *
from lib.common_functions import *


host_server ='email-smtp.us-east-1.amazonaws.com'
port = '587'
user = 'AKIAUH7P5UIABF5K4ZOJ'
password = 'BLj3524L7DMgYEp/s/BioaT8hSY9vpeBiD1QowSExMOF'
email = 'noreply@cyware.com'
name = 'Automation'
send = 'saubhagya.marwaha@cyware.com'

def enable_smtp(self):
    fprint(self, "Putting values into the fields")
    if Build_Version.__contains__("2."):
        clear_field(self.driver.find_element_by_xpath("//input[@name='email_host']"))
        self.driver.find_element_by_xpath("//input[@name='email_host']").send_keys("email-smtp.us-east-1.amazonaws.com")
        clear_field(self.driver.find_element_by_xpath("//input[@name='email_port']"))
        self.driver.find_element_by_xpath("//input[@name='email_port']").send_keys("587")
        clear_field(self.driver.find_element_by_xpath("//input[@name='email_host_user']"))
        self.driver.find_element_by_xpath("//input[@name='email_host_user']").send_keys("AKIAY7O2AD4GME5NLWUN")
        clear_field(self.driver.find_element_by_xpath("//input[@name='email_host_password']"))
        self.driver.find_element_by_xpath("//input[@name='email_host_password']").send_keys(
        "BGSYpU4PjqStpCXPOl3uNQvN/U/fAKyowuLWwPaKWgkm")
        clear_field(self.driver.find_element_by_xpath("//input[@name='from_email']"))
        self.driver.find_element_by_xpath("//input[@name='from_email']").send_keys("noreply@cyware.com")
        clear_field(self.driver.find_element_by_xpath("//input[@name='from_email_name']"))
        self.driver.find_element_by_xpath("//input[@name='from_email_name']").send_keys("CTIX")
        self.driver.find_element_by_xpath("//button[contains(text(),'Update Configuration')]").click()
        fprint(self, "SMTP - Clicked on the Update Configuration button")
        verify_success(self, "SMTP settings updated successfully")
    elif Build_Version.__contains__("3."):
        self.driver.find_element_by_xpath("(//input[@name='host'])[1]").send_keys(host_server)
        fprint(self, "[Passed]-entered the value of host successfully")
        self.driver.find_element_by_xpath("(//input[@name='port'])[1]").send_keys(port)
        fprint(self, "[Passed]-Entered the value of port successfully")
        self.driver.find_element_by_xpath("(//input[@name='username'])[1]").send_keys(user)
        fprint(self, "[Passed]-entered the value of username successfully")
        self.driver.find_element_by_xpath("(//input[@name='password'])[1]").send_keys(password)
        fprint(self, "[Passed]-entered the value of password successfully")
        self.driver.find_element_by_xpath("(//input[@name='from_email'])[1]").send_keys(email)
        fprint(self, "[Passed]-Entered the value of email successfully")
        self.driver.find_element_by_xpath("(//input[@name='sender'])[1]").send_keys(name)
        fprint(self, "[Passed]_entered the value of name successfully")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        fprint(self, "[Passed]-clicked on the save button successfully")
        waitfor(self, 10, By.XPATH, "(//div[@class='cy-color-base-font cy-text-f14'])[1]")
        self.driver.find_element_by_xpath("(//input[@placeholder='Enter Email address'])[1]").send_keys(send)
        fprint(self, "[Passed]-entered the value of email address successfully")
        self.driver.find_element_by_xpath("//button[normalize-space()='Send Test Mail']").click()
        verify_success(self, "General settings saved successfully")


