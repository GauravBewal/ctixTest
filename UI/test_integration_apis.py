import os.path
import unittest
from lib.ui.nav_tableview import *
from lib.ui.nav_threat_data import *

# listitem = ["Indicator", "Malware", "Threat Actor", "Vulnerability", "Attack Pattern", "Campaign",
#             "Course of Action", "Identity", "Infrastructure", "Intrusion Set", "Location",
#             "Malware Analysis", "Observed Data", "Opinion", "Tool", "Report", "Custom Object", "Observable"]
listitem = ["Indicator", "Malware", "Threat Actor", "Vulnerability", "Attack Pattern", "Campaign",
            "Course of Action", "Identity", "Infrastructure", "Intrusion Set", "Location",
            "Malware Analysis", "Tool", "Report"]


class IntegrationApi(unittest.TestCase):

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

    def search(self, api_feed_name):
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        fprint(self, "Clicked on the search bar")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("Source")
        waitfor(self, 20, By.XPATH, "(//span[contains(text(),'Source')]/ancestor::a[1]/parent::li)[1]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'Source')]/ancestor::a[1]/parent::li)[1]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//span[@id='dropdown-0']//input").click()
        self.driver.find_element_by_xpath("//span[@id='dropdown-0']//input").send_keys(api_feed_name)
        waitfor(self, 20, By.XPATH, "(//span[contains(text(),'" + api_feed_name + "')]/ancestor::a[1])")
        self.driver.find_element_by_xpath("(//span[contains(text(),'" + api_feed_name + "')]/ancestor::a[1])").click()
        fprint(self, "Searched - "+api_feed_name)
        waitfor(self, 20, By.XPATH, "//span[text()='Press enter or click to search']")
        self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()

    def apply_filter(self, api_feed_name):
        fprint(self, "Navigating to the Threat Data")
        nav_menu_main(self, "Threat Data")
        # if waitfor(self, 20, By.XPATH, "(//span[contains(text(),'Source')]/ancestor::div[1]/ancestor::div[1])[1]", False):
        #     self.driver.find_element_by_xpath("(//span[contains(text(),'Source')]/ancestor::div[1]/ancestor::div[1])[1]").click()
        #     fprint(self, "Clicked on the Source filter")
        #     if waitfor(self, 20, By.XPATH, "//span[@class='cy-text-f12-medium cy-cursor-pointer cy-color-B30 cy-px-4 cy-mb-3']", False):
        #         fprint(self, "More link is visible")
        #         sleep(2)
        #         self.driver.find_element_by_xpath("//span[@class='cy-text-f12-medium cy-cursor-pointer cy-color-B30 cy-px-4 cy-mb-3']").click()
        #         fprint(self, "Clicked on the More link")
        #         sleep(1)
        #     waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+api_feed_name+"')]/ancestor::div[1]")
        #     fprint(self, "API Feed source is visible - "+api_feed_name)
        #     self.driver.find_element_by_xpath("//span[contains(text(),'"+api_feed_name+"')]/ancestor::div[1]").click()
        #     fprint(self, "API Feed source is clicked - "+api_feed_name)
        #     sleep(1)
        #     self.driver.find_element_by_xpath("(//span[contains(text(),'Threat Data')])[2]").click()
        select_threatData_filter(self, filter_name="Source", object_name=api_feed_name)
        fprint(self, "Clicked on the Threat Data Title, to close the filter")
        sleep(4)

    def verify_polled_data(self, api_feed_name):
        if Build_Version.__contains__("3."):
            if waitfor(self, 20, By.XPATH, "//span[contains(text(),'" + api_feed_name + "')]/ancestor::tr/td[3]//span[contains(text(),'')]", False):
                fprint(self, "Data is visible for - " + api_feed_name)
            else:
                fprint(self, "No data is visible for -" + api_feed_name)
                unittest.TestCase.fail(self, "No data found")
        else:
            for item in listitem:
                waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+item+"')]/parent::a")
                self.driver.find_element_by_xpath("//span[contains(text(),'"+item+"')]/parent::a").click()
                sleep(2)
                self.search(api_feed_name)
                if waitfor(self, 20, By.XPATH, "//div[contains(text(),'CrowdStrike')]/ancestor::tr/td[3]//span[contains(text(),'')]", False):
                    fprint(self, "Data is visible for - "+api_feed_name)
                    break
                else:
                    if item == "Report":
                        fprint(self, "No data is visible for -"+api_feed_name)
                        unittest.TestCase.fail(self, "No data found")

    def poll_data(self, api_feed_name, channel_name="ALL"):
        self.driver.find_element_by_xpath("//img[@alt='" + api_feed_name + "']").click()
        fprint(self, "Clicked on the -"+api_feed_name)
        waitfor(self, 20, By.XPATH, "//tbody/ancestor::table")
        table = self.driver.find_element_by_xpath("//tbody/ancestor::table")
        rows = table.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
        feed_channels = []
        # count = 1
        for row in rows:
            col = row.find_elements(By.TAG_NAME, "td")[-7]
            if channel_name == "ALL":
                feed_channels.append(col.text)
            elif str(col.text).__contains__(channel_name):
                feed_channels.append(col.text)
                fprint(self, "Polling Specific Channel - " + str(col.text))
                break
            # if count == 1:
            #     col = row.find_elements(By.TAG_NAME, "td")[1]
            #     if channel_name == "Null":
            #         feed_channels.append(col.text)
            #     elif str(col.text).__contains__(channel_name):
            #         feed_channels.append(col.text)
            #         fprint(self, "Polling Specific Channel - " + str(col.text))
            # else:
            #     # Get the columns (all the data from column 1)
            #     col = row.find_elements(By.TAG_NAME, "td")[0]  # note: index start from 0, 1 and 2. Getting the data from 0.
            #     if channel_name == "Null":
            #         feed_channels.append(col.text)
            #     elif str(col.text).__contains__(channel_name):
            #         feed_channels.append(col.text)
            #         fprint(self, "Polling Specific Channel - " + str(col.text))
            # count = 0
            # fprint(self, "value store - " + col.text)
        print("Feed channels - ", feed_channels)

        if Build_Version.__contains__("3."):
            for data in feed_channels:
                # if api_feed_name == "Volon":
                #     element = self.driver.find_element_by_xpath("//span[contains(text(),'"+data+"')]")
                #     self.driver.execute_script("arguments[0].scrollIntoView();", element)
                click_on_actions_item(self, data, "Poll Now", "apifeeds")
        else:
            for data in feed_channels:
                waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+data+"')]/ancestor::td/following-sibling::td[6]//button")
                self.driver.find_element_by_xpath("//span[contains(text(),'"+data+"')]/ancestor::td/following-sibling::td[6]//button").click()
                waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+data+"')]/ancestor::td/following-sibling::td[6]//button")
                elms = self.driver.find_elements(By.XPATH, "//span[contains(text(),'Poll Now')]")
                for elm in elms:
                    if elm.is_displayed():
                        elm.click()
                        fprint(self, "Clicked on the option - Poll Now")
        sleep(2)

    def tool_status(self):
        if waitfor(self, 3, By.XPATH, "//span[contains(text(),'Add Instance')]", False):
            try:
                fprint(self, "Add Instance' button is visible, clicking on it")
                self.driver.find_element_by_xpath("//span[contains(text(),'Add Instance')]").click()
            except:
                fprint(self, "Credentials slider is already visible...")
        elif waitfor(self, 5, By.XPATH, "//span[contains(text(),'Enabled')]", False):
            fprint(self, "'Enabled' button is visible")
            self.driver.find_element_by_xpath("//button[@data-testid='actions']").click()
            fprint(self, "Clicked on the action menu")
            sleep(1)  # Sleep is necessary here
            waitfor(self, 3, By.XPATH, "//li[contains(text(),'Manage')]")
            self.driver.find_element_by_xpath("//li[contains(text(),'Manage')]").click()
            fprint(self, "Clicked on the Manage option")
            waitfor(self, 3, By.XPATH, "//button[contains(text(),'Edit')]")
            self.driver.find_element_by_xpath("//button[contains(text(),'Edit')]").click()
            fprint(self, "Clicked on the Edit button")
            waitfor(self, 3, By.XPATH, "//div/span[contains(text(),'Edit')]")
        elif waitfor(self, 5, By.XPATH, "//span[contains(text(),'Disabled')]", False):
            fprint(self, "'Disabled' button is visible")
            self.driver.find_element_by_xpath("//button[@data-testid='actions']").click()
            fprint(self, "Clicked on the action menu")
            sleep(1)  # Sleep is necessary here
            waitfor(self, 3, By.XPATH, "//li[contains(text(),'Manage')]")
            self.driver.find_element_by_xpath("//li[contains(text(),'Manage')]").click()
            fprint(self, "Clicked on the Manage option")
            waitfor(self, 3, By.XPATH, "//button[contains(text(),'Edit')]")
            self.driver.find_element_by_xpath("//button[contains(text(),'Edit')]").click()
            fprint(self, "Clicked on the Edit button")
            waitfor(self, 3, By.XPATH, "//div/span[contains(text(),'Edit')]")

    def configure_apiFeeds(self, api_feed_name):
        fprint(self, "Clicking on the 'Add API Source' Button")
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'Add API Source')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add API Source')]").click()
        # process_console_logs(self)
        fprint(self, "Searching for the API Feed - "+api_feed_name)
        search(self, api_feed_name)
        waitfor(self, 20, By.XPATH, "//p[contains(text(),'" + api_feed_name + "')]")
        fprint(self, "API Feed is visible, Clicking on it - " + api_feed_name)
        self.driver.find_element_by_xpath("//p[contains(text(),'"+api_feed_name+"')]").click()
        fprint(self, "Inside API Feed - "+api_feed_name)
        if waitfor(self, 8, By.XPATH, "//button[contains(text(),'DONE')]", False):
            self.driver.find_element_by_xpath("//button[contains(text(),'DONE')]").click()
            waitfor(self, 20, By.XPATH, "//button[contains(text(),'OK')]")
            self.driver.find_element_by_xpath("//button[contains(text(),'OK')]").click()
        # Checking Tool status (enabled/disabled/inactive)
        self.tool_status()
        # Reading Credentials from the CSV File.
        testplan_file = get_value("testplan")
        if testplan_file == "ui_v3_apifeeds_original_cred.txt":
            file = "api_feeds_original_credentials.csv"
        else:
            file = "api_feeds_orion_credentials.csv"
        fprint(self, "Picked testplan file - "+file)
        filename = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds", file)
        with open(filename, 'r') as obj:
            data = csv.reader(obj)
            for apiFeeds in data:
                if apiFeeds[0] == api_feed_name:
                    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Instance Name*']")
                    fprint(self, "Filling credentials")
                    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Instance Name*']"))
                    self.driver.find_element_by_xpath("//input[@aria-placeholder='Instance Name*']").send_keys(api_feed_name)
                    fprint(self, "Instance name - "+api_feed_name)
                    if api_feed_name == "Flashpoint":
                        if Build_Version.__contains__("3."):
                            clear_field(self.driver.find_element_by_xpath("//input[@name='base_url']"))
                            fprint(self, "TestData - Base URL - " + apiFeeds[1])
                            self.driver.find_element_by_xpath("//input[@name='base_url']").send_keys(apiFeeds[1])
                        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Bearer Token*']"))
                        self.driver.find_element_by_xpath("//input[@aria-placeholder='Bearer Token*']").send_keys(apiFeeds[2])
                        fprint(self, "TestData - Entered Token: " + apiFeeds[2])
                    elif api_feed_name == "MITRE":
                        # As Base_Url for MITRE is fixed and can't be edited
                        pass
                    elif api_feed_name == "Recorded Future" or api_feed_name == "Volon" or api_feed_name == "Flexera" or api_feed_name == "MISP" or api_feed_name == "Alien Vault":
                        clear_field(self.driver.find_element_by_xpath("//input[@name='base_url']"))
                        self.driver.find_element_by_xpath("//input[@name='base_url']").send_keys(apiFeeds[1])
                        fprint(self, "TestData - Base URL: " + apiFeeds[1])
                        clear_field(self.driver.find_element_by_xpath("//input[@name='access_key']"))
                        self.driver.find_element_by_xpath("//input[@name='access_key']").send_keys(apiFeeds[2])
                        fprint(self, "TestData - Entered Access Key: " + apiFeeds[2])
                    else:
                        clear_field(self.driver.find_element_by_xpath("//input[@name='base_url']"))
                        self.driver.find_element_by_xpath("//input[@name='base_url']").send_keys(apiFeeds[1])
                        fprint(self, "TestData - Base URL: " + apiFeeds[1])
                        clear_field(self.driver.find_element_by_xpath("//input[@name='access_key']"))
                        self.driver.find_element_by_xpath("//input[@name='access_key']").send_keys(apiFeeds[2])
                        fprint(self, "TestData - Entered Access Key: " + apiFeeds[2])
                        clear_field(self.driver.find_element_by_xpath("//input[@name='secret_key']"))
                        self.driver.find_element_by_xpath("//input[@name='secret_key']").send_keys(apiFeeds[3])
                        fprint(self, "TestData - Entered Secret Key: " + apiFeeds[3])
                    if api_feed_name == "QRadar" or api_feed_name == "MISP":
                        self.driver.find_element_by_xpath("//span[contains(text(),' Verify SSL ')]").click()
                        sleep(1)
                    self.driver.find_element_by_xpath("//button[text()='Save']").click()
                    fprint(self, "Clicked on the Save Button")
                    verify_success(self, "Instance configuration updated successfully", 15)
                    waitfor(self, 20, By.XPATH, "//span[contains(text(),'Enabled')]")
                    fprint(self, "Enabled Button is visible")
                    process_console_logs(self)
                    break

    def enable_eachFeed(self, api_feed_name, feed_channel):
        fprint(self, "Enabling the Feed Channel - "+feed_channel)
        if waitfor(self, 10, By.XPATH, "//form//input[@type='checkbox' and @value='false']", False):
            self.driver.find_element_by_xpath("//form//span[input[@type='checkbox' and @value='false']]").click()
        else:
            fprint(self, "Seems like older version, trying to click with different xpath")
            self.driver.find_element_by_xpath("//span[contains(text(),'Disabled')]").click()
        if api_feed_name == "Recorded Future":
            fprint(self, "Selecting Risk Type")
            self.driver.find_element_by_xpath("//div[@name='risk_list_type']").click()
            header_text = str(self.driver.find_element_by_xpath("//div[@class='cy-component-modal__header--back']").text)
            fprint(self, "Header Text: " + header_text)
            if header_text.__contains__("Vulnerability Feeds Data"):
                fprint(self, "Vulnerability Feeds Data")
                self.driver.find_element_by_xpath("//div[@name='risk_list_type']").click()
                sleep(2)
                self.driver.find_element_by_xpath(rf_risk_list_type).send_keys("Vulnerability Full")
                set_value("RF_vul_collname", "Collection_" + uniquestr)
            elif header_text.__contains__("Retrieve IP Feeds Data"):
                fprint(self, "Retrieve IP Feeds Data")
                self.driver.find_element_by_xpath("//div[@name='risk_list_type']").click()
                sleep(2)
                self.driver.find_element_by_xpath(rf_risk_list_type).send_keys("IP Full")
                set_value("RF_ip_collname", "Collection_" + uniquestr)
            elif header_text.__contains__("Retrieve Domain Feeds Data"):
                fprint(self, "Retrieve Domain Feeds Data")
                self.driver.find_element_by_xpath("//div[@name='risk_list_type']").click()
                sleep(2)
                self.driver.find_element_by_xpath(rf_risk_list_type).send_keys("Domain Full")
                set_value("RF_domain_collname", "Collection_" + uniquestr)
            elif header_text.__contains__("Retrieve URL Feeds Data"):
                fprint(self, "Retrieve URL Feeds Data")
                self.driver.find_element_by_xpath("//div[@name='risk_list_type']").click()
                sleep(2)
                self.driver.find_element_by_xpath(rf_risk_list_type).send_keys("URL Full")
                set_value("RF_url_collname", "Collection_" + uniquestr)
            elif header_text.__contains__("Retrieve Hash Feeds Data"):
                fprint(self, "Retrieve Hash Feeds Data")
                self.driver.find_element_by_xpath("//div[@name='risk_list_type']").click()
                sleep(2)
                self.driver.find_element_by_xpath(rf_risk_list_type).send_keys("Hash Full")
                set_value("RF_hash_collname", "Collection_" + uniquestr)
            waitfor(self, 20, By.XPATH, "(//li[@role='menuitem']//div[@name='text'])[1]")
            self.driver.find_element_by_xpath("(//li[@role='menuitem']//div[@name='text'])[1]").click()
            fprint(self, "Selected the top Risk type in dropdown")
            self.driver.find_element_by_xpath("//span[@class='cyicon-chevron-down  active']/ancestor::div[1]").click()

        elif api_feed_name == "MITRE":
            sleep(1)
            fprint(self, "Selecting date from the calender")
            self.driver.find_element_by_xpath("//input[@name='last_intel_feed_poll_date']").click()
            fprint(self, "Going back to previous year")
            self.driver.find_element_by_xpath("//button[@aria-label='Previous Year']").click()
            waitfor(self, 20, By.XPATH, "(//td[@class='available'])[1]")
            self.driver.find_element_by_xpath("(//td[@class='available'])[1]").click()
            fprint(self, "Selected previous month date")

        else:
            if feed_channel == "Sinkhole IP Feed":
                waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Collection Name*']")
                fprint(self, "Collection field is visible")
            elif waitfor(self, 5, By.XPATH, "//input[@name='last_intel_feed_poll_date']", False):
                fprint(self, "Selecting date from the calender")
                self.driver.find_element_by_xpath("//input[@name='last_intel_feed_poll_date']").click()
                if waitfor(self, 20, By.XPATH, "(//td[@class='available today']/preceding::td[1])[1]", False):
                    self.driver.find_element_by_xpath("(//td[@class='available today']/preceding::td[1])[1]").click()
                    fprint(self, "Selected Yesterday's date")
                elif waitfor(self, 20, By.XPATH, "//td[@class='available today']/ancestor::tr/preceding::tr[1]/td[7]", False):
                    self.driver.find_element_by_xpath("//td[@class='available today']/ancestor::tr/preceding::tr[1]/td[7]").click()
                    fprint(self, "Selected Yesterday's date")
                else:
                    fprint(self, "Going back to previous month")
                    self.driver.find_element_by_xpath("//button[@aria-label='Previous Month']").click()
                    waitfor(self, 20, By.XPATH, "//td[@class='next-month']")
                    self.driver.find_element_by_xpath("//td[@class='next-month']").click()
                    fprint(self, "Selected previous month date")
        fprint(self, "Giving Collection name - " + uniquestr)
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Collection Name*']").send_keys(
            "Collection_" + uniquestr)
        fprint(self, "Selecting Polling type Manual")
        self.driver.find_element_by_xpath("//div[contains(text(),'Manual')]").click()
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "Clicked on the Save button")
        # sleep(1)    # -----------Sleep is needed here, saving above configuration takes time.
        # Intentionally commented the below line because of the inconsistency in the saving time and also overlapping the other element
        verify_success(self, "updated successfully")
        # process_console_logs(self)

    def enable_apiFeeds(self, api_feed_name, channel_name="Null"):
        fprint(self, "Clicking on the actions menu")
        self.driver.find_element_by_xpath("//button[@data-testid='actions']").click()
        waitfor(self, 20, By.XPATH, "//li[contains(text(),'Manage')]")
        fprint(self, "Clicking on the Manage option")
        self.driver.find_element_by_xpath("//li[contains(text(),'Manage')]").click()
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'Manage  Feed Channel')]")
        fprint(self, "Clicking on the 'Manage Feed Channels' button")
        self.driver.find_element_by_xpath("//button[contains(text(),'Manage  Feed Channel')]").click()
        waitfor(self, 20, By.XPATH, "(//tbody/ancestor::table)[2]")
        fprint(self, "Slider table is visible")
        sleep(4)    # Sleep Required here
        table = self.driver.find_element_by_xpath("(//tbody/ancestor::table)[2]")
        rows = table.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
        feed_channels = []
        for row in rows:
            # Get the columns (all the data from column 1)
            col = row.find_elements(By.TAG_NAME, "td")[0]  # note: index start from 0, 1 and 2. Getting the data from 0.
            if channel_name == "Null":
                feed_channels.append(col.text)
            elif str(col.text).__contains__(channel_name):
                feed_channels.append(col.text)
                fprint(self, "Enabling Specific Channel - "+str(col.text))
        for data in feed_channels:
            waitfor(self, 20, By.XPATH, "(//span[contains(text(),'"+data+"')]//ancestor::tr)[2]")
            if api_feed_name == "Volon":
                element = self.driver.find_element_by_xpath("//*[@class='cy-right-modal-content']//span[contains(text(),'"+data+"')]")
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
            else:
                try:
                    ele = self.driver.find_element_by_xpath("//span[@data-testid='action_name' and contains(text(),'" + data + "')]")
                except:
                    ele = self.driver.find_element_by_xpath("//*[@class='cy-right-modal-content']//span[contains(text(),'"+data+"')]")
                ActionChains(self.driver).move_to_element(ele).perform()
            sleep(2)  # Sleep Required here
            # self.driver.find_element_by_xpath("(//span[contains(text(),'"+data+"')]//ancestor::tr)[2]").click()
            self.driver.find_element_by_xpath("//*[@class='cy-right-modal-content']//span[contains(text(),'"+data+"')]").click()
            self.enable_eachFeed(api_feed_name, data)
            fprint(self, "Feed Channel is Enabled - "+data)
        fprint(self, "Closing the Manage Feed Channel Slider")
        try:
            self.driver.find_element_by_xpath("(//div[contains(text(),'Manage  Feed Channel')]//ancestor::div[2])[1]//following-sibling::div//span[2]").click()
        except:
            fprint(self, "Trying with different xpath...")
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        fprint(self, "Checking the Instance is Enabled or not")
        for data in feed_channels:
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'"+data+"')]/ancestor::td/following-sibling::td[4]//div[@data-testid='is_active']")
            fprint(self, "'"+data+"' is found Enabled")
        if Build_Version.__contains__("3."):
            self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]/ancestor::div[1]/preceding::div[1]").click()
        else:
            self.driver.find_element_by_xpath("//i[@class='cyicon-chevron-left']/ancestor::div[1]").click()
        waitfor(self, 20, By.XPATH, "(//span[contains(text(), 'APIs')])[2]")
        self.driver.find_element_by_xpath("(//span[contains(text(), 'APIs')])[2]").click()
        fprint(self, "Checking " + api_feed_name + " Enabled Card is visible or not")
        search(self, api_feed_name)
        waitfor(self, 20, By.XPATH, "//img[@alt='" + api_feed_name + "']")
        fprint(self, "Enabled Card is visible")

    # Worked for both 3.0 and previous versions
    def test_01_verify_api_feeds_list(self):
        fprint(self, "TC_ID: 5501 - verify_api_feeds_list")
        failures = []
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        fprint(self, "Waiting for the 'Add API Source' Button")
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'Add API Source')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add API Source')]").click()
        fprint(self, "Clicked on the 'Add API Source' Button")
        process_console_logs(self)
        if Build_Version.__contains__("3."):
            filename = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds", "api_feeds_3dot0.csv")
        else:
            filename = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds", "api_feeds.csv")
        fprint(self, "Waiting for the Search Bar")
        with open(filename, 'r') as obj:
            data = csv.reader(obj)
            for apiFeeds in data:
                waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
                fprint(self, "Searching for API Feed - "+apiFeeds[0])
                search(self, apiFeeds[0])
                if waitfor(self, 20, By.XPATH, "//p[text()='"+apiFeeds[0]+"']", False):
                    fprint(self, "API Feed Visible - " + apiFeeds[0])
                else:
                    fprint(self, "API Feed Not Visible - " + apiFeeds[0])
                    failures.append("API Feed Not visible - "+apiFeeds[0])
        self.assert_(failures == [], str(failures))

    # Worked for both 3.0 and previous versions
    def test_02_configuring_riskIQ_api_feed(self):
        fprint(self, "TC_ID: 5502 - configuring_riskIQ_api_feed")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        self.configure_apiFeeds("RiskIQ")
        self.enable_apiFeeds("RiskIQ")
        self.poll_data("RiskIQ")

    # Worked for both 3.0 and previous versions
    def test_03_configuring_crowdStrike_api_feed(self):
        fprint(self, "TC_ID: 5503 - configuring_crowdStrike_api_feed")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        self.configure_apiFeeds("CrowdStrike")
        self.enable_apiFeeds("CrowdStrike")
        self.poll_data("CrowdStrike")

    # Worked for both 3.0 and previous versions
    def test_04_configuring_flashpoint_api_feed(self):
        fprint(self, "TC_ID: 5504 - configuring_flashpoint_api_feed")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        self.configure_apiFeeds("Flashpoint")
        self.enable_apiFeeds("Flashpoint")
        self.poll_data("Flashpoint")

    # Worked for both 3.0 and previous versions
    def test_05_configuring_recordedFuture_api_feed(self):
        fprint(self, "TC_ID: 5505 - configuring_recordedFuture_api_feed")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        self.configure_apiFeeds("Recorded Future")
        self.enable_apiFeeds("Recorded Future")
        self.poll_data("Recorded Future")

    # Worked for both 3.0 and previous versions
    def test_06_configuring_bambenek_api_feed(self):
        fprint(self, "TC_ID: 5506 - configuring_bambenek_api_feed")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        self.configure_apiFeeds("Bambenek")
        self.enable_apiFeeds("Bambenek")
        self.poll_data("Bambenek")

    # Worked for both 3.0 and previous versions
    def test_07_configuring_cofense_api_feed(self):
        fprint(self, "TC_ID: 5507 - configuring_cofense_api_feed")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        self.configure_apiFeeds("Cofense")
        self.enable_apiFeeds("Cofense")
        self.poll_data("Cofense")

    # Worked for both 3.0 and previous versions
    def test_08_configuring_intel471_api_feed(self):
        fprint(self, "TC_ID: 5508 - configuring_intel471_api_feed")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        self.configure_apiFeeds("Intel471")
        self.enable_apiFeeds("Intel471")
        self.poll_data("Intel471")

    # Worked for both 3.0 and previous versions
    def test_09_configuring_volon_api_feed(self):
        fprint(self, "TC_ID: 5509 - configuring_volon_api_feed")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        self.configure_apiFeeds("Volon")
        self.enable_apiFeeds("Volon")
        self.poll_data("Volon")

    # Worked for both 3.0 and previous versions
    def test_10_configuring_anomali_api_feed(self):
        fprint(self, "TC_ID: 5510 - configuring_anomali_api_feed")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        self.configure_apiFeeds("Anomali ThreatStream")
        self.enable_apiFeeds("Anomali ThreatStream")
        self.poll_data("Anomali ThreatStream")

    # Worked for both 3.0 and previous versions
    def test_11_configuring_Flexera_api_feed(self):
        fprint(self, "TC_ID: 5511 - configuring_Flexera_api_feed")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        self.configure_apiFeeds("Flexera")
        self.enable_apiFeeds("Flexera")
        self.poll_data("Flexera")

    def test_12_verify_riskIQ_apifeed_data(self):
        fprint(self, "TC_ID: 5512 - verify_riskIQ_apifeed_data")
        if Build_Version.__contains__("3."):
            self.apply_filter("RiskIQ")
            self.verify_polled_data("RiskIQ")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("RiskIQ")

    def test_13_verify_crowdStrike_apifeed_data(self):
        fprint(self, "TC_ID: 5513 - verify_crowdStrike_apifeed_data")
        if Build_Version.__contains__("3."):
            # sleep(2100)  # 35 minutes wait
            self.apply_filter("CrowdStrike")
            self.verify_polled_data("CrowdStrike")
        else:
            # sleep(4800)  # 80 minutes wait, 2.9.x is slower
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("CrowdStrike")

    def test_14_verify_flashpoint_apifeed_data(self):
        fprint(self, "TC_ID: 5514 - verify_flashpoint_apifeed_data")
        if Build_Version.__contains__("3."):
            self.apply_filter("Flashpoint")
            self.verify_polled_data("Flashpoint")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("Flashpoint")

    def test_15_verify_recordedFuture_apifeed_data(self):
        fprint(self, "TC_ID: 5515 - verify_recordedFuture_apifeed_data")
        if Build_Version.__contains__("3."):
            self.apply_filter("Recorded Future")
            self.verify_polled_data("Recorded Future")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("Recorded Future")

    def test_16_verify_bambenek_apifeed_data(self):
        fprint(self, "TC_ID: 5516 - verify_bambenek_apifeed_data")
        if Build_Version.__contains__("3."):
            self.apply_filter("Bambenek")
            self.verify_polled_data("Bambenek")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("Bambenek")

    def test_17_verify_cofense_apifeed_data(self):
        fprint(self, "TC_ID: 5517 - verify_cofense_apifeed_data")
        if Build_Version.__contains__("3."):
            self.apply_filter("Cofense")
            self.verify_polled_data("Cofense")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("Cofense")

    def test_18_verify_intel471_apifeed_data(self):
        fprint(self, "TC_ID: 5518 - verify_intel471_apifeed_data")
        if Build_Version.__contains__("3."):
            self.apply_filter("Intel471")
            self.verify_polled_data("Intel471")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("Intel471")

    def test_19_verify_anomali_apifeed_data(self):
        fprint(self, "TC_ID: 5519 - verify_anomali_apifeed_data")
        if Build_Version.__contains__("3."):
            self.apply_filter("Anomali ThreatStream")
            self.verify_polled_data("Anomali ThreatStream")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("Anomali ThreatStream")

    def test_20_verify_flexera_apifeed_data(self):
        fprint(self, "TC_ID: 5520 - verify_flexera_apifeed_data")
        if Build_Version.__contains__("3."):
            self.apply_filter("Flexera")
            self.verify_polled_data("Flexera")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("Flexera")

    def test_21_verify_volon_apifeed_data(self):
        fprint(self, "TC_ID: 5521 - verify_volon_apifeed_data")
        if Build_Version.__contains__("3."):
            self.apply_filter("Volon")
            self.verify_polled_data("Volon")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("Volon")

    def test_22_setting_credentials_to_original(self):
        set_value("testplan", "ui_v3_apifeeds_original_cred.txt")

    # Worked for both 3.0 and previous versions
    def test_23_configuring_QRadar_api_feed(self):
        fprint(self, "TC_ID: 5523 - configuring_QRadar_api_feed")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        process_console_logs(self)
        self.configure_apiFeeds("QRadar")
        self.enable_apiFeeds("QRadar")
        self.poll_data("QRadar")

    def test_24_verify_QRadar_apifeed_data(self):
        fprint(self, "TC_ID: 5524 - verify_QRadar_apifeed_data")
        if Build_Version.__contains__("3."):
            self.apply_filter("QRadar")
            self.verify_polled_data("QRadar")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("QRadar")

    # Worked for both 3.0 and previous versions
    def test_25_configuring_AlienVault_api_feed(self):
        fprint(self, "TC_ID: 5525 - configuring_AlienVault_api_feed")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        process_console_logs(self)
        self.configure_apiFeeds("Alien Vault")
        self.enable_apiFeeds("Alien Vault")
        self.poll_data("Alien Vault")

    def test_26_verify_AlienVault_apifeed_data(self):
        fprint(self, "TC_ID: 5526 - verify_AlienVault_apifeed_data")
        if Build_Version.__contains__("3."):
            self.apply_filter("Alien Vault")
            self.verify_polled_data("Alien Vault")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("Alien Vault")

    # Worked for both 3.0 and previous versions
    def test_27_configuring_MISP_api_feed(self):
        fprint(self, "TC_ID: 5527 - configuring_MISP_api_feed")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        process_console_logs(self)
        self.configure_apiFeeds("MISP")
        self.enable_apiFeeds("MISP")
        self.poll_data("MISP")

    def test_28_verify_MISP_apifeed_data(self):
        fprint(self, "TC_ID: 5528 - verify_MISP_apifeed_data")
        if Build_Version.__contains__("3."):
            self.apply_filter("MISP")
            self.verify_polled_data("MISP")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("MISP")

    # Worked for both 3.0 and previous versions
    def test_29_configuring_Mandiant_api_feed(self):
        fprint(self, "TC_ID: 5529 - configuring_Mandiant_api_feed")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        process_console_logs(self)
        self.configure_apiFeeds("Mandiant Threat Intelligence")
        self.enable_apiFeeds("Mandiant Threat Intelligence")
        self.poll_data("Mandiant Threat Intelligence")

    def test_30_verify_Mandiant_apifeed_data(self):
        fprint(self, "TC_ID: 5530 - verify_Mandiant_apifeed_data")
        if Build_Version.__contains__("3."):
            self.apply_filter("Mandiant Threat Intelligence")
            self.verify_polled_data("Mandiant Threat Intelligence")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("Mandiant Threat Intelligence")

    def test_31_configuring_mitre_api_feed(self):
        fprint(self, "TC_ID: 5531 - configuring_mitre_api_feed")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        process_console_logs(self)
        self.configure_apiFeeds("MITRE")
        self.enable_apiFeeds("MITRE")
        self.poll_data("MITRE")

    def test_32_verify_mitre_apifeed_data(self):
        fprint(self, "TC_ID: 5532 - verify_mitre_apifeed_data")
        if Build_Version.__contains__("3."):
            self.apply_filter("MITRE")
            self.verify_polled_data("MITRE")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("MITRE")

    def test_33_configuring_RF_api_feed_enable_hash_channel(self):
        fprint(self, "TC_ID: 5533 - test_33_configuring_RF_api_feed_enable_hash_channel")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        self.configure_apiFeeds("Recorded Future")
        self.enable_apiFeeds("Recorded Future", channel_name="Hash")
        self.poll_data("Recorded Future", channel_name="Hash")

    def test_34_configuring_RF_api_feed_enable_ip_channel(self):
        fprint(self, "TC_ID: 5534 - test_34_configuring_RF_api_feed_enable_ip_channel")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        self.configure_apiFeeds("Recorded Future")
        self.enable_apiFeeds("Recorded Future", channel_name="IP")
        self.poll_data("Recorded Future", channel_name="IP")

    def test_35_configuring_RF_api_feed_enable_domain_channel(self):
        fprint(self, "TC_ID: 5535 - test_35_configuring_RF_api_feed_enable_domain_channel")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        self.configure_apiFeeds("Recorded Future")
        self.enable_apiFeeds("Recorded Future", channel_name="Domain")
        self.poll_data("Recorded Future", channel_name="Domain")

    def test_36_configuring_RF_api_feed_enable_url_channel(self):
        fprint(self, "TC_ID: 5536 - test_36_configuring_RF_api_feed_enable_url_channel")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        self.configure_apiFeeds("Recorded Future")
        self.enable_apiFeeds("Recorded Future", channel_name="URL")
        self.poll_data("Recorded Future", channel_name="URL")

    def test_37_configuring_polyswarm_api_feed(self):
        fprint(self, "TC_ID: 5537 - configuring_polyswarm_api_feed")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to APIs Feed Source")
        self.driver.find_element_by_xpath("//span[contains(text(),'APIs')]").click()
        self.configure_apiFeeds("Polyswarm")
        self.enable_apiFeeds("Polyswarm")
        self.poll_data("Polyswarm")

    def test_38_verify_polyswarm_apifeed_data(self):
        fprint(self, "TC_ID: 5538 - verify_polyswarm_apifeed_data")
        if Build_Version.__contains__("3."):
            self.apply_filter("Polyswarm")
            self.verify_polled_data("Polyswarm")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
            self.verify_polled_data("Polyswarm")

    def test_39_verify_misp_data(self):
        """
            Testcase to validate if data sent from MISP is visible in CTIX
        """
        fprint(self, "TC_ID: 5538 - verify_polyswarm_apifeed_data")
        nav_menu_main(self, "Threat Data")
        filename = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds", "misp_to_ctix.csv")
        with open(filename, 'r') as obj:
            row = csv.reader(obj)
            for data in row:
                verify_data_in_threatdata(self, data[2], "MISP")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
