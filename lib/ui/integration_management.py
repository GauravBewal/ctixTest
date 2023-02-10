from lib.ui.nav_app import *
from lib.common_functions import *
from selenium.webdriver.common.by import By

QRADAR_URL = "https://qrad.stegnophora.in/"
QRADAR_USERNAME = 'kaushal'
QRADAR_PASSWORD = 'kaushal@123'
SPLUNK_USERNAME = 'admin'
SPLUNK_PASSWORD = 'cyware@123'
SPLUNK_TOKEN = "eyJraWQiOiJzcGx1bmsuc2VjcmV0IiwiYWxnIjoiSFM1MTIiLCJ2ZXIiOiJ2MiIsInR0eXAiOiJzdGF0aWMifQ.eyJpc3MiOiJhZG1pbiBmcm9tIGlwLTEwLTEwMC0zLTY4Iiwic3ViIjoiYWRtaW4iLCJhdWQiOiJDVElYIEludGVncmF0aW9uIiwiaWRwIjoiU3BsdW5rIiwianRpIjoiYmVkNjllZTM5MzYyZWY4NTFhNDllYTJiNGQyNjQwMGU0ZjdhOTlmZDMyYTMyOWUyNGJlMDUzODkwMDFhODhjZCIsImlhdCI6MTY1MTY0NzgxNCwiZXhwIjowLCJuYnIiOjE2NTE2NDc4MTR9.8ORE1xGBZ9E_JfqI9M69jqez84b8rooUpHfs_uaTlvEwCTzuHw4mcvM1716rY0l_VyugjqoO0oQVrspsRNmBTw"
CORTEX_ACCESS_ID = '4D9EF81691FED5BA3220B543119CD940'
CORTEX_USERNAME = "admin"
CORTEX_PASSWORD = "3JpO3pa98gPVpzNARFAN"
ZSCALER_USERNAME = "admin@7575986.zscalerbeta.net"
ZSCALER_PASSWORD = "jex3gen*JFV@cnd0tpk"
EXABEAM_USERNAME = "cyware"
EXABEAM_PASSWORD = "Welcome2Exabeam@"
EXABEAM_ACCESSID = "9b94a830-89ab-4636-8920-d51396db9c95"
PHANTOM_ACCESSID = "3QcUI2XmR9BWnz4mX6pCGG7MsiwQCWWVyRxRfImGX9s="


def add_qradar_account(self, **kwargs):
    """
    Function to Add Qradar account in CTIX
    kwargs:
        url:
        username:
        password:
    returns:
        None
    """
    instance_name = kwargs.get("instamce_name", "qradar")
    base_url = kwargs.get("base_url", QRADAR_URL)
    username = kwargs.get("username", QRADAR_USERNAME)
    password = kwargs.get("password", QRADAR_PASSWORD)
    fprint(self, 'Searching for qradar')
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("Qradar")
    self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
    fprint(self, 'Clicking on QRADAR')
    if waitfor(self, 20, By.XPATH, "//div[p[contains(text(), 'Qradar')]]", False):
        self.driver.find_element_by_xpath("//div[p[contains(text(), 'Qradar')]]").click()
    else:
        self.driver.find_element_by_xpath("//div[p[contains(text(), 'QRadar')]]").click()
    if waitfor(self, 8, By.XPATH, "//button[contains(text(), 'DONE')]", False):
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'DONE')]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(), 'OK, GOT IT')]").click()
    sleep(2)
    try:
        fprint(self, 'Clicking on add Instance')
        waitfor(self, 20, By.XPATH, "//button[span[contains(text(), 'Add Instance')]]")
        self.driver.find_element_by_xpath("//button[span[contains(text(), 'Add Instance')]]").click()
    except:
        fprint(self, "Credential Slider is already visible...")
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Instance Name*']")
    sleep(2)
    fprint(self, "Filling in insatnce name")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Instance Name*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Instance Name*']").send_keys(instance_name)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Base Url*']")
    fprint(self, "FIlling in Base Url")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").click()
    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']"))
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").send_keys(base_url+"api/")
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Username*']")
    fprint(self, 'Filling in username')
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Username*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Username*']").send_keys(username)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Password*']")
    fprint(self, 'Filling in password')
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Password*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Password*']").send_keys(password)
    fprint(self, "Clicking on save")
    self.driver.find_element_by_xpath("//button[contains(text(), 'Save')]").click()
    verify_success(self, 'Instance created successfully', 240)


