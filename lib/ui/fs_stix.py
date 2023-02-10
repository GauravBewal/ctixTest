from lib.ui.nav_app import *
from lib.common_functions import *
from selenium.webdriver.common.by import By


def remove_stix_source(self, sourcename):
    fprint(self, "Clicking on the Action menu")
    self.driver.find_element_by_xpath("//p[contains(text(),'" + sourcename + "')]/ancestor::div[1]/div[2]").click()
    fprint(self, "Action menu clicked, Waiting for the Delete Button")
    waitfor(self, 5, By.XPATH, "//li[contains(text(),'Delete')]")
    self.driver.find_element_by_xpath("//li[contains(text(),'Delete')]").click()
    fprint(self, "Clicked on the Delete button")
    waitfor(self, 5, By.XPATH, "//button[@name='Delete']")
    fprint(self, "Confirming Delete")
    self.driver.find_element_by_xpath("//button[@name='Delete']").click()
    verify_success(self, "Selected Source deleted successfully")
    waitfor(self, 5, By.XPATH, "//h1[contains(text(),'No Sources found!')]")
    fprint(self, "Now source is not visible - "+sourcename)
