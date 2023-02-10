from lib.ui.nav_app import *
from lib.common_functions import *
import tkinter as tk # it is imported to copy the value from clipboard
from selenium.webdriver.common.by import By
from lib.api.common_utilities import *

CSAP_USERNAME = "jeet.raikar@cyware.com"
CSAP_PASSWORD = "Jet@cware123"
CFTR_USERNAME = "system@default.tld"
CFTR_PASSWORD = "6*HT!99052y"


def launch_csap(self):
    """
        Function to launch CSAP
    """
    self.driver.maximize_window()
    self.driver.execute_script("window.open('https://csaptest.cywarestg.com/dashboard/situational-awareness');")
    fprint(self, "Opening Up CSAP")
    handles = self.driver.window_handles
    self.driver.switch_to.window(handles[1])
    fprint(self, "Filling in Username in CSAP")
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Enter your email address']")
    self.driver.find_element_by_xpath("//input[@placeholder='Enter your email address']").send_keys(CSAP_USERNAME)
    fprint(self, "Filling in Password in CSAP")
    waitfor(self, 20, By.XPATH, "//input[@type='password']")
    self.driver.find_element_by_xpath("//input[@type='password']").send_keys(CSAP_PASSWORD)
    fprint(self, "Clicking on Login")
    waitfor(self, 20, By.XPATH, "//button[span[text()='Login']]")
    self.driver.find_element_by_xpath("//button[span[text()='Login']]").click()
    waitfor(self, 60, By.XPATH, "//a[contains(@class,'csap-logo')]")
    fprint(self, "Logged into CSAP Successfully, Logo visible")
    sleep(5)    # needed for all elements to be interactable


def create_csap_creds(self):
    """
        Function to create CSAP creds to be used in CTIX
    """
    fprint(self, "Clicking on the Slider Menu")
    sleep(5)    # needed
    waitfor(self, 20, By.XPATH, "//a[@cy-test-id='user-mngmnt-menu']")
    self.driver.find_element_by_xpath("//a[@cy-test-id='user-mngmnt-menu']").click()
    fprint(self, "Clicking on integrations")
    waitfor(self, 20, By.XPATH, "//a/span[text()='Integrations']")
    sleep(2)
    self.driver.find_element_by_xpath("//a/span[text()='Integrations']").click()
    fprint(self, "Clicking on CSAP Integrations")
    waitfor(self, 20, By.XPATH, "//div[text()='CSAP INTEGRATIONS']")
    self.driver.find_element_by_xpath("//div[text()='CSAP INTEGRATIONS']").click()
    fprint(self, "Selecting OpenAPI Credentials")
    waitfor(self, 20, By.XPATH, "//div[span[text()='Open API Credentials']]")
    self.driver.find_element_by_xpath("//div[span[text()='Open API Credentials']]").click()
    fprint(self, "Clicking on Generate API Credentials")
    waitfor(self, 20, By.XPATH, "//button/span[text()='Generate API Credentials']")
    self.driver.find_element_by_xpath("//button/span[text()='Generate API Credentials']").click()
    waitfor(self, 20, By.XPATH, "//div/input[@placeholder='App Name *']")
    set_value('csap_cred_title', "ctix_"+uniquestr[-4:])
    _csap_cred_title = get_value("csap_cred_title")
    sleep(2)    # waiting for form to be loaded completely
    fprint(self, f"Setting openAPI cred title to {_csap_cred_title}")
    self.driver.find_element_by_xpath("//div/input[@placeholder='App Name *']").send_keys(_csap_cred_title)
    waitfor(self, 20, By.XPATH, "//button[span[text()='Generate']]")
    fprint(self, "Clicking on generate")
    self.driver.find_element_by_xpath("//button[span[text()='Generate']]").click()
    waitfor(self, 20, By.XPATH, "//div[text()='Access ID']/following-sibling::div")
    csap_access_id = self.driver.find_element_by_xpath("//div[text()='Access ID']/following-sibling::div").text
    csap_secret_key = self.driver.find_element_by_xpath("//div[text()='Secret Key']/following-sibling::div").text
    csap_endpoint = self.driver.find_element_by_xpath("//div[text()='End Point']/following-sibling::div").text
    set_credentials("csap", "base_url", csap_endpoint)
    set_credentials("csap", "secret_key", csap_secret_key)
    set_credentials("csap", "access_id", csap_access_id)
    return [csap_access_id, csap_secret_key, csap_endpoint]


