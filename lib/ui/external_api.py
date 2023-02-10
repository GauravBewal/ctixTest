from lib.common_functions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert

MISP_URL = "https://misp-v3.stegnophora.in/"
MISP_USERNAME = "admin@admin.test"
MISP_PASSWORD = "h2CpdGi8_cVuRbhizk3D"


def login_misp(self):
    """
        Function to login to MISP
    """
    self.driver.get(MISP_URL)
    waitfor(self, 20, By.XPATH, "//input[@id='UserEmail']")
    fprint(self, "Login page is now visible")
    fprint(self, "Filling in Username")
    self.driver.find_element_by_xpath("//input[@id='UserEmail']").send_keys(MISP_USERNAME)
    fprint(self, "Filling in Password")
    self.driver.find_element_by_xpath("//input[@id='UserPassword']").send_keys(MISP_PASSWORD)
    sleep(1)    # waiting for fields to be filled
    fprint(self, "Clicking on login button")
    self.driver.find_element_by_xpath("//button[text()='Login']").click()
    waitfor(self, 20, By.XPATH, "//h2[text()='Events']")
    fprint(self, "MISP homapage has loaded successfully")


def add_event(self, title):
    """
        Function to create a new event with attributes
        args:
            title(str): name of the event to be created
            data(dict): data to be added in the event as an attribute
            publish(boolean): If the event is to be published
        returns: None
    """
    waitfor(self, 5, By.XPATH, "//li[a[text()='Event Actions']]")
    fprint(self, "Clicking on Event Actions")
    _drp_button = self.driver.find_element_by_xpath("//li[a[text()='Event Actions']]")
    _drp_button.click()
    sleep(1)        # Waiting for the dropdown to be visible
    fprint(self, "Clicking on add event")
    _drp_button.find_element_by_xpath(".//ul/li[a[text()='Add Event']]").click()
    waitfor(self, 10, By.XPATH, "//input[@id='EventInfo']")
    fprint(self, f"filling in Event name as {title}")
    self.driver.find_element_by_xpath("//input[@id='EventInfo']").send_keys(title)
    fprint(self, "Clicking on Submit")
    self.driver.find_element_by_xpath("//button[text()='Submit']").click()
    waitfor(self, 20, By.XPATH, f"//h2[text()='{title}']")


def add_attribute(self, data):
    """
        Funtion to add attributes to an event
        args:
            data(dict): data to be added in the event as an attribute
        returns: None
    """
    self.driver.find_element_by_xpath("//li[a[text()='Add Attribute']]").click()
    waitfor(self, 20, By.XPATH, "//legend[text()='Add Attribute']")
    fprint(self, f"Adding attribute {data[2]}")
    _category_drp = self.driver.find_element_by_xpath("//div[@id='AttributeCategory_chosen']")
    _category_drp.click()
    sleep(1)    # waiting for 1 second for dropdown to load up
    fprint(self, "Selecting categor as newtork category")
    _category_drp.find_element_by_xpath(".//input").send_keys("Network activity")
    sleep(1)
    self.driver.find_element_by_xpath("//li[em[text()='Network activity']]").click()
    _type_drop = self.driver.find_element_by_xpath("//div[@id='AttributeType_chosen']")
    _type_drop.click()
    sleep(1)    # waiting for dropdown to load up
    _type_drop.find_element_by_xpath(".//input").send_keys(data[0])
    sleep(1)
    fprint(self, f"Setting attribute value as {data[2]}")
    self.driver.find_element_by_xpath(f"//li[em[text()='{data[0]}']]").click()
    self.driver.find_element_by_xpath("//textarea[@id='AttributeValue']").send_keys(data[2])
    self.driver.find_element_by_xpath("//div[label[text()='for Intrusion Detection System']]").click()
    fprint(self, "Clicking on the submit button")
    self.driver.find_element_by_xpath("//button[text()='Submit']").click()
    waitfor(self, 5, By.XPATH, "//li[a[text()='Add Attribute']]")


def add_ctix_server_in_misp(self, misp_auth, misp_url):
    """
        Function to add new server to MISP
        args:
            misp_auth: Authorization key for MISP server to be created
            misp_url: Server URL to be added in MISP
        returns: None
    """
    waitfor(self, 5, By.XPATH, "//li[a[text()='Sync Actions']]")
    fprint(self, "Clicking on Sync Actions")
    _drp_button = self.driver.find_element_by_xpath("//li[a[text()='Sync Actions']]")
    _drp_button.click()
    sleep(1)    # required
    fprint(self, "Clicking on list servers")
    self.driver.find_element_by_xpath("//li[a[text()='List Servers']]").click()
    waitfor(self, 10, By.XPATH, "//li[a[text()='New Servers']]")
    self.driver.find_element_by_xpath("//li[a[text()='New Servers']]").click()
    waitfor(self, 10, By.XPATH, "//input[@id='ServerUrl']")
    fprint(self, "Filling in server URL")
    self.driver.find_element_by_xpath("//input[@id='ServerUrl']").send_keys(misp_url)
    fprint(self, "Filling in server name")
    self.driver.find_element_by_xpath("//input[@id='ServerName']").send_keys(misp_url[8:14])
    fprint(self, "Filling in Authorization token")
    self.driver.find_element_by_xpath("//input[@id='ServerAuthkey']").send_keys(misp_auth)
    fprint(self, "Selecting pull option for the server")
    self.driver.find_element_by_xpath("//input[@id='ServerPull']").click()
    sleep(2)    # required
    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    fprint(self, "Clicking on Submit")
    _ele = self.driver.find_element_by_xpath("//span[text()='Submit']")
    _ele.click()


