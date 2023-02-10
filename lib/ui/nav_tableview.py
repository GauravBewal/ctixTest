from lib.common_functions import *
from selenium.webdriver.common.by import By


def click_on_actions_item(self, rowtitle, item, feature="stix"):
    sleep(1)
    waitfor(self, 20, By.XPATH, "//span[contains(text(), '" + rowtitle + "')]")
    ele = self.driver.find_element_by_xpath("//span[contains(text(), '" + rowtitle + "')]")
    ActionChains(self.driver).move_by_offset(1,1).perform()
    sleep(1)
    if feature == "apifeeds":
        self.driver.execute_script("arguments[0].scrollIntoView();", ele)
        sleep(1)
    ActionChains(self.driver).move_to_element(ele).perform()
    sleep(2)
    fprint(self, "Waiting for the channel - "+rowtitle)
    waitfor(self, 10, By.XPATH, "//span[contains(text(), '"+rowtitle+"')]/ancestor::tr//button[@data-testid='action']")
    self.driver.find_element_by_xpath("//span[contains(text(), '"+rowtitle+"')]/ancestor::tr//button[@data-testid='action']").click()
    fprint(self, "Clicked on the action menu of - "+rowtitle)
    fprint(self, "Waiting for the option - " + item)
    if feature == "apifeeds":
        waitfor(self, 5, By.XPATH, "//ul[@class='cy-dropdown-menu__layout']//li/span[contains(text(),'" + item + "')]")
        sleep(2)
        elms = self.driver.find_elements(By.XPATH, "//ul[@class='cy-dropdown-menu__layout']//li/span[contains(text(),'"+item+"')]")
    elif feature == "threatbulletin" or feature == "Watchlist":
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'"+item+"')]")
        sleep(2)
        elms = self.driver.find_elements(By.XPATH, "//div[contains(text(),'"+item+"')]")
    elif feature == "threatdata":
        waitfor(self, 5, By.XPATH, "//div[@data-cy-event='Delete']")
        sleep(2)
        elms = self.driver.find_elements(By.XPATH, "//div[@data-cy-event='Delete']")
    else:
        waitfor(self, 5, By.XPATH, "//ul[@class='cy-dropdown-menu__layout']//li[contains(text(),'"+item+"')]")
        sleep(2)
        elms = self.driver.find_elements(By.XPATH, "//ul[@class='cy-dropdown-menu__layout']//li[contains(text(),'"+item+"')]")
    for elm in elms:
        if elm.is_displayed():
            elm.click()
            fprint(self, "Clicked on the option - " + item)


def visible_column(self, column_name):
    data = []
    self.driver.find_element_by_xpath("//div[@data-testaction='dropdown-link']//div[contains(@class,'cyicon-add-active')]").click()
    waitfor(self, 10, By.XPATH, "//span[contains(text(),'Custom')]/parent::div//div[@class='section-columns']")
    cust_col = self.driver.find_element_by_xpath("//span[contains(text(),'Custom')]/parent::div//div[@class='section-columns']")
    col_names = cust_col.find_elements(By.TAG_NAME, "span")
    for col in col_names:
        print(col.text)
        if str(col.text) != column_name:
            data.append(col.text)
    fprint(self, "Disabling all Active columns")
    for col in data:
        if waitfor(self, 0, By.XPATH, "//span[contains(@class,'column-option__active') and contains(text(),'" + col + "')]", False):
            element = self.driver.find_element_by_xpath("//span[contains(text(),'"+col+"')]/i[contains(@class,'cyicon-check-circle-outline')]")
            self.driver.execute_script("arguments[0].scrollIntoView();", element)
            self.driver.find_element_by_xpath("//span[contains(text(),'"+col+"')]/i[contains(@class,'cyicon-check-circle-outline')]").click()
            fprint(self, "Column Disabled - "+col)
    self.driver.find_element_by_xpath("//div[@data-testaction='dropdown-link']//div[contains(@class,'cyicon-add-active')]").click()