def launch_qradar(self):
    op = Options()
    op.add_argument("–-no-sandbox")
    # op.add_argument('--headless')
    op.add_argument("--log-level=1")
    op.add_argument("-–disable-dev-shm-usage")
    op.add_argument("--disable-extensions")
    if path.exists("/.dockerenv"):
        print("Execution Platform is Docker Container")
        driver_path = "/usr/local/bin/chromedriver"
        self.driver = webdriver.Chrome(driver_path, options=op)
    else:
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=op)
    self.driver.maximize_window()
    self.driver.get(QRADAR_URL)
    h = self.driver.window_handles
    fprint(self, "Redirecting back to QRADAR")
    self.driver.switch_to.window(h[0])
    if waitfor(self, 20, By.XPATH, "//*[@id='advancedButton']", False):
        self.driver.find_element_by_xpath("//*[@id='advancedButton']").click()
        waitfor(self, 20, By.XPATH, "//*[@id='exceptionDialogButton']")
        self.driver.find_element_by_xpath("//*[@id='exceptionDialogButton']").click()
    elif waitfor(self, 30, By.XPATH, "//button[contains(text(), 'Advanced')]", False):
        self.driver.find_element_by_xpath("//button[contains(text(), 'Advanced')]").click()
        waitfor(self, 20, By.XPATH, "//a[@id='proceed-link']")
        self.driver.find_element_by_xpath("//a[@id='proceed-link']").click()
    fprint(self, 'Sleeping for qradar to be ready')
    #sleep(300)
    fprint(self, "Filling in username")
    waitfor(self, 20, By.XPATH, "//input[@id='j_username']")
    self.driver.find_element_by_xpath("//input[@id='j_username']").click()
    self.driver.find_element_by_xpath("//input[@id='j_username']").send_keys(QRADAR_USERNAME)
    fprint(self, "Filling in Password")
    waitfor(self, 20, By.XPATH, "//input[@id='j_password']")
    self.driver.find_element_by_xpath("//input[@id='j_password']").click()
    self.driver.find_element_by_xpath("//input[@id='j_password']").send_keys(QRADAR_PASSWORD)
    fprint(self, "Clicked on Login")
    self.driver.find_element_by_xpath("//input[@value='Login']").click()
    sleep(20)
    waitfor(self, 20, By.XPATH, "//a[@id='TAB_ADMIN']")
    fprint(self, "Redirecting To Admin")
    self.driver.find_element_by_xpath("//a[@id='TAB_ADMIN']").click()
    sleep(10)
    fprint(self, "Sleep done")
    self.driver.switch_to_frame(self.driver.find_element_by_xpath("//iframe[@id='PAGE_ADMIN']"))
    self.driver.switch_to_frame(self.driver.find_element_by_xpath("//frame[@name='rightPane']"))
    return self.driver


