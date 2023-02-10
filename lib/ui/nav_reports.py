from lib.common_functions import *
from selenium.webdriver.common.by import *
from selenium import *

"""
This is support library for Reports
"""
from lib.ui.nav_app import *

def reports_left_menu(self, itemname):
    """
    Click on left menu items in Reports
    """
    self.driver.find_element_by_xpath("//span[contains(text(),'"+itemname+"')]").click()
    fprint(self, "[Passed], Clicked on Left Menu item: " + itemname)



