from lib.ui.nav_app import *
from lib.common_functions import *
from selenium.webdriver.common.by import By


def allowed_indi_search(self, value):
    """
        Function to search for an entry in Allowed Indicators
    """
    _ele = self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']")
    _ele.click()
    clear_field(_ele)
    _ele.send_keys(value)
    self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
    if waitfor(self, 5, By.XPATH, f"//span[@data-testid='value' and contains(text(),'{value}')]"):
        fprint(self, f"Element {value} found in allowed indicators")