def add_splunk_account(self, **kwargs):
    """
        Function to add splunk account to CTIX
        args:
            instance_name: name for the account added
            base_url: Base_URL for the splunk
            username: username of the splunk account
            password: password of the splunk account
    """
    instance_name = kwargs.get("instamce_name", "splunk")
    base_url = kwargs.get("base_url", "https://splunk.stegnophora.in:8089")
    username = kwargs.get("username", SPLUNK_USERNAME)
    password = kwargs.get("password", SPLUNK_PASSWORD)
    fprint(self, 'Searching for splunk')
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("Splunk")
    self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
    fprint(self, 'Clicking on Splunk')
    waitfor(self, 20, By.XPATH, "//div[p[contains(text(), 'Splunk')]]")
    self.driver.find_element_by_xpath("//div[p[contains(text(), 'Splunk')]]").click()
    if waitfor(self, 8, By.XPATH, "//button[contains(text(), 'DONE')]", False):
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'DONE')]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(), 'OK, GOT IT')]").click()
    sleep(2)
    try:
        fprint(self, 'Clicking on add Instance')
        waitfor(self, 20, By.XPATH, "//button[span[contains(text(), 'Add Instance')]]")
        self.driver.find_element_by_xpath("//button[span[contains(text(), 'Add Instance')]]").click()
    except:
        fprint(self, "Credential Slider is already visible...")
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Instance Name*']")
    sleep(2)
    fprint(self, "Filling in insatnce name")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Instance Name*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Instance Name*']").send_keys(instance_name)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Base Url*']")
    fprint(self, "FIlling in Base Url")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").click()
    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']"))
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").send_keys(base_url)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Username*']")
    # fprint(self, "Selecting Authentication token Configuration")
    # self.driver.find_element_by_xpath("//div[contains(text(),' Authentication Token ')]").click()
    fprint(self, 'Filling in username')
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Username*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Username*']").send_keys(username)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Password*']")
    fprint(self, 'Filling in password')
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Password*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Password*']").send_keys(password)
    # fprint(self, 'Filling in Token')
    # self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter Token*']").click()
    # self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter Token*']").send_keys(SPLUNK_TOKEN)
    fprint(self, "Clicking on save")
    self.driver.find_element_by_xpath("//button[contains(text(), 'Save')]").click()
    verify_success(self, 'Instance created successfully')


def launch_splunk(self):
    """
        Function to launch splunk
    """
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', os.getcwd())
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
    if path.exists("/.dockerenv"):
        print("Execution Platform is Docker Container")
        driver_path = "/usr/local/bin/geckodriver"
        self.driver = webdriver.Firefox(firefox_profile=profile, executable_path=driver_path,
                                        service_log_path="/tmp/geckodriver.log")
    else:
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    self.driver.maximize_window()
    self.driver.get("https://splunk.stegnophora.in:8000")
    h = self.driver.window_handles
    fprint(self, "Redirecting back to Splunk")
    self.driver.switch_to.window(h[0])
    self.driver.refresh()
    if waitfor(self, 20, By.XPATH, "//input[@placeholder='Username']", False):
        fprint(self, 'Filling up username in splunk')
        self.driver.find_element_by_xpath("//input[@placeholder='Username']").send_keys('admin')
        fprint(self, "Filling in password in splunk")
        self.driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys('cyware@123')
        sleep(2)
        fprint(self, "Clicking on Sign in")
        self.driver.find_element_by_xpath("//input[@value='Sign In']").click()
    waitfor(self, 20, By.XPATH, "//a[@title='splunk > listen to your data']")
    fprint(self, "Splunk is now open")
    sleep(5)
    self.driver.find_element_by_xpath("//a[@title='splunk > listen to your data']").click()
    if not waitfor(self, 20, By.XPATH, "//i[@data-icon='enterprise']"):
        waitfor(self, 20, By.XPATH, "//button[@id='advancedButton']")
        fprint(self, "Clicking on Advanced button")
        self.driver.find_element_by_xpath("//button[@id='advancedButton']").click()
        waitfor(self, 20, By.XPATH, "//button[@id='exceptionDialogButton']")
        fprint(self, "Clicking on accept risk and continue")
        self.driver.find_element_by_xpath("//button[@id='exceptionDialogButton']").click()
    waitfor(self, 20, By.XPATH, "//a[@title='splunk > listen to your data']")
    fprint(self, "Logged in to Splunk")
    return self.driver


