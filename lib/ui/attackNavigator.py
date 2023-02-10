from selenium.webdriver.common.by import By
from lib.common_functions import *


def click_on_customBase_layer(self):
    waitfor(self, 2, By.XPATH, "//div[@id='tab-custom']")
    self.driver.find_element_by_xpath("//div[@id='tab-custom']").click()
    fprint(self, "Clicked on the Custom Base Layer")


def click_on_technique(self):
    waitfor(self, 2, By.XPATH, "(//table[@aria-describedby='custom-technique-matrix']/tr[1]/td)[1]")
    self.driver.find_element_by_xpath("(//table[@aria-describedby='custom-technique-matrix']/tr[1]/td)[1]").click()
    waitfor(self, 5, By.XPATH, "//span[@data-testaction='slider-close']")


def close_slider(self):
    self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
    sleep(1)  # Closing Slider
