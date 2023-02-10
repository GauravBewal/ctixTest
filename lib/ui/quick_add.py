from lib.ui.nav_threat_data import *
from selenium.webdriver.common.action_chains import ActionChains

meta_title = "metadata intel"
sdo_title_confidence = "221.112.112.134"
sdo_title_description = "221.112.112.135"
sdo_title_tlp = "221.112.112.136"
sdo_title_tag = "221.112.112.137"


def add_sdo_from_csv(self, title, intel_type):
    """
    Function to add all SDO types from quick add

    params:
        type: type of intel creation (Intel/Draft)
    """
    sleep(1)
    fprint(self, "Clicking on New")
    waitfor(self, 20, By.XPATH, "//button[text()=' New']")
    self.driver.find_element_by_xpath("//button[text()=' New']").click()
    fprint(self, "Selecting Quick Add Intel from the dropdown mwnu")
    waitfor(self, 5, By.XPATH, "//li/div[contains(text(),'Quick Add Intel')]")
    self.driver.find_element_by_xpath("//li/div[contains(text(),'Quick Add Intel')]").click()
    fprint(self, "Clicked on the 'Quick Add Intel' option")
    waitfor(self, 10, By.XPATH, "(//div[contains(text(),'Quick Add Intel')])[1]")
    fprint(self, "Clicking on Domain Objects panel under quick add")
    sleep(2)
    self.driver.find_element_by_xpath("//div/span[contains(text(), 'Domain Objects')]").click()
    fprint(self, "Filling in the name for package to be created")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").click()
    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(title + "_" + intel_type)
    filename = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds", "quick_add_sdo_list.csv")
    with open(filename, 'r') as obj:
        data = csv.reader(obj)
        for sdo in data:
            sleep(2)
            fprint(self, "Selecting " + sdo[0] + " from list of SDO")
            self.driver.find_element_by_xpath("//div/div[contains(text(), '" + sdo[0] + "')]").click()
            sleep(1)
            fprint(self, "Clicking on checkbox for " + sdo[0])
            self.driver.find_element_by_xpath("//div[contains(text(), '" + sdo[0] + "')]//span").click()
            sleep(1)
            if sdo[0] == "Location":
                fprint(self, "Selecting Latitude - Longitude from the radio options")
                waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Latitude - Longitude')]")
                self.driver.find_element_by_xpath("//div[contains(text(), 'Latitude - Longitude')]").click()
                sleep(1)
                fprint(self, "Setting the value of latitude")
                self.driver.find_element_by_xpath("//input[@name='latitude']").click()
                self.driver.find_element_by_xpath("//input[@name='latitude']").send_keys(sdo[1])
                fprint(self, "Setting the value for longitude")
                self.driver.find_element_by_xpath("//input[@name='longitude']").click()
                self.driver.find_element_by_xpath("//input[@name='longitude']").send_keys(sdo[2])
            else:
                fprint(self, "Setting the title for " + sdo[0] + " object to " + sdo[1])
                self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").click()
                sleep(1)
                self.driver.find_element_by_xpath \
                    ("//textarea[@aria-placeholder='Value(s)']").send_keys(sdo[1] + "_" + intel_type)
    fprint(self, "[Passed] Added add SDO's in the file to Quick add")
    if intel_type == 'intel':
        fprint(self, "Clicking on Create Intel for data created")
        waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Create Intel')]")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Create Intel')]").click()
        if Build_Version.__contains__("3."):
            verify_success(self, "You can view the created intel as a report object in the Threat Data module")
        else:
            verify_success(self, "You will be notified once the STIX package is created")
        fprint(self, "[Passed] Request for Create Intel sent successfully")
    elif intel_type == "draft":
        fprint(self, "Clicking on Draft for data created")
        waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Draft')]")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Draft')]").click()
        verify_success(self, "STIX package draft created successfully")
        fprint(self, "[Passed] Request for draft creation sent successfully")
    waitfor(self, 20, By.XPATH, "//span[contains(text(), 'Quick Add History')]")