def add_cortex_soar_account(self, **kwargs):
    """
        Function to add CORTEX SOAR Account in CTIX
        kwargs:
            instance_name: Name to be provided to added account
            base_url: Base URL the tool is to be configured to
            access_id: Access id for the account to be added
        returns:
            None
    """
    instance_name = kwargs.get("instance_name", "cortex")
    base_url = kwargs.get("base_url", 'https://xsoar.mycyware.com/')
    access_id = kwargs.get("access_id", CORTEX_ACCESS_ID)
    fprint(self, 'Searching for CORTEX-XSOAR')
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("CORTEX-XSOAR")
    self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
    fprint(self, 'Clicking on Splunk')
    waitfor(self, 20, By.XPATH, "//div[p[contains(text(), 'CORTEX-XSOAR')]]")
    self.driver.find_element_by_xpath("//div[p[contains(text(), 'CORTEX-XSOAR')]]").click()
    if waitfor(self, 8, By.XPATH, "//button[contains(text(), 'DONE')]", False):
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'DONE')]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(), 'OK, GOT IT')]").click()
    sleep(2)
    try:
        fprint(self, 'Clicking on add Instance')
        waitfor(self, 20, By.XPATH, "//button[span[contains(text(), 'Add Instance')]]")
        self.driver.find_element_by_xpath("//button[span[contains(text(), 'Add Instance')]]").click()
    except:
        fprint(self, "Credential Slider is already visible...")
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Instance Name*']")
    sleep(2)
    fprint(self, "Filling in insatnce name")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Instance Name*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Instance Name*']").send_keys(instance_name)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Base Url*']")
    fprint(self, "FIlling in Base Url")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").click()
    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']"))
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").send_keys(base_url)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Access ID*']")
    fprint(self, 'Filling in access_id')
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Access ID*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Access ID*']").send_keys(access_id)
    fprint(self, "Clicking on save")
    self.driver.find_element_by_xpath("//button[contains(text(), 'Save')]").click()
    verify_success(self, 'Instance created successfully')


def launch_cortex_soar(self):
    """
        Function to launch and login to CORTEX SOAR
    """
    self.driver.get("https://xsoar.mycyware.com/")
    waitfor(self, 40, By.XPATH, "//input[@placeholder='Username']")
    fprint(self, "Filling in Username in CORTEX SOAR Form")
    self.driver.find_element_by_xpath("//input[@placeholder='Username']").send_keys(CORTEX_USERNAME)
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Password']")
    fprint(self, "Filling in Password in CORTEX SOAR Form")
    self.driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys(CORTEX_PASSWORD)
    fprint(self, "Clicking on login button")
    self.driver.find_element_by_xpath("//button[span[text()='Login']]").click()
    waitfor(self, 20, By.XPATH, "//span[@title='Dashboards']")
    fprint(self, '[PASSED] Dashboards text is now visible, logged in successfully')
    waitfor(self, 20, By.XPATH, "//div/a/i[@title='Settings']")
    self.driver.find_element_by_xpath("//div/a/i[@title='Settings']").click()
    waitfor(self, 20, By.XPATH, "//span[text()='Settings'][@title='Settings']")
    self.driver.find_element_by_xpath("//a[span[text()='Advanced']]").click()
    sleep(2)    # required
    waitfor(self, 20, By.XPATH, "//a[span[text()='Incident Types']]")
    self.driver.find_element_by_xpath("//a[span[text()='Incident Types']]").click()
    sleep(2)    # required


def cortex_search_and_delete(self, cortex_intel):
    waitfor(self, 20, By.XPATH, "//div/input[@placeholder='Search in Incidents']")
    self.driver.find_element_by_xpath("//div[input[@placeholder='Search in Incidents']]").click()
    self.driver.find_element_by_xpath("//div/input[@placeholder='Search in Incidents']").send_keys(
        cortex_intel)
    self.driver.find_element_by_xpath("//div/input[@placeholder='Search in Incidents']").send_keys(Keys.ENTER)
    waitfor(self, 20, By.XPATH, "//div[text()='Package From CTIX']")
    sleep(2)    # required
    self.driver.find_element_by_xpath("//span[text()='Investigate']").click()
    if waitfor(self, 20, By.XPATH, "//span[text()='" + get_value("CORTEX_INCIDENT") + "']"):
        fprint(self, "Trigger playbook run successfully over old ip")
    waitfor(self, 20, By.XPATH, "//div/span[text()='Actions']")
    self.driver.find_element_by_xpath("//div/span[text()='Actions']").click()
    waitfor(self, 20, By.XPATH, "//div[span[text()='Delete']]")
    self.driver.find_element_by_xpath("//div[span[text()='Delete']]").click()
    waitfor(self, 20, By.XPATH, "//button[span/span[text()='Yes, delete forever']]")
    self.driver.find_element_by_xpath("//button[span/span[text()='Yes, delete forever']]").click()


