from lib.common_functions import *
from selenium.webdriver.common.by import *
from selenium import *
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

"""
This is support library for Tags
"""
from lib.ui.nav_app import *

count = 0
wait_time = 0


def tags_left_menu(self, itemname):
    """
    Click on left menu items in Tags
    """
    self.driver.find_element_by_xpath("//span[contains(text(),'"+itemname+"')]").click()
    fprint(self, "[Passed], Clicked on Left Menu item: " + itemname)


def get_threat_data(self, sdo_type, sdo_title):
    """
    Function to search threat data based on sdo type and title

    params:
        sdo_type: Type of the SDO being queried
        sdo_title: title of the object being queried
    """
    if not waitfor(self, 20, By.XPATH, "//div[h1[contains(text(), 'Threat Data')]]", False):
        fprint(self, "Redirecting to threat Data")
        self.driver.find_element_by_xpath("//i[@class='cyicon-menu']").click()
        waitfor(self, 20, By.XPATH, "//div/span/span[contains(text(), 'Threat Data')]")
        sleep(2)
        self.driver.find_element_by_xpath("//span[contains(text(),'Threat Data')]/ancestor::a").click()
    waitfor(self, 20, By.XPATH, "//li/a/span[contains(text(), '"+sdo_type+"')]")
    fprint(self, "[Passed] Threat Data redirection successful")
    fprint(self, "Clicking on "+sdo_type+" under domain objects")
    self.driver.find_element_by_xpath("//li/a/span[contains(text(), '"+sdo_type+"')]").click()
    waitfor(self, 20, By.XPATH, "//div/div[contains(text(), '"+sdo_type+"')]")
    fprint(self, "[Passed]"+sdo_type+" page under Threat Data loaded successfully")
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
    clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']"))
    fprint(self, "Searching for "+sdo_title+" under "+sdo_type+" objects")
    self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(sdo_title)
    waitfor(self, 20, By.XPATH, "//div[i[@data-testid='filter-search-icon']]")
    fprint(self, "Clicking on the created "+sdo_type+" object")
    self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
    waitfor(self, 20, By.XPATH, "//div[span[@data-testid='name2' and contains(text(), '"+sdo_title+"')]]")
    self.driver.find_element_by_xpath("//div[span[@data-testid='name2' and contains(text(), '"+sdo_title+"')]]").click()
    waitfor(self, 20, By.XPATH, "//div[@data-testid='name2' and contains(text(), '"+sdo_title+"')]")
    fprint(self, "[Passed] Details page for "+sdo_type+" object named "+sdo_title+" loaded successfully")


def validate_tag(self, tag):
    """
    Validate if selected tag is attached to given threat data
    """
    fprint(self, "Validating tag added in intel")
    if Build_Version.__contains__("3."):
        if waitfor(self, 5, By.XPATH, "//button/span[contains(text(), '+ ')]", False):
            self.driver.find_element_by_xpath("//button/span[contains(text(), '+ ')]").click()
        waitfor(self, 10, By.XPATH, "//span[contains(text(), '"+tag+"')]")
    else:
        waitfor(self, 10, By.XPATH, "//div[@trigger='hover'][contains(text(), '"+tag+"')]")
    fprint(self, '[Passed] Tag '+tag+' is added to SDO successfully')


def validate_tlp(self, tlp):
    """
    Validate if tlp applied to the data is valid
    """
    if Build_Version.__contains__("3."):
        _tlp_xpath = "//*[span[contains(text(),'TLP')]]//following-sibling::div//span/span"
        waitfor(self, 10, By.XPATH, _tlp_xpath)
        if not self.driver.find_element_by_xpath(_tlp_xpath).text.upper() == tlp.upper():
            fprint(self, f"[Failed] TLP for SDO does not match expected tlp - {tlp}")
            self.fail(f"TLP for SDO does not match expected tlp")
    else:
        waitfor(self, 10, By.XPATH, "//p[contains(text(),'Assign TLP')]/following-sibling::div//div[contains(text(), "
                                    "'"+tlp.upper()+"')]")
    fprint(self, '[Passed] TLP'+tlp+' is added to SDO successfully')


def validate_confidence(self, confidence):
    """
    Validate if confidence applied to the data is valid
    """
    if Build_Version.__contains__('3.0'):
        self.driver.find_element_by_xpath("//span[contains(text(), 'Key Evidence')]").click()
    else:
        self.driver.find_element_by_xpath("//p[contains(text(), 'Key Evidence')]").click()
    waitfor(self, 10, By.XPATH, "//div[contains(text(), 'Key Evidence')]")
    waitfor(self, 10, By.XPATH, "//td//span[contains(text(), '"+confidence+"')]")
    fprint(self, "[Passed] Source confidence is added to SDO successfully")
    self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
    sleep(2)


