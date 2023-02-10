import os
from selenium.webdriver.common.by import By
from time import sleep
from lib.common_functions import waitfor, fprint, verify_success


def navigate_to_import_intel(self):
    waitfor(self, 5, By.XPATH, '//button[contains(text(), "New")]')
    fprint(self, 'Clicked on "+ New" button')
    self.driver.find_element_by_xpath('//button[contains(text(), "New")]').click()

    waitfor(self, 5, By.XPATH, '//li/div[contains(text(), "Import Intel")]')
    fprint(self, 'Clicked on Import Intel')
    self.driver.find_element_by_xpath('//li/div[contains(text(), "Import Intel")]').click()

    waitfor(self, 5, By.XPATH, '//div[contains(text(), "Intel History")]')
    fprint(self, "[Passed] Import Intel Page is loaded successfully")


def select_format(self, format_name):
    navigate_to_import_intel(self)
    waitfor(self, 5, By.XPATH, '(//div[@data-testaction="close"])[1]')
    fprint(self, "Clicking on file format dropdown")
    self.driver.find_element_by_xpath('(//div[@data-testaction="close"])[1]').click()

    waitfor(self, 5, By.XPATH, f'(//div[contains(text(), "{format_name}")])[1]')
    fprint(self, f"Clicked on {format_name} format")
    self.driver.find_element_by_xpath(f'(//div[contains(text(), "{format_name}")])[1]').click()


def select_collection(self, collection_name):
    waitfor(self, 5, By.XPATH, '(//div[@data-testaction="close"])[2]')
    fprint(self, "Clicking on file collection dropdown")
    self.driver.find_element_by_xpath('(//div[@data-testaction="close"])[2]').click()

    waitfor(self, 5, By.XPATH, '(//input[@name="search-input"])[2]')
    self.driver.find_element_by_xpath('(//input[@name="search-input"])[2]').send_keys(collection_name)

    waitfor(self, 5, By.XPATH, f'(//div[contains(text(), "{collection_name}")])[1]')
    fprint(self, f"Clicked on the collection {collection_name}")
    self.driver.find_element_by_xpath(f'(//div[contains(text(), "{collection_name}")])[1]').click()


def import_file(self, file_name):
    waitfor(self, 5, By.XPATH, "//input[@type = 'file']")
    upload = self.driver.find_element_by_xpath("//input[@type = 'file']")
    file_path = os.path.join(os.environ["PYTHONPATH"], "testdata", f"import_intel/{file_name}")
    fprint(self, f"Uploaded {file_name}")
    upload.send_keys(file_path)
    # Intentionally used sleep waiting for file to be completely uploaded
    sleep(10)

    waitfor(self, 5, By.XPATH, '//button[contains(text(), "Import")]')
    fprint(self, "Clicked on import button")
    self.driver.find_element_by_xpath('//button[contains(text(), "Import")]').click()
    verify_success(self, 'File imported successfully')
