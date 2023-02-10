from lib.common_functions import *
from selenium.webdriver.common.by import By


def add_email_source(self, title, username, password, domain, type, auto_create):
    """
    Function to create an Email Source
    params:
        title: Title for mailbox in CTIX
        username: email id to be configured
        password: password for the email id used
        domain: domain name for the email connection
        type: Domain Type of Email account IMAP, POP or EWS
        auto_create(boolean): If intel needs to be created automatically
    returns: None
    """
    waitfor(self, 2, By.XPATH, "//div[contains(text(),'Email Configuration')]")
    fprint(self, "[PASSED] Email Configuration form opened")
    fprint(self, "filling up configuration details")
    waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='Client Name *']")
    sleep(1)
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Client Name *']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Client Name *']").send_keys(title)
    sleep(1)
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Email/Username *']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Email/Username *']").send_keys(username)
    sleep(1)
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Password *']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Password *']").send_keys(password)
    sleep(1)
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Domain *']").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Domain *']").send_keys(domain)
    waitfor(self, 5, By.XPATH, "//span[@class='cy-wrapper__label--text']")
    canvas = self.driver.find_element_by_xpath \
        ("//div[contains(text(), 'Server Information *')]/following-sibling::div//div[@tabindex='0']")
    ActionChains(self.driver).move_to_element(canvas).move_by_offset(-60, 0).click().perform()
    waitfor(self, 2, By.XPATH, "//div[text()='"+type+"']")
    self.driver.find_element_by_xpath("//div[text()='"+type+"']").click()
    sleep(1)
    fprint(self, "Saving the configuration details")
    self.driver.find_element_by_xpath("//button[contains(text(),'Save and Continue')]").click()
    verify_success(self, "Email configuration created successfully")
    if Build_Version.__contains__("3."):
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Allowed Emails')]")
    else:
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Allowed Indicators')]")
    self.driver.find_element_by_xpath("//button[contains(text(),'Save and Continue')]").click()
    fprint(self, "Submitting allowed indicators")
    verify_success(self, "updated successfully")
    waitfor(self, 5, By.XPATH, "//div[contains(text(),'Intel Creation Preferences')]")
    if auto_create and waitfor(self, 20, By.XPATH, "//span[normalize-space(text())='Create Intel automatically']", False):
        self.driver.find_element_by_xpath("//span[normalize-space(text())='Create Intel automatically']").click()
        set_value("selective_intel", True)
        if waitfor(self, 10, By.XPATH, "//input[@aria-label='Create Intel from Specific Emails']", False):
            set_auto_intel_creation(self, email='jrcyware@gmail.com', search_str='SHA')
        else:
            set_value("selective_intel", False)
            self.driver.find_element_by_xpath("//span[normalize-space(text())='Create Intel automatically']").click()
    fprint(self, "Submitting Intel Creation Preferences")
    self.driver.find_element_by_xpath("//button[contains(text(),'Save and Continue')]").click()
    verify_success(self, "updated successfully")
    fprint(self, "[PASSED] Intel Creation Preferences submitted successfully")
    waitfor(self, 5, By.XPATH, "//div[contains(text(), 'Folder Synchronization')]")
    if type == "IMAP" or type == "EWS":
        fprint(self, "Synchronizing folders")
        sleep(1)
        self.driver.find_element_by_xpath("//span[contains(text(), 'INBOX')]/preceding-sibling::span/div/span").click()
        sleep(1)
        self.driver.find_element_by_xpath("//span[contains(text(), 'INBOX')]/following-sibling::div").click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        verify_success(self, "updated successfully")
        fprint(self, "[PASSED] Folder Synchronization done successfully")
    else:
        fprint(self, "[PASSED] No Folder Synchronization for POP account")
    if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()


def add_metadata(self, **kwargs):
    confidence_score = kwargs.get("confidence_score", "100")
    fprint(self, "Waiting for the Add Metadata button")
    waitfor(self, 20, By.XPATH, "//span[contains(@class,'cyicon-add')]/parent::button[contains(text(),'Metadata')]")
    self.driver.find_element_by_xpath("//span[contains(@class,'cyicon-add')]/parent::button[contains(text(),'Metadata')]").click()
    fprint(self, "Clicked the Add Metadata button")
    waitfor(self, 20, By.XPATH, "//input[@max='100']")
    clear_field(self.driver.find_element_by_xpath("//input[@max='100']"))
    self.driver.find_element_by_xpath("//input[@max='100']").send_keys(confidence_score)
    fprint(self, "Confidence Score is set to - "+confidence_score)
    sleep(1)
    self.driver.find_element_by_xpath("//span[contains(@class,'cyicon-chevron-left')]").click()
    fprint(self, "Clicked on the left button on the slider")