def create_category(self, _category_name):
    waitfor(self, 20, By.XPATH, "//a[@cy-test-id='user-mngmnt-menu']")
    self.driver.find_element_by_xpath("//a[@cy-test-id='user-mngmnt-menu']").click()
    fprint(self, "Selecting Settings from the slidermenu")
    waitfor(self, 20, By.XPATH, "//a/span[text()='Settings']")
    sleep(2) # required
    self.driver.find_element_by_xpath("//a/span[text()='Settings']").click()
    waitfor(self, 20, By.XPATH, "//div[div[text()='Search']]//input")
    fprint(self, "Searching for Category")
    self.driver.find_element_by_xpath("//div[text()='Search']").click()
    self.driver.find_element_by_xpath("//div[div[text()='Search']]//input").send_keys("Category")
    waitfor(self, 20, By.XPATH, "//li[normalize-space(text())='Category']")
    sleep(1) # required
    self.driver.find_element_by_xpath("//li[normalize-space(text())='Category']").click()
    sleep(2)
    fprint(self, f"Searching if {_category_name} name already exists")
    self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys(_category_name)
    self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys(Keys.ENTER)
    if waitfor(self, 10, By.XPATH, "//span[@title='"+_category_name+"']", False):
        fprint(self, f"Expected Category {_category_name} already exists")
        return
    fprint(self, f"Clicking on create as {_category_name} not found")
    self.driver.find_element_by_xpath("//button[span[text()='Create']]").click()
    fprint(self, f"Adding new category with name {_category_name}")
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Category Name *']")
    sleep(2)
    self.driver.find_element_by_xpath("//input[@placeholder='Category Name *']").send_keys(_category_name)
    waitfor(self, 20, By.XPATH, "(//div[contains(@class, 'csap-table__row')][div/div/p/span[@title='Threat Indicators']]/div//button)[1]")
    fprint(self, "Enabling threat indicators")
    self.driver.find_element_by_xpath("(//div[contains(@class, 'csap-table__row')][div/div/p"
                                      "/span[@title='Threat Indicators']]/div//button)[1]").click()
    self.driver.find_element_by_xpath("//button[@type='primary'][span[text()='Create']]").click()
    fprint(self, "Clicked on create successfully")


def create_receipent_group(self, _recipient_grp_name):
    waitfor(self, 20, By.XPATH, "//a[@cy-test-id='user-mngmnt-menu']")
    self.driver.find_element_by_xpath("//a[@cy-test-id='user-mngmnt-menu']").click()
    fprint(self, "Clicking on settings from the slider menu")
    waitfor(self, 20, By.XPATH, "//a/span[text()='Settings']")
    sleep(2)    # required
    self.driver.find_element_by_xpath("//a/span[text()='Settings']").click()
    fprint(self, "Searching for recipient group")
    waitfor(self, 20, By.XPATH, "//div[div[text()='Search']]//input")
    self.driver.find_element_by_xpath("//div[text()='Search']").click()
    self.driver.find_element_by_xpath("//div[div[text()='Search']]//input").send_keys("Recipient Group")
    waitfor(self, 20, By.XPATH, "//li[normalize-space(text())='Recipient Group']")
    sleep(2)    # required
    self.driver.find_element_by_xpath("//li[normalize-space(text())='Recipient Group']").click()
    sleep(2)    # required
    self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys(_recipient_grp_name)
    self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys(Keys.ENTER)
    if waitfor(self, 10, By.XPATH, "//span[@title='"+_recipient_grp_name+"']", False):
        fprint(self, f"Expected Category {_recipient_grp_name} already exists")
        return
    fprint(self, f"Creating new recipient group as {_recipient_grp_name} not found")
    self.driver.find_element_by_xpath("//button[span[text()='Create']]").click()
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Group Name *']")
    self.driver.find_element_by_xpath("//input[@placeholder='Group Name *']").\
        send_keys(_recipient_grp_name)
    waitfor(self, 20, By.XPATH, "//textarea[@placeholder='Group Description *']")
    self.driver.find_element_by_xpath("//textarea[@placeholder='Group Description *']").\
        send_keys("CTIX_CSAP connection for CSAP Alerts")
    waitfor(self, 5, By.XPATH, "//div[div[text()='Group Type']]")
    self.driver.find_element_by_xpath("//div[div[text()='Group Type']]").click()
    sleep(2)    # required
    self.driver.find_element_by_xpath("//li[text()='RED']").click()
    fprint(self, "Clicking on create")
    self.driver.find_element_by_xpath("//button[@type='primary'][span[text()='Create']]").click()


