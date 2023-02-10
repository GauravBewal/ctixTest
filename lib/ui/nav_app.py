from lib.common_functions import *
from selenium.webdriver.common.by import By
from config.process_config import *

if Build_Version.__contains__("3."):
    from lib.ui.locators_3x import *
else:
    from lib.ui.locators_2x import *


def login(self, username, password):
    """
    Login method is used to log into the ctix application. Any user can be used to log into the application.
    :param self: Self Instance
    :param username: Admin Email
    :param password: Admin Password
    """
    self.driver.get(APP_URL)
    if not waitfor(self, 10, By.NAME, "email", False):
        fprint(self, "Refreshing Page")
        self.driver.refresh()
    waitfor(self, 20, By.NAME, "email")
    fprint(self, "Filling in username and password")
    self.driver.find_element_by_name("email").send_keys(username)
    self.driver.find_element_by_name("password").send_keys(password)
    if waitfor(self, 2, By.XPATH, "//button[contains(text(),'Sign in')]", False):
        self.driver.find_element_by_xpath("//button[contains(text(),'Sign in')]").click()
    elif waitfor(self, 2, By.XPATH, "//button[contains(text(),'Continue')]", False):
        self.driver.find_element_by_xpath("//button[contains(text(),'Continue')]").click()
    elif waitfor(self, 1, By.XPATH, "//button[contains(text(),'Login')]"):
        self.driver.find_element_by_xpath("//button[contains(text(),'Login')]").click()
    if waitfor(self, 60, By.XPATH, "//i[@class='cyicon-menu']", False) or \
            waitfor(self, 5, By.XPATH, "//p[contains(text(),'Please set your password')]", False) or \
            waitfor(self, 5, By.XPATH, "//p[contains(text(),'Create Password')]", False):
        fprint(self, "[Passed] Logged in successfully")
    else:
        fprint(self, "[Failed] Log in failed")


def nav_menu_admin(self, itemname):
    """
    This method is used to navigate to any item in the admin menu. After navigating, it automatically checks if there is
    any popup with error or if there are any console errors.
    :param self: Self instance
    :param itemname: Any item from the admin menu, eg: 'User Management', 'Integration Management' etc
    """
    if Build_Version.__contains__("3."):
        waitfor(self, 15, By.XPATH, "//i[@class='cyicon-menu-admin']")
        self.driver.find_element_by_xpath("//i[@class='cyicon-menu-admin']").click()
    else:
        waitfor(self, 15, By.XPATH, "//i[@class='cyicon-admin-settings']")
        self.driver.find_element_by_xpath("//i[@class='cyicon-admin-settings']").click()
    sleep(1)
    fprint(self, "[Passed] Clicked Admin Menu")
    waitfor(self, 2, By.XPATH, "//a[contains(text(),'" + itemname + "')]")
    # sleep(1)
    # To avoid Focus on Hints when Admin button is clicked, we move the focus on top item.
    elm = self.driver.find_element_by_xpath("//a[contains(text(),'User Management')]")
    action = ActionChains(self.driver)
    action.move_to_element(elm).perform()
    sleep(2)
    # Conflicting between Configuration and On-boarding Configuration
    # Separating based on conditions
    if itemname == "Configuration":
        self.driver.find_element_by_xpath("//a[normalize-space(text())='Configuration']").click()
    else:
        self.driver.find_element_by_xpath("//a[contains(text(),'" + itemname + "')]").click()
    fprint(self, "[Passed] Clicked Admin Menu Item : " + itemname)
    if itemname == "Confidence Score":
        # Todo: for 2.8.1 the text is different, build version check required
        if waitfor(self, 5, By.XPATH, "//h1[contains(text(),'Choose a Confidence Score Setup')]", False) or waitfor(self, 5, By.XPATH, "//h1[contains(text(),'Confidence Score')]", False):
            fprint(self, "[Passed] Navigate to Confidence Score")
        else:
            fprint(self, "[Failed] The title is not expected.")
            self.fail("Failed to navigate Confidence Score")

    elif itemname == "Console Status":
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Console Status')]")
    elif itemname == "Configuration":
        waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'Configuration')]")
    else:
        waitfor(self, 5, By.XPATH, "//h1[contains(text(),'" + itemname + "')]")
    check_error_alert(self)
    process_console_logs(self)