def delete_ctix_server_in_misp(self, misp_url):
    """
        Function to delete CTIX server in MISP
        args:
            misp_url: Server URL to be deleted from MISP
        returns: None
    """
    waitfor(self, 5, By.XPATH, "//li[a[text()='Sync Actions']]")
    fprint(self, "Clicking on sync Actions")
    _drp_button = self.driver.find_element_by_xpath("//li[a[text()='Sync Actions']]")
    _drp_button.click()
    sleep(1)    # required
    self.driver.find_element_by_xpath("//li[a[text()='List Servers']]").click()
    fprint(self, "Clicked on list servers")
    waitfor(self, 20, By.XPATH, "//th/a[text()='Id']")
    self.driver.find_element_by_xpath("//th/a[text()='Id']").click()
    sleep(5)    # required
    self.driver.find_element_by_xpath("//th/a[text()='Id']").click()
    self.driver.execute_script("window.scrollTo(document.body.scrollWidth, 0)")
    fprint(self, "Scrolling to the right")
    fprint(self, misp_url[:-1])
    waitfor(self, 20, By.XPATH, f"//tr[td[contains(text(),'{misp_url[:-1]}')]]/td/a[@title='Delete']")
    self.driver.find_element_by_xpath(f"//tr[td[contains(text(),'{misp_url[:-1]}')]]/td/a[@title='Delete']").click()
    fprint(self, "Sleeping for 5 Scconds")
    sleep(5)    # required
    Alert(self.driver).accept()


def pull_data_from_ctix_server(self, misp_url):
    """
        Function to pull data from CTIX server to MISP
    """
    waitfor(self, 5, By.XPATH, "//li[a[text()='Sync Actions']]")
    _drp_button = self.driver.find_element_by_xpath("//li[a[text()='Sync Actions']]")
    _drp_button.click()
    sleep(1)    # required
    fprint(self, "Clicking on list servers")
    self.driver.find_element_by_xpath("//li[a[text()='List Servers']]").click()
    waitfor(self, 20, By.XPATH, "//th/a[text()='Id']")
    self.driver.find_element_by_xpath("//th/a[text()='Id']").click()
    sleep(5)    # required
    self.driver.find_element_by_xpath("//th/a[text()='Id']").click()
    fprint(self, "Scrolling the window to the right")
    self.driver.execute_script("window.scrollTo(document.body.scrollWidth, 0)")
    waitfor(self, 20, By.XPATH, f"//tr[td[contains(text(),'{misp_url[:-1]}')]]/td/a[@title='Pull all']")
    fprint(self, "Clicking on pull all option")
    self.driver.find_element_by_xpath(f"//tr[td[contains(text(),'{misp_url[:-1]}')]]/td/a[@title='Pull all']").click()
    sleep(20)   # waiting for intel to be pulled to MISP


def open_event_in_misp(self, title):
    """
        Function to open up an event created on MISP
        args:
            title: title of the MISP event to be searched
        returns: None
    """
    waitfor(self, 5, By.XPATH, "//li[a[text()='Event Actions']]")
    _drp_button = self.driver.find_element_by_xpath("//li[a[text()='Event Actions']]")
    _drp_button.click()
    fprint(self, "Clicking on List Events")
    _drp_button.find_element_by_xpath(".//ul/li[a[text()='List Events']]").click()
    waitfor(self, 20, By.XPATH, "//input[@id='quickFilterField']")
    fprint(self, f"Searching for {title} in Event Search")
    self.driver.find_element_by_xpath("//input[@id='quickFilterField']").send_keys(title)
    self.driver.find_element_by_xpath("//button[@id='quickFilterButton']").click()
    if not waitfor(self, 10, By.XPATH, f"//h2[text()='{title}']", False):
        self.driver.find_element_by_xpath(f"//td[contains(text(),'{title}')]/preceding-sibling::td/a[@title='View']").click()
        waitfor(self, 10, By.XPATH, f"//h2[text()='{title}']")
    fprint(self, f"Details Page loaded for Event - {title}")


def search_attribute_in_misp_event(self, attribute):
    """
        Function to search if an attribute is present in the MISP event
        args:
            attribute: attribute to be searched in the event
        returns: None
    """
    fprint(self, f"Searching for Attribute - {attribute}")
    waitfor(self, 5, By.XPATH, "//input[@id='quickFilterField']")
    self.driver.find_element_by_xpath("//input[@id='quickFilterField']").send_keys(attribute)
    sleep(5)
    _ele = self.driver.find_element_by_xpath("//button[@id='quickFilterButton']")
    self.driver.execute_script("arguments[0].scrollIntoView();", _ele)
    _ele.click()
    waitfor(self, 10, By.XPATH, f"//span[contains(text(),'{attribute}')]")
    fprint(self, f"Attribue {attribute} found in the event")
