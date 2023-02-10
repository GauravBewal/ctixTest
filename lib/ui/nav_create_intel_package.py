from lib.common_functions import *
from selenium.webdriver.common.by import By
"""
This is support library for Creating Intel Package
"""


def cip_left_menu(self, itemname):
    """
    Click on left menu items in Create Intel Package eg:- STIX Components, Custom Objects, Relations, Publish
    """
    self.driver.find_element_by_xpath("//div[@class='create-intel-packages__form-step-bar']/descendant-or-self::div[contains(text(),'"+itemname+"')]").click()
    fprint(self, "[Passed], Clicked on Left Menu item: " + itemname)


def cip_left_submenu(self, itemname):
    waitfor(self, 5, By.XPATH,
            "//div[@class='create-intel-packages__form-step-bar']/descendant-or-self::span[contains(text(),'"+itemname+"')]")
    self.driver.find_element_by_xpath(
        "//div[@class='create-intel-packages__form-step-bar']/descendant-or-self::span[contains(text(),'"+itemname+"')]").click()
    fprint(self, "[Passed], Clicked on Left Sub Menu item: " + itemname)


def cip_select_collection(self, collection_name):
    waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
    sleep(1)
    # create-intel-packages__form-publish
    # Todo: Change this to proper locator , Click on Searchbox and search the text.

    self.driver.find_element_by_xpath("//div[@class='d-flex justify-content-between align-items-center mb-5 pr-5']//input[@id='main-input']").click()
    self.driver.find_element_by_xpath("//div[@class='d-flex justify-content-between align-items-center mb-5 pr-5']//input[@id='main-input']").send_keys(collection_name)
    # Search Filter icon
    self.driver.find_element_by_xpath("//div[@class='d-flex justify-content-between align-items-center mb-5 pr-5']//i[@data-testid='filter-search-icon']").click()
    sleep(1)
    # Todo: Need to contact developer for data-testid
    waitfor(self, 5, By.XPATH, "//span[contains(text(),'" + collection_name + "')]")
    self.driver.find_element_by_xpath(
        "//span[contains(text(),'"+collection_name+"')]/ancestor-or-self::div[@class='px-3 el-col el-col-20']/following-sibling::div/descendant-or-self::button").click()
    fprint(self, "[Passed], Selected the Collection to publish : " + collection_name)


def cip_navigate_tabs(self, tabname):
    """
    Tab names eg:- Basic details, Common fields, Custom Attributes, STIX
    """
    self.driver.find_element_by_xpath("//span[contains(text(),'"+tabname+"')]").click()
    fprint(self, "[Passed], Navigate to tab : " + tabname)
    a = "dfsf"
    a.__contains__("collapsed")