def add_csap_account(self, **kwargs):
    """
        Function to add CSAP account in CTIX
        kwargs:
            account_name : name of CSAP account to be configured
            csap_creds: Credentials to configure CSAP account
    """
    _new_creds = get_credentials("csap")
    account_name = kwargs.get("instamce_name", "csap")
    fprint(self, 'Searching for CSAP')
    search(self, "CSAP")
    waitfor(self, 20, By.XPATH, "//div[p[contains(text(), 'CSAP')]]")
    fprint(self, 'Clicking on CSAP')
    self.driver.find_element_by_xpath("//div[p[contains(text(), 'CSAP')]]").click()
    if waitfor(self, 8, By.XPATH, "//button[contains(text(), 'DONE')]", False):
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'DONE')]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(), 'OK, GOT IT')]").click()
    sleep(2)
    try:
        fprint(self, 'Clicking on add Account')
        waitfor(self, 20, By.XPATH, "//button[span[contains(text(), 'Add Account')]]")
        self.driver.find_element_by_xpath("//button[span[contains(text(), 'Add Account')]]").click()
    except:
        fprint(self, "Credential Slider is already visible...")
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Account Name*']")
    sleep(2)
    fprint(self, "Filling in account name")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Account Name*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Account Name*']").send_keys(account_name)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Base Url*']")
    fprint(self, "FIlling in Base Url")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").click()
    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']"))
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").send_keys(_new_creds["base_url"])
    fprint(self, 'Filling in Access ID*')
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Access ID*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Access ID*']").send_keys(_new_creds["access_id"])
    fprint(self, 'Filling in Secret Key*')
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Secret Key*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Secret Key*']").send_keys(_new_creds["secret_key"])
    fprint(self, "Clicking on save")
    if waitfor(self, 5, By.XPATH, "//span[span[normalize-space(text())='Verify SSL']]/preceding-sibling::span"
                                  "/input[@value='true']", False):
        self.driver.find_element_by_xpath("//span[span[normalize-space(text())='Verify SSL']]").click()
    self.driver.find_element_by_xpath("//button[contains(text(), 'Save')]").click()
    try:
        verify_success(self, 'Account created successfully')
    except:
        self.driver.find_element_by_xpath("//span[span[normalize-space(text())='Verify SSL']]").click()
        self.driver.find_element_by_xpath("//button[contains(text(), 'Save')]").click()
        verify_success(self, 'Account created successfully')
    fprint(self, "CSAP Account configured successfully")


def add_account(self, product_name, credentials):
    search(self, product_name)
    waitfor(self, 20, By.XPATH, "//div[p[contains(text(), '"+product_name+"')]]")
    fprint(self, 'Product visible clicking on it - '+product_name)
    self.driver.find_element_by_xpath("//div[p[contains(text(), '"+product_name+"')]]").click()
    if waitfor(self, 8, By.XPATH, "//button[contains(text(), 'DONE')]", False):
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'DONE')]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(), 'OK, GOT IT')]").click()
    sleep(1)
    try:
        fprint(self, 'Clicking on the Add Account button')
        waitfor(self, 20, By.XPATH, "//button[span[contains(text(), 'Add Account')]]")
        self.driver.find_element_by_xpath("//button[span[contains(text(), 'Add Account')]]").click()
    except:
        fprint(self, "Credential Slider is already visible...")
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Account Name*']")
    fprint(self, "Filling in account name")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Account Name*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Account Name*']").send_keys(credentials[0])
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Base Url*']")
    fprint(self, "FIlling in Base Url")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").click()
    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']"))
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").send_keys(credentials[1]+"/soarapi/openapi/")
    fprint(self, 'Filling in Access ID*')
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Access ID*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Access ID*']").send_keys(credentials[2])
    fprint(self, 'Filling in Secret Key*')
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Secret Key*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Secret Key*']").send_keys(credentials[3])
    fprint(self, "Clicking on Save button")
    self.driver.find_element_by_xpath("//button[contains(text(), 'Save')]").click()
    verify_success(self, "Account created successfully")


