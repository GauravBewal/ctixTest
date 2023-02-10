import os.path
import unittest
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PROJECTS.UI.test_quick_add_intel import ioc_ipv4
from lib.ui.nav_app import *
from lib.ui.nav_threat_data import select_threatData_filter, verify_data_in_threatdata, click_on_intel
indicator_type1 = ["IP", "Hash", "Domain", "URL"]
indicator_type2 = ["IP", "Hash", "Domain", "URL", "Vulnerability"]
enrich_policy1 = ["Enrich_PolicyIP", "Enrich_PolicyHash", "Enrich_PolicyDomain", "Enrich_PolicyURL"]
enrich_policy2 = ["Enrich_PolicyIP", "Enrich_PolicyHash", "Enrich_PolicyDomain", "Enrich_PolicyURL", "Enrich_PolicyVulnerability"]
file = os.path.join(os.environ["PYTHONPATH"], "testdata", "quick_add_intel_data.csv")
file_name = open(file)
csvreader = csv.reader(file_name)
first_row = next(csvreader)
ioc_ip = first_row[1]


class EnrichmentManagement(unittest.TestCase):

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

    def search_policy(self, item):
        fprint(self, "Searching for the Enrichment Policy - " + item)
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(item)
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'Press enter or click to search')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Press enter or click to search')]").click()
        sleep(1)

    def tool_status(self):
        if waitfor(self, 3, By.XPATH, "//span[contains(text(),'Add Account')]", False):
            fprint(self, "'Add Account' button is visible, clicking on it")
            self.driver.find_element_by_xpath("//span[contains(text(),'Add Account')]").click()
        elif waitfor(self, 5, By.XPATH, "//span[contains(text(),'Enabled')]", False):
            fprint(self, "'Enabled' button is visible")
            self.driver.find_element_by_xpath("//button[@data-testid='actions']").click()
            fprint(self, "Clicked on the action menu")
            sleep(1)    # Sleep is necessary here
            waitfor(self, 3, By.XPATH, "//li[contains(text(),'Manage')]")
            self.driver.find_element_by_xpath("//li[contains(text(),'Manage')]").click()
            fprint(self, "Clicked on the Manage option")
            waitfor(self, 3, By.XPATH, "//button[contains(text(),'Edit')]")
            self.driver.find_element_by_xpath("//button[contains(text(),'Edit')]").click()
            fprint(self, "Clicked on the Edit button")
            waitfor(self, 3, By.XPATH, "//div[contains(text(),'Credentials')]")
        elif waitfor(self, 5, By.XPATH, "//span[contains(text(),'Disabled')]", False):
            fprint(self, "'Disabled' button is visible")
            self.driver.find_element_by_xpath("//button[@data-testid='actions']").click()
            fprint(self, "Clicked on the action menu")
            sleep(1)    # Sleep is necessary here
            waitfor(self, 3, By.XPATH, "//li[contains(text(),'Manage')]")
            self.driver.find_element_by_xpath("//li[contains(text(),'Manage')]").click()
            fprint(self, "Clicked on the Manage option")
            waitfor(self, 3, By.XPATH, "//button[contains(text(),'Edit')]")
            self.driver.find_element_by_xpath("//button[contains(text(),'Edit')]").click()
            fprint(self, "Clicked on the Edit button")
            waitfor(self, 3, By.XPATH, "//div[contains(text(),'Credentials')]")

    def tool_status_SpecialCase(self):
        if waitfor(self, 3, By.XPATH, "//span[contains(text(),'Add Account')]", False):
            try:
                fprint(self, "Found Add Account Button, Clicking on it")
                self.driver.find_element_by_xpath("//span[contains(text(),'Add Account')]").click()
                fprint(self, "Add Account Button Clicked")
            except:
                fprint(self, "Credential Slider is already visible...")
        else:
            fprint(self, "Waiting for the Reset Option")
            self.driver.find_element_by_xpath("//span[@class='cyicon-more-vertical']").click()
            waitfor(self, 5, By.XPATH, "//li[contains(text(),'Reset Tool')]")
            self.driver.find_element_by_xpath("//li[contains(text(),'Reset Tool')]").click()
            fprint(self, "Clicked on the Reset Option")
            waitfor(self, 5, By.XPATH, "//button[contains(text(),'Yes, Reset')]")
            fprint(self, "Clicked on the 'Yes Reset' in popup")
            self.driver.find_element_by_xpath("//button[contains(text(),'Yes, Reset')]").click()
            verify_success(self, "Selected Enrichment Tool reset successfully")
            waitfor(self, 5, By.XPATH, "//span[contains(text(),'Add Account')]")
            fprint(self, "Found Add Account Button, Clicking on it")
            self.driver.find_element_by_xpath("//span[contains(text(),'Add Account')]").click()

    def quota_data(self):
        waitfor(self, 3, By.XPATH, "//div[contains(text(),'Quota')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Quota Duration')]").click()
        self.driver.find_element_by_xpath("//div[contains(text(),'Daily')]").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Quota Rate']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Quota Rate']").send_keys("10")
        self.driver.find_element_by_xpath("//button[contains(text(),'Update')]").click()

    def enable_feed(self):
        table = self.driver.find_element_by_xpath("//tbody/ancestor::table")
        rows = table.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
        feed_channels = []
        for row in rows:
            # Get the columns (all the data from column 1)
            col = row.find_elements(By.TAG_NAME, "td")[0]  # note: index start from 0, 1 and 2. Getting the data from 0.
            feed_channels.append(col.text)
            print(col.text)
        for data in feed_channels:
            waitfor(self, 5, By.XPATH, "//span[contains(text(),'"+data+"')]//ancestor::td//following-sibling::td//div[@data-testid='is_active']")
            fprint(self, "Clicking on the toggle button to enable "+data)
            self.driver.find_element_by_xpath("//span[contains(text(),'"+data+"')]//ancestor::td//following-sibling::td//div[@data-testid='is_active']").click()
            verify_success(self, "Feed Enrichment Type")

    def verify_policy_isvisible(self, policyname):
        self.search_policy(policyname)
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'"+policyname+"')]")
        fprint(self, "Policy Visible - "+policyname)

    def add_policy_detail(self, flag):
        if Build_Version.__contains__("3."):
            indicator = indicator_type2
        else:
            indicator = indicator_type1
        for iType in indicator:
            self.driver.find_element_by_xpath("//button[contains(text(),'Add')]").click()
            fprint(self, "Clicked on the Add Policy Button")
            waitfor(self, 5, By.XPATH, "//input[@placeholder='Add Policy Title']")
            self.driver.find_element_by_xpath("//input[@placeholder='Add Policy Title']").click()
            if flag == 1:
                self.driver.find_element_by_xpath("//input[@placeholder='Add Policy Title']").send_keys("Enrich_Policy"+uniquestr)
                fprint(self, "Policy Name is - Enrich_Policy"+uniquestr)
            else:
                self.driver.find_element_by_xpath("//input[@placeholder='Add Policy Title']").send_keys("Enrich_Policy"+iType)
                fprint(self, "Policy Name is - Enrich_Policy" + iType)
            # Selecting Indicator type
            self.driver.find_element_by_xpath("(//div[contains(text(),'"+iType+"')])[1]").click()
            fprint(self, "Selected Indicator Type - "+ iType)
            if waitfor(self, 0, By.XPATH, "//button[contains(text(),'Next Step')]", False):
                self.driver.find_element_by_xpath("//button[contains(text(),'Next Step')]").click()
            waitfor(self, 5, By.XPATH, "//button/div[contains(text(),'Parallel')]")
            self.driver.find_element_by_xpath("//button/div[contains(text(),'Parallel')]").click()
            fprint(self, "Selected Run type - Parallel")
            # Preference 1
            fprint(self, "Selecting Enrichment Tools")
            if Build_Version.__contains__("3."):
                self.driver.find_element_by_xpath("(//div[contains(@class,'cy-enrichment-form__select-box')])[1]").click()
            else:
                self.driver.find_element_by_xpath("//span[contains(text(),'Source 1')]/parent::div/div").click()
            if iType == "Vulnerability":
                waitfor(self, 5, By.XPATH, "//div[text()='CVE Details']")
                self.driver.find_element_by_xpath("//div[text()='CVE Details']").click()
                fprint(self, "Selected Preferences - CVE Details")
            else:
                waitfor(self, 5, By.XPATH, "//div[text()='Virus Total']")
                self.driver.find_element_by_xpath("//div[text()='Virus Total']").click()
                fprint(self, "Selected Preferences - Virus Total")
            sleep(1)
            # Preference 2
            if iType == "IP":
                if Build_Version.__contains__("3."):
                    self.driver.find_element_by_xpath("(//div[contains(@class,'cy-enrichment-form__select-box')])[2]").click()
                else:
                    self.driver.find_element_by_xpath("//span[contains(text(),'Source 2')]/parent::div/div").click()
                waitfor(self, 5, By.XPATH, "//div[text()='AbuseIPDB']")
                self.driver.find_element_by_xpath("//div[text()='AbuseIPDB']").click()
                fprint(self, "Selected Preferences - AbuseIPDB")
                sleep(1)
            self.driver.find_element_by_xpath("//button[contains(text(),'Next Step')]").click()
            fprint(self, "Clicked on the Next Step button")
            waitfor(self, 5, By.XPATH, "//p[contains(text(),'Select Source and Collection')]")
            try:
                wait = WebDriverWait(self.driver, 2)
                wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'All Sources')]")))
                self.driver.find_element_by_xpath("//span[contains(text(),'All Sources')]").click()
                fprint(self, "Selected 'All Sources', under Source and Collection")
            except:
                self.driver.find_element_by_xpath("//span[contains(text(),' Source * ')]/ancestor::div[@name='header']").click()
                waitfor(self, 5, By.XPATH, "//input[@name='search-input']")
                self.driver.find_element_by_xpath("//input[@name='search-input']").send_keys("Import")
                waitfor(self, 5, By.XPATH, "//div[contains(text(),'Import') and @name='text']")
                self.driver.find_element_by_xpath("//div[contains(text(),'Import') and @name='text']").click()
                self.driver.find_element_by_xpath("//span[contains(text(),'All Collections')]").click()
            sleep(1)
            self.driver.find_element_by_xpath("//button[contains(text(),'Next Step')]").click()
            fprint(self, "Clicked on the Next Step button")
            waitfor(self, 5, By.XPATH, "//p[contains(text(),'Do you want to apply a condition?')]")
            # TODO : Need to Add related condition if user select "YES"
            self.driver.find_element_by_xpath("//div[contains(text(),'No')]").click()
            fprint(self, "Selected 'No' under 'Do you want to apply a condition?'")
            self.driver.find_element_by_xpath("(//button[contains(text(),'Policy')])[2]").click()
            fprint(self, "Clicked on the Save Policy")
            verify_success(self, "Enrichment Policy Created successfully")
            self.verify_policy_isvisible("Enrich_Policy"+iType)
            if flag == 1:
                self.verify_policy_isvisible("Enrich_Policy"+uniquestr)
                break

    def enable_tool(self):
        sleep(3)
        Enable_button = self.driver.find_elements_by_xpath("//tr[@class='el-table__row cy-table__row-pointer']")
        print(len(Enable_button))
        for button in range(1, len(Enable_button)+1):
            waitfor(self, 5, By.XPATH, "(//tr//div[@class='cy-switch-btn-wrapper__icon'])["+str(button)+"]")
            _button_element=self.driver.find_element_by_xpath("(//tr//div[@class='cy-switch-btn-wrapper__icon'])["+str(button)+"]")
            _button_element.click()
            verify_success(self, 'Feed Enrichment Type enabled successfully')

    def disable_columns(self):
        data = []
        self.driver.find_element_by_xpath("//div[@data-testaction='dropdown-link']//div[contains(@class,'cyicon-add-active')]").click()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Custom')]/parent::div//div[@class='section-columns']")
        cust_col = self.driver.find_element_by_xpath("//span[contains(text(),'Custom')]/parent::div//div[@class='section-columns']")
        col_names = cust_col.find_elements(By.TAG_NAME, "span")
        for col in col_names:
            print(col.text)
            if str(col.text) != "Status":
                data.append(col.text)
        fprint(self, "Disabling all Active columns")
        for col in data:
            if waitfor(self, 0, By.XPATH, "//span[contains(@class,'column-option__active') and contains(text(),'" + col + "')]", False):
                element = self.driver.find_element_by_xpath("//span[contains(text(),'"+col+"')]/i[contains(@class,'cyicon-check-circle-outline')]")
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                self.driver.find_element_by_xpath("//span[contains(text(),'"+col+"')]/i[contains(@class,'cyicon-check-circle-outline')]").click()
                fprint(self, "Column Disabled - "+col)
        self.driver.find_element_by_xpath("//div[@data-testaction='dropdown-link']//div[contains(@class,'cyicon-add-active')]").click()

    def test_01_enrichment_management_listing(self):
        fprint(self, "TC_ID: 1 - Enrichment-listing")
        nav_menu_admin(self, "Enrichment Management")
        process_console_logs(self)
        clear_console_logs(self)
        fprint(self, "TC_ID: 1 - Enrichment-listing")

    # Work on both 2.9.x and 3.x
    def test_02_enrichment_configuring_tools(self):
        fprint(self, "TC_ID: 2 - Enrichment-tool add")
        nav_menu_admin(self, "Enrichment Management")
        filename = os.path.join(os.environ["PYTHONPATH"], "testdata","credential.csv")
        # Open variable-based csv, iterate over the rows and map values to a list of dictionaries containing key/value pairs
        with open(filename, 'r') as data:
            for line in csv.DictReader(data):
                _value = line["Account Name*"]
                fprint(self, "Searching for - " + _value)
                self.driver.find_element_by_xpath(qai_ioc_type_search).click()
                self.driver.find_element_by_xpath(qai_ioc_type_search).clear()
                self.driver.find_element_by_xpath(qai_ioc_type_search).send_keys(_value)
                self.driver.find_element_by_xpath("//span[contains(text(),'Press enter or click to search')]").click()
                if waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+_value+"')]", False):
                    fprint(self, "Enrichment Tool is visible, clicking on it - " + _value)
                    self.driver.find_element_by_xpath("//span[contains(text(),'"+_value+"')]//ancestor::div[3]").click()
                    if waitfor(self, 5, By.XPATH,"//button[contains(text(),'DONE')]", False):
                        fprint(self, "Walkthrough is visible - Done")
                        self.driver.find_element_by_xpath("//button[contains(text(),'DONE')]").click()
                        waitfor(self, 5, By.XPATH, "//button[contains(text(),'OK')]")
                        fprint(self, "Walkthrough is visible - Ok")
                        self.driver.find_element_by_xpath("//button[contains(text(),'OK')]").click()
                    self.tool_status()
                    sleep(2)
                    fprint(self, "Credentials Form is visible, Entering credentials now...")
                    for x in line:
                        _value1 = line["" + x + ""]
                        if _value1 != '':
                            clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='" + x + "']"))
                            self.driver.find_element_by_xpath("//input[@aria-placeholder='" + x + "']").click()
                            # self.driver.find_element_by_xpath("//input[@aria-placeholder='" + x + "']").send_keys(Keys.COMMAND, "a", Keys.BACK_SPACE)
                            self.driver.find_element_by_xpath("//input[@aria-placeholder='" + x + "']").send_keys(_value1)
                    self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
                    fprint(self, "Clicked on the Save button")
                    waitfor(self, 8, By.XPATH, "//div[contains(@class, 'cy-message__text')]")
                    fprint(self, "Notification Alert is visible")
                    actual_res = str(self.driver.find_element_by_xpath("//div[contains(@class, 'cy-message__text')]").text)
                    self.driver.find_element_by_xpath("//div[@class='el-notification__closeBtn el-icon-close']").click()
                    fprint(self, "Closed Notification Alert")
                    print("--------------"+_value+"-"+actual_res+"---------------------")
                    if actual_res.__contains__("Invalid Credentials"):
                        fprint(self, "[Error] , Expected  message is found - " + str(actual_res))
                        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
                        fprint(self, "Credentials slider is closed")
                    elif actual_res.__contains__("Account updated successfully"):
                        fprint(self, "[Passed] Expected message is found, " + str(actual_res))
                    else:
                        if actual_res.__contains__("Account created successfully"):
                            fprint(self, "[Passed] Expected message is found, " + str(actual_res))
                            waitfor(self, 3, By.XPATH, "//div[contains(text(),'Quota')]")
                            fprint(self, "Quota tab is visible")
                            self.driver.find_element_by_xpath("//button[contains(text(),'Skip')]").click()
                            fprint(self, "Clicked on the Skip button")
                    waitfor(self, 10, By.XPATH, "//span[contains(text(),'Enrichment Tools')]")
                    self.driver.find_element_by_xpath("//span[contains(text(),'Enrichment Tools')]").click()
                    fprint(self, "Clicked on the Enrichment Tool Breadcrumb")
                    waitfor(self, 20, By.XPATH, "//h1[contains(text(),'Enrichment Management')]")
                    fprint(self, "Enrichment Management Title is visible")
                else:
                    fprint(self, ""+_value+" ------ Either Tool name is invalid or tool not enabled in LMS")
        fprint(self, "TC_ID: 2 - All Enrichment-tool with valid credentials added successfully")

    # Work on both 2.9.x and 3.x
    def test_03_abuseIPDB_configuration(self):
        fprint(self, "TC_ID: 1212 - Abuse IPDB Enrichment-tool add" + uniquestr)
        nav_menu_admin(self, "Enrichment Management")
        filename = os.path.join(os.environ["PYTHONPATH"], "testdata", "credential.csv")
        with open(filename, 'r') as data:
            for line in csv.DictReader(data):
                _value = line["Account Name*"]
                if _value == "AbuseIPDB":
                    fprint(self, "Searching for - " + _value)
                    self.driver.find_element_by_xpath(enrichment_management_search).click()
                    self.driver.find_element_by_xpath(enrichment_management_search).clear()
                    self.driver.find_element_by_xpath(enrichment_management_search).send_keys(_value)
                    self.driver.find_element_by_xpath("//span[contains(text(),'Press enter or click to search')]").click()
                    if waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+_value+"')]"):
                        fprint(self, "Enrichment Tool is visible, clicking on it - " + _value)
                        self.driver.find_element_by_xpath("//span[contains(text(),'"+_value+"')]//ancestor::div[3]").click()
                        if waitfor(self, 5, By.XPATH,"//button[contains(text(),'DONE')]", False):
                            fprint(self, "Walkthrough is visible - Done")
                            self.driver.find_element_by_xpath("//button[contains(text(),'DONE')]").click()
                            waitfor(self, 5, By.XPATH, "//button[contains(text(),'OK')]")
                            fprint(self, "Walkthrough is visible - Ok")
                            self.driver.find_element_by_xpath("//button[contains(text(),'OK')]").click()
                        self.tool_status_SpecialCase()
                        sleep(2)
                        fprint(self, "Credentials Form is visible, Entering credentials now...")
                        for x in line:
                            _value1 = line["" + x + ""]
                            if _value1 != '':
                                clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='" + x + "']"))
                                self.driver.find_element_by_xpath("//input[@aria-placeholder='" + x + "']").click()
                                self.driver.find_element_by_xpath("//input[@aria-placeholder='" + x + "']").send_keys(_value1)
                        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
                        fprint(self, "Clicked on the Save button")
                        if waitfor(self, 20, By.XPATH, "//div[@role='alert']", False):
                            fprint(self, "Found Alert")
                            sleep(1)
                            textis = str(self.driver.find_element_by_xpath("//div[contains(@class, 'cy-message__text')]").text)
                            if textis.__contains__("Account created successfully"):
                                fprint(self, "Expected message is found - Account created successfully!")
                                waitfor(self, 5, By.XPATH, "//div[contains(text(),'Quota')]")
                                fprint(self, "Quota tab is visible")
                                self.driver.find_element_by_xpath("//button[contains(text(),'Skip')]").click()
                                fprint(self, "Clicked on the Skip button")
                                self.enable_feed()
                            elif textis.__contains__("Abuseipdb is giving a status response code 429"):
                                fprint(self, "Did not receive the expected message, trying with the different key")
                                clear_field(self.driver.find_element_by_xpath("//input[@name='access_key']"))
                                sleep(2)
                                self.driver.find_element_by_xpath("//input[@name='access_key']").click()
                                self.driver.find_element_by_xpath("//input[@name='access_key']").send_keys("dde4f88ec02bb74281719ae1ee27671e6e31ffd35b4fe74679d765c6ea7d88442f291a5525723796")
                                self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
                                fprint(self, "Clicked on the Save button")
                                verify_success(self, "Account created successfully")
                                waitfor(self, 20, By.XPATH, "//div[contains(text(),'Quota')]")
                                fprint(self, "Quota tab is visible")
                                self.driver.find_element_by_xpath("//button[contains(text(),'Skip')]").click()
                                fprint(self, "Clicked on the Skip button")
                                self.enable_feed()
                            else:
                                fprint(self, "Case Status: [Failed] Expected alert is not found")
                                self.fail("Case Status: [Failed] Expected alert is not found")
                            break
                        else:
                            fprint(self, "Case Status: [Failed] No Alert is found")
                            self.fail("Case Status: [Failed] No Alert is found")

    # Work on both 2.9.x and 3.x
    def test_04_virusTotal_configuration(self):
        fprint(self, "TC_ID: 1213 - Virus Total Enrichment-tool add" + uniquestr)
        nav_menu_admin(self, "Enrichment Management")
        filename = os.path.join(os.environ["PYTHONPATH"], "testdata", "credential.csv")
        with open(filename, 'r') as data:
            for line in csv.DictReader(data):
                _value = line["Account Name*"]
                if _value == "Virus Total":
                    fprint(self, "Searching for - " + _value)
                    self.driver.find_element_by_xpath(enrichment_management_search).click()
                    self.driver.find_element_by_xpath(enrichment_management_search).clear()
                    self.driver.find_element_by_xpath(enrichment_management_search).send_keys(_value)
                    self.driver.find_element_by_xpath("//span[contains(text(),'Press enter or click to search')]").click()
                    if waitfor(self, 10, By.XPATH, "//span[contains(text(),'" + _value + "')]"):
                        fprint(self, "Enrichment Tool is visible, clicking on it - " + _value)
                        self.driver.find_element_by_xpath("//span[contains(text(),'"+_value+"')]//ancestor::div[3]").click()
                        if waitfor(self, 5, By.XPATH, "//button[contains(text(),'DONE')]", False):
                            fprint(self, "Walkthrough is visible - Done")
                            self.driver.find_element_by_xpath("//button[contains(text(),'DONE')]").click()
                            waitfor(self, 5, By.XPATH, "//button[contains(text(),'OK')]")
                            fprint(self, "Walkthrough is visible - Ok")
                            self.driver.find_element_by_xpath("//button[contains(text(),'OK')]").click()
                        self.tool_status_SpecialCase()
                        sleep(2)
                        fprint(self, "Credentials Form is visible, Entering credentials now...")
                        for x in line:
                            _value1 = line["" + x + ""]
                            if _value1 != '':
                                clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='" + x + "']"))
                                self.driver.find_element_by_xpath("//input[@aria-placeholder='" + x + "']").click()
                                self.driver.find_element_by_xpath("//input[@aria-placeholder='" + x + "']").send_keys(_value1)
                        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
                        fprint(self, "Clicked on the Save button")
                        if waitfor(self, 20, By.XPATH, "//div[@role='alert']", False):
                            fprint(self, "Found Alert")
                            sleep(1)
                            textis = str(self.driver.find_element_by_xpath("//div[contains(@class, 'cy-message__text')]").text)
                            if textis.__contains__("Account created successfully"):
                                fprint(self, "Expected message is found - Account created successfully!")
                                waitfor(self, 5, By.XPATH, "//div[contains(text(),'Quota')]")
                                fprint(self, "Quota tab is visible")
                                self.driver.find_element_by_xpath("//button[contains(text(),'Skip')]").click()
                                fprint(self, "Clicked on the Skip button")
                                self.enable_feed()
                            elif textis.__contains__("VirusTotal is giving a status response code 204"):
                                fprint(self, "Did not receive the expected message, trying with the different key")
                                clear_field(self.driver.find_element_by_xpath("//input[@name='access_key']"))
                                sleep(2)
                                self.driver.find_element_by_xpath("//input[@name='access_key']").click()
                                self.driver.find_element_by_xpath("//input[@name='access_key']").send_keys("4c868b5830e92da33f7c020b6fb6bbbe419524021150ee80d8b1181741309029")
                                self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
                                fprint(self, "Clicked on the Save button")
                                verify_success(self, "Account created successfully")
                                waitfor(self, 20, By.XPATH, "//div[contains(text(),'Quota')]")
                                fprint(self, "Quota tab is visible")
                                self.driver.find_element_by_xpath("//button[contains(text(),'Skip')]").click()
                                fprint(self, "Clicked on the Skip button")
                                self.enable_feed()
                            else:
                                fprint(self, "Case Status: [Failed] Expected alert is not found")
                                self.fail("Case Status: [Failed] Expected alert is not found")
                            break
                        else:
                            fprint(self, "Case Status: [Failed] No Alert is found")
                            self.fail("Case Status: [Failed] No Alert is found")

    def test_05_enrichment_reset_tools(self):
        fprint(self, "TC_ID: 5 - Enrichment-active/inactive-listing" + uniquestr)
        nav_menu_admin(self, "Enrichment Management")
        filename = os.path.join(os.environ["PYTHONPATH"], "testdata", "credential.csv")
        with open(filename, 'r') as data:
            for line in csv.DictReader(data):
                _value = line["Account Name*"]
                fprint(self, "Searching for - " + _value)
                self.driver.find_element_by_xpath(enrichment_management_search).click()
                self.driver.find_element_by_xpath(enrichment_management_search).clear()
                self.driver.find_element_by_xpath(enrichment_management_search).send_keys(_value)
                self.driver.find_element_by_xpath("//span[contains(text(),'Press enter or click to search')]").click()
                if waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+_value+"')]", False):
                    fprint(self, "Enrichment Tool is visible, clicking on it - " + _value)
                    self.driver.find_element_by_xpath("//span[contains(text(),'" + _value + "')]//ancestor::div[3]").click()
                    if waitfor(self, 5, By.XPATH,"//button[contains(text(),'DONE')]", False):
                        fprint(self, "Walkthrough is visible - Done")
                        self.driver.find_element_by_xpath("//button[contains(text(),'DONE')]").click()
                        waitfor(self, 5, By.XPATH, "//button[contains(text(),'OK')]")
                        fprint(self, "Walkthrough is visible - Ok")
                        self.driver.find_element_by_xpath("//button[contains(text(),'OK')]").click()
                    if waitfor(self, 3, By.XPATH, "//span[contains(text(),'Add Account')]", False):
                        fprint(self, "Warning : "+_value+" is not configured, hence no Reset Option")
                    else:
                        self.driver.find_element_by_xpath("//button[@data-testid='actions']").click()
                        fprint(self, "Action button is clicked")
                        sleep(2)    # Sleep is necessary here
                        self.driver.find_element_by_xpath("//li[contains(text(),'Reset Tool')]").click()
                        fprint(self, "Reset Tool option is clicked")
                        sleep(2)    # Sleep is necessary here
                        self.driver.find_element_by_xpath("//button[contains(text(),'Yes')]").click()
                        fprint(self, "Confirmed 'Yes Reset' is clicked")
                        verify_success(self,"Selected Enrichment Tool reset successfully")
                    waitfor(self, 10, By.XPATH, "//span[contains(text(),'Enrichment Tools')]")
                    self.driver.find_element_by_xpath("//span[contains(text(),'Enrichment Tools')]").click()
                    fprint(self, "Clicked on the Enrichment Tool Breadcrumb")
                    waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Enrichment Management')]")
                    fprint(self, "Enrichment Management Title is visible")

    def test_06_enrichment_management_active_inactive_listing(self):
        failure = []
        fprint(self, "TC_ID: 6 - Enrichment-active/inactive-listing")
        nav_menu_admin(self, "Enrichment Management")
        enrich_filter = ['Active', 'Inactive']
        for filter in enrich_filter:
            self.driver.find_element_by_xpath("//i[@class='cyicon-chevron-down']").click()
            fprint(self, "Clicked on the Dropdown")
            sleep(1)
            self.driver.find_element_by_xpath("//li[contains(text(),'"+str(filter)+"')]").click()
            fprint(self, "Clicked on the Option - " + filter)
            sleep(2)
            if filter == 'Inactive':
                if waitfor(self, 5, By.XPATH, "//span[@class='cy-switch-btn__icon pl-0 pr-2 cyicon-cross-lg']", False):
                    failure.append("Active Tools are visible, when Inactive is selected.")
                else:
                    fprint(self, "[Passed] No Active Enrichment Tool is visible")
            elif filter == 'Active':
                if waitfor(self, 5, By.XPATH, "//span[@class='cy-switch-btn__icon cyicon-check-lg']", False):
                    failure.append("Inactive Tools are visible, when Active is selected.")
                else:
                    fprint(self, "[Passed] No Inactive Enrichment Tool is visible")
            self.assert_(failure == [], str(failure))
        process_console_logs(self)
        clear_console_logs(self)

    def test_07_add_enrichment_policy(self):
        fprint(self, "TC_ID: 1214 - Enrichment-policy")
        nav_menu_admin(self, "Enrichment Management")
        self.driver.find_element_by_xpath("//span[contains(text(),'Enrichment Policy')]/ancestor::a").click()
        fprint(self, "Waiting for the Add Policy Button")
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Add')]")
        self.add_policy_detail(4)
        process_console_logs(self)
        clear_console_logs(self)
        fprint(self, "TC_ID: 4 - Enrichment-added-policy")

    def test_08_edit_enrichment_policy(self):
        fprint(self, "TC_ID: 1215 - Edit Enrichment-policy")
        nav_menu_admin(self, "Enrichment Management")
        self.driver.find_element_by_xpath("//span[contains(text(),'Enrichment Policy')]/ancestor::a").click()
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Enrichment Policy')]")
        fprint(self, "Waiting for the Enrichment Policy Title")
        self.search_policy("Enrich_Policy"+uniquestr)
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'Enrich_Policy"+uniquestr+"')]")
        fprint(self, "Enrichment Policy is visible - Enrich_Policy" + uniquestr)
        self.driver.find_element_by_xpath("//span[contains(text(),'Enrich_Policy"+uniquestr+"')]").click()
        fprint(self, "Clicked on the Enrichment Policy - Enrich_Policy" + uniquestr)
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Edit Policy')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Edit Policy')]").click()
        fprint(self, "Clicked on the Edit Policy")
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Add Policy Title']")
        self.driver.find_element_by_xpath("//input[@placeholder='Add Policy Title']").clear()
        self.driver.find_element_by_xpath("//input[@placeholder='Add Policy Title']").send_keys("EDIT_POLICY")
        self.driver.find_element_by_xpath("//button[contains(text(),'Update Policy')]").click()
        verify_success(self, "Enrichment Policy updated successfully")
        self.driver.refresh()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'EDIT_POLICY')]")
        fprint(self, "Newly Edited Policy is visible")
        process_console_logs(self)
        clear_console_logs(self)

    def test_09_delete_enrichment_policy(self):
        fprint(self, "TC_ID: 1216 - Delete Enrichment-policy")
        nav_menu_admin(self, "Enrichment Management")
        self.driver.find_element_by_xpath("//span[contains(text(),'Enrichment Policy')]/ancestor::a").click()
        fprint(self, "Waiting for the Enrichment Policy Title")
        self.search_policy("EDIT_POLICY")
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'EDIT_POLICY')]")
        fprint(self, "Enrichment Policy is visible - EDIT_POLICY")
        self.driver.find_element_by_xpath("//span[contains(text(),'EDIT_POLICY')]/ancestor::td//..//button[@data-testid='action']/ancestor::td").click()
        fprint(self, "Clicked on the Action menu")
        waitfor(self, 5, By.XPATH, "//ancestor::ul[@x-placement]//li[contains(text(),'Delete')]")
        self.driver.find_element_by_xpath("//ancestor::ul[@x-placement]//li[contains(text(),'Delete')]").click()
        fprint(self, "Clicked on the Delete Option")
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Delete')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Delete')]").click()
        fprint(self, "Clicked on the Confirm Delete Button")
        verify_success(self, "Enrichment Policy deleted successfully")
        self.driver.refresh()
        waitfor(self, 20, By.XPATH, "//h1[contains(text(),'No Enrichment Policy found!')]")
        process_console_logs(self)
        clear_console_logs(self)

    def test_10_add_enrichment_policy_for_all_indicatorTypes(self):
        fprint(self, "TC_ID: 1217 - Enrichment-policy for all indicator types")
        nav_menu_admin(self, "Enrichment Management")
        self.driver.find_element_by_xpath("//span[contains(text(),'Enrichment Policy')]/ancestor::a").click()
        fprint(self, "Waiting for the Enrichment Policy Title")
        if waitfor(self, 5, By.XPATH, "//div[contains(text(),'Enrichment Policy')]", False):
            pass
        else:
            waitfor(self, 5, By.XPATH, "//span[contains(text(),'/ Enrichment Policy')]")
        fprint(self, "Title is visible")
        self.add_policy_detail(0)
        # process_console_logs(self)
        # clear_console_logs(self)

    def test_11_disable_enrichment_policy(self):
        fprint(self, "TC_ID: 1218 - disable_enrichment_policy")
        nav_menu_admin(self, "Enrichment Management")
        self.driver.find_element_by_xpath("//span[contains(text(),'Enrichment Policy')]/ancestor::a").click()
        if Build_Version.__contains__("3."):
            data = enrich_policy2
        else:
            data = enrich_policy1
        waitfor(self, 10, By.XPATH, "//span[@data-key='name']")
        fprint(self, "Policy Table visible, Disabling unnecessary columns")
        self.disable_columns()
        sleep(1)
        for enrich_policy in data:
            fprint(self, "Waiting for the Enrichment Policy - " + enrich_policy)
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'" + enrich_policy + "')]")
            fprint(self, "Policy Visible, Disabling it ")
            self.driver.find_element_by_xpath("//span[contains(text(),'"+enrich_policy+"')]/ancestor::td/following-sibling::td[3]//div[@data-testid='is_active']").click()
            fprint(self, "Enrichment Policy Disabled - "+enrich_policy)
            sleep(2)

    def test_12_CVEDetails_configuration(self):
        fprint(self, "TC_ID: 1219 - CVEDetails_configuration")
        nav_menu_admin(self, "Enrichment Management")
        filename = os.path.join(os.environ["PYTHONPATH"], "testdata", "credential.csv")
        with open(filename, 'r') as data:
            for line in csv.DictReader(data):
                _value = line["Account Name*"]
                if _value == "CVE Details":
                    fprint(self, "Searching for - " + _value)
                    self.driver.find_element_by_xpath(enrichment_management_search).click()
                    self.driver.find_element_by_xpath(enrichment_management_search).clear()
                    self.driver.find_element_by_xpath(enrichment_management_search).send_keys(_value)
                    self.driver.find_element_by_xpath(
                        "//span[contains(text(),'Press enter or click to search')]").click()
                    if waitfor(self, 10, By.XPATH, "//span[contains(text(),'" + _value + "')]"):
                        fprint(self, "Enrichment Tool is visible, clicking on it - " + _value)
                        self.driver.find_element_by_xpath(
                            "//span[contains(text(),'" + _value + "')]//ancestor::div[3]").click()
                        if waitfor(self, 5, By.XPATH, "//button[contains(text(),'DONE')]", False):
                            fprint(self, "Walkthrough is visible - Done")
                            self.driver.find_element_by_xpath("//button[contains(text(),'DONE')]").click()
                            waitfor(self, 5, By.XPATH, "//button[contains(text(),'OK')]")
                            fprint(self, "Walkthrough is visible - Ok")
                            self.driver.find_element_by_xpath("//button[contains(text(),'OK')]").click()
                        self.tool_status_SpecialCase()
                        sleep(2)
                        fprint(self, "Credentials Form is visible, Entering credentials now...")
                        for x in line:
                            _value1 = line["" + x + ""]
                            if _value1 != '':
                                # self.driver.find_element_by_xpath("//input[@aria-placeholder='" + x + "']").send_keys(Keys.COMMAND, "a", Keys.BACK_SPACE)
                                clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='" + x + "']"))
                                self.driver.find_element_by_xpath("//input[@aria-placeholder='" + x + "']").click()
                                self.driver.find_element_by_xpath("//input[@aria-placeholder='" + x + "']").send_keys(
                                    _value1)
                        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
                        fprint(self, "Clicked on the Save button")
                        verify_success(self, "Account created successfully")
                        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Quota')]")
                        fprint(self, "Quota tab is visible")
                        self.driver.find_element_by_xpath("//button[contains(text(),'Skip')]").click()
                        fprint(self, "Clicked on the Skip button")
                        self.enable_feed()
                        break

    def test_13_enrichment_verification(self):
        failures = []
        fprint(self, "TC_ID: 1220 - enrichment_verification")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, filter_name="IOC Type", object_name="Ipv4 addr")
        verify_data_in_threatdata(self, value=ioc_ip, source="Import")
        click_on_intel(self, source="Import", value=ioc_ip)
        if waitfor(self, 10, By.XPATH, "//p[contains(text(),'Automated')]/preceding::p[contains(text(),'100')]", False):
            fprint(self, "Passed - Confidence Score 100 is visible")
        else:
            fprint(self, "[Failed] - Confidence Score is not 100")
            failures.append("Confidence Score is not 100 ")
        self.driver.find_element_by_xpath("//div[contains(text(),'Enrichment')]").click()
        fprint(self, "Clicked on the Enrichment tab")
        if waitfor(self, 10, By.XPATH, "//span[contains(text(),'Sources Reported Malicious')]/ancestor::div[2]/following-sibling::div//img[contains(@alt,'AbuseIPDB')]", False) \
                and waitfor(self, 10, By.XPATH, "//span[contains(text(),'Sources Reported Malicious')]/ancestor::div[2]/following-sibling::div//img[contains(@alt,'Virus Total')]"):
            fprint(self, "Passed - AbuseIPDB and Virus Total is visible, under sources reported malicious section")
        else:
            fprint(self, "[Failed] - AbuseIPDB or Virus Total is not visible, under sources reported malicious section")
            failures.append("AbuseIPDB or Virus Total is not visible, under sources reported malicious section - ")
        if waitfor(self, 10, By.XPATH, "(//div[contains(text(),'abuseConfidenceScore')]/following-sibling::div[contains(text(),'100')])[1]", False):
            fprint(self, "Passed - Abuse Confidence Score 100 is visible")
        else:
            fprint(self, "[Failed] - Abuse Confidence Score is not 100")
            failures.append("Abuse Confidence Score is not 100")
        if waitfor(self, 10, By.XPATH, "//div[contains(text(),'execution status')]/following-sibling::div[contains(text(),'SUCCESS')]", False):
            fprint(self, "Passed - Success is visible under Execution Status")
        else:
            fprint(self, "[Failed] - Success is not visible under Execution Status")
            failures.append("Success is not visible under Execution Status")
        self.assert_(failures == [], str(failures))

    # Work for both 2.9.x and 3.x
    def test_14_add_IOCType_ip(self):
        textis = ""
        fprint(self, "TC_ID: 1221 - QuickAddIntel_config_Indicator_IOCs")
        failures = []
        fprint(self, "Waiting for the New Button...")
        self.driver.find_element_by_xpath("//button[contains(text(),'New')]").click()
        fprint(self, "Clicked on the New Button")
        waitfor(self, 5, By.XPATH, "//li/div[contains(text(),'Quick Add Intel')]")
        self.driver.find_element_by_xpath("//li/div[contains(text(),'Quick Add Intel')]").click()
        fprint(self, "Clicked on the 'Quick Add Intel' option")
        waitfor(self, 10, By.XPATH, "(//div[contains(text(),'Quick Add Intel')])[1]")
        waitfor(self, 10, By.XPATH, qai_ioc_type_search)
        if Build_Version.__contains__("3."):
            clear_field(self.driver.find_element_by_xpath(qai_ioc_type_search))
            fprint(self, "Searching - IPv4")
            self.driver.find_element_by_xpath(qai_ioc_type_search).click()
            self.driver.find_element_by_xpath(qai_ioc_type_search).send_keys("IPv4")
        else:
            sleep(2)
            self.driver.find_element_by_xpath("//div[@class='cy-filters__section px-1 d-flex']").click()
            # self.driver.find_element_by_xpath("//ul//input[@placeholder='Search']").click()
            clear_field(self.driver.find_element_by_xpath("//input[@id='main-input'][@placeholder='Search']"))
            fprint(self, "Searching - IPv4")
            self.driver.find_element_by_xpath\
                ("//input[@id='main-input'][@placeholder='Search']").send_keys("IPv4")
            self.driver.find_element_by_xpath\
                ("//input[@type='checkbox']/ancestor::div[contains(text(),'IPv4')]").click()
            sleep(2)
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'IPv4')]/ancestor::div[1]")
        # self.driver.find_element_by_xpath("//div[contains(text(),'IPv4')]/ancestor::div[1]").click()
        self.driver.find_element_by_xpath("//div[contains(text(),'IPv4')]/div[1]/div").click()
        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys("test_IPv4")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").send_keys(ioc_ip)
        self.driver.find_element_by_xpath("//button[contains(text(),'Create Intel')]").click()
        # verify_success(self, "You will be notified once the STIX package is created")
        if waitfor(self, 15, By.XPATH, "//i[@class = 'cyicon-check-o-active']", False):
            sleep(1)
            textis = self.driver.find_element_by_xpath("//div[contains(@class, 'cy-message__text')]").text
            if textis == "You can view the created intel as a report object in the Threat Data module." or textis == "You will be notified once the STIX package is created!":
                fprint(self, "[Passed] Expected message is found, " + str(textis))
                self.driver.find_element_by_xpath("//div[@class='el-notification__closeBtn el-icon-close']").click()
                repeat = 1
                while repeat <= 6:
                    if waitfor(self, 20, By.XPATH, "//span[contains(text(),'test_IPv4')]/ancestor::td/following-sibling::td[3]//span[contains(text(),'Created')]", False):
                        fprint(self, "Created Status of intel is visible - test_IPv4")
                        self.driver.find_element_by_xpath(
                            "//span[contains(text(),'Quick Add History')]").click()
                        break
                    else:
                        self.driver.find_element_by_xpath("//button[contains(text(),'Refresh')]").click()
                        fprint(self, "Created Status of intel is not visible, Clicked on the Refresh Button")
                        if repeat == 6:
                            fprint(self, "[Failed] - Created Status of intel is not visible - test_IPv4")
                            failures.append("Created Status of intel is not visible - test_IPv4")
                            self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
                        repeat = repeat + 1
            else:
                fprint(self,
                       "[Failed] Alert found with different msg. Found: " + str(
                           textis) + "Expected: You will be notified once the STIX package is created! or You can view the created intel as a report object in the Threat Data module.")
                self.driver.find_element_by_xpath("//div[contains(text(),'IPv4')]/div[1]/div").click()
                failures.append("Case Status: [Failed] Alert found but expected message is not found -"+textis)
        else:
            fprint(self, "[Failed] - Getting some error in adding - IPv4")
            self.driver.find_element_by_xpath("//div[contains(text(),'IPv4')]/div[1]/div").click()
            fprint(self, "[Failed] - Expected message is not found")
            failures.append("Expected message is not found - "+textis)
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        self.assert_(failures == [], str(failures))
        fprint(self, "Waiting for 2 minutes...")
        sleep(120)

    # Work only for 2.9.x
    def test_15_v2_enrichment_verification(self):
        failures = []
        fprint(self, "TC_ID: 1222 - enrichment_verification")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Waiting for the Search bar")
        search(self, ioc_ip)
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Import')]/ancestor::td/preceding::td[1]//span[contains(text(),'"+ioc_ip+"')]")
        fprint(self, "Searched item is visible - " + ioc_ip)
        sleep(2)
        wait = WebDriverWait(self.driver, 10)
        ele = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(text(),'Import')]/ancestor::td/preceding::td[1]//span[contains(text(),'"+ioc_ip+"')]")))
        self.driver.execute_script("arguments[0].click();", ele)
        sleep(2)
        fprint(self, "Clicked on - " + ioc_ip)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Investigations')]/parent::a")
        fprint(self, "Clicking on the Investigations Tab")
        self.driver.find_element_by_xpath("//span[contains(text(),'Investigations')]/parent::a").click()
        if waitfor(self, 20, By.XPATH, "//div[contains(text(),'AbuseIPDB')]/parent::div//span[contains(text(),'Run Successfully')]", False):
            fprint(self, "[Passed] - AbuseIPDB Status is Green, hence Ran Successfully")
        else:
            fprint(self, "[Failed] - AbuseIPDB did not Ran")
            failures.append("AbuseIPDB did not Ran")
        if waitfor(self, 10, By.XPATH, "//div[contains(text(),'abuseConfidenceScore')]/following-sibling::div[contains(text(),'100')]", False):
            fprint(self, "[Passed] - AbuseIPDB Confidence Score is 100, Visible")
        else:
            fprint(self, "[Failed] - AbuseIPDB Confidence Score is not 100 or not visible")
            failures.append("AbuseIPDB Confidence Score is not 100 or not visible")
        if waitfor(self, 10, By.XPATH, "//div[contains(text(),'Virus Total')]/parent::div//span[contains(text(),'Run Successfully')]", False):
            fprint(self, "[Passed] - Virus Total Status is Green, hence Ran Successfully")
        else:
            fprint(self, "[Failed] - Virus Total did not Ran")
            failures.append("Virus Total did not Ran")
        self.assert_(failures == [], str(failures))


if __name__ == '__main__':
    unittest.main(testRunner=reporting())