def set_auto_intel_creation(self, **kwargs):
    """
    Function to set IOC types and mail for auto intel creation
    kwargs:
        email: email source from which intel is to be auto created
        search_str: subvstring of IOC types to be created
    returns:
        None
    """
    email = kwargs.get("email", "jrcyware@gmail.com")
    search_str = kwargs.get("search_str", "SHA")
    set_value("auto_mail_pattern", search_str)
    fprint(self, "Clicking on object Types")
    self.driver.find_element_by_xpath("//div[span[normalize-space(text())='Object Type *']]/following-sibling::"
                                      "div[div[@name='data-value']]").click()
    fprint(self, "Clearing all values from the input form for object types")
    self.driver.find_element_by_xpath("//div[@data-testaction='clear']").click()
    fprint(self, f"Searching for {search_str}")
    self.driver.find_element_by_xpath("//div[span[normalize-space(text())='Object Type *']]/"
                                      "following-sibling::div//input").send_keys(search_str)
    sleep(2)    # required
    [i.click() for i in self.driver.find_elements_by_xpath("//ul[@id='dropdown-list']/li")]
    self.driver.find_element_by_xpath("//div[@data-testaction='close']").click()
    self.driver.find_element_by_xpath("//div[span[normalize-space(text())='Create Intel from Specific Emails']]/"
                                      "following-sibling::div").click()
    fprint(self, "Filling in email for auto intel creation")
    self.driver.find_element_by_xpath("//div[span[normalize-space(text())='Create Intel from Specific Emails']]/"
                                      "following-sibling::div//input").send_keys(email)
    self.driver.find_element_by_xpath("//div[span[normalize-space(text())='Create Intel from Specific Emails']]/"
                                      "following-sibling::div//input").send_keys(Keys.ENTER)


def load_mail(self, account_name, subject, **kwargs):
    """
    Function to load the mail with subject in mailbox of provided account_name

    params:
        account_name: Name of the account having the mail
        subject: Subject of the mail to be parsed

    returns: None
    """
    action = kwargs.get("action", "Create")
    waitfor(self, 20, By.XPATH, "//div[@role='button']/span/button[text()]")
    self.driver.find_element_by_xpath("//div[@role='button']/span/button[text()]").click()
    fprint(self, "Selecting "+account_name+" account from threat mailbox")
    waitfor(self, 20, By.XPATH, "//div/*[contains(text(),'"+account_name+"')]")
    sleep(4)
    self.driver.find_element_by_xpath("//div/*[contains(text(),'"+account_name+"')]").click()
    fprint(self, "Clicking on Inbox")
    if waitfor(self, 5, By.XPATH, "//span[contains(text(), 'Inbox')]//ancestor::a/span/i", False):
        self.driver.find_element_by_xpath("//span[contains(text(), 'Inbox')]//ancestor::a/span/i").click()
    else:
        waitfor(self, 5, By.XPATH, "//div[span/span[contains(text(), 'INBOX')]]", False)
        self.driver.find_element_by_xpath("//div[span/span[contains(text(), 'INBOX')]]").click()
    fprint(self, "Searching for mail with subject "+subject)
    waitfor(self, 20, By.XPATH, "//input[@id='main-input']")
    self.driver.find_element_by_xpath("//input[@id='main-input']").click()
    sleep(2)
    self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys(subject)
    self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
    if Build_Version.__contains__("3."):
        waitfor(self, 20, By.XPATH, "//div[@data-testid='title']//span")
    else:
        waitfor(self, 20, By.XPATH, "//div[@data-testid='title']")
    fprint(self, "Selecting mail with subject "+subject)
    if action == "Create":
        if Build_Version.__contains__("3."):
            if self.driver.find_element_by_xpath("//div[@data-testid='title']//span").text == subject:
                self.driver.find_element_by_xpath("//button[text()='Create Intel']").click()
        elif Build_Version.__contains__("2."):
            if self.driver.find_element_by_xpath("//div[@data-testid='title']").text == subject:
                self.driver.find_element_by_xpath("//button[text()='Create an Intel Package']").click()
    elif action == "Allow":
        self.driver.find_element_by_xpath("//button[text()='Allow Indicators']").click()
    elif action == "View":
        pass

