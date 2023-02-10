from lib.ui.nav_app import *


def create_subs(self, name, desc):
    nav_menu_admin(self, "STIX Collections")
    waitfor(self, 10, By.XPATH, "//button[contains(text(),'STIX Collection')]")
    self.driver.find_element_by_xpath("//button[contains(text(),'STIX Collection')]").click()
    waitfor(self, 10, By.XPATH, "//div[contains(text(),'New STIX Collection')]")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Collection Name *']").send_keys(name)
    self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description *']").send_keys(desc)
    self.driver.find_element_by_xpath("//input[@name='inbox']/ancestor::span[@class='cy-checkbox cy-flex']").click()
    self.driver.find_element_by_xpath("//button[contains(text(),' Save Collection')]").click()
    verify_success(self, "STIX Collection created successfully")


def create_subscriber(self, name, collections, confidence="90"):
    nav_menu_admin(self, "Integration Management")
    waitfor(self, 10, By.XPATH, "//span[contains(text(),'Subscribers ')]/parent::a")
    self.driver.find_element_by_xpath("//span[contains(text(),'Subscribers ')]/parent::a").click()
    waitfor(self, 2, By.XPATH, "//button[contains(text(),'Add Subscriber')]")
    self.driver.find_element_by_xpath("//button[contains(text(),'Add Subscriber')]").click()
    waitfor(self, 10, By.XPATH, "//input[@aria-placeholder='Subscriber Name *']")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Subscriber Name *']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Subscriber Name *']").send_keys(name)
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Name*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Name*']").send_keys("automation_name")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Email *']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Email *']").send_keys("automation@cyware.com")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Confidence *']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Confidence *']").send_keys(confidence)
    self.driver.find_element_by_xpath("(//div[@name='collections'])[1]").click()
    for collection in collections:
        clear_field(self.driver.find_element_by_xpath("//div[@name='collections']//input[@placeholder='Search']"))
        self.driver.find_element_by_xpath("//div[@name='collections']//input[@placeholder='Search']").send_keys(collection)
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'" + collection + "')]/parent::div")
        sleep(1)    # required
        self.driver.find_element_by_xpath("//div[contains(text(),'" + collection + "')]/parent::div").click()
    self.driver.find_element_by_xpath("//button[@data-testid='save-subscribers']").click()
    verify_success(self, "Subscriber created successfully")
    waitfor(self, 10, By.XPATH, "//p[contains(text(),'Username')]/parent::div/div/p")
    username = self.driver.find_element_by_xpath("//p[contains(text(),'Username')]/parent::div/div/p").text
    password = self.driver.find_element_by_xpath("//p[contains(text(),'Password')]/parent::div/div/p").text
    url_1dotx = self.driver.find_element_by_xpath("//p[contains(text(),'TAXII-1 URL')]/parent::div/div/p").text
    url_2dot0 = self.driver.find_element_by_xpath("//p[contains(text(),'TAXII-2 URL')]/parent::div/div/p").text
    url_2dot1 = self.driver.find_element_by_xpath("//p[contains(text(),'TAXII-2.1 URL')]/parent::div/div/p").text
    self.driver.find_element_by_xpath("//div[span[normalize-space(text())='MISP']]").click()
    misp_auth = self.driver.find_element_by_xpath("//p[contains(text(),'MISP Auth Key')]/parent::div/div/p").text
    misp_url = self.driver.find_element_by_xpath("//p[contains(text(),'MISP URL')]/parent::div/div/p").text
    fprint(self, "username - " + username + " password - " + password)
    fprint(self, "url_2dot1 - " + url_2dot1)
    fprint(self, "url_2dot0 - " + url_2dot0)
    fprint(self, "url_1dotx - " + url_1dotx)
    set_value("username", username)
    set_value("password", password)
    set_value("url_1dotx", url_1dotx)
    set_value("url_2dot0", url_2dot0)
    set_value("url_2dot1", url_2dot1)
    self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
    fprint(self, "Credentials Slider close")
    self.driver.find_element_by_xpath("(//a[@href='/ctix/sources/custom'])[2]")
    return [username, password, url_1dotx, url_2dot0, url_2dot1, misp_auth, misp_url]