def validate_description(self, description):
    """
    Validate if description applied to the data is valid
    """
    waitfor(self, 10, By.XPATH, "//div[span[contains(text(), 'Description')]]//div[@aria-haspopup='list']/button")
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Description')]]//div[@aria-haspopup='list']/button")\
        .click()
    sleep(2)
    self.driver.find_element_by_xpath("//li/span[contains(text(), 'Import')]").click()
    sleep(1)
    _d = str(self.driver.find_element_by_xpath("//div[@data-testid='description']").text)
    if _d == str(description):
        fprint(self, "[Passed] Description for the SDO matches the one added")
    else:
        fprint(self, "[Failed] Description of the SDO does not match, Expected: " + str(description) + " Received: " + _d)


def verify_data_in_threatdata(self, value, source):
    fprint(self, "Waiting for the Search Bar")
    waitfor(self, 20, By.XPATH, threat_data_main_search_field)
    fprint(self, "Searching for the Feed under Indicator - "+value)
    clear_field(self.driver.find_element_by_xpath(threat_data_main_search_field))
    self.driver.find_element_by_xpath(threat_data_main_search_field).click()
    # clear_field(self.driver.find_element_by_xpath(threat_data_main_search_field))
    self.driver.find_element_by_xpath(threat_data_main_search_field).send_keys(value)
    if Build_Version.__contains__("2.9"):
        self.driver.find_element_by_xpath("//span[contains(text(),'Press enter or click to search')]").click()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+value+"')]")
    elif Build_Version.__contains__("3."):
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+source+"')]/ancestor::tr/td[3]//span[contains(text(),'"+value+"')]")
    fprint(self, "Feed Visible - " + value)


def beforeVerifying_PolledData(self, sdo, tempflag=0):
    from lib.ui.nav_app import nav_menu_main
    if waitfor(self, 5, By.XPATH, "(//span[contains(text(),'Threat Data')])[2]", False):
        fprint(self, "Threat Data page is visible")
    else:
        fprint(self, "Navigating to the Threat Data page")
        nav_menu_main(self, "Threat Data")
    if tempflag == 0:
        self.driver.refresh()
    fprint(self, "Waiting for the Search Bar")
    waitfor(self, 20, By.XPATH, threat_data_main_search_field)
    # fprint(self, "Opening 'Object Type' Accordion")
    self.driver.find_element_by_xpath("//div[@data-testid='object_type']").click()
    fprint(self, " Dropdown opened, waiting for the " + sdo + " Option to click")
    if sdo == "Malware":
        waitfor(self, 5, By.XPATH, "(//div[contains(text(),'" + sdo + "')]/ancestor::li[1])[3]")
        self.driver.find_element_by_xpath("(//div[contains(text(),'" + sdo + "')]/ancestor::li[1])[3]").click()
        fprint(self, "Clicked on the " + sdo + " Option")
        # self.driver.find_element_by_xpath("//button[contains(text(),'Apply')]").click()
        # fprint(self, "Clicked on the Apply Button")
    else:
        waitfor(self, 5, By.XPATH, "(//div[contains(text(),'" + sdo + "')]/ancestor::li[1])[2]")
        self.driver.find_element_by_xpath("(//div[contains(text(),'" + sdo + "')]/ancestor::li[1])[2]").click()
        fprint(self, "Clicked on the " + sdo + " Option")
        # self.driver.find_element_by_xpath("//button[contains(text(),'Apply')]").click()
        # fprint(self, "Clicked on the Apply Button")
    sleep(1)


