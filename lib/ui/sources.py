import unittest
from lib.ui.nav_app import *



def create_creds(self,coll):
    """ declaring global variables so that it can be used in the next function """
    global username
    global password
    global url_2dot1
    nav_menu_admin(self, "Integration Management")
    waitfor(self, 10, By.XPATH, "//span[contains(text(),'Subscribers ')]")
    self.driver.find_element_by_xpath("//span[contains(text(),'Subscribers ')]").click()
    waitfor(self, 10, By.XPATH, "//button[contains(text(),'Add Subscriber')]")
    self.driver.find_element_by_xpath("//button[contains(text(),'Add Subscriber')]").click()
    waitfor(self, 10, By.XPATH, "//input[@aria-placeholder='Subscriber Name *']")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Subscriber Name *']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Subscriber Name *']").send_keys("Test_Inbox")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Name*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Name*']").send_keys("Aut_name_test")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Email *']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Email *']").send_keys("Test@cyware.com")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Confidence *']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Confidence *']").send_keys("90")
    self.driver.find_element_by_xpath("(//div[@name='collections'])[1]").click()
    waitfor(self, 10, By.XPATH, "//div[contains(text(),'"+coll+"')]")
    self.driver.find_element_by_xpath("//div[contains(text(),'"+coll+"')]").click()
    self.driver.find_element_by_xpath("//button[@data-testid='save-subscribers']").click()
    verify_success(self, "Subscriber created successfully")
    waitfor(self, 10, By.XPATH, "//p[contains(text(),'Username')]/parent::div/div/p")
    username = self.driver.find_element_by_xpath("//p[contains(text(),'Username')]/parent::div/div/p").text
    password = self.driver.find_element_by_xpath("//p[contains(text(),'Password')]/parent::div/div/p").text
    url_1dotx = self.driver.find_element_by_xpath("//p[contains(text(),'TAXII-1 URL')]/parent::div/div/p").text
    url_2dot0 = self.driver.find_element_by_xpath("//p[contains(text(),'TAXII-2 URL')]/parent::div/div/p").text
    url_2dot1 = self.driver.find_element_by_xpath("//p[contains(text(),'TAXII-2.1 URL')]/parent::div/div/p").text
    fprint(self, "username - " + username + " password - " + password)
    fprint(self, "url_2dot1 - " + url_2dot1)
    fprint(self, "url_2dot0 - " + url_2dot0)
    fprint(self, "url_1dotx - " + url_1dotx)
    waitfor(self, 10, By.XPATH, "//span[@data-testaction='slider-close']")
    self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
    sleep(3)  # mandatory


def create_source(self, sourcename, col):
    """ utility function to create source"""
    create_creds(self, col)
    # nav_menu_admin(self, "Integration Management")
    waitfor(self, 10, By.XPATH, "//span[contains(text(),'STIX')]")
    self.driver.find_element_by_xpath("//span[contains(text(),'STIX')]").click()
    waitfor(self, 2, By.XPATH, "(//button[contains(text(),'STIX Source')])[1]")
    fprint(self, "Button found, now clicking on it")
    self.driver.find_element_by_xpath("(//button[contains(text(),'STIX Source')])[1]").click()
    waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Source Name *']")
    fprint(self, "Adding Configuration Details : ")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Source Name *']").send_keys(sourcename)
    fprint(self, "Source Name - " + sourcename)
    self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description *']").send_keys(
        "test_STIX_Description")
    fprint(self, "Source Description - test_STIX_Description")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Discovery Service URL *']").send_keys(url_2dot1)
    fprint(self, "Discovery Service URL - " + url_2dot1)
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Confidence *']").send_keys("70")
    fprint(self, "Confidence Score - 70")
    self.driver.find_element_by_xpath("(//div[@name='taxii_option'])[1]").click()
    waitfor(self, 5, By.XPATH, "//div[text()='STIX 2.1']")
    self.driver.find_element_by_xpath("//div[text()='STIX 2.1']").click()
    fprint(self, "STIX version - STIX 2.1")
    self.driver.find_element_by_xpath("(//div[@name='category'])[1]").click()
    waitfor(self, 20, By.XPATH, "//div[text()='Community Feeds']")
    sleep(2)
    self.driver.find_element_by_xpath("//div[text()='Community Feeds']").click()
    fprint(self, "Category - Community Feeds")
    self.driver.find_element_by_xpath("(//div[@name='authentication_type'])[1]").click()
    waitfor(self, 5, By.XPATH, "//div[text()='Basic']")
    self.driver.find_element_by_xpath("//div[text()='Basic']").click()
    fprint(self, "Authentication Tyoe - Basic")
    waitfor(self, 5, By.XPATH, "//input[@name='username']")
    self.driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
    fprint(self, "Entered Username")
    self.driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
    self.driver.find_element_by_xpath("//button[@data-testid='save-custom-sources']").click()
    fprint(self, "Clicked on the Save Source Button")
    verify_success(self, "Source created successfully")