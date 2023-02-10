from selenium.webdriver.common.by import By
from lib.common_functions import waitfor, fprint


def click_on_saved_search_link(self):
    self.driver.find_element_by_xpath("//span[contains(text(),'Switch To')]").click()
    waitfor(self, 5, By.XPATH, "//span[contains(text(),'Saved Search')]")
    fprint(self, "Clicked on the Saved Search and its screen is visible now")


def save_search(self, title):
    self.driver.find_element_by_xpath("//span[contains(text(),' Save Search ')]/parent::button").click()
    waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Title *']")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Title *']").send_keys(title)
    fprint(self, "Given title is - " + title)
    self.driver.find_element_by_xpath("//span[contains(text(),'Share it globally')]").click()
    fprint(self, "Clicked on the 'Share it globally' checkbox")
    self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
    fprint(self, "Clicked on the Save Button")
    waitfor(self, 5, By.XPATH, "//span[contains(text(),'" + title + "')]")
    fprint(self, "Under the newly added saved search filter")
    waitfor(self, 5, By.XPATH, "(//span[contains(text(),'" + title + "')])[2]")
    fprint(self, "Added Saved search filter is visible in the left panel")


def click_and_choose_from_dropdown_option(self, title, option):
    self.driver.find_element_by_xpath("//span[contains(text(),'" + title + "')]/ancestor::div[contains(@class,'cy-flex-between-center')]//div[@data-testaction='dropdown-link']").click()
    fprint(self, "Clicked on the Action menu")
    waitfor(self, 5, By.XPATH, "//li[contains(text(),'" + option + "')]")
    elements = self.driver.find_elements(By.XPATH, "//li[contains(text(),'" + option + "')]")
    for element in elements:
        if element.is_displayed():
            element.click()
    fprint(self, "Clicked on the Option - " + option)