def verify_polleddata_in_threatdata(self, source_name, csv_file):
    if csv_file == "quick_add_intel_data.csv":
        file_name = os.path.join(os.environ["PYTHONPATH"], "testdata", csv_file)
    else:
        file_name = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds", csv_file)
    if not Build_Version.__contains__("3."):
        self.driver.refresh()
        fprint(self, "Waiting for the Indicator Tab")
        waitfor(self, 20, By.XPATH, "//span[text()='Indicator']")
    with open(file_name, 'r') as obj:
        data = csv.reader(obj)
        for file_data in data:
            if not Build_Version.__contains__("3.") and csv_file != "webscraper_data.csv":
                fprint(self, "Clicking on the tab - " + file_data[0])
                self.driver.find_element_by_xpath("//span[text()='" + file_data[0] + "']").click()
            if Build_Version.__contains__("3."):
                fprint(self, "Searching for the Feed under " + file_data[0] + " - " + file_data[1])
                self.driver.find_element_by_xpath(threat_data_main_search_field).click()
                clear_field(self.driver.find_element_by_xpath(threat_data_main_search_field))
                self.driver.find_element_by_xpath(threat_data_main_search_field).send_keys(file_data[1])
                waitfor(self, 10, By.XPATH,
                        "//span[contains(text(),'" + source_name + "')]/ancestor::tr/td[3]//span[contains(text(),'" +
                        file_data[1] + "')]")
                fprint(self, "Feed Visible - " + file_data[1])
                if csv_file == "quick_add_intel_data.csv":
                    break
            else:
                fprint(self, "Waiting for the Search Bar")
                waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
                fprint(self, "Searching for the Feed - " + file_data[1])
                self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
                self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
                self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(
                    file_data[1])
                self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
                waitfor(self, 10, By.XPATH,
                        "//div[contains(text(),'" + source_name + "')]/ancestor::td/preceding::td[1]//span[contains(text(),'" +
                        file_data[1] + "')]")
                fprint(self, "Feed Visible - " + file_data[1])


def verify_threatdata_name(self, sdo, sdo_name, source_name):
    from lib.ui.nav_app import nav_menu_main
    """
        Function to search threat data based on name

        Requirements:
            page for the sdo needs to be loaded (use 'beforeVerifying_PolledData')

        params:
            sdo: type of object being searched
            sdo_name: name pf the sdo to be searched
    """
    # beforeVerifying_PolledData(self, sdo)
    nav_menu_main(self, "Threat Data")
    fprint(self, "Searching for the Feed under " + sdo + " - " + sdo_name)
    self.driver.find_element_by_xpath(threat_data_main_search_field).click()
    clear_field(self.driver.find_element_by_xpath(threat_data_main_search_field))
    self.driver.find_element_by_xpath(threat_data_main_search_field).send_keys(sdo_name)
    if waitfor(self, 10, By.XPATH,
               "//span[contains(text(),'" + source_name + "')]/ancestor::tr/td[3]//span[contains(text(),'" + sdo_name + "')]"):
        fprint(self, "Feed Visible - " + sdo_name)


def click_on_eye_button(self, source, value):
    fprint(self, "Hovering on the row")
    ele = self.driver.find_element_by_xpath("//span[contains(text(),'"+source+"')]/ancestor::tr/td[3]//span[contains(text(),'"+value+"')]")
    ActionChains(self.driver).move_to_element(ele).perform()
    sleep(2)
    self.driver.find_element_by_xpath("//i[contains(@class,'cyicon-eye')]").click()
    fprint(self, "Clicked on the Eye button")


def click_on_intel(self, source, value):
    wait = WebDriverWait(self.driver, 10)
    ele = wait.until(EC.presence_of_element_located((By.XPATH,
                                                     "//span[contains(text(),'"+source+"')]/ancestor::tr/td[3]//span[contains(text(),'"+value+"')]")))
    fprint(self, "Clicking on the Intel - " + value)
    self.driver.execute_script("arguments[0].click();", ele)


def search_object(self, filter_name, object_name):
    global count
    if count == 0:
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'" + filter_name + "')]/parent::div//i[contains(@class,'cyicon-search')]/parent::button")
        self.driver.find_element_by_xpath("//span[contains(text(),'" + filter_name + "')]/parent::div//i[contains(@class,'cyicon-search')]/parent::button").click()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'" + filter_name + "')]/ancestor::div[@role='tab']/following-sibling::div//input[@name='searchbar']")
        fprint(self, "Search Bar is visible")
    fprint(self, "Searching - "+object_name)
    self.driver.find_element_by_xpath("//span[contains(text(),'" + filter_name + "')]/ancestor::div[@role='tab']/following-sibling::div//input[@name='searchbar']").click()
    clear_field(self.driver.find_element_by_xpath("//span[contains(text(),'" + filter_name + "')]/ancestor::div[@role='tab']/following-sibling::div//input[@name='searchbar']"))
    self.driver.find_element_by_xpath("//span[contains(text(),'" + filter_name + "')]/ancestor::div[@role='tab']/following-sibling::div//input[@name='searchbar']").send_keys(object_name)
    waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+object_name+"')]")
    fprint(self, "Searched object is visible - "+object_name)
    count = count + 1