def quick_add_redirect(self, title, intel_type):
    """
    Function to redirect to package from quick add history

    params:
        type: type of intel creation (Intel/Draft)
    """
    fprint(self, "[Passed] Quick add History slider is open")
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
    # self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
    clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']"))
    fprint(self, "Searching for the created package")
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']"). \
        send_keys(title + "_" + intel_type)
    self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
    sleep(2)
    wait_for_history(self, title, intel_type)


def validate_package_objects(self):
    """
    Validate if package has all expected domain objects
    """
    filename = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds", "quick_add_sdo_list.csv")
    with open(filename, 'r') as obj:
        data = csv.reader(obj)
        for sdo in data:
            fprint(self, "Validating if " + sdo[3] + " object is present in created package")
            waitfor(self, 20, By.XPATH, "//div[span[contains(text(), '" + sdo[3] + "')]]")
            self.driver.find_element_by_xpath("//div[span[contains(text(), '" + sdo[3] + "')]]").click()
            fprint(self, "[Passed] " + sdo[3] + " object is found in the created package")


def validate_threat_data(self, intel_type):
    """
    Validate if created SDO are present in threat data
    """
    filename = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds", "quick_add_sdo_list.csv")
    with open(filename, 'r') as obj:
        data = csv.reader(obj)
        for sdo in data:
            if sdo[0] == 'Location':
                continue
            else:
                get_threat_data(self, sdo[0], sdo[1] + "_" + intel_type)


def validate_draft_objects(self):
    """
    Function to validate if all SDO are present in the created Draft
    """
    filename = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds", "quick_add_sdo_list.csv")
    with open(filename, 'r') as obj:
        data = csv.reader(obj)
        for sdo in data:
            _object = sdo[0]
            if sdo[0] == 'Location':
                fprint(self, "Validating draft for created " + sdo[0] + " object")
                waitfor(self, 20, By.XPATH, "//div[span[contains(text(), '" + sdo[0] + "')]]")
                self.driver.find_element_by_xpath("//div[span[contains(text(), '" + sdo[0] + "')]]").click()
                waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Location: " + sdo[1] + ", " + sdo[2] + "')]")
                fprint(self, "[Passed] Created " + sdo[0] + " object found in the draft")
                continue
            if sdo[0] == 'Course of Action':
                _object = "Course of action"
            else:
                fprint(self, "Validating draft for created " + sdo[0] + " object")
                waitfor(self, 20, By.XPATH, "//div[span[contains(text(), '" + _object + "')]]")
                sleep(1)
                self.driver.find_element_by_xpath("//div[span[contains(text(), '" + _object + "')]]").click()
                waitfor(self, 20, By.XPATH, "//div[contains(text(), '" + sdo[1] + "_draft')]")
                fprint(self, "[Passed] Created " + sdo[0] + " object found in the draft")
    fprint(self, "[Passed] All selected SDO are present in created Draft")


def validate_redirect_package_page(self, title):
    """
        Validating details on the redirected page
        params:
            title: title of the created package
    """
    fprint(self, "Clicking on View for created Intel")
    waitfor(self, 20, By.XPATH, "//li[contains(text(), 'View')]")
    self.driver.find_element_by_xpath("//li[contains(text(), 'View')]").click()
    waitfor(self, 20, By.XPATH, "//div[contains(text(), '" + title + "')]")
    fprint(self, "Redirecting to Intel Packages")
    nav_menu_main(self, "Intel Packages")
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
    fprint(self, "Searching for the created Intel Package")
    clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']"))
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(title + "")
    sleep(2)
    self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
    waitfor(self, 20, By.XPATH, "//div[span[@data-testid='title' and contains(text(), '" + title + "')]]")
    self.driver.find_element_by_xpath("//div[span[@data-testid='title' and contains(text(), '" + title + "')]]").click()
    fprint(self, "Details page for the created package loading successfully")
    sleep(2)
    waitfor(self, 20, By.XPATH, "//div[@data-testid='title' and contains(text(), '" + title + "')]")
    fprint(self, "Clicking on Domain objects in the created package")
    waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Domain Objects')]]")
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Domain Objects')]]").click()
    waitfor(self, 20, By.XPATH, "//div[p[contains(text(), 'Domain Objects')]]")
    fprint(self, "Domain objects page for created package loaded successfully")


