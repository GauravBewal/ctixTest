from lib.ui.nav_app import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def tags_left_menu(self, itemname):
    """
    Click on left menu items in Tags
    """
    self.driver.find_element_by_xpath("//span[contains(text(),'"+itemname+"')]").click()
    fprint(self, "[Passed], Clicked on Left Menu item: " + itemname)


# def tags_add(self,itemname):
#     """
#     Verify if Navigation to Tag module
#     """
#     nav_menu_main(self, "Tags")
#     return tags_add()

def add_tag(self, tag_name):
    """
        Function to add new tag
    """
    nav_menu_main(self, "Tags")
    search(self, tag_name)
    if waitfor(self, 5, By.XPATH, "//span[contains(text(), '"+tag_name+"')]", False):
        return None
    try:
        wait = WebDriverWait(self.driver, 1)
        if wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Add')]"))):
            self.driver.find_element_by_xpath("//button[contains(text(),'Add')]").click()
            fprint(self, "[Passed]- Clicked on  Add Tag Button")
    except:
        fprint(self, "Add Button is not visible, maybe its a first tag")
    waitfor(self, 5, By.XPATH, "//input[contains(@aria-placeholder,'Tag Name*')]")
    fprint(self, "[Passed] -Adding the tag name")
    self.driver.find_element_by_xpath("//input[contains(@aria-placeholder,'Tag Name*')]").send_keys(tag_name)
    fprint(self, "[Passed] -Selecting the color for the tag")
    waitfor(self, 5, By.XPATH, "//p[contains(text(),'Pick a Color')]/parent::div/div/div[1]")
    self.driver.find_element_by_xpath("//p[contains(text(),'Pick a Color')]/parent::div/div/div[1]").click()
    self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
    fprint(self, "[Passed] - Clicked on Save")
    verify_success(self, "Tag created successfully")
    # action = ActionChains(self.driver)
    # nav_menu_main(self, "Tags")
    # waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
    # self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
    # sleep(1)
    # self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(tagname)
    # self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
    # if waitfor(self, 5, By.XPATH, "//span[contains(text(), '"+tagname+"')]", False):
    #     return None
    # else:
    #     self.driver.find_element_by_xpath("//button[@data-testid='new-tag']").click()
    #     waitfor(self, 20, By.XPATH, "//input[@name='name']")
    #     self.driver.find_element_by_xpath("//input[@name='name']").send_keys(tagname)
    #     sleep(2)
    #     if Build_Version.__contains__("3."):
    #         _ele = self.driver.find_element_by_xpath("//p/following-sibling::div/div/span")
    #         action.move_to_element(_ele).perform()
    #         action.click(_ele).perform()
    #         self.driver.find_element_by_xpath("//button[contains(text(), 'Save')]").click()
    #     else:
    #         _ele = self.driver.find_element_by_xpath("//div[@data-test-id='Tag this color']")
    #         action.move_to_element(_ele).perform()
    #         action.click(_ele).perform()
    #         self.driver.find_element_by_xpath("//button[@data-testid='save-tag']").click()
    #     verify_success(self, "Tag created successfully")