def launch_zscaler(self):
    """
        Function to launch ZScaler
    """
    self.driver.get("https://admin.zscalerbeta.net/")
    waitfor(self, 20, By.XPATH, "//input[@id='login-panel-input-email']")
    fprint(self, "ZScaler login page is now visible")
    fprint(self, "Entering username")
    self.driver.find_element_by_xpath("//input[@id='login-panel-input-email']").send_keys(ZSCALER_USERNAME)
    waitfor(self, 20, By.XPATH, "//input[@id='login-panel-input-password']")
    fprint(self, "Entering password")
    self.driver.find_element_by_xpath("//input[@id='login-panel-input-password']").send_keys(ZSCALER_PASSWORD)
    fprint(self, "Clicking on sign in")
    waitfor(self, 20, By.XPATH, "//span[text()='Sign In']")
    self.driver.find_element_by_xpath("//span[text()='Sign In']").click()
    sleep(5)
    waitfor(self, 300, By.XPATH, "//div[@data-item='administration']")
    fprint(self, "Page is now loaded successfully")
    if waitfor(self, 30, By.XPATH, "//span[@class='donnotshow']/span", False):
        self.driver.find_element_by_xpath("//span[@class='donnotshow']/span").click()
        self.driver.find_element_by_xpath("//span[@class='donnotshow']/following-sibling::span[text()='Close']").click()
    sleep(10)   # needed as not all elements are readily visible


def get_zscaler_key(self):
    """
        Function to get the zscaler key from ZScaler webpage
    """
    launch_zscaler(self)
    self.driver.find_element_by_xpath("//div[@data-item='administration']").click()
    waitfor(self, 20, By.XPATH, "//li[span[text()='Cloud Service API Security']]")
    self.driver.find_element_by_xpath("//li[span[text()='Cloud Service API Security']]").click()
    waitfor(self, 20, By.XPATH, "//span[@data-text-column='0']")
    set_value('zscaler_key', self.driver.find_element_by_xpath("//span[@data-text-column='0']").text)
    handles = self.driver.window_handles
    self.driver.switch_to_window(handles[1])


def add_zscaler_account(self, **kwargs):
    """
        Function to add ZSCALER Account in CTIX
        kwargs:
            instance_name: Name to be provided to added account
            base_url: Base URL the tool is to be configured to
            username: Username for ZScaler account
            password: Password for ZScaler account
            api_key: API_KEY for the account to be added
        returns:
            None
    """
    instance_name = kwargs.get("instance_name", "zscaler")
    base_url = kwargs.get("base_url", 'https://admin.zscalerbeta.net/api/v1')
    username = kwargs.get("username", ZSCALER_USERNAME)
    password = kwargs.get("password", ZSCALER_PASSWORD)
    api_key = kwargs.get("api_key", get_value("zscaler_key"))
    fprint(self, 'Searching for Zscaler Network Security')
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").\
        send_keys("Zscaler Network Security")
    self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
    fprint(self, 'Clicking on Zscaler Network Security')
    waitfor(self, 20, By.XPATH, "//div[p[contains(text(), 'Zscaler Network Security')]]")
    self.driver.find_element_by_xpath("//div[p[contains(text(), 'Zscaler Network Security')]]").click()
    if waitfor(self, 8, By.XPATH, "//button[contains(text(), 'DONE')]", False):
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'DONE')]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(), 'OK, GOT IT')]").click()
    sleep(2)
    try:
        fprint(self, 'Clicking on add Instance')
        waitfor(self, 20, By.XPATH, "//button[span[contains(text(), 'Add Instance')]]")
        self.driver.find_element_by_xpath("//button[span[contains(text(), 'Add Instance')]]").click()
    except:
        fprint(self, "Credential Slider is already visible...")
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Instance Name*']")
    sleep(2)
    fprint(self, "Filling in insatnce name")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Instance Name*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Instance Name*']").send_keys(instance_name)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Base Url*']")
    fprint(self, "FIlling in Base Url")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").click()
    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']"))
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").send_keys(base_url)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Username*']")
    fprint(self, 'Filling in Username')
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Username*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Username*']").send_keys(username)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Password*']")
    fprint(self, 'Filling in Password')
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Password*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Password*']").send_keys(password)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='API Key*']")
    fprint(self, 'Filling in API Key')
    self.driver.find_element_by_xpath("//input[@aria-placeholder='API Key*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='API Key*']").send_keys(api_key)
    fprint(self, "Clicking on save")
    self.driver.find_element_by_xpath("//button[contains(text(), 'Save')]").click()
    verify_success(self, 'Instance created successfully', timeout=20)


