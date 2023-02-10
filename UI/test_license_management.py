import unittest
from datetime import *

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lib.ui.nav_app import *
from lib.ui.nav_tableview import *

enterprise_license = "02acea01-f0ef-4c38-8b27-821084c03fc7"
lite_license = "62ce8875-6aa0-488b-bf08-cad26c7f1f18"
alert_component_id = ['openapi', 'rules', 'source', 'subscriber', 'user']
before_openapi_count = 0
before_rule_count = 0
before_source_count = 0
before_subscriber_count = 0
before_user_count = 0


class LicenseManagement(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.driver = initialize_browser(self)
        login(self, Admin_Email, Admin_Password)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    @classmethod
    def setUp(self):
        clear_console_logs(self)

    def license_update(self):
        self.driver.find_element_by_xpath(
            "(//button[@type = 'button']//ancestor::div[@data-testaction = 'dropdown-link'])[2]").click()
        fprint(self, "[Passed] - Clicked on actions 3 dots")
        waitfor(self, 5, By.XPATH, "//li[contains(text(), 'Update')]")
        self.driver.find_element_by_xpath("//li[contains(text(), 'Update')]").click()
        fprint(self, "[Passed] - Clicked on Update")
        if CTIX_LITE == False:
            self.driver.find_element_by_xpath("//input[@aria-placeholder = 'Enter License Key*']").send_keys(
                enterprise_license)
            waitfor(self, 5, By.XPATH, "(//button[contains(text(), 'Update')])[1]")
            self.driver.find_element_by_xpath("(//button[contains(text(), 'Update')])[1]").click()
            fprint(self, "[Passed] - Clicked on update")
            sleep(5)
            verify_success(self, "updated successfully")
            fprint(self, "[Passed] - License Updated for CTIX Enterprise")

        else:
            self.driver.find_element_by_xpath("//input[@aria-placeholder = 'Enter License Key*']").send_keys(
                lite_license)
            waitfor(self, 5, By.XPATH, "(//button[contains(text(), 'Update')])[1]")
            self.driver.find_element_by_xpath("(//button[contains(text(), 'Update')])[1]").click()
            fprint(self, "[Passed] - Clicked on update")
            sleep(5)
            verify_success(self, "updated successfully")
            fprint(self, "[Passed] - License Updated for CTIX Lite")

    def date_difference(self, expiry):
        today_date = str(date.today())
        formatted_today_date = datetime.datetime.strptime(today_date, '%Y-%m-%d')
        formatted_expire_date = datetime.datetime.strptime(expiry, '%b %d, %Y, %I:%M %p')
        delta = formatted_expire_date - formatted_today_date
        return delta.days

    def get_count(self, component_id):
        count = self.driver.find_element_by_xpath("//div[@id='" + component_id + "']").text
        count_of_component = count[0:count.find("/")]
        return count_of_component

    def test_01_license_update(self):
        fprint(self, "License update for ctix lite")
        nav_menu_admin(self, "License Management")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'License Management')]")
        fprint(self, "[Passed] - Navigated to License Management page")
        self.license_update()

    def test_02_license_show_button(self):
        fprint(self, "Verify License show button")
        nav_menu_admin(self, "License Management")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'License Management')]")
        fprint(self, "[Passed] - Navigated to License Management page")
        self.driver.find_element_by_xpath("//button[@type = 'button']//i[@class = 'cyicon-eye-active']").click()
        fprint(self, "[Passed] - Clicked on show icon")
        if CTIX_LITE == False:
            waitfor(self, 5, By.XPATH, "//div[contains(text(), '" + enterprise_license + "')]")
            fprint(self, "[Passed] - Showing the license for enterprise version")
        else:
            waitfor(self, 5, By.XPATH, "//div[contains(text(), '" + lite_license + "')]")
            fprint(self, "[Passed] - Showing the license for lite version")

    def test_03_license_copy(self):
        fprint(self, "Copy the license")
        nav_menu_admin(self, "License Management")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'License Management')]")
        fprint(self, "[Passed] - Navigated to License Management page")
        self.driver.find_element_by_xpath("//button[@type = 'button']//span[@class = 'cyicon-copy']").click()
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Copied')]")))
        fprint(self, "[Passed] - License copied successfully")

    def test_04_license_version(self):
        fprint(self, "Validate license version")
        nav_menu_admin(self, "License Management")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'License Management')]")
        fprint(self, "[Passed] - Navigated to License Management page")
        self.driver.refresh()
        sleep(5)
        if CTIX_LITE == False:
            enterprise = self.driver.find_element_by_xpath("//span[contains(text(), 'CTIX Enterprise')]").text
            if enterprise == "CTIX Enterprise":
                fprint(self, "[Passed] - License is for enterprise version")
        else:
            lite = self.driver.find_element_by_xpath("//span[contains(text(), 'CTIX Lite')]").text
            if lite == "CTIX Lite":
                fprint(self, "[Passed] - License is for Lite version")

    def test_05_validate_tenant_info(self):
        fprint(self, "Validate tenant information")
        nav_menu_admin(self, "License Management")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'License Management')]")
        fprint(self, "[Passed] - Navigated to License Management page")
        current_url = self.driver.current_url
        fprint(self, current_url)
        url = current_url.replace('https://', '')
        domain_name = url.split('.').pop(0)
        tenant_name = self.driver.find_element_by_xpath(
            "//span[contains(text(),'Tenant Name')]/following-sibling::span").text
        if (tenant_name == domain_name):
            fprint(self, "[Passed] - Tenant Name validated successfully")
        tenant_code = self.driver.find_element_by_xpath(
            "//span[contains(text(),'Tenant Code')]/following-sibling::span").text
        if (tenant_code == domain_name):
            fprint(self, "[Passed] - Tenant Code validated successfully")

    def test_06_validate_expire_date(self):
        fprint(self, "Validate tenant information")
        nav_menu_admin(self, "License Management")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'License Management')]")
        fprint(self, "[Passed] - Navigated to License Management page")
        expire_date = self.driver.find_element_by_xpath(
            "//div[contains(text(), 'Expires on')]/following-sibling::div").text
        diff_days = self.driver.find_element_by_xpath(
            "//span[contains(text(),'day(s) from now')]/preceding-sibling::span").text
        delta_in_days = self.date_difference(expiry=expire_date)
        if str(diff_days) == str(delta_in_days):
            fprint(self, "[Passed] - Both the days are equal")
        else:
            self.fail("[Failed] - Days difference is not matching")

    def test_07_get_all_component_count(self):
        fprint(self, "Validate tenant information")
        nav_menu_admin(self, "License Management")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'License Management')]")
        fprint(self, "[Passed] - Navigated to License Management page")
        fprint(self, "[Passed] - Get count for open api before adding")
        before_openapi_count = self.get_count(component_id='openapi')
        set_value("open_api_count", self.get_count(component_id='openapi'))
        fprint(self, "[Passed] - Count is " + before_openapi_count)
        fprint(self, "[Passed] - Get count for rules before adding")
        before_rule_count = self.get_count(component_id='rules')
        set_value("rules_count", before_rule_count)
        fprint(self, "[Passed] - Count is " + before_rule_count)
        fprint(self, "[Passed] - Get count for source before adding")
        before_source_count = self.get_count(component_id='source')
        set_value("source_count", before_source_count)
        fprint(self, "[Passed] - Count is " + before_source_count)
        fprint(self, "[Passed] - Get count for subscriber before adding")
        before_subscriber_count = self.get_count(component_id='subscriber')
        set_value("subscriber_count", before_subscriber_count)
        fprint(self, "[Passed] - Count is " + before_subscriber_count)
        fprint(self, "[Passed] - Get count for user before adding")
        before_user_count = self.get_count(component_id='user')
        set_value("user_count", before_user_count)
        fprint(self, "[Passed] - Count is " + before_user_count)

    def test_08_validate_open_api_count(self):
        fprint(self, "Validate tenant information")
        nav_menu_admin(self, "License Management")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'License Management')]")
        fprint(self, "[Passed] - Navigated to License Management page")
        after_adding_open_api = self.get_count(component_id='openapi')
        fprint(self, "[Passed] Count is " + after_adding_open_api)
        if int(after_adding_open_api) == int(get_value("open_api_count")) + 1:
            fprint(self, "[Passed] - Count is matching")
        else:
            fprint(self, "[Failed] - Count doesn't match")
            self.fail("Count doesn't match")

    def test_09_validate_rules_count(self):
        fprint(self, "Validate tenant information")
        nav_menu_admin(self, "License Management")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'License Management')]")
        fprint(self, "[Passed] - Navigated to License Management page")
        after_adding_rules = self.get_count(component_id='rules')
        fprint(self, "[Passed] Count is " + after_adding_rules)
        if int(after_adding_rules) == int(get_value("rules_count")) + 1:
            fprint(self, "[Passed] - Count is matching")
        else:
            fprint(self, "[Failed] - Count doesn't match")
            self.fail("Count doesn't match")

    def test_10_validate_source_count(self):
        fprint(self, "Validate tenant information")
        nav_menu_admin(self, "License Management")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'License Management')]")
        fprint(self, "[Passed] - Navigated to License Management page")
        after_adding_source = self.get_count(component_id='source')
        fprint(self, "[Passed] Count is " + after_adding_source+" and expected is "+get_value("source_count"))
        if int(after_adding_source) > int(get_value("source_count")):
            fprint(self, "[Passed] - Source count increased")
        else:
            fprint(self, "[Failed] - Count doesn't match")
            self.fail("Count doesn't match")

    def test_11_validate_subscriber_count(self):
        fprint(self, "Validate tenant information")
        nav_menu_admin(self, "License Management")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'License Management')]")
        fprint(self, "[Passed] - Navigated to License Management page")
        after_adding_subscriber = self.get_count(component_id='subscriber')
        fprint(self, "[Passed] Count is " + after_adding_subscriber)
        if int(after_adding_subscriber) == int(get_value("subscriber_count")) + 1:
            fprint(self, "[Passed] - Count is matching")
        else:
            fprint(self, "[Failed] - Count doesn't match")
            self.fail("Count doesn't match")

    def test_12_validate_user_count(self):
        fprint(self, "Validate tenant information")
        nav_menu_admin(self, "License Management")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'License Management')]")
        fprint(self, "[Passed] - Navigated to License Management page")
        after_adding_user = self.get_count(component_id='user')
        fprint(self, "[Passed] Count is " + after_adding_user)
        if int(after_adding_user) == int(get_value("user_count")) + 1:
            fprint(self, "[Passed] - Count is matching")
        else:
            fprint(self, "[Failed] - Count doesn't match")
            self.fail("Count doesn't match")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())