def parse_and_select(self, domain, mail, ioctype):
    """
    Function to parse and create data from mail
    params:
        domain: Type of connection POP or IMAP
        mail: key for subject of mail in threat_mailbox_data.json
        ioctype: IOC Type of the intel to be created
    returns:
        None
    """
    if Build_Version.__contains__("2."):
        sleep(2)
        _ele = self.driver.find_element_by_xpath("//div[contains(text(),'Create an Intel Package')]")
        fprint(self, _ele.value_of_css_property('visibility'))
        if self.driver.find_element_by_xpath("//div[contains(text(),'Create an Intel Package')]"). \
                value_of_css_property('visibility') == 'hidden':
            self.driver.find_element_by_xpath("//button[contains(text(),'Create New Intel Packages')]").click()
            waitfor(self, 10, By.XPATH, "//div[contains(text(),'Create an Intel Package')]")
    if waitfor(self, 2, By.XPATH, "//div[@data-testid='"+ioctype+"']", False):
        self.driver.find_element_by_xpath("//div[@data-testid='"+ioctype+"']").click()
        for i in self.email_data[domain][mail][ioctype]:
            waitfor(self, 20, By.XPATH, "//div[@data-testid='"+ioctype+"']//span[contains(text(),'"+i+"')]")
            fprint(self, "Selecting " + i + " from "+ ioctype)
            self.driver.find_element_by_xpath("//div[@data-testid='"+ioctype+
                                              "']//li[div[following-sibling::span[contains(text(),'"+i+"')]]]").click()
    else:
        ioc_dict = {"Registry Keys": "Windows registry key", "URLs": "URL", "IPv4": "Ipv4 addr", "IPv6": "Ipv6 addr",
                       "Emails": "Email addr", "Domains": "Domain", "SHA224": "SHA-224",
                       "File Paths": "File Path", "SSDeep": "SSDEEP"}
        new_ioctype = ioc_dict[ioctype] if ioctype in ioc_dict else ioctype
        waitfor(self, 20, By.XPATH, "//span[i][following-sibling::div//span[normalize-space(text())='"+new_ioctype+"']]")
        fprint(self, f"Selecting intel of type - {new_ioctype}")
        self.driver.find_element_by_xpath\
            ("//span[i][following-sibling::div//span[normalize-space(text())='"+new_ioctype+"']]").click()
        for i in self.email_data[domain][mail][ioctype]:
            waitfor(self, 20, By.XPATH, "//span[following-sibling::span/span[normalize-space(text())='"+i+"']]")
            self.driver.find_element_by_xpath\
                ("//span[following-sibling::span/span[normalize-space(text())='"+i+"']]").click()
        sleep(1)    # required here


def create_selected_intel(self):
    if Build_Version.__contains__("3."):
        if waitfor(self, 2, By.XPATH, "//button[text()='Create']", False):
            self.driver.find_element_by_xpath("//button[text()='Create']").click()
        else:
            self.driver.find_element_by_xpath("//div[@class='cy-create-intel']//button[text()='Create Intel']").click()
            if waitfor(self, 2, By.XPATH, "//i[@class = 'cyicon-check-o-active']", False):
                verify_success(self, "You can view the created intel as a report object in the Threat Data module", 60)
                fprint(self, "Success alert visible")
                return
            fprint(self, "Clicking on create new alternate intel")
            if waitfor(self, 2, By.XPATH, "//button[text()='Save']", False):    # smaller wait time needed
                self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "You can view the created intel as a report object in the Threat Data module", 60)
    elif Build_Version.__contains__('2.'):
        self.driver.find_element_by_xpath("//button[text()='Create']").click()
        verify_success(self, "You will be notified once Intel Package is created")


