import unittest
from lib.ui.my_profile import *
from lib.ui.smtp import *
from lib.ui.quick_add import quick_create_ip
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from lib.ui.dashboard_elements import add_dashboard

enable_flag = 0
new_user = "test1234@cyware.com"
new_password = "Newpassword@123"
new_user_with_custom_permissions = "testuserpermissions@cyware.com"
testGroup = "testGroup"


class UserManagement(unittest.TestCase):

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

    def search_user(self, name):
        fprint(self, "searching for the user with username: "+name)
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(name)
        self.driver.find_element_by_xpath("//div//i[@data-testid='filter-search-icon']").click()
        if waitfor(self, 10, By.XPATH, "//span[@data-testid='email' and contains(text(), '"+name+"')]"):
            fprint(self, "User: "+name+" exists.")
        else:
            fprint(self, "User: "+name+" does not exists.")

    def enableSMTP(self):
        waitfor(self, 5, By.XPATH, "(//span[contains(@class,'cy-switch-btn__icon pl-0 pr-2 cyicon-cross-lg')])[1]")
        self.driver.find_element_by_xpath("(//span[contains(@class,'cy-switch-btn__icon pl-0 pr-2 cyicon-cross-lg')])[1]").click()
        fprint(self, "Enabling SMTP")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'SMTP Over TLS')]")
        fprint(self, "Enabled state is visible, filling up the credentials")
        enable_smtp(self)
        fprint(self, "SMTP Enabled")

    def disableSMTP(self):
        if waitfor(self, 5, By.XPATH, "(//span[contains(@class,'cy-switch-btn__icon cyicon-check-lg')])[1]", False):
            fprint(self, "Toggle Button is visible now Disabling SMTP")
            self.driver.find_element_by_xpath("(//span[contains(@class,'cy-switch-btn__icon cyicon-check-lg')])[1]").click()
            fprint(self, "Waiting for the confirmation popup")
            waitfor(self, 5, By.XPATH, "//button[contains(text(),'Yes, Proceed')]")
            fprint(self, "Clicking on the 'Yes Proceed' button")
            self.driver.find_element_by_xpath("//button[contains(text(),'Yes, Proceed')]").click()
            fprint(self, "Waiting for the text - Two Factor Authentication will not work if SMTP services are disabled")
            waitfor(self, 5, By.XPATH,"//p[contains(text(),'Two Factor Authentication will not work if SMTP services are disabled')]")
            fprint(self, "Text Visible, Clicking on the Update Configuration button")
            self.driver.find_element_by_xpath("//button[contains(text(),'Update Configuration')]").click()
            verify_success(self, "updated successfully")
            fprint(self, "SMTP Disabled")
        else:
            fprint(self, "SMTP found already Disabled")

    def checkUser(self, username=new_user):
        email = self.driver.find_element_by_xpath("//span[@data-testid='email']").text
        if email == username:
            fprint(self, "User Exist")

    def smtpStatus(self):
        fprint(self, "Checking SMTP is Enable or Disable")
        # Checked for the Enable Button
        if waitfor(self, 5, By.XPATH, "(//span[contains(@class,'cy-switch-btn__icon cyicon-check-lg')])[1]", False):
            fprint(self, "Found Enabled")
            global enable_flag
            enable_flag = 1

    def edit_user_permission(self, module_name, type):
        _search_bar = "(//input[@placeholder='Search or filter results'])[2]"
        sign_out(self)
        fprint(self, "Logging in new user.")
        login(self, new_user_with_custom_permissions, Admin_Password)
        nav_menu_admin(self, 'User Management')
        fprint(self, "Updating User Group.")
        waitfor(self, 10, By.XPATH, "//span/following-sibling::span[text()='User Groups']")
        self.driver.find_element_by_xpath("//span/following-sibling::span[text()='User Groups']").click()
        waitfor(self, 10, By.XPATH, "//span[text() = '"+testGroup+"']")
        self.driver.find_element_by_xpath("//span[text() = '"+testGroup+"']").click()
        waitfor(self, 10, By.XPATH, "//button[contains(text(),'Edit')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Edit')]").click()
        fprint(self, "Checking if all the permissions are enabled.")
        if waitfor(self, 10, By.XPATH, "//span[contains(text(),'Enable All')]/parent::div//input[contains(@class,'cy-switch-input') and @value='false']", False):
            waitfor(self, 10, By.XPATH, "//span[contains(text(),'Enable All')]//following-sibling::div")
            self.driver.find_element_by_xpath(
                "//span[contains(text(),'Enable All')]//following-sibling::div").click()
        waitfor(self, 10, By.XPATH,"//span[contains(@class,'cyicon-search')]")
        self.driver.find_element_by_xpath("//span[contains(@class,'cyicon-search')]").click()
        if waitfor(self, 10, By.XPATH, "//input[@placeholder='Type here to search']", False):
            _search_bar = "//input[@placeholder='Type here to search']"
        fprint(self, "Search bar is visible, searching - " + module_name)
        self.driver.find_element_by_xpath(_search_bar).click()
        self.driver.find_element_by_xpath(_search_bar).clear()
        self.driver.find_element_by_xpath(_search_bar).send_keys(
            module_name)
        self.driver.find_element_by_xpath("(//span[contains(text(),'Press enter or click to search')])[2]").click()
        waitfor(self, 10, By.XPATH,
                "(//div[contains(text(), '" + module_name + "')])[1]//following-sibling::div/div")
        self.driver.find_element_by_xpath(
            "(//div[contains(text(), '" + module_name + "')])[1]//following-sibling::div/div").click()
        fprint(self, "Disabling all the permissions of the particular module.")
        if waitfor(self, 10, By.XPATH, "(//div[contains(text(), '" + module_name + "')])[1]//following-sibling::div/div/span", False):
            self.driver.find_element_by_xpath("(//div[contains(text(), '" + module_name + "')])[1]//following-sibling::div/div/span").click()
        elif waitfor(self, 10, By.XPATH, "(//div[contains(text(), '" + module_name + "')])[1]//following-sibling::div/div/button", False):
            self.driver.find_element_by_xpath("(//div[contains(text(), '" + module_name + "')])[1]//following-sibling::div/div/button").click()
        else:
            fprint(self,"[Failed] "+module_name+" button not visible.")
            self.fail()
        if type == 'View':
            fprint(self, "Enabling view permissions")
            waitfor(self, 10, By.XPATH,
                    "(//div[contains(text(), 'View " + module_name + "')])[1]//following-sibling::div")
            self.driver.find_element_by_xpath("(//div[contains(text(), 'View " + module_name + "')])[1]").click()
        elif type == 'Create':
            fprint(self, "Enabling create permission")
            waitfor(self, 10, By.XPATH,
                    "(//div[contains(text(), 'Create " + module_name + "')])[1]//following-sibling::div")
            self.driver.find_element_by_xpath("(//div[contains(text(), 'Create " + module_name + "')])[1]").click()
        else:
            fprint(self, " Enabling view and update permission")
            waitfor(self, 10, By.XPATH, "(//div[contains(text(), 'Update "+module_name+"')])[1]")
            self.driver.find_element_by_xpath("(//div[contains(text(), 'Update "+module_name+"')])[1]").click()
        waitfor(self, 10, By.XPATH, "//button[contains(text(), 'Update User Group')]")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Update User Group')]").click()
        sleep(2)

    def disable_view_permission(self, module_name):
        sign_out(self)
        _search_bar = "(//input[@placeholder='Search or filter results'])[2]"
        fprint(self, "Logging in new user.")
        login(self, new_user_with_custom_permissions, Admin_Password)
        nav_menu_admin(self, 'User Management')
        waitfor(self, 10, By.XPATH, "//span/following-sibling::span[text()='User Groups']")
        self.driver.find_element_by_xpath("//span/following-sibling::span[text()='User Groups']").click()
        waitfor(self, 10, By.XPATH, "//span[text() = '" + testGroup + "']")
        self.driver.find_element_by_xpath("//span[text() = '" + testGroup + "']").click()
        waitfor(self, 10, By.XPATH, "//button[contains(text(),'Edit')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Edit')]").click()
        waitfor(self, 10, By.XPATH, "//span[contains(@class,'cyicon-search')]")
        self.driver.find_element_by_xpath("//span[contains(@class,'cyicon-search')]").click()
        if waitfor(self, 10, By.XPATH, "//input[@placeholder='Type here to search']", False):
            _search_bar = "//input[@placeholder='Type here to search']"
        fprint(self, "Search bar is visible, searching - " + module_name)
        self.driver.find_element_by_xpath(_search_bar).click()
        self.driver.find_element_by_xpath(_search_bar).clear()
        self.driver.find_element_by_xpath(_search_bar).send_keys(
            module_name)
        self.driver.find_element_by_xpath("(//span[contains(text(),'Press enter or click to search')])[2]").click()
        waitfor(self, 10, By.XPATH, "(//div[contains(text(), '" + module_name + "')])[1]")
        self.driver.find_element_by_xpath("(//div[contains(text(), '" + module_name + "')])[1]").click()
        if waitfor(self, 10, By.XPATH, "((//div[contains(text(), '"+module_name+"')])[1]//following::span/input[@value='true'])[2]", False):
            self.driver.find_element_by_xpath("(//div[contains(text(), '"+module_name+"')])[1]/following-sibling::div").click()
        waitfor(self, 10, By.XPATH, "//button[contains(text(), 'Update User Group')]")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Update User Group')]").click()
        sleep(2)
        waitfor(self, 15, By.XPATH, "//i[@class='cyicon-menu']")
        self.driver.find_element_by_xpath("//i[@class='cyicon-menu']").click()
        sleep(1)
        fprint(self, "[Passed] Clicked Main Menu")
        self.driver.find_element_by_xpath("//div[@class='cy-sidebar__hidden__search-box']//input").send_keys(module_name)
        sleep(0.5)
        if (waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+module_name+"')]", False)):
            fprint(self, "[Failed]- "+module_name+" module is present on main menu listing.")
            self.fail(module_name + " module is present on main menu listing.")
        else:
            fprint(self, "[Passed]- "+module_name+" module is removed from the main menu.")

    def click_on_actionMenu(self):
        ele = self.driver.find_element_by_xpath("//span[@data-testid='email']")
        ActionChains(self.driver).move_to_element(ele).perform()
        sleep(1)
        ele = self.driver.find_element_by_xpath("//button[@data-testid='action']")
        self.driver.execute_script("arguments[0].click();", ele)
        fprint(self, "Clicked on the Action menu")

    def test_01_user_listing_loading(self):
        """
        Verify if user listing page is loading
        """
        nav_menu_admin(self, "User Management")
        fprint(self, "----------- TC_ID 1: Verifying if user listing page is loading ----------")
        waitfor(self, 2, By.XPATH, "//span/following-sibling::span[text()='User Listing']")
        self.driver.find_element_by_xpath("//span/following-sibling::span[text()='User Listing']").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(),'User Listing')]")
        fprint(self, "[PASSED] User listing page loaded successfully")
        process_console_logs(self)

    def test_02_user_group_loading(self):
        """
        Verify if user group listing page is loading
        """
        nav_menu_admin(self, "User Management")
        fprint(self, "----------- TC_ID 2: Verifying if user groups page is loading ----------")
        waitfor(self, 2, By.XPATH, "//span/following-sibling::span[text()='User Groups']")
        self.driver.find_element_by_xpath("//span/following-sibling::span[text()='User Groups']").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(),'User Groups')]")
        fprint(self, "[PASSED] User Groups page loaded successfully")
        process_console_logs(self)

    def test_03_activity_log_loading(self):
        """
        Verify if activity logs page is loading
        """
        nav_menu_admin(self, "User Management")
        fprint(self, "----------- TC_ID 3: Verifying if Activity Logs page is loading ----------")
        waitfor(self, 2, By.XPATH, "//span/following-sibling::span[text()='Activity Logs']")
        self.driver.find_element_by_xpath("//span/following-sibling::span[text()='Activity Logs']").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(),'Activity Logs')]")
        fprint(self, "[PASSED] User Groups page loaded successfully")
        process_console_logs(self)

    def test_04_user_slider(self):
        """
        Verify add user slider is working
        """
        nav_menu_admin(self, "User Management")
        fprint(self, "----------- TC_ID 1: Verifying if add new user slider is loading ----------")
        waitfor(self, 2, By.XPATH, "//span/following-sibling::span[text()='User Listing']")
        self.driver.find_element_by_xpath("//span/following-sibling::span[text()='User Listing']").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(),'User Listing')]")
        self.driver.find_element_by_xpath("//button[text()='Add New']").click()
        waitfor(self, 2, By.XPATH, "//div[text()='New User']")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        fprint(self, "[PASSED] New User slider is loaded successfully")
        process_console_logs(self)

    def test_05_user_group_slider(self):
        """
        Verify if add user group slider is working
        """
        nav_menu_admin(self, "User Management")
        fprint(self, "----------- TC_ID 2: Verifying if new user groups slider is loading ----------")
        waitfor(self, 2, By.XPATH, "//span/following-sibling::span[text()='User Groups']")
        self.driver.find_element_by_xpath("//span/following-sibling::span[text()='User Groups']").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(),'User Groups')]")
        self.driver.find_element_by_xpath("//button[text()='New User Group']").click()
        waitfor(self, 2, By.XPATH, "//div[text()='Add User Group']")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        fprint(self, "[PASSED] New User Group slider working as expected")
        process_console_logs(self)

    def test_06_activity_logs_export(self):
        """
        Verify if activity logs export is working
        """
        nav_menu_admin(self, "User Management")
        fprint(self, "----------- TC_ID 3: Verifying if Activity Logs export is working ----------")
        waitfor(self, 2, By.XPATH, "//span/following-sibling::span[text()='Activity Logs']")
        self.driver.find_element_by_xpath("//span/following-sibling::span[text()='Activity Logs']").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(),'Activity Logs')]")
        self.driver.find_element_by_xpath("//button[@data-testaction='open-export']").click()
        waitfor(self, 2, By.XPATH, "//li[text()='CSV']")
        self.driver.find_element_by_xpath("//li[text()='CSV']").click()
        verify_success(self, "Your file will be downloaded in a moment")
        fprint(self, "[PASSED] CSV Export of Activity Logs successful")
        process_console_logs(self)

    def test_07_verify_admin_user_creation(self):
        fprint(self, "TC_ID: 4001  - admin_user_creation")
        nav_menu_admin(self, "User Management")
        search(self, new_user)
        fprint(self, "Looking for the User - "+new_user)
        if waitfor(self, 5, By.XPATH, "//span[@data-testid='email']", False):
            self.checkUser()
        else:
            fprint(self, "User Not Found, Disabling SMTP")
            fprint(self, "Switching to Configuration page")
            nav_menu_admin(self, "Configuration")
            fprint(self, "Clicking on the SMTP Tab")
            self.driver.find_element_by_xpath("//span[contains(text(),'SMTP')]").click()
            fprint(self, "Waiting for the Enable/Disable Toggle Button")
            self.smtpStatus()
            self.disableSMTP()
            fprint(self, "Switching back to User Management page")
            nav_menu_admin(self, "User Management")
            self.driver.find_element_by_xpath("//button[contains(text(),'Add New')]").click()
            fprint(self, "Creating a new user - "+new_user)
            waitfor(self, 20, By.XPATH, "//input[@name='first_name']")
            sleep(2)
            fprint(self, "Putting values into the fields")
            self.driver.find_element_by_xpath("//input[@name='first_name']").send_keys("testFirst")
            self.driver.find_element_by_xpath("//input[@name='last_name']").send_keys("testLast")
            if waitfor(self, 5, By.XPATH, "//input[@name='username']", False):
                self.driver.find_element_by_xpath("//input[@name='username']").send_keys(new_user)
            self.driver.find_element_by_xpath("//input[@name='email']").send_keys(new_user)
            self.driver.find_element_by_xpath("(//div[@name='groups'])[1]").click()
            waitfor(self, 5, By.XPATH, "//div/div[text()='Admin']")
            self.driver.find_element_by_xpath("//div/div[text()='Admin']").click()
            self.driver.find_element_by_xpath("//button[contains(text(),'Add User')]").click()
            verify_success(self, "User created successfully")
            # Storing credentials
            fprint(self, "Waiting for the Credential slider")
            waitfor(self, 5, By.XPATH, "(//p[contains(@class,'cy-credentials__value')])[1]")
            fprint(self, "Credential slider is visible, below are the details -")
            email = self.driver.find_element_by_xpath("(//p[contains(@class,'cy-credentials__value')])[1]").text
            waitfor(self, 5, By.XPATH, "(//p[contains(@class,'cy-credentials__value')])[2]")
            password = self.driver.find_element_by_xpath("(//p[contains(@class,'cy-credentials__value')])[2]").text
            fprint(self, "EMAIL - " + email + " PASSWORD - " + password)
            fprint(self, "Refreshing the page")
            self.driver.refresh()
            search(self, new_user)
            fprint(self, "Looking for the user again - "+new_user)
            if waitfor(self, 5, By.XPATH, "//span[@data-testid='email']", False):
                self.checkUser()
            if enable_flag == 1:
                fprint(self, "Enabling SMTP")
                fprint(self, "Switching to Configuration page")
                nav_menu_admin(self, "Configuration")
                fprint(self, "Clicking on the SMTP Tab")
                self.driver.find_element_by_xpath("//span[contains(text(),'SMTP')]").click()
                fprint(self, "Waiting for the Enable/Disable Toggle Button")
                self.enableSMTP()

    # Only for CTIX Version 3.0
    def test_07_v3_verify_admin_user_creation(self):
        fprint(self, "TC_ID: 4002  - v3_admin_user_creation")
        nav_menu_admin(self, "User Management")
        search(self, new_user)
        fprint(self, "Looking for the User - "+new_user)
        if waitfor(self, 5, By.XPATH, "//span[@data-testid='email']", False):
            self.checkUser()
        else:
            fprint(self, "User Not Found, Adding a new user")
            self.driver.find_element_by_xpath("//button[@data-testid='new-user']").click()
            fprint(self, "Creating a new user - "+new_user)
            waitfor(self, 5, By.XPATH, "//input[@name='first_name']", False)
            fprint(self, "Putting values into the fields")
            self.driver.find_element_by_xpath("//input[@name='first_name']").send_keys("testFirst")
            self.driver.find_element_by_xpath("//input[@name='last_name']").send_keys("testLast")
            if waitfor(self, 5, By.XPATH, "//input[@name='username']", False):
                self.driver.find_element_by_xpath("//input[@name='username']").send_keys(new_user)
            self.driver.find_element_by_xpath("//input[@name='email']").send_keys(new_user)
            self.driver.find_element_by_xpath("(//div[@name='groups'])[1]").click()
            waitfor(self, 5, By.XPATH, "//div/div[text()='Admin']", False)
            self.driver.find_element_by_xpath("//div/div[text()='Admin']").click()
            if waitfor(self, 2, By.XPATH, "//div[@name='email_alerts']", False):
                self.driver.find_element_by_xpath("//div[@name='email_alerts']").click()
            self.driver.find_element_by_xpath("//div//span[@class = 'cyicon-chevron-down  active']").click()
            waitfor(self, 5, By.XPATH, "//div[@name='allowed_tlp']", False)
            self.driver.find_element_by_xpath("//div[@name='allowed_tlp']").click()
            waitfor(self, 5, By.XPATH, "//div[text()='RED']/ancestor::div[1]")
            self.driver.find_element_by_xpath("//div[text()='RED']/ancestor::div[1]").click()
            fprint(self, "Clicking on the Add User Button")
            try:
                self.driver.find_element_by_xpath("//button[contains(text(),'Add User')]").click()
            except:
                fprint(self, "Trying with different xpath...")
                self.driver.find_element_by_xpath("(//button[contains(text(),'Add User')])[2]").click()
            verify_success(self, "User created successfully")
            fprint(self, "Waiting for the Credential slider")
            waitfor(self, 5, By.XPATH, "(//p[contains(@class,'cy-credentials__value')])[1]")
            fprint(self, "Credential slider is visible, below are the details -")
            email = self.driver.find_element_by_xpath("(//p[contains(@class,'cy-credentials__value')])[1]").text
            waitfor(self, 5, By.XPATH, "(//p[contains(@class,'cy-credentials__value')])[2]")
            password = self.driver.find_element_by_xpath("(//p[contains(@class,'cy-credentials__value')])[2]").text
            set_value("password",self.driver.find_element_by_xpath("(//p[contains(@class,'cy-credentials__value')])[2]").text)
            set_value("email",self.driver.find_element_by_xpath("(//p[contains(@class,'cy-credentials__value')])[1]").text)
            fprint(self, "EMAIL - " + email + " PASSWORD - " + password)
            fprint(self, "Refreshing the page")
            self.driver.refresh()
            search(self, new_user)
            fprint(self, "Looking for the user again - "+new_user)
            waitfor(self, 10, By.XPATH, "(//span[contains(text(),'"+new_user+"')])[1]")
            fprint(self, "User is visible now - "+new_user)

    def test_08_verify_login_from_new_user(self):
        fprint(self, "TC_ID: 40144  - verify new user creation by logging in.")
        fprint(self, "sign out current user.")
        sign_out(self)
        email = get_value("email")
        password = get_value("password")
        fprint(self, "Logging in new user.")
        change_password(self, email, password)
        waitfor(self, 20, By.XPATH, "//*[contains(text(),'Dashboards')]")
        fprint(self, "[PASSED] New User login done successfully!")

    def test_09_verify_reset_password(self):
        """
        Verify reset password.
        """
        # username = get_value("email")
        fprint(self, "TC_ID : 40115 - verify reset password.")
        nav_menu_admin(self, "User Management")
        self.search_user("test1234@cyware.com")
        waitfor(self, 10, By.XPATH, "//button[@data-testid='action']")
        fprint(self, "clicking on actions.")
        ele = self.driver.find_element_by_xpath("//button[@data-testid='action']")
        self.driver.execute_script("arguments[0].click();", ele)
        fprint(self, "selecting reset password.")
        waitfor(self, 5, By.XPATH, "(//li[contains(text(),'Reset Password')])[2]")
        self.driver.find_element_by_xpath("(//li[contains(text(),'Reset Password')])[2]").click()
        waitfor(self, 5, By.XPATH, "//button[text()='Yes, Reset']")
        self.driver.find_element_by_xpath("//button[text()='Yes, Reset']").click()
        fprint(self, "Waiting for the new Credential slider")
        waitfor(self, 5, By.XPATH, "(//p[contains(@class,'cy-credentials__value')])[1]")
        fprint(self, "Credential slider is visible, below are the details -")
        waitfor(self, 5, By.XPATH, "(//p[contains(@class,'cy-credentials__value')])[2]")
        password = self.driver.find_element_by_xpath("(//p[contains(@class,'cy-credentials__value')])[2]").text
        set_value("password",
                  self.driver.find_element_by_xpath("(//p[contains(@class,'cy-credentials__value')])[2]").text)
        fprint(self, " NEW PASSWORD - " + password)
        fprint(self, "[PASSED] Reset password successful.")
        process_console_logs(self)

    def test_10_verify_reset_password_login(self):
        fprint(self, "TC_ID : 40116 - verify reset password by logging in.")
        sign_out(self)
        email = get_value("email")
        password = get_value("password")

        fprint(self, "EMAIL - " + email + " PASSWORD - " + password)
        login(self, email, password)
        if waitfor(self, 5, By.XPATH, "//p[contains(text(),'Please set your password')]", False) or \
                waitfor(self, 5, By.XPATH, "//p[contains(text(),'Create Password')]", False):
            fprint(self, "[Passed] - Change Password Screen appears on reset password.")

            if waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='Current Password*']", False):
                self.driver.find_element_by_xpath("//input[@aria-placeholder='Current Password*']").send_keys(
                    password)
            elif waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='Enter Current Password *']"):
                self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter Current Password *']").send_keys(
                    password)
            fprint(self, "[Passed] - Entered Current Password in the text field")
            if waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='New Password*']", False):
                self.driver.find_element_by_xpath("//input[@aria-placeholder='New Password*']").send_keys(new_password)
            elif waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='Enter New Password *']"):
                self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter New Password *']").send_keys(new_password)
            fprint(self, "[Passed] - Entered New Password in the text field")
            if waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Confirm your new password*']", False):
                self.driver.find_element_by_xpath("//input[@aria-placeholder='Confirm your new password*']").send_keys(new_password)
            elif waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Confirm New Password *']"):
                self.driver.find_element_by_xpath("//input[@aria-placeholder='Confirm New Password *']").send_keys(new_password)
            fprint(self, "[Passed] - Entered new password: "+new_password+" in the 'Confirm New Password' text field")
            waitfor(self, 5, By.XPATH, "//button[contains(text(),'Set Password')]")
            self.driver.find_element_by_xpath("//button[contains(text(),'Set Password')]").click()
            waitfor(self, 20, By.XPATH, "//*[contains(text(),'Dashboards')]")
            fprint(self, "[Passed] - Password changed successfully")

    def test_11_verify_user_Activity_logs(self):
        fprint(self, "TC_ID : 40117 - verify activity logs.")
        fprint(self, "logging out current user.")
        sign_out(self)
        fprint(self, "logging in new user.")
        email = get_value("email")
        login(self, email, new_password)
        fprint(self, "Adding intel via quick add.")
        quick_create_ip(self, "1.1.1.1", "1.1.1.1")
        nav_menu_admin(self, "User Management")
        fprint(self, "Checking in Activity logs for quick add ip.")
        self.search_user("test1234@cyware.com")
        waitfor(self, 10, By.XPATH, "//button[@data-testid='action']")
        fprint(self, "clicking on actions.")
        ele = self.driver.find_element_by_xpath("//button[@data-testid='action']")
        self.driver.execute_script("arguments[0].click();", ele)
        fprint(self, "selecting User Activity Logs.")
        waitfor(self, 10, By.XPATH, "(//div//li[contains(text(),'User Activity Logs')])[2]")
        self.driver.find_element_by_xpath("(//div//li[contains(text(),'User Activity Logs')])[2]").click()
        if waitfor(self, 10, By.XPATH, "//span[contains(text(), 'User (API) Activity Logs')]", False):
            waitfor(self, 10, By.XPATH, "(//input[@placeholder='Search or filter results'])")
            self.driver.find_element_by_xpath("(//input[@placeholder='Search or filter results'])").send_keys('/ctixapi/conversion/quick-intel/create-stix/')
            self.driver.find_element_by_xpath("(//div//i[@data-testid='filter-search-icon'])").click()
        elif waitfor(self, 10, By.XPATH, "//div[contains(text(), 'User Activity Logs')]"):
            waitfor(self, 10, By.XPATH, "(//input[@placeholder='Search or filter results'])[2]")
            self.driver.find_element_by_xpath("(//input[@placeholder='Search or filter results'])[2]").send_keys('/ctixapi/conversion/quick-intel/create-stix/')
            self.driver.find_element_by_xpath("(//div//i[@data-testid='filter-search-icon'])[2]").click()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'POST')]")
        fprint(self, "[PASSED] Verified Activity logs successful.")

    def test_12_verify_deactivate_user(self):
        """
        Verify if user deactivation is working
        """
        username = get_value("email")
        fprint(self, "TC_ID : 40118 - verify if able to deactivate a user")
        nav_menu_admin(self, "User Management")
        self.search_user(username)
        waitfor(self, 10, By.XPATH, "//button[@data-testid='action']")
        fprint(self, "clicking on actions.")
        ele = self.driver.find_element_by_xpath("//button[@data-testid='action']")
        self.driver.execute_script("arguments[0].click();", ele)
        fprint(self, "selecting deactivate user.")
        waitfor(self, 5, By.XPATH, "(//div//li[contains(text(),'Deactivate')])[2]")
        self.driver.find_element_by_xpath("(//div//li[contains(text(),'Deactivate')])[2]").click()
        waitfor(self, 5, By.XPATH, " //button[text()='Yes, Deactivate']")
        self.driver.find_element_by_xpath("//button[text()='Yes, Deactivate']").click()
        verify_success(self, "Selected User(s) Deactivated successfully")
        fprint(self, "[PASSED] User deactivated successfully.")
        process_console_logs(self)

    def test_13_verify_deactivate_user_login(self):
        """
        Verify if user is deactivated successfully
        """
        fprint(self, "TC_ID : 40119 - verify if user is deactivated successfully")
        nav_menu_admin(self, "User Management")
        username = get_value("email")
        self.search_user(username)
        if waitfor(self, 5, By.XPATH, "//span[@data-testid='active_status' and contains(text(), 'Inactive')]", False):
            fprint(self, "[PASSED] User inactive status verified successfully.")
        elif waitfor(self, 1, By.XPATH, "//div[@data-testid='is_active' and contains(text(), 'Inactive')]"):
            fprint(self, "[PASSED] User inactive status verified successfully.")
        fprint(self, "Verify whether deactivated user is able to login.")
        sign_out(self)
        fprint(self, "Logging in deactivated user using credentials: email - "+username+"  password - "+new_password)
        waitfor(self, 20, By.NAME, "email")
        self.driver.find_element_by_name("email").send_keys(username)
        self.driver.find_element_by_name("password").send_keys(new_password)
        if waitfor(self, 2, By.XPATH, "//button[contains(text(),'Login')]", False):
            self.driver.find_element_by_xpath("//button[contains(text(),'Login')]").click()
        elif waitfor(self, 2, By.XPATH, "//button[contains(text(),'Continue')]", False):
            self.driver.find_element_by_xpath("//button[contains(text(),'Continue')]").click()
        elif waitfor(self, 1, By.XPATH, "//button[contains(text(),'Sign in')]"):
            self.driver.find_element_by_xpath("//button[contains(text(),'Sign in')]").click()
        waitfor(self, 10, By.XPATH, "//div//p[contains(text(), 'Invalid User Credentials')]")
        fprint(self, "[PASSED] Verified User deactivation successfully.")

    def test_14_activate_deactivated_user(self):
        fprint(self, "TC_ID : 40120 verify if deactivated user is activated successfully")
        nav_menu_admin(self, "User Management")
        fprint(self, "check is user is deactivated")
        email = get_value("email")
        self.search_user(email)
        fprint(self, "Activating the user")
        self.click_on_actionMenu()
        waitfor(self, 5, By.XPATH, "//div//li[contains(text(),'Activate')]")
        fprint(self, "Selecting activate user option")
        self.driver.find_element_by_xpath("(//div//li[contains(text(),'Activate')])[2]").click()
        waitfor(self, 5, By.XPATH, "//button[text()='Yes, Activate']")
        self.driver.find_element_by_xpath("//button[text()='Yes, Activate']").click()
        verify_success(self, "Selected User(s) Activated successfully")
        fprint(self, "[PASSED] Activated a deactive user successfully.")
        process_console_logs(self)

    def test_15_delete_deactivated_user(self):
        fprint(self, "TC_ID : 40121 verify if able to delete a user")
        email = get_value("email")
        nav_menu_admin(self, "User Management")
        self.search_user(email)
        fprint(self, "Deactivating user - "+email)
        self.click_on_actionMenu()
        waitfor(self, 5, By.XPATH, "(//div//li[contains(text(),'Deactivate')])[2]")
        self.driver.find_element_by_xpath("(//div//li[contains(text(),'Deactivate')])[2]").click()
        waitfor(self, 5, By.XPATH,"//button[text()='Yes, Deactivate']")
        self.driver.find_element_by_xpath("//button[text()='Yes, Deactivate']").click()
        verify_success(self, "Selected User(s) Deactivated successfully")
        fprint(self, "User deactivated successfully.")
        fprint(self, "Deleting a deactivated user")
        waitfor(self, 5, By.XPATH, "//button[@data-testid='action']")
        ele = self.driver.find_element_by_xpath("//button[@data-testid='action']")
        self.driver.execute_script("arguments[0].click();", ele)
        waitfor(self, 5, By.XPATH, "(//div//li[contains(text(),'Delete')])[2]")
        self.driver.find_element_by_xpath("(//div//li[contains(text(),'Delete')])[2]").click()
        waitfor(self, 5, By.XPATH, "//button[@data-testalert='confirm-delete']")
        self.driver.find_element_by_xpath("//button[@data-testalert='confirm-delete']").click()
        verify_success(self, "User deleted successfully")
        fprint(self, "[PASSED] Deleted a deactive user successfully.")

    def test_16_user_group_creation(self):
        """
        Verify if add user group is working
        """
        nav_menu_admin(self, "User Management")
        fprint(self, "TC_ID : 40122 Verify creation of new user group. ")
        waitfor(self, 10, By.XPATH, "//span/following-sibling::span[text()='User Groups']")
        self.driver.find_element_by_xpath("//span/following-sibling::span[text()='User Groups']").click()
        waitfor(self, 10, By.XPATH, "//button[text()='Add User Group']")
        self.driver.find_element_by_xpath("//button[text()='Add User Group']").click()
        waitfor(self, 10, By.XPATH, "//div[text()='Add User Group']")
        waitfor(self, 10, By.XPATH, "//input[@aria-placeholder='Name *']")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys(testGroup)
        if waitfor(self, 10, By.XPATH, "//div[contains(text(),'User Group Active')]//preceding-sibling::button", False):
            self.driver.find_element_by_xpath(
                "//div[contains(text(),'User Group Active')]//preceding-sibling::button").click()
            waitfor(self, 10, By.XPATH, "//span[contains(text(),'Enable All')]//following-sibling::div/button")
            self.driver.find_element_by_xpath(
                "//span[contains(text(),'Enable All')]//following-sibling::div/button").click()
        elif waitfor(self, 10, By.XPATH, "//label[contains(text(),'User Group Active')]//preceding-sibling::span", False):
            self.driver.find_element_by_xpath(
                "//label[contains(text(),'User Group Active')]//preceding-sibling::span").click()
            waitfor(self, 10, By.XPATH, "//span[contains(text(),'Enable All')]//following-sibling::div/span")
            self.driver.find_element_by_xpath(
                "//span[contains(text(),'Enable All')]//following-sibling::div/span").click()
        else:
            self.fail()
        waitfor(self, 10, By.XPATH, "(//button[contains(text(),'Add User Group')])[2]")
        self.driver.find_element_by_xpath("(//button[contains(text(),'Add User Group')])[2]").click()
        verify_success(self, "User Group created successfully")
        waitfor(self, 10, By.XPATH, "//span[text()='" + testGroup + "']")
        fprint(self, "[PASSED] User group created successfully!")

    def test_16_clone_user_group(self):
        """
        Verify if user group clone is working
        """
        nav_menu_admin(self, "User Management")
        fprint(self, "TC_ID : 40216 Verify clone of user group. ")
        waitfor(self, 10, By.XPATH, "//span/following-sibling::span[text()='User Groups']")
        self.driver.find_element_by_xpath("//span/following-sibling::span[text()='User Groups']").click()
        search(self, testGroup)
        waitfor(self, 10, By.XPATH, "//span[text()='"+testGroup+"']")
        waitfor(self, 10, By.XPATH, "(//span[text()='"+testGroup+"']//following::div/button)[1]")
        self.driver.find_element_by_xpath("(//span[text()='"+testGroup+"']//following::div/button)[1]").click()
        waitfor(self, 10, By.XPATH, "//li[contains(text(),'Clone')]")
        ele = self.driver.find_element_by_xpath("//div//li[contains(text(),'Clone')]")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", ele)
        self.driver.execute_script("arguments[0].click();", ele)
        waitfor(self, 10, By.XPATH, "//input[@aria-placeholder='Name *']")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").clear()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Name *']").send_keys('clone')
        waitfor(self, 10, By.XPATH, "(//button[text() = 'Add User Group'])[2]")
        self.driver.find_element_by_xpath("(//button[text() = 'Add User Group'])[2]").click()
        verify_success(self, "User Group updated successfully")
        fprint(self, 'searching for clone group.')
        search(self, ""+testGroup+"clone")
        fprint(self, '[PASSED] User group clone done successfully!')

    def test_17_add_user_with_custom_permissions(self):
        fprint(self, "TC_ID : 40217 Verify creation of new user with custom permissions.")
        nav_menu_admin(self, 'User Management')
        search(self, new_user_with_custom_permissions)
        fprint(self, "Looking for the User - " + new_user_with_custom_permissions)
        if waitfor(self, 5, By.XPATH, "//span[@data-testid='email']", False):
            self.checkUser(new_user_with_custom_permissions)
        else:
            fprint(self, "User Not Found, Adding a new user")
            self.driver.find_element_by_xpath("//button[@data-testid='new-user']").click()
            fprint(self, "Creating a new user - " + new_user_with_custom_permissions)
            waitfor(self, 5, By.XPATH, "//input[@name='first_name']", False)
            fprint(self, "Putting values into the fields")
            self.driver.find_element_by_xpath("//input[@name='first_name']").send_keys("Firstname")
            self.driver.find_element_by_xpath("//input[@name='last_name']").send_keys("Lastname")
            if waitfor(self, 5, By.XPATH, "//input[@name='username']", False):
                self.driver.find_element_by_xpath("//input[@name='username']").send_keys(new_user_with_custom_permissions)
            self.driver.find_element_by_xpath("//input[@name='email']").send_keys(new_user_with_custom_permissions)
            self.driver.find_element_by_xpath("(//div[@name='groups'])[1]").click()
            waitfor(self, 5, By.XPATH, "//div/div[text()='"+testGroup+"']", False)
            self.driver.find_element_by_xpath("//div/div[text()='"+testGroup+"']").click()
            if waitfor(self, 2, By.XPATH, "//div[@name='email_alerts']", False):
                self.driver.find_element_by_xpath("//div[@name='email_alerts']").click()
            self.driver.find_element_by_xpath("//div//span[@class = 'cyicon-chevron-down  active']").click()
            waitfor(self, 5, By.XPATH, "//div[@name='allowed_tlp']", False)
            self.driver.find_element_by_xpath("//div[@name='allowed_tlp']").click()
            waitfor(self, 5, By.XPATH, "//div[text()='RED']/ancestor::div[1]")
            self.driver.find_element_by_xpath("//div[text()='RED']/ancestor::div[1]").click()
            try:
                self.driver.find_element_by_xpath("//button[contains(text(),'Add User')]").click()
            except:
                fprint(self, "Trying with different xpath...")
                self.driver.find_element_by_xpath("(//button[contains(text(),'Add User')])[2]").click()
            verify_success(self, "User created successfully")
            fprint(self, "Waiting for the Credential slider")
            waitfor(self, 5, By.XPATH, "(//p[contains(@class,'cy-credentials__value')])[1]")
            fprint(self, "Credential slider is visible, below are the details -")
            email = self.driver.find_element_by_xpath("(//p[contains(@class,'cy-credentials__value')])[1]").text
            waitfor(self, 5, By.XPATH, "(//p[contains(@class,'cy-credentials__value')])[2]")
            password = self.driver.find_element_by_xpath("(//p[contains(@class,'cy-credentials__value')])[2]").text
            set_value("password",
                      self.driver.find_element_by_xpath("(//p[contains(@class,'cy-credentials__value')])[2]").text)
            set_value("email",
                      self.driver.find_element_by_xpath("(//p[contains(@class,'cy-credentials__value')])[1]").text)
            fprint(self, "EMAIL - " + email + " PASSWORD - " + password)
            fprint(self, "Refreshing the page")
            self.driver.refresh()
            search(self, new_user_with_custom_permissions)
            fprint(self, "Looking for the user again - " + new_user_with_custom_permissions)
            waitfor(self, 10, By.XPATH, "(//span[contains(text(),'" + new_user_with_custom_permissions + "')])[1]")
            fprint(self, "User is visible now - " + new_user_with_custom_permissions)
            fprint(self, "verify new user creation by logging in.")
            fprint(self, "sign out current user.")
            sign_out(self)
            email = get_value("email")
            password = get_value("password")
            fprint(self, "Logging in new user.")
            change_password(self, email, password)
            waitfor(self, 20, By.XPATH, "//*[contains(text(),'Dashboards')]")
            fprint(self, "[PASSED] New User login done successfully!")

    def test_18_verify_dashboard_view_permissions(self):
        fprint(self, "TC_ID : 40218 Verify dashboard view permissions.")
        self.edit_user_permission('Dashboards', 'View')
        nav_menu_main(self, 'Dashboards')
        fprint(self, 'User can only view dashboard, not able to add/edit it.')
        fprint(self, 'Checking if user can view dashboard.')
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Domain Objects vs Source')]")
        fprint(self, '[PASSED]- user can view dashboard.')
        fprint(self, 'Checking if user cannot add dashboard.')
        waitfor(self, 20, By.XPATH, "//div[@class = 'cy-permission-disabled']/button[@data-testid='add-dashboard']")
        fprint(self, '[PASSED]- user cannot ADD dashboard.')
        fprint(self, 'Checking if user cannot edit dashboard.')
        waitfor(self, 20, By.XPATH, "//div[@class = 'cy-permission-disabled']/li[@data-testaction='edit-dashboard']")
        fprint(self, '[PASSED]- user cannot edit dashboard.')
        fprint(self, '[PASSED]- View permission for dashboard verified successfully!')

    def test_19_verify_dashboard_create_permissions(self):
        fprint(self, "TC_ID : 40219 Verify dashboard create permissions.")
        self.edit_user_permission('Dashboards', 'Create')
        nav_menu_main(self, 'Dashboards')
        fprint(self, 'User can only create dashboard, not able to view/edit it.')
        fprint(self, 'Checking if user can add dashboard.')
        add_dashboard(self)
        fprint(self, '[PASSED]- user can ADD dashboard.')
        fprint(self, 'Checking if user cannot view dashboard.')
        if waitfor(self, 2, By.XPATH, "//div[contains(text(),'Domain Objects vs Source')]", False):
            fprint(self, "[Failed] - User can view dashboard")
            self.fail("[FAILED]- user can view dashboard.")
        else:
            fprint(self, '[PASSED]- user cannot view dashboard.')
        fprint(self, '[PASSED]- Create permission for dashboard verified successfully!')

    def test_20_verify_dashboard_View_Update_permissions(self):
        fprint(self, "TC_ID : 40220 Verify dashboard view & update permissions.")
        self.edit_user_permission('Dashboards', 'View & Update')
        nav_menu_main(self, 'Dashboards')
        fprint(self, 'User cannot create dashboard,only view/edit it.')
        fprint(self, 'Checking if user can view dashboard.')
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Domain Objects vs Source')]")
        fprint(self, '[PASSED]- user can view dashboard.')
        fprint(self, 'Checking if user can edit dashboard.')
        waitfor(self, 20, By.XPATH, "//li[@data-testaction='edit-dashboard']")
        fprint(self, '[PASSED]- user can edit dashboard.')
        fprint(self, 'Checking if user cannot add dashboard.')
        waitfor(self, 20, By.XPATH, "//div[@class = 'cy-permission-disabled']/button[@data-testid='add-dashboard']")
        fprint(self, '[PASSED]- user cannot ADD dashboard.')
        fprint(self, '[PASSED]- View & Update permission for dashboard verified successfully!')

    def test_21_verify_threat_data_view_permission(self):
        fprint(self, "TC_ID : 40221 Verify Threat data view permissions.")
        self.edit_user_permission('Threat Data', 'View')
        nav_menu_main(self, 'Threat Data')
        fprint(self, 'User can only view threat')
        if (waitfor(self, 2, By.XPATH, "//h1//span[contains(text(),'Threat Data')]", False)):
            fprint(self, '[PASSED]- user can view Threat data.')
        else:
            fprint(self, "[Failed] - User cannot view threat data")
            self.fail("[FAILED]- user cannot view threat data.")
        fprint(self, '[PASSED]- View permission for Threat Data verified successfully!')

    def test_22_verify_rule_create_permissions(self):
        fprint(self, "TC_ID : 40222 Verify Rule create permissions.")
        self.edit_user_permission('Rule', 'Create')
        nav_menu_main(self, 'Rules')
        fprint(self, 'User can only create Rule, not able to edit it.')
        fprint(self, 'Checking if user can add Rule.')
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'New')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'New')]").click()
        waitfor(self, 20, By.XPATH, "//li/a[contains(text(),'Rule')]")
        self.driver.find_element_by_xpath("//li/a[contains(text(),'Rule')]").click()
        if waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Skip')]", False):
            self.driver.find_element_by_xpath("//button[contains(text(), 'Skip')]").click()
        sleep(2)
        fprint(self, "Filling in rule name")
        waitfor(self, 20, By.XPATH, "//div/preceding-sibling::div/div/div/input[@aria-placeholder='Rule Name *']")
        self.driver.find_element_by_xpath("//div/preceding-sibling::div/div/div/input[@aria-placeholder='Rule Name *']").click()
        clear_field(self.driver.find_element_by_xpath("//div/preceding-sibling::div/div/div/input[@aria-placeholder='Rule Name *']"))
        self.driver.find_element_by_xpath("//div/preceding-sibling::div/div/div/input[@aria-placeholder='Rule Name *']").send_keys("permissions")
        fprint(self, "Filling in rule name")
        sleep(2)
        waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Submit')]")
        fprint(self, "Clicking on Submit")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Submit')]").click()
        waitfor(self, 20 , By.XPATH, "//button[contains(text(),'Save as Draft')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save as Draft')]").click()
        verify_success(self, "Rule created successfully", 10)
        fprint(self, 'Checking Rule is created or not...')
        search(self, "permissions")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'permissions')]")
        # fprint(self, 'Checking if user cannot view rules.')
        # if waitfor(self, 5, By.XPATH, "//span[contains(text(),'Rule Name')]", False):
        #     fprint(self, "[Failed]- User can view Rules.")
        #     self.fail("[FAILED]- user can view rules.")
        # else:
        #     fprint(self, '[PASSED]- user cannot view Rules.')
        fprint(self, '[PASSED]- Create permission for Rules verified successfully!')

    def test_23_verify_rules_view_permission(self):
        failures = []
        fprint(self, "TC_ID : 40223 Verify Rules view permissions.")
        self.edit_user_permission('Rule', 'View')
        nav_menu_main(self, 'Rules')
        fprint(self, 'User can only view rules, not able to add/edit it.')
        fprint(self, 'Checking if user can view rules.')
        if waitfor(self, 5, By.XPATH, "//span[contains(text(),'Rule Name')]", False):
            fprint(self, '[PASSED]- user can view Rules.')
        else:
            fprint(self, "[Failed] - User cannot view rules")
            failures.append("User cannot view rules")
        fprint(self, 'Checking if user cannot add Rule.')
        if waitfor(self, 5, By.XPATH, "//div[@class = 'cy-permission-disabled']/button[contains(text(),'New Rule')]", False):
            fprint(self, '[PASSED]- user cannot add Rules.')
        else:
            fprint("[Failed]- user can add rules.")
            failures.append("User can add rules.")
        fprint(self, 'Checking if user cannot edit Rules.')
        if waitfor(self, 5, By.XPATH, "//div[@class = 'cy-permission-disabled']//following::li[contains(text(),'Edit')]", False):
            fprint(self, '[PASSED]- user cannot edit Rules.')
        else:
            fprint("[Failed]- user can edit rules.")
            failures.append("User can edit rules.")
        self.assert_(failures == [], str(failures))
        fprint(self, '[PASSED]- View permission for Rules verified successfully!')

    def test_24_verify_rule_view_Update_permissions(self):
        failures = []
        fprint(self, "TC_ID : 40224 Verify Rule view & update permissions.")
        self.edit_user_permission('Rule', 'View & Update')
        nav_menu_main(self, 'Rules')
        fprint(self, 'User cannot create Rule,only view/edit it.')
        fprint(self, 'Checking if user can view Rules.')
        if waitfor(self, 5, By.XPATH, "//span[contains(text(),'Rule Name')]", False):
            fprint(self, '[PASSED]- user can view Rules.')
        else:
            fprint(self, "[Failed] - User cannot view rules")
            failures.append("User cannot view rules.")
        fprint(self, 'Checking if user cannot add Rule.')
        if waitfor(self, 5, By.XPATH, "//div[@class = 'cy-permission-disabled']/button[contains(text(),'New Rule')]", False):
            fprint(self, '[PASSED]- user cannot add Rules.')
        else:
            fprint(self, "[Failed]- user can add rules.")
            failures.append("User can add rules.")
        fprint(self, 'Checking if user can edit Rules.')
        if waitfor(self, 5, By.XPATH, "//li[contains(text(),'Edit')]", False):
            fprint(self, '[PASSED]- user can edit Rules.')
        else:
            fprint(self, "[Failed]- user cannot edit rules.")
        self.assert_(failures == [], str(failures))
        fprint(self, '[PASSED]- View & Update permission for Rules verified successfully!')

    def test_25_verify_report_create_permission(self):
        failures = []
        fprint(self, "TC_ID : 40225 Verify Report create permissions.")
        self.edit_user_permission('Reports', 'Create')
        nav_menu_main(self, 'Reports')
        fprint(self, 'User can only create reports, cannot edit/view it.')
        if waitfor(self, 5, By.XPATH, "//button[contains(text(),'Add')]", False):
            fprint(self, "Adding report")
            if waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Enter Title*']", False):
                self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter Title*']").send_keys(
                    "automation_report" + uniquestr)
                sleep(1)
                self.driver.find_element_by_xpath("//button[contains(text(),'Add')]").click()
            else:
                self.driver.find_element_by_xpath("//button[contains(text(),'Add')]").click()
                waitfor(self, 10, By.XPATH, "//input[@placeholder='Report Name*']")
                self.driver.find_element_by_xpath("//input[@placeholder='Report Name*']").send_keys("automation_report" + uniquestr)
            waitfor(self, 20, By.XPATH, "(//input [@type = 'checkbox']/following::span)[1]")
            ele = self.driver.find_element_by_xpath("(//input [@type = 'checkbox']/following::span)[1]")
            self.driver.execute_script("arguments[0].scrollIntoView();", ele)
            self.driver.execute_script("arguments[0].click();", ele)
            waitfor(self, 20, By.XPATH, "//span[contains(text(), 'Save')]/ancestor::button")
            self.driver.find_element_by_xpath("//span[contains(text(), 'Save')]/ancestor::button").click()
            waitfor(self, 5, By.XPATH, "//li[contains(text(), 'Global Report')]")
            self.driver.find_element_by_xpath("//li[contains(text(), 'Global Report')]").click()
            verify_success(self, "Report created successfully")
            fprint(self, '[PASSED]- user can create Reports.')
        else:
            fprint(self, "[Failed] - User cannot create report.")
            failures.append("User cannot create reports.")
        fprint(self, 'Checking if user cannot view report.')
        if waitfor(self, 5, By.XPATH, "(//span[contains(text(),'Title')])[2]", False):
            fprint(self, "[Failures]- user can view rules.")
            failures.append("User can view rules.")
        else:
            fprint(self, '[PASSED]- user cannot view Rules.')
        self.assert_(failures == [], str(failures))
        fprint(self, '[PASSED]- Create permission for Reports verified successfully!')

    def test_26_verify_report_view_permission(self):
        failures = []
        fprint(self, "TC_ID : 40226 Verify Report view  permissions.")
        self.edit_user_permission('Report', 'View')
        nav_menu_main(self, 'Reports')
        fprint(self, 'User can only view reports, cannot edit/create it.')
        if waitfor(self, 5, By.XPATH, "(//span[contains(text(),'Title')])[2]", False):
            fprint(self, '[PASSED]- user can view Report.')
        else:
            fprint(self, "[Failed] - User cannot view report")
            failures.append("User cannot view report.")
        fprint(self, 'Checking if user cannot add report.')
        if waitfor(self, 5, By.XPATH, "//div[@class = 'cy-permission-disabled']/button[contains(text(),'Add')]", False):
            fprint(self, '[PASSED]- user cannot add reports.')
        else:
            fprint(self,"[Failed]- user can add report.")
            failures.append("User can add report.")
        fprint(self, 'Checking if user cannot edit Report.')
        waitfor(self, 5, By.XPATH, "//button[@data-testid='action']/i")
        ele = self.driver.find_element_by_xpath("//button[@data-testid='action']/i")
        self.driver.execute_script("arguments[0].scrollIntoView();", ele)
        self.driver.execute_script("arguments[0].click();", ele)
        if waitfor(self, 5, By.XPATH,
                   "//div[@class = 'cy-permission-disabled']//following::div[contains(text(),'Edit')]", False):
            fprint(self, '[PASSED]- user cannot edit Report.')
        else:
            fprint(self, "[Failed]- user can edit report.")
            failures.append("User can edit report.")
        self.assert_(failures == [], str(failures))
        fprint(self, '[PASSED]- View permission for Report verified successfully!')

    def test_27_verify_report_view_Update_permissions(self):
        failures = []
        fprint(self, "TC_ID : 40227 Verify Report view & update permissions.")
        self.edit_user_permission('Report', 'View & Update')
        nav_menu_main(self, 'Reports')
        fprint(self, 'User cannot create Report,only view/edit it.')
        fprint(self, 'Checking if user can view Report.')
        if waitfor(self, 5, By.XPATH, "(//span[contains(text(),'Title')])[2]", False):
            fprint(self, '[PASSED]- user can view Report.')
        else:
            fprint(self, "[Failed] - User cannot view report")
            failures.append("user cannot view report.")
        fprint(self, 'Checking if user cannot add report.')
        if waitfor(self, 5, By.XPATH, "//div[@class = 'cy-permission-disabled']/button[contains(text(),'Add')]", False):
            fprint(self, '[PASSED]- user cannot add reports.')
        else:
            fprint("[Failed]- user can add report.")
            failures.append("User can add report")
        fprint(self, 'Checking if user can edit Report.')
        waitfor(self, 5, By.XPATH, "//button[@data-testid='action']/i")
        ele = self.driver.find_element_by_xpath("//button[@data-testid='action']/i")
        self.driver.execute_script("arguments[0].scrollIntoView();", ele)
        self.driver.execute_script("arguments[0].click();", ele)
        if waitfor(self, 5, By.XPATH, "//*[contains(text(),'Edit')]", False):
            fprint(self, '[PASSED]- user can edit Report.')
        else:
            fprint(self, "[Failed]- user cannot edit report.")
            failures.append("user cannot edit report")
        self.assert_(failures == [], str(failures))
        fprint(self, '[PASSED]- View & Update permission for Report verified successfully!')

    def test_28_verify_disable_view_RSS_Feeds_permission(self):
        fprint(self, "TC_ID : 40228 Verify RSS Feeds view  permissions.")
        self.disable_view_permission("RSS Feeds")
        fprint(self, '[PASSED]- Disable view permission verified successfully!')

    def test_29_verify_ThreatMailbox_view_permission(self):
        failures = []
        fprint(self, "TC_ID : 40229 Verify ThreatMailbox view permissions.")
        self.edit_user_permission('Threat Mailbox', 'View')
        nav_menu_main(self, 'Threat Mailbox')
        fprint(self, 'User can only view Mailbox, not able to add/edit it.')
        fprint(self, 'Checking if user can view ThreatMailbox.')
        if waitfor(self, 5, By.XPATH, "//span[contains(text(),'Inbox')]", False):
            fprint(self, '[PASSED]- user can view Threat Mailbox.')
        else:
            fprint(self, "[Failed] - User cannot view Mailbox")
            failures.append("User cannot view Mailbox.")
        fprint(self, 'Checking if user cannot add Mailbox.')
        if waitfor(self, 5, By.XPATH, "//button[contains(text(),'Add New Account')]", False):
            self.fail("[Failed]- user can add Mailbox.")
        else:
            fprint(self, '[PASSED]- user cannot add Mailbox.')
        fprint(self, 'Checking if user cannot edit Mailbox.')
        waitfor(self, 5, By.XPATH, "//i[@class='cyicon-more-vertical']")
        ele = self.driver.find_element_by_xpath("//i[@class='cyicon-more-vertical']")
        self.driver.execute_script("arguments[0].scrollIntoView();", ele)
        self.driver.execute_script("arguments[0].click();", ele)
        if waitfor(self, 5, By.XPATH,
                   "//div[@class = 'cy-permission-disabled']//following::li[contains(text(),'Edit')]", False):
            fprint(self, '[PASSED]- user cannot edit Threat Mailbox.')
        else:
            fprint(self, "[Failed]- user can edit Mailbox.")
            failures.append("User can edit Mailbox.")
        self.assert_(failures == [], str(failures))
        fprint(self, '[PASSED]- View permission for Mailbox verified successfully!')

    def test_30_verify_ThreatMailbox_create_permissions(self):
        failures = []
        fprint(self, "TC_ID : 40230 Verify Threat Mailbox create permissions.")
        self.edit_user_permission('Threat Mailbox', 'Create')
        nav_menu_main(self, 'Threat Mailbox')
        fprint(self, 'User can only add Threat Mailbox, not able to view/edit it.')
        fprint(self, 'Checking if user can add Mailbox.')
        if waitfor(self, 5, By.XPATH, "//button[contains(text(),'Add New Account')]", False):
            fprint(self, '[PASSED]- user can add Threat mailbox.')
        else:
            fprint(self, "[Failed] - User cannot add Mailbox")
            failures.append("User cannot add Mailbox.")
        fprint(self, 'Checking if user cannot view Mailbox.')
        if verify_success(self, ""):
            fprint(self, '[PASSED]- user cannot view Mailbox.')
        else:
            fprint(self, "[Failed] - User can view Mailbox")
            self.fail("[FAILED]- user can view Mailbox.")
        fprint(self, 'Checking if user cannot edit Mailbox.')
        fprint(self, 'Checking if user cannot edit Mailbox.')
        waitfor(self, 5, By.XPATH, "//i[@class='cyicon-more-vertical']")
        ele = self.driver.find_element_by_xpath("//i[@class='cyicon-more-vertical']")
        self.driver.execute_script("arguments[0].scrollIntoView();", ele)
        self.driver.execute_script("arguments[0].click();", ele)
        if waitfor(self, 5, By.XPATH,
                   "//div[@class = 'cy-permission-disabled']//following::li[contains(text(),'Edit')]"):
            fprint(self, '[PASSED]- user cannot edit Threat Mailbox.')
        else:
            self.fail("[FAILED]- user can edit Mailbox.")
        fprint(self, '[PASSED]- Create permission for Mailbox verified successfully!')

    def test_31_verify_ThreatMailbox_view_Update_permissions(self):
        failures = []
        fprint(self, "TC_ID : 40231 Verify Mailbox view & update permissions.")
        self.edit_user_permission('Threat Mailbox', 'View & Update')
        nav_menu_main(self, 'Threat Mailbox')
        fprint(self, 'User cannot create Mailbox ,only view/edit it.')
        fprint(self, 'Checking if user can view Mailbox.')
        fprint(self, 'Checking if user can view ThreatMailbox.')
        if waitfor(self, 5, By.XPATH, "//span[contains(text(),'Inbox')]", False):
            fprint(self, '[PASSED]- user can view Threat Mailbox.')
        else:
            fprint(self, "[Failed] - User cannot view Mailbox")
            failures.append("User cannot view Mailbox")
        fprint(self, 'Checking if user cannot add Mailbox.')
        if waitfor(self, 5, By.XPATH, "//button[contains(text(),'Add New Account')]", False):
            fprint(self, "[Failed]- user can add Mailbox.")
            failures.append("User can add Mailbox")
        else:
            fprint(self, '[PASSED]- user cannot add Mailbox.')
        fprint(self, 'Checking if user can edit Mailbox.')
        waitfor(self, 5, By.XPATH, "//i[@class='cyicon-more-vertical']")
        ele = self.driver.find_element_by_xpath("//i[@class='cyicon-more-vertical']")
        self.driver.execute_script("arguments[0].scrollIntoView();", ele)
        self.driver.execute_script("arguments[0].click();", ele)
        if waitfor(self, 5, By.XPATH, "//li[contains(text(),'Edit')]", False):
            fprint(self, '[PASSED]- user can edit Threat Mailbox.')
        else:
            fprint(self, "[Failed]- user cannot edit Mailbox.")
            failures.append("User cannot edit Mailbox")
        self.assert_(failures == [], str(failures))
        fprint(self, '[PASSED]- View & Update permission for Mailbox verified successfully!')

    def test_32_verify_Twitter_disable_view_permissions(self):
        fprint(self, "TC_ID : 40232 Verify Twitter view permissions.")
        self.disable_view_permission("Twitter")
        fprint(self, '[PASSED]- Disable view permission verified successfully!')

    def test_33_verify_Notes_create_permission(self):
        fprint(self, "TC_ID : 40233 Verify Notes create permissions.")
        self.edit_user_permission('Notes', 'Create')
        nav_menu_main(self, 'Global Notes')
        fprint(self, 'User can only View and Add Notes, not able to edit it.')
        fprint(self, 'Checking if user can add Notes.')
        if waitfor(self, 5, By.XPATH, "//*[contains(text(),'Add Note')]", False):
            self.driver.find_element_by_xpath("//*[contains(text(),'Add Note')]").click()
            waitfor(self, 10, By.XPATH, "//textarea[@placeholder = 'Add your note']")
            self.driver.find_element_by_xpath("//textarea[@placeholder = 'Add your note']").send_keys(
                "permission_notes")
            waitfor(self, 10, By.XPATH, "//button[contains(text(),'Save')]")
            self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
            verify_success(self, "Note created successfully", 10)
            fprint(self, '[PASSED]- user can add Notes.')
        # fprint(self, 'Checking if user cannot view Notes.')
        # if waitfor(self, 5, By.XPATH, "//span[contains(text(),'Permission Denied')]", False):
        #     fprint(self, '[PASSED]- user cannot view Notes.')
        # else:
        #     fprint(self, "[Failed] - User can view Notes")
        #     failures.append("User can view Notes")
        # fprint(self, 'User cannot view notes , therefore unable to edit it.')

        self.driver.find_element_by_xpath("//input[@name='searchbar']").click()
        self.driver.find_element_by_xpath("//input[@name='searchbar']").send_keys("permission_notes")
        waitfor(self, 5, By.XPATH, "//pre[contains(text(),'permission_notes')]")
        self.driver.find_element_by_xpath("//pre[contains(text(),'permission_notes')]/parent::div//div[@data-testaction='dropdown-link']").click()
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'Edit')]/ancestor::div[@class='cy-permission-disabled']")
        fprint(self, '[PASSED]- Create permission for Notes verified successfully!')

    def test_34_verify_Notes_view_permission(self):
        failures = []
        fprint(self, "TC_ID : 40234 Verify Notes view permissions.")
        self.edit_user_permission('Notes', 'View')
        nav_menu_main(self, 'Global Notes')
        fprint(self, 'User can only view Notes, not able to create/edit it.')
        fprint(self, 'Checking if user can view Notes.')
        if waitfor(self, 5, By.XPATH, "//*[contains(text(),'permission_notes')]", False):
            fprint(self, '[PASSED]- user can view Notes.')
        else:
            fprint(self, "[Failed] - User cannot view Notes")
            failures.append("User cannot view Notes")
        fprint(self, 'Checking if user cannot add Notes.')
        if waitfor(self, 10, By.XPATH, "//div[@class = 'cy-permission-disabled']//span[contains(text(),'Add Note')]", False):
            fprint(self, "[Passed]- User cannot add notes")
        else:
            fprint(self, "[Failed]- User can add notes.")
            failures.append("User can add notes.")
        fprint(self, 'Checking if user cannot edit Notes.')
        if waitfor(self, 10, By.XPATH, "//div[@class = 'cy-permission-disabled']//span[contains(text(),'Edit')]", False):
            fprint(self, "[Passed]- User cannot edit notes.")
        else:
            fprint(self, "[Failed]- User can edit notes.")
            failures.append("User can edit notes.")
        self.assert_(failures == [], str(failures))
        fprint(self, '[PASSED]- View permission for Notes verified successfully!')

    def test_35_verify_Notes_View_Update_permission(self):
        failures = []
        fprint(self, "TC_ID : 40235 Verify Notes view & Update permissions.")
        self.edit_user_permission('Notes', 'View & Update')
        nav_menu_main(self, 'Global Notes')
        fprint(self, 'User can only view and edit Notes, not able to create it.')
        fprint(self, 'Checking if user can view Notes.')
        if waitfor(self, 5, By.XPATH, "//*[contains(text(),'permission_notes')]", False):
            fprint(self, '[PASSED]- user can view Notes.')
        else:
            fprint(self, "[Failed] - User cannot view Notes")
            failures.append("User cannot view Notes")
        fprint(self, 'Checking if user cannot add Notes.')
        if waitfor(self, 10, By.XPATH, "//div[@class = 'cy-permission-disabled']//span[contains(text(),'Add Note')]", False):
            fprint(self, "[Passed]- User cannot add notes")
        else:
            fprint(self, "[Failed]- User can add notes.")
            failures.append("User can add notes.")
        fprint(self, 'Checking if user can edit Notes.')
        if waitfor(self, 10, By.XPATH, "//span[contains(text(),'Edit')]", False):
            fprint(self, "[Passed]- User can edit notes.")
        else:
            fprint(self, "[Failed]- User cannot edit notes.")
            failures.append("User cannot edit notes.")
        self.assert_(failures == [], str(failures))
        fprint(self, '[PASSED]- View & update permission for Notes verified successfully!')

    def test_36_verify_Threat_Investigations_view_permission(self):
        fprint(self, "TC_ID : 40236 Verify Threat Investigations view permissions.")
        self.disable_view_permission("Threat Investigations")
        fprint(self, '[PASSED]- Disable view permission for Threat Investigations verified successfully!')

    def test_37_verify_disable_Encode_Decode_Base64_view_permission(self):
        fprint(self, "TC_ID : 40237 Verify Encode_Decode_Base64 view permissions.")
        self.disable_view_permission("Encode")
        fprint(self, '[PASSED]- Disable view permission for Encode_Decode_Base64 verified successfully!')

    def test_38_verify_disable_CVSS_calculator_view_permission(self):
        fprint(self, "TC_ID : 40238 Verify CVSS Calculator view permissions.")
        self.disable_view_permission("CVSS Calculator")
        fprint(self, '[PASSED]- Disable view permission for CVSS Calculator verified successfully!')

    def test_39_verify_disable_Fang_Defang_view_permission(self):
        fprint(self, "TC_ID : 40239 Verify Fang-Defang view permissions.")
        self.disable_view_permission("Fang")
        fprint(self, '[PASSED]- Disable view permission for Fang-Defang verified successfully!')

    def test_40_verify_disable_STIX_Conversion_view_permission(self):
        fprint(self, "TC_ID : 40240 Verify STIX Conversion view permissions.")
        self.disable_view_permission("STIX Conversion")
        fprint(self, '[PASSED]- Disable view permission for STIX Conversion verified successfully!')

    def test_41_verify_disable_Network_Utilities_view_permission(self):
        fprint(self, "TC_ID : 40237 Verify Network Utilities view permissions.")
        self.disable_view_permission("Network Utilities")
        fprint(self, '[PASSED]- Disable view permission for Network Utilities verified successfully!')

    def test_42_verify_Tasks_create_permission(self):
        fprint(self, "TC_ID : 40242 Verify Tasks create permissions.")
        self.edit_user_permission('Tasks', 'Create')
        nav_menu_main(self, 'Global Tasks')
        fprint(self, 'User can View and Add Tasks, not able to edit it.')
        fprint(self, 'Checking if user can add Tasks.')
        if waitfor(self, 5, By.XPATH, "//button[contains(text(),'Add Task')]", False):
            self.driver.find_element_by_xpath("//button[contains(text(),'Add Task')]").click()
            waitfor(self, 10, By.XPATH, "//textarea[@placeholder = 'Enter a task']")
            self.driver.find_element_by_xpath("//textarea[@placeholder = 'Enter a task']").send_keys(
                "user_permission_tasks")
            waitfor(self, 5, By.XPATH, "//i[contains(@class,'cyicon-user')]/parent::span[contains(@class,'cy-round-full')]")
            self.driver.find_element_by_xpath("//i[contains(@class,'cyicon-user')]/parent::span[contains(@class,'cy-round-full')]").click()
            waitfor(self, 5, By.XPATH, "//span[contains(text(),'Assign to Self')]")
            self.driver.find_element_by_xpath("//span[contains(text(),'Assign to Self')]").click()

            waitfor(self, 10, By.XPATH, "//span[contains(text(),'Save')]/parent::button")
            self.driver.find_element_by_xpath("//span[contains(text(),'Save')]/parent::button").click()
            # verify_success(self, "Task created successfully", 10)
            fprint(self, '[PASSED]- user can add Tasks.')
        # fprint(self, 'Checking if user cannot view Tasks.')
        # if waitfor(self, 5, By.XPATH, "//span[contains(text(),'Permission Denied')]", False):
        #     fprint(self, '[PASSED]- user cannot view Tasks.')
        # else:
        #     fprint(self, "[Failed] - User can view Tasks")
        #     failures.append("User can view Tasks")
        waitfor(self, 5, By.XPATH, "//pre[contains(text(),'user_permission_tasks')]")
        if waitfor(self, 2, By.XPATH, "//pre[contains(text(),'user_permission_tasks')]/parent::div/following-sibling::div//button", False):
            fprint(self, "[Failed] - Edit Action is visible, which should not")
            self.fail(msg="[Failed] - Edit Action is visible, which should not")
        else:
            fprint(self, "[Passed] - Edit Action is not visible")
        fprint(self, '[PASSED]- Create permission for Tasks verified successfully!')

    def test_43_verify_Tasks_view_permission(self):
        failures = []
        fprint(self, "TC_ID : 40243 Verify Tasks view permissions.")
        self.edit_user_permission('Tasks', 'View')
        nav_menu_main(self, 'Global Tasks')
        fprint(self, 'User can only view Tasks, not able to create/edit it.')
        fprint(self, 'Checking if user can view Tasks.')
        if waitfor(self, 5, By.XPATH, "//*[contains(text(),'user_permission_tasks')]", False):
            fprint(self, '[PASSED]- user can view Tasks.')
        else:
            fprint(self, "[Failed]- user cannot view Tasks.")
            failures.append("user cannot view Tasks")
        fprint(self, 'Checking if user cannot add Tasks.')
        if waitfor(self, 10, By.XPATH, "//div[@class = 'cy-permission-disabled']//button[contains(text(),'Add Task')]", False):
            fprint(self, "[PASSED]- User cannot add tasks")
        else:
            fprint(self, "[Failed]- User can add tasks.")
            failures.append("User can add tasks.")
        fprint(self, 'Checking if user cannot edit tasks.')
        if waitfor(self, 10, By.XPATH, "//li[contains(text(),'Edit')]", False):
            fprint(self, "[Failed]- User can edit tasks.")
            failures.append("User can edit tasks.")
        else:
            fprint(self, '[PASSED]- User cannot edit tasks.')
        self.assert_(failures == [], str(failures))
        fprint(self, '[PASSED]- View permission for tasks verified successfully!')

    def test_44_verify_Tasks_View_Update_permission(self):
        failures = []
        fprint(self, "TC_ID : 40244 Verify Tasks view & Update permissions.")
        self.edit_user_permission('Tasks', 'View & Update')
        nav_menu_main(self, 'Global Tasks')
        fprint(self, 'User can only view and edit Tasks, not able to create it.')
        fprint(self, 'Checking if user can view Tasks.')
        if waitfor(self, 5, By.XPATH, "//*[contains(text(),'user_permission_tasks')]", False):
            fprint(self, '[PASSED]- user can view Tasks.')
        else:
            fprint(self, "[Failed] - User cannot view Tasks")
            failures.append("User cannot view Tasks")
        fprint(self, 'Checking if user cannot add Tasks.')
        if waitfor(self, 10, By.XPATH, "//div[@class = 'cy-permission-disabled']//button[contains(text(),'Add Task')]", False):
            fprint(self, "[PASSED] User cannot add task.")
        else:
            fprint("[Failed] User can add task.")
            failures.append("User can add task.")
        fprint(self, 'Checking if user can edit tasks.')
        waitfor(self, 10, By.XPATH, "(//pre[contains(text(),'user_permission_tasks')]/following::div[@class='cy-popper-wrapper'])[1]")
        self.driver.find_element_by_xpath("(//pre[contains(text(),'user_permission_tasks')]/following::div[@class='cy-popper-wrapper'])[1]").click()
        if waitfor(self, 10, By.XPATH, "//li[contains(text(),'Edit')]", False):
            fprint(self, "[PASSED]- User can edit tasks.")
        else:
            fprint(self, "[Failed]- User cannot edit tasks.")
            failures.append("User cannot edit tasks")
        self.assert_(failures == [], str(failures))
        fprint(self, '[PASSED]- View & update permission for tasks verified successfully!')

    def test_45_verify_Tags_create_permission(self):
        fprint(self, "TC_ID : 40245 Verify Tags create permissions.")
        self.edit_user_permission('Tags', 'Create')
        nav_menu_main(self, 'Tags')
        fprint(self, 'User can only View and Add Tags, not able to edit it.')
        fprint(self, 'Checking if user can add Tags.')
        if waitfor(self, 5, By.XPATH, "//button[contains(text(),'Add')]", False):
            wait = WebDriverWait(self.driver, 10)
            ele = wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Add')]")))
            self.driver.execute_script("arguments[0].click();", ele)
            fprint(self, "[Passed]- Clicked on  Add Tag Button")
            waitfor(self, 5, By.XPATH, "//input[contains(@aria-placeholder,'Tag Name*')]")
            fprint(self, "[Passed] -Adding the tag name")
            self.driver.find_element_by_xpath("//input[contains(@aria-placeholder,'Tag Name*')]").send_keys('user_permission_tag')
            fprint(self, "[Passed] -Selecting the color for the tag")
            waitfor(self, 5, By.XPATH, "//p[contains(text(),'Pick a Color')]/parent::div/div/div[1]")
            self.driver.find_element_by_xpath("//p[contains(text(),'Pick a Color')]/parent::div/div/div[1]").click()
            self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
            fprint(self, "[Passed] - Clicked on Save")
            verify_success(self, "Tag created successfully")
            fprint(self, '[PASSED]- user can add Tags.')
        # if (waitfor(self, 5, By.XPATH, "//span[contains(text(),'Permission Denied')]", False)):
        #     fprint(self, '[PASSED]- user cannot view Tags.')
        # else:
        #     fprint(self, "[Failed] - User can view Tags")
        #     failures.append("User can view Tags")
        search(self, "user_permission_tag")
        waitfor(self, 5, By.XPATH, "(//span[@data-value='user_permission_tag'])[1]")
        element = self.driver.find_element_by_xpath("(//span[@data-value='user_permission_tag'])[1]")
        ActionChains(self.driver).move_to_element(element).perform()
        waitfor(self, 5, By.XPATH, "//button[@data-testid='action']")
        self.driver.find_element_by_xpath("//button[@data-testid='action']").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(),'Edit')]/ancestor::div[@class='cy-permission-disabled']")
        fprint(self, '[PASSED]- Create permission for Tags verified successfully!')

    def test_46_verify_Tags_view_permission(self):
        failures = []
        fprint(self, "TC_ID : 40246 Verify Tags view permissions.")
        self.edit_user_permission('Tags', 'View')
        nav_menu_main(self, 'Tags')
        fprint(self, 'User can only view Tags, not able to create/edit it.')
        fprint(self, 'Checking if user can view Tags.')
        search(self, 'user_permission_tag')
        if waitfor(self, 5, By.XPATH, "//*[contains(text(),'user_permission_tag')]", False):
            fprint(self, '[PASSED]- user can view Tags.')
        else:
            fprint(self, "[Failed]- user cannot view Tags.")
            failures.append("user cannot view Tags")
        fprint(self, 'Checking if user cannot add Tasks.')
        if (waitfor(self, 10, By.XPATH, "//div[@class = 'cy-permission-disabled']//button[contains(text(),'Add')]",
                    False)):
            fprint(self, "[PASSED]- User cannot add tags")
        else:
            fprint(self, "[Failed]- User can add tasks.")
            failures.append("User can add tasks.")
        fprint(self, 'Checking if user cannot edit tags.')
        if waitfor(self, 10, By.XPATH, "//li[contains(text(),'Edit')]", False):
            fprint(self, "[Failed]- User can edit tags.")
            failures.append("User can edit tags.")
        else:
            fprint(self, '[PASSED]- User cannot edit tags.')
        self.assert_(failures == [], str(failures))
        fprint(self, '[PASSED]- View permission for tags verified successfully!')

    def test_47_verify_Tags_View_Update_permission(self):
        failures = []
        fprint(self, "TC_ID : 40247 Verify Tags view & Update permissions.")
        self.edit_user_permission('Tags', 'View & Update')
        nav_menu_main(self, 'Tags')
        fprint(self, 'User can only view and edit Tags, not able to create it.')
        fprint(self, 'Checking if user can view Tags.')
        search(self, 'user_permission_tag')
        if waitfor(self, 5, By.XPATH, "//*[contains(text(),'user_permission_tag')]", False):
            fprint(self, '[PASSED]- user can view Tags.')
        else:
            fprint(self, "[Failed] - User cannot view Tags")
            failures.append("User cannot view Tags")
        fprint(self, 'Checking if user cannot add Tags.')
        if waitfor(self, 10, By.XPATH, "//div[@class = 'cy-permission-disabled']//button[contains(text(),'Add')]", False):
            fprint(self, "[PASSED] User cannot add tags.")
        else:
            fprint(self, "[Failed] User can add tag.")
            failures.append("User can add tag.")
        fprint(self, 'Checking if user can edit tag.')
        search(self, 'user_permission_tag')
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'user_permission_tag')]//following::button[@data-testid='action'])[1]")
        ele = self.driver.find_element_by_xpath("(//span[contains(text(),'user_permission_tag')]//following::button[@data-testid='action'])[1]")
        self.driver.execute_script("arguments[0].click();", ele)
        if waitfor(self, 10, By.XPATH, "//span[contains(text(),'user_permission_tag')]//following::div[contains(text(),'Edit')]", False):
            fprint(self, "[PASSED]- User can edit tags.")
        else:
            fprint(self, "[Failed]- User cannot edit tags.")
            failures.append("User cannot edit tags")
        self.assert_(failures == [], str(failures))
        fprint(self, '[PASSED]- View & update permission for tags verified successfully!')

    def test_48_verify_Attack_Navigator_create_permission(self):
        failures = []
        fprint(self, "TC_ID : 40248 Verify Attack Navigator create permissions.")
        self.edit_user_permission('ATT&CK Navigator', 'Create')
        nav_menu_main(self, 'ATT&CK Navigator')
        fprint(self, 'User can only view and add ATT&CK Navigator, not able to edit it.')
        fprint(self, 'Checking if user can add new MITRE layer')
        waitfor(self, 20, By.XPATH, "//span[contains(@class,'cyicon-add')]")
        self.driver.find_element_by_xpath("//span[contains(@class,'cyicon-add')]").click()
        if waitfor(self, 20, By.XPATH, "//li[contains(text(), 'New MITRE Layer')]", False):
            self.driver.find_element_by_xpath("//li[contains(text(), 'New MITRE Layer')]").click()
            fprint(self, "Clicking on Save Button")
            waitfor(self, 5, By.XPATH, "//button[@data-testaction='save-button']")
            self.driver.find_element_by_xpath("//button[@data-testaction='save-button']").click()
            verify_success(self, "Layer created successfully")
        else:
            fprint(self, "[Failed]- Unable to add MITRE Layer.")
            failures.append("User cannot add MITRE Layer")
        fprint(self, 'Checking if user can ADD new Custom Base layer')
        waitfor(self, 20, By.XPATH, "(//span[contains(@class,'cyicon-add')])[1]")
        self.driver.find_element_by_xpath("(//span[contains(@class,'cyicon-add')])[1]").click()
        if waitfor(self, 10, By.XPATH, "//li[contains(text(), 'New Custom Base Layer')]", False):
            self.driver.find_element_by_xpath("//li[contains(text(), 'New Custom Base Layer')]").click()
        else:
            fprint(self, "[Failed]- Unable to add Custom Base Layer.")
            failures.append("User cannot add Custom Base Layer")
        fprint(self, "Click on Save Button")
        self.driver.find_element_by_xpath("(//button[contains(text(),'Save')])[1]").click()
        fprint(self, 'Checking if user can add Custom Technique')
        if waitfor(self, 5, By.XPATH, "//button[@data-testaction='customTechniques-button']", False):
            self.driver.find_element_by_xpath("//button[@data-testaction='customTechniques-button']").click()
            waitfor(self, 20, By.XPATH, "//div[contains(text(),'Custom Technique')]")
            fprint(self, "Enterprise - ATT&CK Navigator_Add Custom technique slider is opened")
            self.driver.find_element_by_xpath("//input[@name='name']").click()
            self.driver.find_element_by_xpath("//input[@name='name']").send_keys('Userpermission')
            self.driver.find_element_by_xpath("//div[@data-testid='tactics']").click()
            sleep(2)
            waitfor(self, 20, By.XPATH, "//div[contains(text(),'Reconnaissance')]")
            self.driver.find_element_by_xpath("//div[contains(text(),'Reconnaissance')] ").click()
            self.driver.find_element_by_xpath("//button[@data-testaction='submit']").click()
            verify_success(self, "Custom Technique created successfully")
        else:
            fprint(self, "[Failed] - User cannot add Custom Technique.")
            failures.append("User cannot add Custom Technique.")
        fprint(self, "Checking if user is unable to edit it.")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Custom Base Layer')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Custom Base Layer')]").click()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Userpermission')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Userpermission')]").click()
        if waitfor(self, 10, By.XPATH, "//div[@class='cy-permission-disabled']//button[contains(text(),'Edit')]", False):
            fprint(self, "[PASSED]- User cannot edit technique.")
        else:
            fprint(self, "[Failed]- User can edit Custom Technique.")
            failures.append("User can edit Custom Technique.")
        self.assert_(failures == [], str(failures))
        fprint(self, '[PASSED]- Create permission for Att&ck Navigator verified successfully!')

    def test_49_verify_Attack_Navigator_View_Update_permission(self):
        failures = []
        fprint(self, "TC_ID : 40249 Verify Att&ck Navigator view & Update permissions.")
        self.edit_user_permission('ATT&CK Navigator', 'View & Update')
        nav_menu_main(self, 'ATT&CK Navigator')
        fprint(self, 'User can only view and edit, not able to create it.')
        fprint(self, 'Checking if user can view AND EDIT technique.')
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Custom Base Layer')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Custom Base Layer')]").click()
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Userpermission')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Userpermission')]").click()
        if waitfor(self, 10, By.XPATH, "//button[contains(text(),'Edit')]", False):
            self.driver.find_element_by_xpath("//button[contains(text(),'Edit')]").click()
            waitfor(self, 10, By.XPATH, "//input[@name='name']")
            self.driver.find_element_by_xpath("//input[@name='name']").click()
            self.driver.find_element_by_xpath("//input[@name='name']").send_keys('_edit')
            self.driver.find_element_by_xpath("(//button[contains(text(),'Update')])[1]").click()
            verify_success(self, "updated successfully.")
            fprint(self, "[PASSED]- User can view and edit technique.")
        else:
            fprint(self, "[Failed]- User cannot edit Custom Technique.")
            failures.append("User cannot edit Custom Technique.")
        self.assert_(failures == [], str(failures))
        fprint(self, '[PASSED]- View & update permission for Attack Navigator verified successfully!')


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