def select_threatData_filter(self, filter_name, object_name="null"):
    fprint(self, "Searching Filter - "+filter_name)
    waitfor(self, 10, By.XPATH, "//button[normalize-space(text())='Reset']/preceding-sibling::div//input")
    clear_field(self.driver.find_element_by_xpath("//button[normalize-space(text())='Reset']/preceding-sibling::div//input"))
    self.driver.find_element_by_xpath("//button[normalize-space(text())='Reset']/preceding-sibling::div//input").click()
    self.driver.find_element_by_xpath("//button[normalize-space(text())='Reset']/preceding-sibling::div//input").send_keys(filter_name)
    sleep(2)
    if filter_name == "Published":
        if waitfor(self, 10, By.XPATH, "//span[contains(text(),'Published Date')]/parent::div", False):
            fprint(self, "Published Date Filter is visible")
            filter_name = "Published Date"
        else:
            waitfor(self, 10, By.XPATH, "//span[contains(text(),'Published on')]/parent::div")
            fprint(self, "Published on Filter is visible")
            filter_name = "Published on"
    fprint(self, "Filter Appear - " + filter_name)
    if filter_name != "Object Type":
        print(filter_name)
        self.driver.find_element_by_xpath(f"//span[contains(text(),'{filter_name}')]/ancestor::div[@role='button']/div").click()
    fprint(self, "Filter accordion opened")
    if object_name != "null":
        search_object(self, filter_name, object_name)
        if object_name == "Indicator":
            self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        elif object_name == "High":
            self.driver.find_element_by_xpath("//li//span[contains(text(),'High')]").click()
        else:
            try:
                self.driver.find_element_by_xpath("//li[@name='select-option']//span[contains(text(),'"+object_name+"')]").click()
                fprint(self, "First click works")
            except:
                self.driver.find_element_by_xpath("(//span[contains(text(),'" + object_name + "')])[2]").click()
                fprint(self, "Tried with second click also")


def validate_all_metadata(self, **kwargs):
    """
    Function to validate all metadata of an intel
    """
    object1 = kwargs.get("object")
    source = kwargs.get("source", "Import")
    tag = kwargs.get("tag", None)
    tlp = kwargs.get("tlp", None)
    confidence = kwargs.get("confidence", None)
    description = kwargs.get("description", None)
    waitfor(self, 20, By.XPATH, f"//span[contains(text(),'{source}')]"
                                f"/ancestor::tr/td[3]//span[contains(text(),'{object1}')]")
    sleep(2)
    _ele = self.driver.find_elements_by_xpath(
        f"//span[contains(text(), '{object1}')]//ancestor::tr")[1]
    ActionChains(self.driver).click(_ele).perform()
    waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
    self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
    if tag:
        fprint(self, f"Validating if tag {tag} is added to {object1}")
        validate_tag(self, tag)
    if tlp:
        fprint(self, f"Validating if TLP attached for {object1} is {tlp}")
        validate_tlp(self, tlp)
    if description:
        fprint(self, f"Validating if description is attached to {object1}")
        validate_description(self, description)
    if confidence:
        fprint(self, f"Validating if confidence is set to {confidence} for {object1} ")
        validate_confidence(self, confidence)


def bulk_ioc_lookup_upload_file(self, fileName):
    global wait_time
    self.driver.find_element_by_xpath("//div[contains(text(),'Bulk IOC lookup')]").click()
    self.driver.find_element_by_xpath("//div[contains(text(),'Bulk IOC lookup')]/input").send_keys(fileName)
    waitfor(self, 10, By.XPATH, "//span[contains(text(),'In Progress')]")
    fprint(self, "Started Uploading - In Progress")
    while wait_time < 60:
        if waitfor(self, 5, By.XPATH, "//button[contains(text(),'Show')]", False):
            fprint(self, "Uploading of File is completed, Show button is visible.")
            break
        else:
            wait_time = wait_time + 5
            if wait_time >= 60:
                fprint(self, "[Failed] - File Upload taking longer time than expected.")
                self.fail("[Failed] - File Upload taking longer time than expected.")
            fprint(self, "Still In Progress, waiting for 5 seconds more...")


def validate_actioned_by_rule(self, intel, rule_name, third_party=False):
    """
        Function to validate if rule is run on intel
    """
    waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                "/ancestor::tr/td[3]//span[contains(text(),'" + intel + "')]")
    sleep(2)
    _ele = self.driver.find_elements_by_xpath(
        "//span[contains(text(), '" + intel + "')]//ancestor::tr")[1]
    ActionChains(self.driver).click(_ele).perform()
    fprint(self, "Clicking on Actions Taken")
    waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Action Taken')]")
    self.driver.find_element_by_xpath("//div[contains(text(), 'Action Taken')]").click()
    if third_party:
        waitfor(self, 20, By.XPATH, "//div[@id='tab-third_party']")
        self.driver.find_element_by_xpath("//div[@id='tab-third_party']").click()
    waitfor(self, 20, By.XPATH, "//span[contains(text(), '" + rule_name + "')]")