def wait_for_history(self, title, intel_type):
    """
    Waiting for feed creation in quick add history
    params:
        title: Title of added intel
        intel_type: Type of Intel Created (Intel or Draft)
    """
    for i in range(12):
        fprint(self, title + "_" + intel_type)
        if waitfor(self, 5, By.XPATH, "//span[contains(text(), "+ title + "_" + intel_type +
                                      ")]/ancestor::tr/td//span[contains(text(), 'Failed')]", False):
            raise Exception("[Failed] Package creation failed")
        elif intel_type == 'intel' and \
                waitfor(self, 5, By.XPATH, "//span[contains(text(), " + title + "_" + intel_type +
                                           ")]/ancestor::tr/td//span[contains(text(), 'Created')]", False):
            fprint(self, "Redirecting to the created intel package")
            break
        elif intel_type == 'draft' and \
                waitfor(self, 5, By.XPATH, "//span[contains(text(), " + title + "_" + intel_type +
                                           ")]/ancestor::tr/td//span[contains(text(), 'Draft')]", False):
            fprint(self, "Redirecting to the created draft package")
            break
        elif i == 11:
            raise Exception("[Failed] Package creation taking longer than expected ")
        fprint(self, "Refreshing quick add history")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Refresh')]").click()
    if not Build_Version.__contains__("3."):
        self.driver.find_element_by_xpath("//span[contains(text(), " + title + "_" + intel_type +
                                      ")]/ancestor::tr/td//button").click()
    sleep(1)


def get_object_details(csv_file):
    sdo_dict = {}
    filename = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds", csv_file)
    with open(filename, 'r') as obj:
        data = csv.reader(obj)
        for sdo in data:
            sdo_dict[sdo[0]] = sdo[1]
    return sdo_dict


def add_metadata(self, confidence=None, tlp=None, tag=None, description=None):
    """
    Add metadata to createc intel via quick add

    Args:
        self: driver object for execution
        confidence: source confidence for created intel
        tlp: tlp of the Intel being created
        tag: tags to be applied to intel created
        description: description to be added to created intel
    """
    actions = ActionChains(self.driver)
    self.driver.find_element_by_xpath("//div[contains(text(), 'Add Metadata')]").click()
    sleep(2)
    if confidence:
        fprint(self, "Setting Confidence to "+str(confidence))
        _ele = self.driver.find_element_by_xpath("//span[contains(text(),'high')]")
        self.driver.find_element_by_xpath("//div[contains(@class,'el-slider__button')]").click()
        fprint(self, "Clicked on te slider")
        sleep(1)
        actions.move_to_element(_ele).perform()
        fprint(self, "Moved to an element")
        sleep(5)
        clear_field(self.driver.find_element_by_xpath("//span[text()='Score']/following-sibling::div/input"))
        self.driver.find_element_by_xpath("//span[text()='Score']/following-sibling::div/input").send_keys(confidence)
        fprint(self, "[Passed] Confidence set to "+str(confidence)+" successfully")
    if tlp:
        sleep(2)
        fprint(self, "Setting TLP to "+tlp)
        self.driver.find_element_by_xpath("//div[contains(text(), '"+tlp+"')]/div/input[@type='radio']").click()
        fprint(self, "[Passed] TLP set to "+tlp+" successfully")
    if tag:
        fprint(self, 'Setting tag to '+tag)
        self.driver.find_element_by_xpath("//button[span[contains(text(), 'Add Tag')]]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//input[@placeholder='Search Tags']").send_keys(tag)
        if waitfor(self, 20, By.XPATH, "//div[text()='"+tag+"']", False):
            self.driver.find_element_by_xpath("//div[text()='"+tag+"']").click()
        elif waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Add Tag')]"):
            self.driver.find_element_by_xpath("//button[contains(text(), 'Add Tag')]").click()
        fprint(self, "[Passed] "+tag+" tag added to intel successfully")
    if description:
        fprint(self, "Setting Description for intel")
        self.driver.find_element_by_xpath("//div/textarea[@name='description']").click()
        self.driver.find_element_by_xpath("//div/textarea[@name='description']").send_keys(description)
        fprint(self, "[Passed] Description for intel is set successfully")