def nav_menu_main(self, itemname):
    """
    This method is used to navigate to any item in the main menu. After navigating, it automatically checks if there is
    any popup with error or if there are any console errors.
    :param self: Self instance
    :param itemname: Any item from the main menu, eg: 'Threat Data', 'Reports', 'Twitter Feeds'
    """
    # Todo: The action cursor move to code is repeated, some single method should be implemented.
    waitfor(self, 15, By.XPATH, "//i[@class='cyicon-menu']")
    self.driver.find_element_by_xpath("//i[@class='cyicon-menu']").click()
    sleep(1)
    fprint(self, "[Passed] Clicked Main Menu")
    # Check if any item requires menu expansion before the item can be clicked
    self.driver.find_element_by_xpath("//div[@class='cy-sidebar__hidden__search-box']//input").send_keys(itemname)
    sleep(0.5)
    if itemname in ("Fang - Defang", "STIX conversion", "Encode - Decode: Base64", "CVSS Calculator", "Network Utilities"):
        waitfor(self, 2, By.XPATH, "//span[contains(text(),'Analyst Workbench')]")
        fprint(self, "Menu item is part of Analyst Workbench")
        if not str(self.driver.find_element_by_xpath("//span[contains(text(),'Analyst Workbench')]").get_attribute(
                "class")).__contains__("collapsed"):
            fprint(self, "Analyst Workbench is collapsed - Expanding it")
            self.driver.find_element_by_xpath("//span[contains(text(),'Analyst Workbench')]").click()
            sleep(1)
            fprint(self, "[Passed] Analyst Workbench is expanded")
        #sleep(0.5)
        try:
            elm = self.driver.find_element_by_xpath("//span[contains(text(),'" + itemname + "')]/ancestor::a")
            # Move cursor to the element before clicking it, Dashboard and Console Status fails sometimes because of hint
            action = ActionChains(self.driver)
            action.move_to_element(elm).perform()
            self.driver.find_element_by_xpath("//span[contains(text(),'" + itemname + "')]/ancestor::a").click()
        except:
            if itemname == "STIX conversion":
                fprint(self, "Trying to click, by using different Xpath...")
                elm = self.driver.find_element_by_xpath("//span[contains(text(),'STIX Conversion')]/ancestor::a")
                # Move cursor to the element before clicking it, Dashboard and Console Status fails sometimes because of hint
                action = ActionChains(self.driver)
                action.move_to_element(elm).perform()
                self.driver.find_element_by_xpath("//span[contains(text(),'STIX Conversion')]/ancestor::a").click()
            else:
                fprint(self, "[Failed] Didn't found the XPath")
                self.fail("[Failed] Didn't found the XPath")

    # If no expansion is required then go to else part
    elif itemname == "Watchlist" and Build_Version.__contains__("2."):
        # Note: Since we are using contains in xpath, some items will be substring and won't be clicked properly.
        # Exceptions to those items are done in if condition.
        # 'Watchlist' conflicts with 'Watchlist Alerts'
        waitfor(self, 2, By.XPATH, "//span[contains(text(),'" + itemname + "')]/ancestor::a")
        elm = self.driver.find_element_by_xpath(
            "(//span[contains(text(),'" + itemname + "')]/ancestor::a)[2]")  # 2nd occurance
        # Move cursor to the element before clicking it, Dashboard and Console Status fails sometimes because of hint
        action = ActionChains(self.driver)
        action.move_to_element(elm).perform()
        #sleep(1)
        self.driver.find_element_by_xpath("(//span[contains(text(),'" + itemname + "')]/ancestor::a)[2]").click()
    elif itemname == "Threat Visualizer" or itemname == "Threat Investigations":
        # Todo: There was a change in the build after 2.8 release.We need to identify this based on version.
        fprint(self, "Checking if it is Threat Visualizer or Threat Investigations")
        if waitfor(self, 4, By.XPATH, "//span[contains(text(),'Threat Investigations')]/ancestor::a", False):
            fprint(self, "Threat Investigations is visible, will proceed with this")
            itemname = "Threat Investigations"
        elif waitfor(self, 4, By.XPATH, "//span[contains(text(),'Threat Visualizer')]/ancestor::a", False):
            fprint(self, "Threat Visualizer is visible, will proceed with this")
            itemname = "Threat Visualizer"
        else:
            fprint(self, "Couldn't find Threat Investigations or Threat Visualizer")
            itemname = "Threat Investigations"
        elm = self.driver.find_element_by_xpath("//span[contains(text(),'" + itemname + "')]/ancestor::a")
        # Move cursor to the element before clicking it, Dashboard and Console Status fails sometimes because of hint
        action = ActionChains(self.driver)
        action.move_to_element(elm).perform()
        #sleep(1)
        self.driver.find_element_by_xpath("//span[contains(text(),'" + itemname + "')]/ancestor::a").click()
    else:
        waitfor(self, 2, By.XPATH, "//span[contains(text(),'" + itemname + "')]/ancestor::a")
        elm = self.driver.find_element_by_xpath("//span[contains(text(),'" + itemname + "')]/ancestor::a")
        # Move cursor to the element before clicking it, Dashboard and Console Status fails sometimes because of hint
        action = ActionChains(self.driver)
        action.move_to_element(elm).perform()
        #sleep(1)
        self.driver.find_element_by_xpath("//span[contains(text(),'" + itemname + "')]/ancestor::a").click()
    fprint(self, "[Passed] Clicked Main Menu Item : " + itemname)

    # Wait for the page to Load
    if itemname == "ATT&CK Navigator":
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'ATT&CK Navigator')]")
    elif waitfor(self, 5, By.XPATH, "//span[contains(text(),'" + itemname + "')]/ancestor::h1", False):
        fprint(self, "Threat Data title is visible")
        # Todo: Right now "Threat Data" text is under span tag, will remove this condition when it is fixed.
    # wait for the page load of threat Bulletin
    elif itemname == "Threat Bulletin":
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Threat Bulletin')]")
        fprint(self, "Threat Bulletin page is visible")
    elif itemname == "Dashboards":
        waitfor(self, 5, By.XPATH, "//*[contains(text(),'Dashboards') and contains(@class,'cy-page__title')]")
        fprint(self, "Dashboard page is visible")
    else:
        try:
            waitfor(self, 5, By.XPATH, "//h1[contains(text(),'" + itemname + "')]")
        except:
            if itemname == "STIX conversion":
                waitfor(self, 1, By.XPATH, "//h1[contains(text(),'STIX Conversion')]")
            elif waitfor(self, 1, By.XPATH, f"//*[contains(text(),'{itemname}')]", False):
                fprint(self, "Module loaded successfully")
            else:
                fprint(self, "[Failed] Didn't found the Expected Element")
                self.fail("[Failed] Didn't found the Expected Element")
    check_error_alert(self)
    process_console_logs(self)