def validate_csap_intel(self, intel, status):
    """
        Validate if the intel is visible in CSAP
        params:
            intel: IOC that is semnt to CSAP
            status: status of alert send draft/published
    """
    waitfor(self, 20, By.XPATH, "//div[@class='clear-icon']")
    fprint(self, "Clicking on filters")
    self.driver.find_element_by_xpath("//div[@class='clear-icon']").click()
    sleep(1)    # required
    if not waitfor(self, 5, By.XPATH, "//input[@id='main-input']", False):
        self.driver.find_element_by_xpath("//div[@id='cy-test__filter']").click()
    fprint(self, f"searching for {intel}")
    self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys(intel)
    self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys(Keys.ENTER)
    fprint(self, f"Validating if {intel} is received as {status}")
    waitfor(self, 20, By.XPATH, f"//td[div/div[contains(text(),'{intel}')]]/following-sibling::td[div//span[normalize-space(text())='{status.upper()}']]")
    waitfor(self, 20, By.XPATH, f"//td[div//span[normalize-space(text())='{status.upper()}']]/preceding-sibling::td[div/div[contains(text(),'{intel}')]]")
    self.driver.find_element_by_xpath(f"//td[div//span[normalize-space(text())='{status.upper()}']]/preceding-sibling::td[div/div[contains(text(),'{intel}')]]").click()


def cyware_product_login(self, credentials):
    """
        Function to login in the CSOL
    """
    waitfor(self, 60, By.XPATH, "//input[@aria-placeholder='Enter your e-mail address']")
    fprint(self, "Login page of is visible, entering credentials")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter your e-mail address']").send_keys(credentials[0])
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter your password']").send_keys(credentials[1])
    self.driver.find_element_by_xpath("//button[contains(text(),'Login')]").click()
    fprint(self, "Clicked on the Login button")
    waitfor(self, 60, By.XPATH, "//i[contains(@class,'cyicon-menu')]/parent::div")
    fprint(self, "Logged into Successfully")


def csol_add_label(self, label_name):
    """
        Function to add new labels into CSOL
        params:
            label_name: Name of the label to be added
    """
    waitfor(self, 20, By.XPATH, "//button[i[contains(@class,'icon-plus')]]")
    sleep(2)
    self.driver.find_element_by_xpath("//button[i[contains(@class,'icon-plus')]]").click()
    sleep(2)
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Enter Label Name']")
    self.driver.find_element_by_xpath("//input[@placeholder='Enter Label Name']").send_keys("rule_"+label_name)
    self.driver.find_element_by_xpath("//button[text()='Create']").click()
    waitfor(self, 20, By.XPATH, "//div[@class='el-notification__closeBtn el-icon-close']")
    self.driver.find_element_by_xpath("//div[@class='el-notification__closeBtn el-icon-close']").click()


def csol_add_event(self, event_name):
    """
        Function to add new events into CSOL
        params:
            event_name: Name of the event to be added
    """
    waitfor(self, 20, By.XPATH, "//button[i[contains(@class,'icon-plus')]]")
    self.driver.find_element_by_xpath("//button[i[contains(@class,'icon-plus')]]").click()
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Enter Event Source App']")
    self.driver.find_element_by_xpath("//input[@placeholder='Enter Event Source App']").send_keys("CTIX")
    waitfor(self, 5, By.XPATH, "//input[@placeholder='Enter Source Event Type']")
    self.driver.find_element_by_xpath("//input[@placeholder='Enter Source Event Type']").send_keys("RULE_"+event_name)
    waitfor(self, 5, By.XPATH, "//div[@name='labels' and contains(@class, 'cy-wrapper')]")
    self.driver.find_element_by_xpath("//div[@name='labels' and contains(@class, 'cy-wrapper')]").click()
    waitfor(self, 5, By.XPATH, "//div[@name='labels']//input[@placeholder='Search ...']")
    self.driver.find_element_by_xpath("//div[@name='labels']//input[@placeholder='Search ...']").send_keys("rule_"+event_name)
    waitfor(self, 20, By.XPATH, f"//li[div//div[text()='rule_{event_name}']]")
    self.driver.find_element_by_xpath(f"//li[div//div[text()='rule_{event_name}']]").click()
    self.driver.find_element_by_xpath("//button[text()='Create']").click()
    waitfor(self, 20, By.XPATH, "//div[@class='el-notification__closeBtn el-icon-close']")
    self.driver.find_element_by_xpath("//div[@class='el-notification__closeBtn el-icon-close']").click()