def quick_create_ip(self, ip, title, metadata_confidence=80):
    """
    Quick create intel with IP

    Args:
        ip:
        title:
    """
    #Todo: This code needs to be revamped properly
    actions = ActionChains(self.driver)
    fprint(self, "Navigating to the Threat Data page")
    nav_menu_main(self, 'Threat Data')
    fprint(self, "Clicking on New")
    waitfor(self, 20, By.XPATH, "//button[text()=' New']")
    self.driver.find_element_by_xpath("//button[text()=' New']").click()
    fprint(self, "Selecting Quick Add Intel from the dropdown mwnu")
    waitfor(self, 5, By.XPATH, "//li/div[contains(text(),'Quick Add Intel')]")
    self.driver.find_element_by_xpath("//li/div[contains(text(),'Quick Add Intel')]").click()
    fprint(self, "Clicked on the 'Quick Add Intel' option")
    waitfor(self, 10, By.XPATH, "(//div[contains(text(),'Quick Add Intel')])[1]")
    fprint(self, "Filling in the name for package to be created")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").click()
    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(title)
    fprint(self, "Setting the title for Indictaor object to " + ip)
    self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").click()
    sleep(1)
    self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").send_keys(ip)
    if metadata_confidence == 0:
        add_metadata(self, confidence="0", tlp="Red", tag='filterTag', description="meta description")
    else:
        add_metadata(self, confidence=metadata_confidence, tlp="Red", tag='automatetag', description="meta description")
    fprint(self, "Clicking on Create Intel for data created")
    waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Create Intel')]")
    sleep(2)
    self.driver.find_element_by_xpath("//button[contains(text(), 'Create Intel')]").click()
    if Build_Version.__contains__("3."):
        verify_success(self, "You can view the created intel as a report object in the Threat Data module")
    else:
        verify_success(self, "You will be notified once the STIX package is created", 15)
    fprint(self, "[Passed] Request for Create Intel sent successfully")
    fprint(self, "Waiting for intel to be with Created Status")
    repeat = 1
    while repeat <= 6:
        if waitfor(self, 20, By.XPATH, "//span[contains(text(),'" + title + "')]/ancestor::td/following-sibling::td[3]//span[contains(text(),'Created')]",
                   False):
            fprint(self, "[Passed] Created Status of intel is visible - " + title)
            self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
            break
        else:
            if Build_Version.__contains__("3.0"):
                self.driver.find_element_by_xpath("//button[contains(text(),'Refresh')]").click()
                fprint(self, "Created Status of intel is not visible, Clicked on the Refresh Button")
            else:
                fprint(self, "Created status for intel not visible, Redirecting back to Quick Add History")
                self.driver.find_element_by_xpath("//span[contains(text(), 'Quick Add History')]").click()
                waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Quick Add History')]")
                self.driver.find_element_by_xpath("//button[contains(text(), 'Quick Add History')]").click()
            if repeat == 6:
                self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
                fprint(self, "[Failed] Intel is not found with Created Status")
            repeat = repeat + 1
    self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
    fprint(self, "Waiting for 30 seconds...")
    sleep(30)


