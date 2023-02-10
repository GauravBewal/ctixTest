from lib.ui.nav_app import *


def create_collection(self, title, polling=True, inbox=True):
    """
        Function to create a new STIX collection
    """
    nav_menu_admin(self, "STIX Collection")
    self.driver.find_element_by_xpath("//button[normalize-space(text())='Add STIX Collection']").click()
    waitfor(self, 3, By.XPATH, "//div[text()='New STIX Collection']")
    fprint(self, "[Passed] - Clicked on Add Stix Collection")
    sleep(1)  # Let the slide open animation complete
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Collection Name *']").send_keys(title)
    self.driver.find_element_by_name("description").send_keys("This is created via automation test suite")
    # Checkbox takes the span which is sibling to the input
    if polling and waitfor(self, 1, By.XPATH, "//input[@name='polling' and @value='false']", False):
        self.driver.find_element_by_xpath("//span[input[@name='polling']]/following-sibling::span").click()
    if inbox and waitfor(self, 1, By.XPATH, "//input[@name='inbox' and @value='false']", False):
        self.driver.find_element_by_xpath("//span[input[@name='inbox']]/following-sibling::span").click()
    self.driver.find_element_by_xpath("//button[contains(text(),'Save Collection')]").click()
    fprint(self, "[Passed] - Clicked on Save Collection")
    verify_success(self, "STIX Collection created successfully")