def select_expiration_date(self):
    """
    Function to select the expiration date of next year
    """
    waitfor(self, 10, By.XPATH, "//button[@aria-label ='Next Year']")
    self.driver.find_element_by_xpath("//button[@aria-label ='Next Year']").click()
    fprint(self, "[Passed]-clicked on the next year")
    waitfor(self, 10, By.XPATH, "//span[contains(text(),'31')]/ancestor::td[@class='available']")
    self.driver.find_element_by_xpath("//span[contains(text(),'31')]/ancestor::td[@class='available']").click()
    waitfor(self, 10, By.XPATH, "//button//span[contains(text(),'OK')]")
    self.driver.find_element_by_xpath("//button//span[contains(text(),'OK')]").click()
    waitfor(self, 10, By.XPATH, "//div[contains(text(),'Associated User *')]")


def launch_cftr(self):
    """
    Test case to launch te cftr product
    """
    self.driver.maximize_window()
    self.driver.execute_script("window.open('https://alpha.cywaredev.com/cftr/home');")
    fprint(self, "Opening Up CFTR")
    handles = self.driver.window_handles
    self.driver.switch_to.window(handles[1])
    fprint(self, "Filling in Username in CFTR")
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Enter your e-mail address']")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter your e-mail address']").send_keys(CFTR_USERNAME)
    fprint(self, "Filling in Password in CSOL")
    waitfor(self, 20, By.XPATH, "//input[@type='password']")
    self.driver.find_element_by_xpath("//input[@type='password']").send_keys(CFTR_PASSWORD)
    fprint(self, "Clicking on Login")
    waitfor(self, 20, By.XPATH, "//button[contains(text(),'Login')]")
    self.driver.find_element_by_xpath("//button[contains(text(),'Login')]").click()
    waitfor(self, 20, By.XPATH, "(//a[contains(@class,'router-link-active')])[1]")
    fprint(self, "Logged into CSAP Successfully, Logo visible")
    sleep(5)  # needed for all elements to be interactable

def create_cftr_creds(self):
    """
    Functions to generate the creds from the cftr side
    """
    launch_cftr(self)
    waitfor(self, 20, By.XPATH, "//i[@class='icon icon-admin-panel']")
    self.driver.find_element_by_xpath("//i[@class='icon icon-admin-panel']").click()
    waitfor(self, 20, By.XPATH, "//div[contains(text(),'Admin Panel')]")
    waitfor(self, 20, By.XPATH, "//div[contains(text(),'Open APIs')]")
    self.driver.find_element_by_xpath("//div[contains(text(),'Open APIs')]").click()
    waitfor(self, 10, By.XPATH, "//div[contains(text(),'Add New API')]")
    self.driver.find_element_by_xpath("//div[contains(text(),'Add New API')]").click()
    waitfor(self, 10, By.XPATH, "//span[contains(text(),'Create API')]")
    self.driver.find_element_by_xpath("//input[@placeholder='API Title *']").send_keys("ctix-integration")
    self.driver.find_element_by_xpath("//textarea[@placeholder='API Description']").send_keys("Creds-generate-for-ctix")
    self.driver.find_element_by_xpath("//input[@placeholder='API Expiration Date*']").click()
    select_expiration_date(self)
    self.driver.find_element_by_xpath("//span[contains(@class,'cyicon-chevron-down')]").click()
    waitfor(self, 10, By.XPATH, "//div[contains(text(),'System Default')]")
    self.driver.find_element_by_xpath("//div[contains(text(),'System Default')]").click()
    waitfor(self, 10, By.XPATH, "//button[contains(text(),'Save')]")
    self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
    waitfor(self, 20, By.XPATH, "//span[contains(text(),'Credentials')]")
    self.driver.find_element_by_xpath("(//span[@data-original-title='Copy'])[1]").click()
    root = tk.Tk() # using to copy the value from the clipboard
    cftr_api_url = root.clipboard_get()# getting the value from clipboard
    self.driver.find_element_by_xpath("(//span[@data-original-title='Copy'])[2]").click()
    cftr_secret_key = root.clipboard_get()
    self.driver.find_element_by_xpath("(//span[@data-original-title='Copy'])[3]").click()
    cftr_access_id = root.clipboard_get()
    print(cftr_api_url)
    print(cftr_secret_key)
    print(cftr_access_id)
    set_credentials("cftr", "api_url", cftr_api_url)
    set_credentials("cftr", "secret_key", cftr_secret_key)
    set_credentials("cftr", "access_id", cftr_access_id)
    self.driver.find_element_by_xpath("(//i[contains(@class, 'icon icon-close')])[3]").click()