def quick_add_intel_with_ioc_sdo(self, ioc_type, title, ioc_value, sdo_type, sdo_value, metadata_confidence=80):
    fprint(self, "Clicking on the New Button")
    waitfor(self, 20, By.XPATH, "//button[text()=' New']")
    self.driver.find_element_by_xpath("//button[text()=' New']").click()
    waitfor(self, 20, By.XPATH, "//li/*[contains(text(), 'Quick Add Intel')]")
    fprint(self, "Clicking on the Quick Add Intel from the dropdown menu")
    sleep(1)
    self.driver.find_element_by_xpath("//li/*[contains(text(), 'Quick Add Intel')]").click()
    waitfor(self, 20, By.XPATH, qai_ioc_type_search)
    clear_field(self.driver.find_element_by_xpath(qai_ioc_type_search))
    fprint(self, "Searching IOC - " + ioc_type)
    self.driver.find_element_by_xpath(qai_ioc_type_search).click()
    self.driver.find_element_by_xpath(qai_ioc_type_search).send_keys(ioc_type)
    waitfor(self, 10, By.XPATH, "//div[contains(text(),'" + ioc_type + "')]/ancestor::div[1]")
    fprint(self, "IOC is visible, selecting it")
    self.driver.find_element_by_xpath("//div[contains(text(),'" + ioc_type + "')]/div[1]/div").click()
    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(title)
    fprint(self, "Entered Title - "+title)
    self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").send_keys(ioc_value)
    fprint(self, "Entered IOC Value - " + ioc_value)
    sleep(1)
    fprint(self, "Switching to the Domain Objects to add relation with the Domain")
    self.driver.find_element_by_xpath("//div[@id='tab-sdos']").click()
    waitfor(self, 20, By.XPATH, qai_ioc_type_search)
    clear_field(self.driver.find_element_by_xpath(qai_ioc_type_search))
    fprint(self, "Searching SDO - " + sdo_type)
    self.driver.find_element_by_xpath(qai_ioc_type_search).click()
    self.driver.find_element_by_xpath(qai_ioc_type_search).send_keys(sdo_type)
    waitfor(self, 10, By.XPATH, "//div[contains(text(),'" + sdo_type + "')]/ancestor::div[1]")
    fprint(self, "SDO is visible, selecting it")
    self.driver.find_element_by_xpath("//div[contains(text(),'" + sdo_type + "')]/div[1]/div").click()
    self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").send_keys(sdo_value)
    fprint(self, "Adding Metadata values")
    if metadata_confidence == 0:
        add_metadata(self, confidence="0", tlp="Red", tag='automatetag', description="meta description")
    else:
        add_metadata(self, confidence=metadata_confidence, tlp="Red", tag='automatetag', description="meta description")
    self.driver.find_element_by_xpath("//button[contains(text(),'Create Intel')]").click()
    fprint(self, "Clicked on the Create Intel Button")
    if Build_Version.__contains__("3."):
        verify_success(self, "You can view the created intel as a report object in the Threat Data module")
    else:
        verify_success(self, "You will be notified once the STIX package is created", 15)
    fprint(self, "[Passed] Request for Create Intel sent successfully")
    fprint(self, "Waiting for the Intel Status - Created")
    repeat = 1
    while repeat <= 6:
        if waitfor(self, 20, By.XPATH, "//span[contains(text(),'" + title + "')]/ancestor::td/following-sibling::td[3]//span[contains(text(),'Created')]",
                   False):
            fprint(self, "[Passed] Created Status of intel is visible - " + title)
            self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
            break
        else:
            if Build_Version.__contains__("3.0"):
                self.driver.find_element_by_xpath("//button[contains(text(),'Refresh')]").click()
                fprint(self, "Created Status of intel is not visible, Clicked on the Refresh Button")
            else:
                fprint(self, "Created status for intel not visible, Redirecting back to Quick Add History")
                self.driver.find_element_by_xpath("//span[contains(text(), 'Quick Add History')]").click()
                waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Quick Add History')]")
                self.driver.find_element_by_xpath("//button[contains(text(), 'Quick Add History')]").click()
            if repeat == 6:
                self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
                fprint(self, "[Failed] Intel is not found with Created Status")
            repeat = repeat + 1
    self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
    sleep(1)


