from lib.common_functions import *
from selenium.webdriver.common.by import By
from config.process_config import *


def sign_out(self):
    fprint(self, "Sign out from the profile")
    waitfor(self, 5, By.XPATH, "//a[@href='/ctix/profile']")
    ele = self.driver.find_element_by_xpath("//a[@href='/ctix/profile']")
    self.driver.execute_script("arguments[0].click();", ele)
    sleep(5)
    waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Sign Out')]")
    self.driver.find_element_by_xpath("//button[contains(text(), 'Sign Out')]").click()
    fprint(self, "clicked on sign out")
    waitfor(self, 5, By.XPATH, "//div[contains(text(), 'Are you sure you want to sign out?')]")
    self.driver.find_element_by_xpath("//button[@name = 'Yes']").click()
    fprint(self, "clicked on yes for sign out")
    fprint(self, "user signed out successfully")
    waitfor(self, 10, By.XPATH, "//a[@href = '/ctix/user/login']")
    self.driver.find_element_by_xpath("//a[@href = '/ctix/user/login']").click()
    fprint(self, "clicked on login link")
    process_console_logs(self)