# def add_ctix_to_cftr(self):
#     """
#     utility function to add the ctix creds on the cftr side
#     """
#     launch_cftr(self)
#     waitfor(self, 20, By.XPATH, "//i[@class='icon icon-admin-panel']")
#     self.driver.find_element_by_xpath("//i[@class='icon icon-admin-panel']").click()
#     waitfor(self, 20, By.XPATH, "//div[contains(text(),'Admin Panel')]")
#     waitfor(self, 20, By.XPATH, "//div[contains(text(),'Configurations')]")
#     self.driver.find_element_by_xpath("//div[contains(text(),'Configurations')]").click()
#     waitfor(self, 20, By.XPATH, "//div[contains(text(),'Integration')]")
#     self.driver.find_element_by_xpath("//div[contains(text(),'Integration')]").click()
#     waitfor(self, 20, By.XPATH, "//div[contains(text(),'CTIX')]")
#     self.driver.find_element_by_xpath("//div[contains(text(),'CTIX')]").click()
#     waitfor(self, 20, By.XPATH, "(//button[contains(text(),'Edit')])[1]")
#     self.driver.find_element_by_xpath("(//button[contains(text(),'Edit')])[1]").click()
#     waitfor(self, 10, By.XPATH, "(//button[contains(text(),'Save')])[1]")
#     self.driver.find_element_by_xpath("//input[@aria-placeholder='Base URL *']").clear()
#     self.driver.find_element_by_xpath("//input[@aria-placeholder='Base URL *']").send_keys(base_url)
#     self.driver.find_element_by_xpath("//input[@aria-placeholder='Access ID *']").clear()
#     self.driver.find_element_by_xpath("//input[@aria-placeholder='Access ID *']").send_keys(access_id)
#     self.driver.find_element_by_xpath("//input[@aria-placeholder='Secret Key *']").clear()
#     self.driver.find_element_by_xpath("//input[@aria-placeholder='Secret Key *']").send_keys(secret_key)
#     self.driver.find_element_by_xpath("(//button[contains(text(),'Save')])[1]").click()
#     waitfor(self, 20, By.XPATH, "//div[contains(text(),'Are you sure you want to save configuration?')]")
#     self.driver.find_element_by_xpath("//button[contains(text(),'Yes, Save')]").click()
#     verify_success(self, "Configuration updated successfully")

def csap_add_ctix_integration(self):
    """
        Function to add CTIX integration in CSAP
    """
    launch_csap(self)
    self.driver.get("https://csaptest.cyware.com/dashboard/orchestration/ctix-integration")
    waitfor(self, 20, By.XPATH, "//button[span[text()='Edit Credentials']]")
    self.driver.find_element_by_xpath("//button[span[text()='Edit Credentials']]").click()
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Access ID *']")
    clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Access ID *']"))
    self.driver.find_element_by_xpath("//input[@placeholder='Access ID *']").send_keys(access_id)
    clear_field(self.driver.find_element_by_xpath('//input[@placeholder="Secret Key *"]'))
    self.driver.find_element_by_xpath("//input[@placeholder='Secret Key *']").send_keys(secret_key)
    clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Endpoint *']"))
    self.driver.find_element_by_xpath("//input[@placeholder='Endpoint *']").send_keys(base_url)
    self.driver.find_element_by_xpath("//button[span[text()='Update']]").click()
    sleep(5)