def check_error_alert(self):
    """
    Checks if there is any alert error displayed on the screen.
    This method should be called immediately after navigating to a menu.
    It will check the error for 8 seconds. If it doesn't appear till 8 seconds it will conclude it as passed.
    """
    # "//div[@role='alert']" can also be used for generic alert finding
    # cy-message__text might give you the error message content as well.
    fprint(self, "Checking Alerts for any failure messages")
    if waitfor(self, 2, By.XPATH, "//i[@class = 'cyicon-error']", False):
        fprint(self, "[Failed] Error Alert is observed on the screen")
        # Close the error message so that it don't interfere with others
        self.driver.find_element_by_xpath("//div[@class='el-notification__closeBtn el-icon-close']").click()
        sleep(0.5)
        self.fail("Case Status: [Failed] Error alert is observed on the screen")
    else:
        fprint(self, "Passed - No Error Alert is found on the screen")


def verify_fail_alert(self, comparewithtext):
    if waitfor(self, 5, By.XPATH, "//i[@class = 'cyicon-error']", False):
        textis = self.driver.find_element_by_xpath("//div[contains(@class, 'cy-message__text')]").text
        if textis == comparewithtext:
            fprint(self, "[Passed] Expected message is found, " + str(textis))
            self.driver.find_element_by_xpath("//div[@class='el-notification__closeBtn el-icon-close']").click()
            sleep(3)
        else:
            fprint(self,
                   "[Failed] Alert found with different msg. Found: " + str(textis) + "Expected:" + comparewithtext)
            self.fail("Case Status: [Failed] Alert found but expected message is not found")
    else:
        fprint(self, "Case Status: [Failed] Expected alert is not found")
        self.fail("Case Status: [Failed] Expected alert is not found")