def add_exabeam_account(self, **kwargs):
    """
        Function to add Exabeam account into CTIX

    """
    instance_name = kwargs.get("instamce_name", "exabeam")
    base_url = kwargs.get("base_url", "https://tbd2-int-e2e.aa.exabeam.com/api")
    username = kwargs.get("access_id", EXABEAM_ACCESSID)
    fprint(self, 'Searching for exabeam')
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("Exabeam")
    self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
    fprint(self, 'Clicking on Exabeam')
    if waitfor(self, 20, By.XPATH, "//div[p[contains(text(), 'Exabeam')]]", False):
        self.driver.find_element_by_xpath("//div[p[contains(text(), 'Exabeam')]]").click()
    else:
        self.driver.find_element_by_xpath("//div[p[contains(text(), 'Exabeam')]]").click()
    if waitfor(self, 20, By.XPATH, "//button[contains(text(), 'DONE')]", False):
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'DONE')]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(), 'OK, GOT IT')]").click()
    sleep(2)
    fprint(self, 'Clicking on add Instance')
    waitfor(self, 20, By.XPATH, "//button[span[contains(text(), 'Add Instance')]]")
    self.driver.find_element_by_xpath("//button[span[contains(text(), 'Add Instance')]]").click()
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Instance Name*']")
    sleep(2)
    fprint(self, "Filling in insatnce name")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Instance Name*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Instance Name*']").send_keys(instance_name)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Base Url*']")
    fprint(self, "FIlling in Base Url")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").click()
    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']"))
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").send_keys(base_url)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Access ID*']")
    fprint(self, 'Filling in access_id')
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Access ID*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Access ID*']").send_keys(username)
    fprint(self, "Clicking on save")
    self.driver.find_element_by_xpath("//button[contains(text(), 'Save')]").click()
    verify_success(self, 'Instance created successfully', 60)


def launch_exabeam(self):
    """
        Function to launch Exabeam
    """
    self.driver.get("https://tbd2-int-e2e.aa.exabeam.com/")
    fprint(self, "Filling in Username")
    waitfor(self, 60, By.XPATH, "//input[@id='exabeam-username']")
    sleep(5)    # needed for item to appear
    self.driver.find_element_by_xpath("//input[@id='exabeam-username']").send_keys(EXABEAM_USERNAME)
    waitfor(self, 60, By.XPATH, "//input[@id='exabeam-password']")
    fprint(self, "Filling in Password")
    self.driver.find_element_by_xpath("//input[@id='exabeam-password']").send_keys(EXABEAM_PASSWORD)
    self.driver.find_element_by_xpath("//button[@id='exabeam-login-button']").click()
    waitfor(self, 300, By.XPATH, "//div[text()='ADVANCED ANALYTICS']")
    fprint(self, "Logged into EXABEAM successfully")
    sleep(5)    # needed
    waitfor(self, 20, By.XPATH, "//div[@class='settings-container']")
    self.driver.find_element_by_xpath("//div[@class='settings-container']").click()
    fprint(self, "Clicking on analytics")
    waitfor(self, 20, By.XPATH, "//div[text()='Analytics']")
    self.driver.find_element_by_xpath("//div[text()='Analytics']").click()
    fprint(self, "Clicking on Generate context")
    waitfor(self, 20, By.XPATH, "//div[text()='Generate Context']")
    self.driver.find_element_by_xpath("//div[text()='Generate Context']").click()
    fprint(self, "Clicking on CONTEXT TABLES section")
    waitfor(self, 20, By.XPATH, "//div[normalize-space(text())='CONTEXT TABLES']")
    self.driver.find_element_by_xpath("//div[normalize-space(text())='CONTEXT TABLES']").click()
    waitfor(self, 20, By.XPATH, "//div[i[text()='search']]")
    sleep(5)    # needed