def quick_add_domain_object(self, type, title, value):
    fprint(self, "Clicking on the New Button")
    waitfor(self, 20, By.XPATH, "//button[text()=' New']")
    self.driver.find_element_by_xpath("//button[text()=' New']").click()
    waitfor(self, 20, By.XPATH, "//li/div[contains(text(), 'Quick Add Intel')]")
    fprint(self, "Clicking on the Quick Add Intel from the dropdown menu")
    waitfor(self, 20, By.XPATH, "//li/div[contains(text(), 'Quick Add Intel')]")
    self.driver.find_element_by_xpath("//li/div[contains(text(), 'Quick Add Intel')]").click()
    waitfor(self, 20, By.XPATH, "//span[contains(text(),'Domain Objects')]")
    self.driver.find_element_by_xpath("//span[contains(text(),'Domain Objects')]").click()
    waitfor(self, 20, By.XPATH, qai_ioc_type_search)
    clear_field(self.driver.find_element_by_xpath(qai_ioc_type_search))
    fprint(self, "Searching Object - " + type)
    ele = self.driver.find_element_by_xpath(qai_ioc_type_search)
    self.driver.execute_script("arguments[0].click();", ele)
    self.driver.find_element_by_xpath(qai_ioc_type_search).send_keys(type)
    waitfor(self, 10, By.XPATH, "//div[contains(text(),'" + type + "')]/ancestor::div[1]")
    fprint(self, "IOC is visible, selecting it")
    self.driver.find_element_by_xpath("//div[contains(text(),'" + type + "')]/div[1]/div").click()
    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(title)
    fprint(self, "Entered Title - " + title)

    if type == 'Location':
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'Clear All')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Clear All')]").click()
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Countries')]//preceding-sibling::div/input[@type='radio']")
        self.driver.find_element_by_xpath(
            "//div[contains(text(),'Countries')]//preceding-sibling::div/input[@type='radio']").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Countries*')]")
        ele = self.driver.find_element_by_xpath("//span[contains(text(),'Countries*')]")
        ActionChains(self.driver).click(ele).perform()
        self.driver.find_element_by_xpath(
            "//span[contains(text(),'Countries')]//following::input[@placeholder='Search']").send_keys(value)
        waitfor(self, 20, By.XPATH, "//li//div[text()='" + value + "']")
        self.driver.find_element_by_xpath("//li//div[text()='" + value + "']").click()
    else:
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").send_keys(value)
        fprint(self, "Entered IOC Value - " + value)
        sleep(1)
    self.driver.find_element_by_xpath("//button[contains(text(),'Create Intel')]").click()
    fprint(self, "Clicked on the Create Intel Button")
    if Build_Version.__contains__("3."):
        verify_success(self, "You can view the created intel as a report object in the Threat Data module")
    else:
        verify_success(self, "You will be notified once the STIX package is created", 15)
    fprint(self, "[Passed] Request for Create Intel sent successfully")
    fprint(self, "Waiting for the Intel Status - Created")
    repeat = 1
    while repeat <= 6:
        if waitfor(self, 20, By.XPATH,
                   "//span[contains(text(),'" + title + "')]/ancestor::td/following-sibling::td[3]//span[contains(text(),'Created')]",
                   False):
            fprint(self, "[Passed] Created Status of intel is visible - " + title)
            self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
            break
        else:
            if Build_Version.__contains__("3.0"):
                self.driver.find_element_by_xpath("//button[contains(text(),'Refresh')]").click()
                fprint(self, "Created Status of intel is not visible, Clicked on the Refresh Button")
            else:
                fprint(self, "Created status for intel not visible, Redirecting back to Quick Add History")
                self.driver.find_element_by_xpath("//span[contains(text(), 'Quick Add History')]").click()
                waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Quick Add History')]")
                self.driver.find_element_by_xpath("//button[contains(text(), 'Quick Add History')]").click()
            if repeat == 6:
                self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
                fprint(self, "[Failed] Intel is not found with Created Status")
            repeat = repeat + 1
    self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()