def create_new_csap_alert(self, title, summary, category, recipient, ioc_body, tlp):
    """
        Function to create new alert in CSAP
    """
    waitfor(self, 20, By.XPATH, "//div[normalize-space(text())='Alerts']")
    self.driver.find_element_by_xpath("//div[normalize-space(text())='Alerts']").click()
    sleep(2)  # required
    self.driver.find_element_by_xpath("//button[span[text()='Create']]").click()
    waitfor(self, 10, By.XPATH, "//li[@role='menuitem' and normalize-space(text())='New Alert']")
    self.driver.find_element_by_xpath("//li[@role='menuitem' and normalize-space(text())='New Alert']").click()
    waitfor(self, 20, By.XPATH, "//h1[normalize-space(text())='Create Alert']")
    self.driver.find_element_by_xpath("//input[@placeholder='Title *']").send_keys(title)
    _summary = self.driver.find_element_by_xpath("//span[text()='Summary *']/preceding-sibling::div/p")
    self.driver.execute_script("arguments[0].textContent = arguments[1];", _summary, summary)
    _summary.click()
    sleep(2)
    self.driver.find_element_by_xpath("//div[text()='Category *']").click()
    sleep(2)
    self.driver.find_element_by_xpath("//div[text()='Category *']/following-sibling::div//input").send_keys(category)
    waitfor(self, 20, By.XPATH, f"//div[text()='{category}']")
    self.driver.find_element_by_xpath(f"//div[text()='{category}']").click()
    self.driver.find_element_by_xpath("//div[div[text()='TLP *']]").click()
    sleep(1)    # required
    self.driver.find_element_by_xpath(f"//li[text()='{tlp.upper()}']").click()
    self.driver.find_element_by_xpath("//button[div/div/span[text()='Indicators']]").click()
    _ioc_body = self.driver.find_element_by_xpath("//span[text()='Threat Indicator']/preceding-sibling::div/p")
    waitfor(self, 20, By.XPATH, "//span[text()='Threat Indicator']/preceding-sibling::div/p")
    self.driver.find_element_by_xpath("//span[text()='Threat Indicator']/preceding-sibling::div").click()
    self.driver.execute_script("arguments[0].textContent = arguments[1];", _ioc_body, ioc_body)
    sleep(2)    # required when large data is provided
    self.driver.find_element_by_xpath("//button[span[text()='Parse Indicators']]").click()
    self.driver.find_element_by_xpath("//button[span[text()='Parse Indicators']]").click()
    sleep(5)   # required in case of large data
    self.driver.find_element_by_xpath("//button[div/div/span[text()='Recipients']]").click()
    waitfor(self, 20, By.XPATH, "//div[div[text()='User Recipient Group(s)']]")
    self.driver.find_element_by_xpath("//div[div[text()='User Recipient Group(s)']]").click()
    self.driver.find_element_by_xpath("//div[div[text()='User Recipient Group(s)']]//input").send_keys(recipient)
    waitfor(self, 20, By.XPATH, f"//li[contains(text(), '{recipient}')]")
    self.driver.find_element_by_xpath(f"//li[contains(text(), '{recipient}')]").click()
    sleep(2)    # required
    self.driver.find_element_by_xpath("//button[div/div/span[text()='Finish']]").click()
    waitfor(self, 20, By.XPATH, "//div[text()='Post this Alert to other Platforms.']")
    self.driver.find_element_by_xpath("//div[text()='Post this Alert to other Platforms.']"
                                      "/following-sibling::div//label[span[normalize-space(text())='CTIX']]").click()


def click_on_product(self, product_name):
    waitfor(self, 2, By.XPATH, "//p[contains(text(),'"+product_name+"')]")
    self.driver.find_element_by_xpath("//p[contains(text(),'"+product_name+"')]").click()


def go_back_to_product_page(self):
    if waitfor(self, 2, By.XPATH, "//span[@data-testaction='slider-close']", False):
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        sleep(1)    # Required to reduce the chances of Element Overlapping
        self.driver.find_element_by_xpath("//div[contains(@class,'cy-page__back-button')]").click()
        waitfor(self, 5, By.XPATH, "//span[contains(text(),' / Cyware Products ')]")
        return True
    else:
        return False
