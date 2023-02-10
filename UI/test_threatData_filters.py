import unittest
from lib.ui.nav_threat_data import *
from lib.ui.quick_add import quick_create_ip
count = 0
flag = 0
indicatorAllowedStatus = "67.55.71.88"
reviewedStatus = "67.55.71.89"
falsePositive = '67.55.71.80'
relation = "67.55.71.82"
manualReview = "67.55.71.90"
deprecatedStatus = "67.55.70.80"
domain = "caentivage.com"
subs_domain = "testabc.com"
actionedOn = "221.221.221.14"
actionAppType = "221.221.221.16"
rules = "221.221.221.16"
previous_date = "0"
file = os.path.join(os.environ["PYTHONPATH"], "testdata", "quick_add_intel_data.csv")
file_name = open(file)
csvreader = csv.reader(file_name)
first_row = next(csvreader)
enrich_ip = first_row[1]


class ThreatDataFilters(unittest.TestCase):

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

    def check_value_in_threatData_listing(self, value):
        data = []
        waitfor(self, 10, By.XPATH, "//tbody")
        fprint(self, "Threat Data listing is visible")
        table = self.driver.find_element_by_xpath("//tbody")
        rows = table.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
        for row in rows:
            # Get the columns (all the data from column 1)
            if value == "tlp":
                col = row.find_element_by_xpath("//td[contains(@class,'cy-tlp--red')]")
                # text = col.get_attribute("innerHTML")
                text = col.get_attribute("class")
                print(str(text))
                data.append(str(text))
            else:
                col = row.find_elements(By.TAG_NAME, "td")[2]  # note: index start from 0, 1 and 2. Getting the data from 0.
                text = col.get_attribute("innerHTML")
                print(str(text))
                data.append(str(text))
        if value == "url":
            for obj in data:
                if not (str(obj).__contains__("http") or str(obj).__contains__("tcp") or str(obj).__contains__("mailto") or str(obj).__contains__("www")):
                    fprint(self, "[Failed] Not getting correct Filtered data for the URL - " + str(obj))
                    self.fail("Not getting correct Filtered data for the URL- " + str(obj))
        elif value == "tlp":
            for obj in data:
                if not str(obj).__contains__("cy-tlp--red"):
                    fprint(self, "[Failed] Not getting correct Filtered data for the TLP - " + str(obj))
                    self.fail("Not getting correct Filtered data for the TLP - " + str(obj))
        else:
            for obj in data:
                if not str(obj).__contains__(value):
                    fprint(self, "[Failed] Not getting correct Filtered data for - " + str(obj))
                    self.fail("Not getting correct Filtered data for - " + str(obj))
        fprint(self, "[Passed] Getting correct Filtered data for the - " + value)

    def check_data_in_threatData_listing(self, value, min_range=0, max_range=0):
        obj_data = []
        waitfor(self, 20, By.XPATH, "//tbody")
        fprint(self, "Threat Data listing is visible")
        table = self.driver.find_element_by_xpath("//tbody")
        rows = table.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
        for row in rows:
            # Get the columns (all the data from column 1)
            col = row.find_elements(By.TAG_NAME, "td")[4]  # note: index start from 0, 1 and 2. Getting the data from 0.
            print("data - "+col.text)
            obj_data.append(col.text)
        if value:
            for data in obj_data:
                if str(data).__contains__(value):
                    continue
                else:
                    fprint(self, "actual - "+str(data)+" expected - "+str(value))
                    fprint(self, "[Failed] Not getting correct Filtered data for the - " + value)
                    self.fail("Not getting correct Filtered data for the - " + value)
        else:
            for data in obj_data:
                if min_range <= int(data) <= max_range:
                    continue
                else:
                    fprint(self, "actual - " + str(data) + " expected - should be under range "+str(min_range)+" to "+str(max_range))
                    fprint(self, "[Failed] Not getting correct Filtered data")
                    self.fail("Not getting correct Filtered data")
        fprint(self, "[Passed] Getting correct Filtered Data")

    def check_dates_in_threatdata_listing(self, yesterday_date, today_date):
        obj_data = []
        waitfor(self, 20, By.XPATH, "//tbody")
        fprint(self, "Threat Data listing is visible")
        table = self.driver.find_element_by_xpath("//tbody")
        rows = table.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
        for row in rows:
            # Get the columns (all the data from column 1)
            col = row.find_elements(By.TAG_NAME, "td")[4]  # note: index start from 0, 1 and 2. Getting the data from 0.
            print("data - " + col.text)
            obj_data.append(col.text)
        for data in obj_data:
            if str(data).__contains__(yesterday_date) or str(data).__contains__(today_date):
                continue
            else:
                fprint(self, "[Failed] actual - " + str(data) + " expected between - " + str(yesterday_date)+" and "+str(today_date))
                self.fail("Not getting correct Filtered data")
        fprint(self, "[Passed] Getting correct Filtered Data")

    def yesterday_date(self):
        global previous_date
        prev_date = datetime.datetime.now()
        ytd_date = int(prev_date.strftime("%d")) - 1
        if len(str(ytd_date)) > 1:
            ytd_date = prev_date.strftime("%b") + " " + str(ytd_date) + ", " + str(prev_date.year)
        else:
            ytd_date = prev_date.strftime("%b") + " 0" + str(ytd_date) + ", " + str(prev_date.year)
        fprint(self, "Yesterday's date - " + ytd_date)
        previous_date = ytd_date

    def date_pick_from_calendar(self, to_time="12:00:00 PM"):
        waitfor(self, 10, By.XPATH, "//input[@placeholder='From Date']")
        self.driver.find_element_by_xpath("//input[@placeholder='From Date']").click()
        waitfor(self, 10, By.XPATH, "//td[@class='available today']")
        element = self.driver.find_element_by_xpath("//td[@class='available today']/preceding::td[1]")
        ActionChains(self.driver).double_click(element).perform()
        # if from_date == "validUntil":
        #     self.driver.find_element_by_xpath("(//input[@placeholder='Select date'])[1]").click()
        #     clear_field(self.driver.find_element_by_xpath("(//input[@placeholder='Select date'])[1]"))
        #     self.driver.find_element_by_xpath("(//input[@placeholder='Select date'])[1]").send_keys("Sep 24 2020")
        #     self.driver.find_element_by_xpath("(//input[@placeholder='Select date'])[1]").send_keys(Keys.ENTER)
        #     sleep(4)
        self.driver.find_element_by_xpath("//h1/span[normalize-space()='Threat Data']").click()
        fprint(self, "Entered From date")
        waitfor(self, 10, By.XPATH, "//input[@placeholder='End Date']")
        self.driver.find_element_by_xpath("//input[@placeholder='End Date']").click()
        waitfor(self, 10, By.XPATH, "//td[@class='available today']")
        self.driver.find_element_by_xpath("(//td[@class='available today'])[2]").click()
        try:
            self.driver.find_element_by_xpath("(//input[@placeholder='Select time'])[2]").click()
        except:
            self.driver.find_element_by_xpath("//td[@class='available today']").click()
        clear_field(self.driver.find_element_by_xpath("(//input[@placeholder='Select time'])[2]"))
        self.driver.find_element_by_xpath("(//input[@placeholder='Select time'])[2]").send_keys(to_time)
        self.driver.find_element_by_xpath("(//input[@placeholder='Select time'])[2]").send_keys(Keys.ENTER)
        sleep(1)
        # if from_date == "validUntil":
        #     self.driver.find_element_by_xpath("(//input[@placeholder='Select date'])[2]").click()
        #     clear_field(self.driver.find_element_by_xpath("(//input[@placeholder='Select date'])[2]"))
        #     self.driver.find_element_by_xpath("(//input[@placeholder='Select date'])[2]").send_keys("Sep 24 2020")
        #     self.driver.find_element_by_xpath("(//input[@placeholder='Select date'])[2]").send_keys(Keys.ENTER)
        #     sleep(4)
        fprint(self, "Entered To date")
        date = datetime.datetime.now()
        current_date = date.strftime("%b")+" "+date.strftime("%d")+", "+str(date.year)
        fprint(self, "Today's date - " + current_date)
        self.driver.find_element_by_xpath("//h1/span[normalize-space()='Threat Data']").click()
        return current_date

    def enable_disabled_columns(self, col_name):
        element = self.driver.find_element_by_xpath("//span[contains(@class,'column-option') and contains(text(),'"+col_name+"')]/i[contains(@class,'cyicon-check-circle-outline')]")
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.driver.find_element_by_xpath("//span[contains(@class,'column-option') and contains(text(),'"+col_name+"')]/i[contains(@class,'cyicon-check-circle-outline')]").click()
        fprint(self, "Column Enabled - " + col_name)

    def disable_active_columns(self, data):
        for col in data:
            if waitfor(self, 0, By.XPATH, "//span[contains(@class,'column-option__active') and contains(text(),'"+col+"')]", False):
                element = self.driver.find_element_by_xpath("//span[contains(text(),'"+col+"') and contains(@class,'column-option__active')]/i[contains(@class,'cyicon-check-circle-outline')]")
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                self.driver.find_element_by_xpath("//span[contains(text(),'"+col+"') and contains(@class,'column-option__active')]/i[contains(@class,'cyicon-check-circle-outline')]").click()
                fprint(self, "Column Disabled - "+col)

    def visible_column(self, col_name):
        global flag
        data = []
        self.driver.find_element_by_xpath("//div[@data-testaction='dropdown-link']//div[contains(@class,'cyicon-add-active')]").click()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Custom')]/parent::div//div[@class='section-columns']")
        cust_col = self.driver.find_element_by_xpath("//span[contains(text(),'Custom')]/parent::div//div[@class='section-columns']")
        col_names = cust_col.find_elements(By.TAG_NAME, "span")
        for col in col_names:
            data.append(col.text)
        if flag == 0:
            fprint(self, "Disabling all Active columns")
            self.disable_active_columns(data)
            flag = flag + 1
            fprint(self, "Enabling Column - "+col_name)
            self.enable_disabled_columns(col_name)
        self.driver.find_element_by_xpath("//div[@data-testaction='dropdown-link']//div[contains(@class,'cyicon-add-active')]").click()

    def verify_data_in_threatdata(self, value):
        fprint(self, "Waiting for the Search Bar")
        waitfor(self, 20, By.XPATH, threat_data_main_search_field)
        fprint(self, "Searching for the Feed under Indicator - " + value)
        clear_field(self.driver.find_element_by_xpath(threat_data_main_search_field))
        self.driver.find_element_by_xpath(threat_data_main_search_field).click()
        self.driver.find_element_by_xpath(threat_data_main_search_field).send_keys(value)
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'" + value + "')]")
        fprint(self, "Feed Visible - " + value)

    def click_on_intel(self, value):
        wait = WebDriverWait(self.driver, 10)
        ele = wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(),'" + value + "')]")))
        fprint(self, "Clicking on the Intel - " + value)
        self.driver.execute_script("arguments[0].click();", ele)

    def test_01_verify_objectType_filter(self):
        fprint(self, "TC_ID: 4000501 - test_01_verify_objectType_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Clear Selected')]").click()
        fprint(self, "Clicked on the  - Clear Selected")
        select_threatData_filter(self, "Object Type", "Malware")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.visible_column("Type")
        self.check_data_in_threatData_listing("malware")

    def test_02_verify_iocType_filter(self):
        fprint(self, "TC_ID: 4000502 - test_02_verify_iocType_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "IOC Type", "URL")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.check_value_in_threatData_listing("url")

    def test_03_verify_TLP_filter(self):
        fprint(self, "TC_ID: 4000503 - test_03_verify_TLP_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "TLP", "Red")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.check_value_in_threatData_listing("tlp")

    def test_04_verify_sourceConfidence_filter(self):
        fprint(self, "TC_ID: 4000504 - test_04_verify_sourceConfidence_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "Source Confidence", "High")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.visible_column("Source Confidence")
        self.check_data_in_threatData_listing("High")

    def test_05_verify_tags_filter(self):
        fprint(self, "TC_ID: 4000505 - test_05_verify_tags_filter")
        nav_menu_main(self, "Threat Data")
        quick_create_ip(self, "68.58.78.98", "filterIP", metadata_confidence=0)
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "Tags", "filterTag")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.visible_column("Tags")
        self.check_data_in_threatData_listing("filterTag")

    def test_06_verify_sourceType_filter(self):
        fprint(self, "TC_ID: 4000506 - test_06_verify_sourceType_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "Source Type", "Web Scraper")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.visible_column("Source")
        self.check_data_in_threatData_listing("test_automation_title")

    def test_07_verify_sourceCollection_filter(self):
        fprint(self, "TC_ID: 4000507 - test_07_verify_sourceCollection_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "Source Collections", "Free Text")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.visible_column("Source Collection")
        self.check_data_in_threatData_listing("Free Text")

    def test_08_verify_analystScore_filter(self):
        fprint(self, "TC_ID: 4000508 - test_08_verify_analystScore_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "Analyst Score")
        waitfor(self, 10, By.XPATH, "//input[@placeholder='Min']")
        # Analyst Score is Set in the threat data details page file
        self.driver.find_element_by_xpath("//input[@placeholder='Min']").send_keys("40")
        fprint(self, "Entering Minimum value - 40")
        self.driver.find_element_by_xpath("//input[@placeholder='Max']").send_keys("50")
        fprint(self, "Entering Maximum value - 50")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.visible_column("Analyst Score")
        self.check_data_in_threatData_listing(value=False, min_range=40, max_range=50)

    def test_09_verify_manualReview_filter(self):
        fprint(self, "TC_ID: 4000509 - test_09_verify_manualReview_filter")
        nav_menu_main(self, "Threat Data")
        # IP taken from the Confidence Score properties file
        self.verify_data_in_threatdata(manualReview)
        self.click_on_intel(manualReview)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Manual Review')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Manual Review')]").click()
        verify_success(self, "Selected objects are added for manual review successfully")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Under Manual Review')]")
        fprint(self, "Under Manual Review, option is visible")
        self.driver.find_element_by_xpath("//span[@class='cy-page__back-button']").click()
        select_threatData_filter(self, "Manual Review")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Yes')]//ancestor::li[@name='select-option']")
        self.driver.find_element_by_xpath("//span[contains(text(),'Yes')]//ancestor::li[@name='select-option']").click()
        fprint(self, "Selected Yes Option")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.verify_data_in_threatdata(manualReview)
        fprint(self, "[Passed] Getting correct Filtered Data")

    def test_10_verify_indicatorAllowedStatus_filter(self):
        fprint(self, "TC_ID: 4000510 - test_10_verify_IndicatorAllowedStatus_filter")
        nav_menu_main(self, "Threat Data")
        # IP taken from the Confidence Score properties file
        self.verify_data_in_threatdata(indicatorAllowedStatus)
        self.click_on_intel(indicatorAllowedStatus)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Indicator Allowed')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Indicator Allowed')]").click()
        fprint(self, "Clicked on the Indicator Allowed")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Add to Indicator Allowed')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Add to Indicator Allowed')]").click()
        fprint(self, "Clicked on the option - Add to Indicator Allowed")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Save')]/parent::button")
        self.driver.find_element_by_xpath("//span[contains(text(),'Save')]/parent::button").click()
        verify_success(self, "successfully")
        self.driver.find_element_by_xpath("//span[@class='cy-page__back-button']").click()
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "Indicators Allowed Status")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Indicators Allowed ')]/parent::span")
        try:
            self.driver.find_element_by_xpath("//span[contains(text(),'Indicators Allowed ')]/parent::span").click()
        except:
            fprint(self, "Trying with different xpath...")
            self.driver.find_element_by_xpath("(//span[contains(text(),'Indicators Allowed ')]/parent::span)[2]").click()
        fprint(self, "Clicked on the Indicators Allowed Option")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.verify_data_in_threatdata(indicatorAllowedStatus)
        fprint(self, "[Passed] Getting correct Filtered Data")

    def test_11_verify_reviewedStatus_filter(self):
        fprint(self, "TC_ID: 4000511 - test_09_verify_reviewedStatus_filter")
        nav_menu_main(self, "Threat Data")
        # IP taken from the Confidence Score properties file
        self.verify_data_in_threatdata(reviewedStatus)
        self.click_on_intel(reviewedStatus)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Manual Review')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Manual Review')]").click()
        verify_success(self, "Selected objects are added for manual review successfully")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Under Manual Review')]")
        fprint(self, "Under Manual Review, option is visible")
        self.driver.find_element_by_xpath("//span[contains(text(),'Under Manual Review')]").click()
        fprint(self, "Clicked on the option - Under Manual Review")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Mark as Reviewed')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Mark as Reviewed')]").click()
        fprint(self, "Mark as Reviewed, option is visible, clicked on it")
        verify_success(self, "Selected objects are marked as reviewed successfully")
        if waitfor(self, 5, By.XPATH, "//span[contains(text(),'Manually Reviewed')]", False) or \
                waitfor(self, 1, By.XPATH, "//span[contains(text(),'Manual Reviewed')]"):
            fprint(self, "Manual Reviewed, option is visible")
        fprint(self, "Manual Reviewed, option is visible")
        self.driver.find_element_by_xpath("//span[@class='cy-page__back-button']").click()
        select_threatData_filter(self, "Reviewed Status")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Reviewed')]//ancestor::li[@name='select-option']")
        self.driver.find_element_by_xpath("//span[contains(text(),'Reviewed')]//ancestor::li[@name='select-option']").click()
        fprint(self, "Selected Reviewed Option")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.verify_data_in_threatdata(reviewedStatus)
        fprint(self, "[Passed] Getting correct Filtered Data")

    def test_12_verify_hasRelations_filter(self):
        fprint(self, "TC_ID: 4000512 - test_12_verify_hasRelations_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "Has Relations")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Yes')]//ancestor::li[@name='select-option']")
        self.driver.find_element_by_xpath("//span[contains(text(),'Yes')]//ancestor::li[@name='select-option']").click()
        fprint(self, "Selected Yes Option")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        # IP taken from the Confidence Score properties file
        self.verify_data_in_threatdata(relation)
        fprint(self, "[Passed] Getting correct Filtered Data")

    def test_13_verify_relationType_filter(self):
        fprint(self, "TC_ID: 4000513 - test_13_verify_relationType_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "Relation Type", "related-to")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        # IP taken from the Confidence Score properties file
        self.verify_data_in_threatdata(relation)
        fprint(self, "[Passed] Getting correct Filtered Data")

    def test_14_verify_relatedObject_filter(self):
        fprint(self, "TC_ID: 4000514 - test_13_verify_relationType_filter")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "Related Object", "Campaign")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        # IP taken from the Confidence Score properties file
        self.verify_data_in_threatdata(relation)
        fprint(self, "[Passed] Getting correct Filtered Data")

    def test_15_verify_falsePositive_filter(self):
        fprint(self, "TC_ID: 4000515 - test_15_verify_falsePositive_filter")
        nav_menu_main(self, "Threat Data")
        # IP taken from the Confidence Score properties file
        self.verify_data_in_threatdata(falsePositive)
        self.click_on_intel(falsePositive)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'False Positive')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'False Positive')]").click()
        fprint(self, "False Positive, option is visible and clicked on it")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Mark False Positive')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Mark False Positive')]").click()
        fprint(self, "Mark False Positive, option is visible and clicked on it")
        verify_success(self, "Selected indicators are marked as false positive successfully")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Marked False Positive')]")
        self.driver.find_element_by_xpath("//span[@class='cy-page__back-button']").click()
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "False Positive Status")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'False Positive ')]/parent::span")
        self.driver.find_element_by_xpath("//span[contains(text(),'False Positive ')]/parent::span").click()
        fprint(self, "Clicked on the False Positive Option")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.verify_data_in_threatdata(falsePositive)
        fprint(self, "[Passed] Getting correct Filtered Data")

    def test_16_verify_createdOn_filter(self):
        fprint(self, "TC_ID: 4000516 - test_16_verify_createdOn_filter")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "Created")
        date = self.date_pick_from_calendar()
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.visible_column("Created")
        self.yesterday_date()
        self.check_dates_in_threatdata_listing(yesterday_date=previous_date, today_date=date)

    def test_17_verify_modifiedOn_filter(self):
        fprint(self, "TC_ID: 4000517 - test_17_verify_modifiedOn_filter")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "Modified")
        self.date_pick_from_calendar("11:00:00 AM")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.visible_column("Created")
        self.yesterday_date()
        self.check_dates_in_threatdata_listing(yesterday_date="PM", today_date="AM")

    def test_18_verify_confidenceScore_filter(self):
        fprint(self, "TC_ID: 4000518 - test_18_confidenceScore_filter")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "Confidence Score")
        waitfor(self, 10, By.XPATH, "//input[@placeholder='Min']")
        self.driver.find_element_by_xpath("//input[@placeholder='Min']").send_keys("30")
        fprint(self, "Entering Minimum value - 30")
        self.driver.find_element_by_xpath("//input[@placeholder='Max']").send_keys("60")
        fprint(self, "Entering Maximum value - 60")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.visible_column("Conf Score")
        self.check_data_in_threatData_listing(False, min_range=30, max_range=60)

    def test_19_verify_countries_filter(self):
        fprint(self, "TC_ID: 4000519 - test_19_country_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "Countries", "Australia")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.visible_column("Country")
        self.check_data_in_threatData_listing("Australia")

    def test_20_verify_publishedCollections_filter(self):
        fprint(self, "TC_ID: 4000520 - test_20_publishedCollection_filter")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "Published Collections", "col_2.1")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        # ToDo: need to brainstorm more how to verify by below lines.
        # self.visible_column("Published Collections")
        # self.check_data_in_threatData_listing("col_2.1")
        self.verify_data_in_threatdata("NewName")

    def test_21_verify_publishedOn_filter(self):
        fprint(self, "TC_ID: 4000521 - test_21_publishedOn_filter")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "Published")
        self.date_pick_from_calendar()
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        # domain picked from the subscriber case
        self.verify_data_in_threatdata(subs_domain)

    def test_22_verify_deprecatedStatus_filter(self):
        fprint(self, "TC_ID: 4000522 - test_22_deprecatedStatus_filter")
        nav_menu_main(self, "Threat Data")
        # IP taken from the Confidence Score properties file
        self.verify_data_in_threatdata(deprecatedStatus)
        self.click_on_intel(deprecatedStatus)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Deprecate')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Deprecate')]").click()
        fprint(self, "Deprecate, option is visible and clicked on it")
        waitfor(self, 20, By.XPATH, "(//span[contains(text(),'Deprecate')])[2]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'Deprecate')])[2]").click()
        verify_success(self, "Selected indicators are deprecated successfully")
        self.driver.find_element_by_xpath("//span[@class='cy-page__back-button']").click()
        select_threatData_filter(self, "Deprecated Status")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Deprecated')]//ancestor::li[@name='select-option']")
        self.driver.find_element_by_xpath("//span[contains(text(),'Deprecated')]//ancestor::li[@name='select-option']").click()
        fprint(self, "Selected Deprecated Option")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.verify_data_in_threatdata(deprecatedStatus)
        fprint(self, "[Passed] Getting correct Filtered Data")

    def test_23_verify_enrichmentTools_filter(self):
        fprint(self, "TC_ID: 4000523 - test_23_enrichmentTools_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "Enrichment Tools", "AbuseIPDB")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        # Ipv4 picked from the quick add intel
        self.verify_data_in_threatdata(enrich_ip)

    def test_24_verify_enrichmentVerdict_filter(self):
        fprint(self, "TC_ID: 4000524 - test_24_enrichmentVerdict_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "Enrichment Verdict")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Malicious')]//ancestor::li[@name='select-option']")
        self.driver.find_element_by_xpath("//span[contains(text(),'Malicious')]//ancestor::li[@name='select-option']").click()
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        # domain picked from the subscriber case
        fprint(self, "Searching - "+subs_domain)
        self.driver.find_element_by_xpath(threat_data_main_search_field).click()
        self.driver.find_element_by_xpath(threat_data_main_search_field).send_keys(subs_domain)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Do a new search query / apply filters')]")
        fprint(self, "[Passed] Getting correct Filtered Data")

    def test_25_verify_enrichedStatus_filter(self):
        fprint(self, "TC_ID: 4000525 - test_25_enrichedStatus_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "Enriched Status", "Enriched")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        # Ipv4 picked from the quick add intel
        self.verify_data_in_threatdata(enrich_ip)

    def test_26_verify_enrichedOn_filter(self):
        fprint(self, "TC_ID: 4000526 - test_26_enrichedOn_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "Enriched")
        self.date_pick_from_calendar()
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        # domain picked from the subscriber case
        self.verify_data_in_threatdata(enrich_ip)

    def test_27_verify_rules_filter(self):
        fprint(self, "TC_ID: 4000527 - test_27_rules_filter")
        nav_menu_main(self, "Threat Data")
        # Rule taken from the Rules cases - manual review
        select_threatData_filter(self, "Rules", "auto_rule_manual_review")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        # Ipv4 picked from the rules.py file
        self.verify_data_in_threatdata(rules)

    def test_28_verify_actionedOn_filter(self):
        fprint(self, "TC_ID: 4000528 - test_28_actionedOn_filter")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "Actioned on")
        self.date_pick_from_calendar("9:00:00 PM")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        # domain picked from the quick add intel case
        self.verify_data_in_threatdata(domain)

    def test_29_verify_actionMedium_filter(self):
        fprint(self, "TC_ID: 4000529 - test_29_verify_actionMedium_filter")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "Action Medium", "Manual")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        # Domain picked from the quick add intel
        self.verify_data_in_threatdata(domain)

    def test_30_verify_actionedAppType_filter(self):
        fprint(self, "TC_ID: 4000530 - test_30_verify_actionedAppType_filter")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "Actioned App Type", "3rd Party")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        # Ipv4 picked from the trigger playbook v3
        self.verify_data_in_threatdata(actionAppType)

    def test_31_verify_validFrom_filter(self):
        fprint(self, "TC_ID: 4000531 - test_31_verify_validFrom_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "Valid from")
        date = self.date_pick_from_calendar(to_time="4:00:00 PM")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.visible_column("Valid From")
        self.yesterday_date()
        self.check_dates_in_threatdata_listing(yesterday_date=previous_date, today_date=date)

    def test_32_verify_validUntil_filter(self):
        fprint(self, "TC_ID: 4000532 - test_32_verify_validUntil_filter")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//*[contains(text(),'Clear Selected')]")
        self.driver.find_element_by_xpath("//*[contains(text(),'Clear Selected')]").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        select_threatData_filter(self, "Valid Until")
        date = self.date_pick_from_calendar()
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        self.visible_column("Valid Until")
        self.check_data_in_threatData_listing(date)

    def test_33_verify_actionedBy_filter(self):
        fprint(self, "TC_ID: 4000533 - test_33_verify_actionedBy_filter")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "Actioned By", "testuserpermissions@cyware.com")
        sleep(2)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Do a new search query / apply filters')]")
        fprint(self, "[Passed] Getting correct Filtered Data")

    def test_34_verify_actionedOn_filter(self):
        fprint(self, "TC_ID: 4000534 - test_34_verify_actionedOn_filter")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "Actioned on")
        self.date_pick_from_calendar(to_time="4:00:00 PM")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        # Ipv4 picked from the quick add intel
        self.verify_data_in_threatdata(actionedOn)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())