def verify_success_alert(self, comparewithtext, timeout=20):
    if waitfor(self, timeout, By.XPATH, "//i[@class = 'cyicon-check-o-active']", False):
        sleep(1)
        textis = self.driver.find_element_by_xpath("//div[contains(@class, 'cy-message__text')]").text
        if textis == comparewithtext:
            fprint(self, "[Passed] Expected message is found, " + str(textis))
            self.driver.find_element_by_xpath("//div[@class='el-notification__closeBtn el-icon-close']").click()
            sleep(3)
        else:
            fprint(self,
                   "[Failed] Alert found with different msg. Found: " + str(textis) + "Expected:" + comparewithtext)
            self.fail("Case Status: [Failed] Alert found but expected message is not found")
    else:
        fprint(self, "Case Status: [Failed] Expected alert is not found")
        self.fail("Case Status: [Failed] Expected alert is not found")


def verify_alert(self, comparewithtext, timeout=5):
    if waitfor(self, timeout, By.XPATH, "//div[contains(@class, 'cy-message__text')]", False):
        textis = self.driver.find_element_by_xpath("//div[contains(@class, 'cy-message__text')]").text
        actual_message = textis.strip()
        print("Actual Alert message - "+actual_message)
        if comparewithtext in actual_message:
            fprint(self, "[Passed] Expected message is found, " + str(actual_message))
            self.driver.find_element_by_xpath("//div[@class='el-notification__closeBtn el-icon-close']").click()
            sleep(3)
        else:
            fprint(self,
                   "[Failed] Alert found with different msg. Found:" + str(actual_message) + "Expected:" + comparewithtext)
            self.fail("Case Status: [Failed] Alert found but expected message is not found")
    else:
        fprint(self, "Case Status: [Failed] Expected alert is not found")
        self.fail("Case Status: [Failed] Expected alert is not found")


def change_password(self, email, password):
    fprint(self, "EMAIL - " + email + " PASSWORD - " + password)
    login(self, email, password)

    if waitfor(self, 5, By.XPATH, "//p[contains(text(),'Please set your password')]", False) or \
            waitfor(self, 5, By.XPATH, "//p[contains(text(),'Create Password')]", False):
        fprint(self, "[Passed] - Change Password Screen appears on First Login")

        if waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='Current Password*']", False):
            self.driver.find_element_by_xpath("//input[@aria-placeholder='Current Password*']").send_keys(
                password)
        elif waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='Enter Current Password *']"):
            self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter Current Password *']").send_keys(
                password)

        fprint(self, "[Passed] - Entered Current Password in the text field")
        if waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='New Password*']", False):
            self.driver.find_element_by_xpath("//input[@aria-placeholder='New Password*']").send_keys(Admin_Password)
        elif waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='Enter New Password *']"):
            self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter New Password *']").send_keys(
                Admin_Password)

        fprint(self, "[Passed] - Entered New Password in the text field")
        if waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Confirm your new password*']", False):
            self.driver.find_element_by_xpath("//input[@aria-placeholder='Confirm your new password*']").send_keys(
                Admin_Password)
        elif waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Confirm New Password *']"):
            self.driver.find_element_by_xpath("//input[@aria-placeholder='Confirm New Password *']").send_keys(
                Admin_Password)
        fprint(self, "[Passed] - Entered new password in the 'Confirm New Password' text field")
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Set Password')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Set Password')]").click()
        sleep(10)
        fprint(self, "[Passed] - Password changed successfully")