def add_splunk_phantom_account(self, **kwargs):
    """
        Testcase to add Splunk Phantom Account
    """
    instance_name = kwargs.get("instamce_name", "phantom")
    base_url = kwargs.get("base_url", "https://phan.stegnophora.in/")
    access_id = kwargs.get("username", PHANTOM_ACCESSID)
    fprint(self, 'Searching for Splunk Phantom')
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("Splunk Phantom")
    self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
    waitfor(self, 20, By.XPATH, "//div[p[contains(text(), 'Splunk Phantom')]]")
    fprint(self, 'Clicking on Splunk Phantom')
    self.driver.find_element_by_xpath("//div[p[contains(text(), 'Splunk Phantom')]]").click()
    if waitfor(self, 8, By.XPATH, "//button[contains(text(), 'DONE')]", False):
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'DONE')]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(), 'OK, GOT IT')]").click()
    sleep(2)
    try:
        fprint(self, 'Clicking on add Instance')
        waitfor(self, 20, By.XPATH, "//button[span[contains(text(), 'Add Instance')]]")
        self.driver.find_element_by_xpath("//button[span[contains(text(), 'Add Instance')]]").click()
    except:
        fprint(self, "Credential Slider is already visible...")
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Instance Name*']")
    sleep(2)
    fprint(self, "Filling in insatnce name")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Instance Name*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Instance Name*']").send_keys(instance_name)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Base Url*']")
    fprint(self, "FIlling in Base Url")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").click()
    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']"))
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Base Url*']").send_keys(base_url)
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Access ID*']")
    fprint(self, 'Filling in Access ID*')
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Access ID*']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Access ID*']").send_keys(access_id)
    waitfor(self, 20, By.XPATH, "//span[input[@name='ssl_encrypted']]")
    self.driver.find_element_by_xpath("//span[input[@name='ssl_encrypted']]").click()
    fprint(self, "Clicking on save")
    self.driver.find_element_by_xpath("//button[contains(text(), 'Save')]").click()
    verify_success(self, 'Instance created successfully')


def launch_splunk_phantom(self):
    """
        Function to launch splunk phantom
    """
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.download.dir', os.getcwd())
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'text/csv')
    if path.exists("/.dockerenv"):
        print("Execution Platform is Docker Container")
        driver_path = "/usr/local/bin/geckodriver"
        self.driver = webdriver.Firefox(firefox_profile=profile, executable_path=driver_path,
                                        service_log_path="/tmp/geckodriver.log")
    else:
        self.driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    self.driver.maximize_window()
    self.driver.get("https://phan.stegnophora.in/browse/")
    h = self.driver.window_handles
    fprint(self, "Redirecting back to Splunk")
    self.driver.switch_to.window(h[0])
    self.driver.refresh()
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Username']")
    fprint(self, 'Filling up username in splunk phantom')
    self.driver.find_element_by_xpath("//input[@placeholder='Username']").send_keys('admin')
    fprint(self, "Filling in password in splunk phantom")
    self.driver.find_element_by_xpath("//input[@placeholder='Password']").send_keys('admin@phantom')
    sleep(2)
    fprint(self, "Clicking on Sign in")
    self.driver.find_element_by_xpath("//button[text()='Sign in']").click()
    if not waitfor(self, 20, By.XPATH, "//div[@class='logo']", False):
        waitfor(self, 20, By.XPATH, "//button[@id='advancedButton']")
        fprint(self, "Clicking on Advanced button")
        self.driver.find_element_by_xpath("//button[@id='advancedButton']").click()
        waitfor(self, 20, By.XPATH, "//button[@id='exceptionDialogButton']")
        fprint(self, "Clicking on accept risk and continue")
        self.driver.find_element_by_xpath("//button[@id='exceptionDialogButton']").click()
    fprint(self, "Splunk Phantom is now open")
    fprint(self, "Logged in to Splunk")