def create_intel(self, type, title, value, **kwargs):
    meta_tag = kwargs.get("tags", None)
    meta_tlp = kwargs.get("tlp", None)
    meta_desc = kwargs.get("description", None)
    meta_conf = kwargs.get("confidence", None)
    fprint(self, "Clicking on the New Button")
    waitfor(self, 20, By.XPATH, "//button[text()=' New']")
    self.driver.find_element_by_xpath("//button[text()=' New']").click()
    waitfor(self, 20, By.XPATH, "//li/*[contains(text(), 'Quick Add Intel')]")
    fprint(self, "Clicking on the Quick Add Intel from the dropdown menu")
    sleep(1)
    self.driver.find_element_by_xpath("//li/*[contains(text(), 'Quick Add Intel')]").click()
    waitfor(self, 20, By.XPATH, qai_ioc_type_search)
    clear_field(self.driver.find_element_by_xpath(qai_ioc_type_search))
    fprint(self, "Searching IOC - " + type)
    self.driver.find_element_by_xpath(qai_ioc_type_search).click()
    self.driver.find_element_by_xpath(qai_ioc_type_search).send_keys(type)
    waitfor(self, 10, By.XPATH, "//div[contains(text(),'" + type + "')]/ancestor::div[1]")
    fprint(self, "IOC is visible, selecting it")
    self.driver.find_element_by_xpath("//div[contains(text(),'" + type + "')]/div[1]/div").click()
    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(title)
    fprint(self, "Entered Title - " + title)
    self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").send_keys(value)
    fprint(self, "Entered IOC Value - " + value)
    sleep(1)
    add_metadata(self, tag=meta_tag, tlp=meta_tlp, description=meta_desc, confidence=meta_conf)
    self.driver.find_element_by_xpath("//button[contains(text(),'Create Intel')]").click()
    fprint(self, "Clicked on the Create Intel Button")
    if Build_Version.__contains__("3."):
        verify_success(self, "You can view the created intel as a report object in the Threat Data module",20)
    else:
        verify_success(self, "You will be notified once the STIX package is created", 15)
    fprint(self, "[Passed] Request for Create Intel sent successfully")
    fprint(self, "Waiting for the Intel Status - Created")
    repeat = 1
    while repeat <= 6:
        if waitfor(self, 20, By.XPATH,
                   "//span[contains(text(),'" + title + "')]/ancestor::td/following-sibling::td[3]//span[contains(text(),'Created')]",
                   False):
            fprint(self, "[Passed] Created Status of intel is visible - " + title)
            self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
            break
        else:
            if Build_Version.__contains__("3.0"):
                self.driver.find_element_by_xpath("//button[contains(text(),'Refresh')]").click()
                fprint(self, "Created Status of intel is not visible, Clicked on the Refresh Button")
            else:
                fprint(self, "Created status for intel not visible, Redirecting back to Quick Add History")
                self.driver.find_element_by_xpath("//span[contains(text(), 'Quick Add History')]").click()
                waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Quick Add History')]")
                self.driver.find_element_by_xpath("//button[contains(text(), 'Quick Add History')]").click()
            if repeat == 6:
                self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
                fprint(self, "[Failed] Intel is not found with Created Status")
            repeat = repeat + 1
    self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
    sleep(1)
