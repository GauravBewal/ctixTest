from lib.ui.nav_app import *
from lib.common_functions import *
from selenium.webdriver.common.by import By

from lib.ui.nav_tableview import click_on_actions_item


def create_source(self, name, url):
    waitfor(self, 2, By.XPATH, "//input[@placeholder='Search or filter results']")
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
    clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']"))
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(name)
    self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
    if waitfor(self, 2, By.XPATH, "//span[text()='" + name + "']", False):
        fprint(self, name + " source already exists")
        return None
    if not waitfor(self, 3, By.XPATH, "//button[contains(text(),'Add RSS Source')]", False):
        try:
            self.driver.find_element_by_xpath("//i[@class='cyicon-cross-o-active cy-filters__icon']").click()
        except:
            fprint(self, "Cross button not found")
    sleep(1)
    self.driver.find_element_by_xpath("//button[contains(text(),'Add RSS Source')]").click()
    fprint(self, "[Passed] clicked on Add RSS Source")
    waitfor(self, 2, By.XPATH, "//div[text()='New Source']")
    sleep(1)
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Source Name*']"). \
        send_keys(name)
    sleep(1)
    self.driver.find_element_by_xpath("//input[@aria-placeholder='URL*']").send_keys(url)
    fprint(self, "[Passed] filled up form details")
    if Build_Version.__contains__("3."):
        waitfor(self, 2, By.XPATH,
                "//span[contains(text(), 'Create intel automatically')]/preceding-sibling::span/input")
        _ele = self.driver.find_element_by_xpath \
            ("//span[contains(text(), 'Create intel automatically')]/preceding-sibling::span/input")
        if _ele.get_attribute("value") == "true":  # Uncheck auto intel creation if active
            self.driver.find_element_by_xpath \
                    (
                    "//span[contains(text(), 'Create intel automatically')]/preceding-sibling::span/input").click()
        sleep(1)
    else:
        waitfor(self, 2, By.XPATH,
                "//span[contains(text(), 'Automatically create Intel Packages')]/preceding-sibling::span/input")
        _ele = self.driver.find_element_by_xpath \
            ("//span[contains(text(), 'Automatically create Intel Packages')]/preceding-sibling::span/input")
        if _ele.get_attribute("value") == "true":  # Uncheck auto intel creation if active
            self.driver.find_element_by_xpath \
                    (
                    "//span[contains(text(), 'Automatically create Intel Packages')]/preceding-sibling::span/input").click()
        sleep(1)
    self.driver.find_element_by_xpath("//button[text()='Add']").click()
    fprint(self, "[Passed] Clicked on Add")
    # if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
    #     self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
    # else:
    verify_success(self, "RSS Feed Source added successfully")
    sleep(2)
    fprint(self, "[Passed] Obtained required Success Alert for " + name)
    sleep(1)
    fprint(self, "Searching for created RSS Source")
    waitfor(self, 2, By.XPATH, "//input[@placeholder='Search or filter results']")
    clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']"))
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(name)
    self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
    waitfor(self, 2, By.XPATH, "//p[contains(text(),'" + name + "')]")
    # self.driver.find_element_by_xpath("//p[contains(text(),'" + name + "')]").click()
    fprint(self, "Added " + name + " source successfully")


def perform_action(self, **kwargs):
    name = kwargs.get('name')
    action = kwargs.get('action')
    fprint(self, "Searching for the created source")
    self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']").click()
    clear_field(self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']"))
    sleep(1)
    self.driver.find_element_by_xpath("//div/input[@placeholder='Search or filter results']").send_keys(name)
    sleep(3)
    self.driver.find_element_by_xpath("//i[@data-testid='filter-search-icon']").click()
    if waitfor(self, 7, By.XPATH, "//div/p[contains(text(), '"+name+"')]"):
        sleep(1)
        if str(action) == "View Collections":
            if Build_Version.__contains__("3."):
                self.driver.find_element_by_xpath("//div[p[contains(text(), '" + name + "')]]").click()
            else:
                fprint(self, "Click on Action Button")
                self.driver.find_element_by_xpath("//button[@data-testid='action']").click()
                waitfor(self, 5, By.XPATH, "(//li[contains(text(), 'View Collections')])")
                sleep(2)
                fprint(self, "Clicked On View Collection")
                self.driver.find_element_by_xpath("(//li[contains(text(), 'View Collections')])").click()

        else:
            fprint(self, "Click on Options Menu")
            self.driver.find_element_by_xpath("//div[p[contains(text(), '"+name+"')]]//button[span]").click()
            waitfor(self, 2, By.XPATH, "//li[contains(text(), '" + action + "')]")
            sleep(2)
            fprint(self, "Click on Menu item: " + action)
            self.driver.find_element_by_xpath("//li[contains(text(), '" + action + "')]").click()
            fprint(self, "[Passed] Clicked on " + action+" for"+name)


def create_intel_from_feed(self):
    """
        Function to parse and create intel from first feed of RSS Source
    """
    self.driver.find_element_by_xpath("//button[text()=' Create Intel ']").click()
    if waitfor(self, 10, By.XPATH, "//div[@role='tablist']//span[i]", False):
        self.driver.find_element_by_xpath("//div[@role='tablist']//span[i]").click()
        waitfor(self, 5, By.XPATH, "//div[@role='tabpanel']//input[@type='checkbox']/parent::span[1]")
        self.driver.find_element_by_xpath("//div[@role='tabpanel']//input[@type='checkbox']/parent::span[1]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//button[text()='Create Intel']").click()
        verify_success(self, "You can view the created intel as a report object in the Threat Data module")
    else:
        fprint(self, "[Failed] No intel found for the selected source")
        return 0
    return 1