def verify_data_in_phantom(self, intel, package_name):
    """
        Function to check for intel in splunk phantom
    """
    waitfor(self, 20, By.XPATH, "//li[a[@class='nav-link' and text()='Indicators']]")
    fprint(self, "Clicking on Indicators")
    self.driver.find_element_by_xpath("//li[a[@class='nav-link' and text()='Indicators']]").click()
    waitfor(self, 20, By.XPATH, "//div[input[@placeholder='Search indicator values']]")
    fprint(self, f"Searching for indicator {intel}")
    self.driver.find_element_by_xpath("//div/input[@placeholder='Search indicator values']").send_keys()
    self.driver.find_element_by_xpath("//div[input[@placeholder='Search indicator values']]/i").click()
    waitfor(self, 20, By.XPATH, f"//div[span[text()='{intel}']]")
    self.driver.find_element_by_xpath(f"//div[span[text()='{intel}']]").click()
    fprint(self, f"Looking for Event name of {intel}")
    waitfor(self, 20, By.XPATH, f"//div[@class='grid-cell' and text()='{intel}']")
    self.driver.find_element_by_xpath(f"//div[@class='grid-cell' and text()='{intel}']").click()
    waitfor(self, 20, By.XPATH, "//div[contains(@class, 'event-name')][span[@class='overlay-hover']]")
    sleep(2)  # required
    fprint(self, f'Renaming event name to {package_name}')
    self.driver.find_element_by_xpath("//div[contains(@class, 'event-name')][span[@class='overlay-hover']]").click()
    clear_field(self.driver.find_element_by_xpath("//div[contains(@class, 'event-name')]/input"))
    self.driver.find_element_by_xpath("//div[contains(@class, 'event-name')]/input").send_keys(package_name)
    self.driver.find_element_by_xpath("//button[contains(@class, 'back-btn')]").click()
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Search event names']")
    sleep(5)
    fprint(self, f"Deleting event - {package_name}")
    self.driver.find_element_by_xpath("//input[@placeholder='Search event names']").send_keys(package_name)
    self.driver.find_element_by_xpath("//input/following-sibling::i").click()
    waitfor(self, 20, By.XPATH, f"//div[text()='{package_name}']")
    self.driver.find_elements_by_xpath("//span[@class='checkmark']")[1].click()
    waitfor(self, 20, By.XPATH, "//button[text()='DELETE']")
    fprint(self, "Clicking on Delete")
    self.driver.find_element_by_xpath("//button[text()='DELETE']").click()
    waitfor(self, 20, By.XPATH, "//button[@data-key='delete']")
    self.driver.find_element_by_xpath("//button[@data-key='delete']").click()
    fprint(self, f"Deleted event {package_name} successfully!")
    sleep(5)
    self.driver.close()


def manage_actions(self):
    waitfor(self, 20, By.XPATH, "//button[@data-testid='actions']")
    sleep(1)
    self.driver.find_element_by_xpath("//button[@data-testid='actions']").click()
    fprint(self, "Selecting Manage from Actions")
    waitfor(self, 20, By.XPATH, "//li[contains(text(), 'Manage')]")
    self.driver.find_element_by_xpath("//li[contains(text(), 'Manage')]").click()
    fprint(self, "Clicking on Manage Action Button")
    waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Manage  Action')]")
    sleep(1)
    self.driver.find_element_by_xpath("//button[contains(text(), 'Manage  Action')]").click()
    fprint(self, "Clicked on Manage Actions button")
    waitfor(self, 20, By.XPATH, "//span[@data-testid='label']")
    tool_actions = self.driver.find_elements_by_xpath\
        ("//div[@id='cy-compact-table']//table/tbody/tr//span[@data-testid='label']")
    tool_actions = [i.text for i in tool_actions]
    for num, action_name in enumerate(tool_actions):
        self.driver.find_element_by_xpath("//div[@id='cy-compact-table']//table/tbody/tr//span[@data-testid='label']"
                                           "[normalize-space()='"+action_name+"']").click()
        if waitfor(self, 10, By.XPATH, "//form//input[@type='checkbox' and @value='false']", False):
            self.driver.find_element_by_xpath("//form//span[input[@type='checkbox' and @value='false']]").click()
        else:
            self.driver.find_element_by_xpath("//div[span/span[contains(text(), 'Disabled')]]").click()
        sleep(1)
        fprint(self, 'Enabling the status of the account actions')
        fprint(self, "Clicking on the Save button")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Save')]").click()
        fprint(self, "Enabling action - "+action_name)
        verify_success(self, "updated successfully")
        sleep(2)    # needed here
    self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