def create_intel_metadata(self, **kwargs):
    """
    Function to create intel with metadata
    params:
        object_types: all objects from the mail that need to be created
        title: title of the report to be created
    returns:
        None
    """
    object_types = kwargs.get("object_types")
    title = kwargs.get("title")
    only_report = kwargs.get("only_report", False)
    confidence = kwargs.get("confidence", "20")
    tlp = kwargs.get("TLP", "green")
    tag = kwargs.get("tag", 'all_meta')
    ioc_dict = {"Registry Keys": "Windows registry key", "URLs": "URL", "IPv4": "Ipv4 addr", "IPv6": "Ipv6 addr",
                "Emails": "Email addr", "Domains": "Domain", "SHA224": "SHA-224",
                "File Paths": "File Path", "SSDeep": "SSDEEP"}
    for ioc_type in object_types:
        waitfor(self, 20, By.XPATH,
                f"//span[i][following-sibling::div//span[normalize-space(text())"
                f"='{ioc_dict[ioc_type] if ioc_type in ioc_dict else ioc_type}']]")
        self.driver.find_element_by_xpath \
            (f"//span[i][following-sibling::div//span[normalize-space(text())="
             f"'{ioc_dict[ioc_type] if ioc_type in ioc_dict else ioc_type}']]").click()
        for i in self.email_data["IMAP"]["selective_intel"][ioc_type]:
            fprint(self, f"Selecting {i} from {ioc_type} type")
            waitfor(self, 20, By.XPATH, "//span[following-sibling::span/span[normalize-space(text())='" + i + "']]")
            self.driver.find_element_by_xpath \
                ("//span[following-sibling::span/span[normalize-space(text())='" + i + "']]").click()
    apply_metadata(self, confidence=confidence, tlp=tlp, tag=tag, only_report=only_report)
    fprint(self, "Clicking on create Intel")
    self.driver.find_element_by_xpath("//*[@class='cy-right-modal-content']//button[text()='Create Intel']").click()
    if waitfor(self, 10, By.XPATH, "//div[normalize-space(text())='Create New Report']", False):
        self.driver.find_element_by_xpath("//div[normalize-space(text())='Create New Report']").click()
        sleep(2)    # required
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Enter New Title*']")
        fprint(self, f"Setting report title as {title}")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter New Title*']").send_keys(title)
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, "You can view the created intel as a report object in the Threat Data module")


def apply_metadata(self, confidence, tlp, tag, only_report):
    """
    Function to apply metadata to selected objects
    """
    self.driver.find_element_by_xpath("//button[contains(text(), 'Metadata')]").click()
    fprint(self, f"Selecting TLP as {tlp}")
    waitfor(self, 10, By.XPATH, f"//div[normalize-space(text())='{tlp}']")
    self.driver.find_element_by_xpath("//button[span[normalize-space(text())='Add Tag']]").click()
    sleep(2)  # required
    fprint(self, f"Filling in tag value as {tag}")
    self.driver.find_element_by_xpath("//input[@placeholder='Search Tags']").send_keys(tag)
    waitfor(self, 10, By.XPATH, "//button[normalize-space(text())='+ Add Tag']")
    self.driver.find_element_by_xpath("//button[normalize-space(text())='+ Add Tag']").click()
    sleep(2)    # required
    self.driver.find_element_by_xpath(f"//div[normalize-space(text())='{tlp}']").click()
    waitfor(self, 5, By.XPATH, "//span[text()='Score']/following-sibling::div/input")
    sleep(2)    # required
    fprint(self, f"Filling in confidence score value as {confidence}")
    clear_field(self.driver.find_element_by_xpath("//span[text()='Score']/following-sibling::div/input"))
    self.driver.find_element_by_xpath("//span[text()='Score']/following-sibling::div/input").send_keys(int(confidence))
    if only_report and waitfor(self, 20, By.XPATH, "//span[text()='Apply Metadata to all objects']/preceding-sibling::span/"
                                "input[@value='true']", False):
        fprint(self, "Unchecking metadata for all objects")
        self.driver.find_element_by_xpath("//div[span[text()='Apply Metadata to all objects']]").click()
    elif only_report is False and waitfor(self, 20, By.XPATH, "//span[text()='Apply Metadata to all objects']/preceding-sibling::span/"
                                "input[@value='false']", False):
        fprint(self, "Unchecking metadata for all objects")
        self.driver.find_element_by_xpath("//div[span[text()='Apply Metadata to all objects']]").click()


def read_mail_file(self, file_name):
    """
        Function to open up the contents of a file in mailbox
        params:
            name: name of the file to be read
    """
    if waitfor(self, 10, By.XPATH, f"//span[normalize-space(text())='{file_name}']/ancestor::div[@role='button']", False):
        self.driver.find_element_by_xpath\
            (f"//span[normalize-space(text())='{file_name}']/ancestor::div[@role='button']").click()
        return 1
    else:
        fprint(self, "Expected file not found")
        return 0
