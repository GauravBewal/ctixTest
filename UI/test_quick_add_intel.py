import unittest
from lib.ui.nav_threat_data import *
from lib.ui.quick_add import add_metadata, sdo_title_tag, sdo_title_tlp, sdo_title_confidence, sdo_title_description, \
    meta_title, create_intel

file = os.path.join(os.environ["PYTHONPATH"], "testdata", "quick_add_intel_data.csv")
file_name = open(file)
csvreader = csv.reader(file_name)
first_row = next(csvreader)
ioc_ipv4 = first_row[1]
cc_updateTagRefset_url = "https://googly.com"
cc_updateTagRefset_domain = "customercase.com"


class QuickAddIntel(unittest.TestCase):

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

    def verify_data_in_threatdata(self, value):
        if waitfor(self, 5, By.XPATH, "(//span[contains(text(),'Threat Data')])[2]", False):
            fprint(self, "Threat Data page is visible")
        else:
            fprint(self, "Navigating to the Threat Data page")
            nav_menu_main(self, "Threat Data")
        fprint(self, "Waiting for the Search Bar")
        if Build_Version.__contains__("3."):
            waitfor(self, 20, By.XPATH, threat_data_main_search_field)
            fprint(self, "Searching for the Feed under Indicator - "+value)
            clear_field(self.driver.find_element_by_xpath(threat_data_main_search_field))
            self.driver.find_element_by_xpath(threat_data_main_search_field).click()
            # clear_field(self.driver.find_element_by_xpath(threat_data_main_search_field))
            self.driver.find_element_by_xpath(threat_data_main_search_field).send_keys(value)
            waitfor(self, 10, By.XPATH,
                    "//span[contains(text(),'Import')]/ancestor::tr/td[3]//span[contains(text(),'" + value + "')]")
        else:
            waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
            fprint(self, "Searching for the Feed under Indicator - " + value)
            clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']"))
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
            # clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Search']"))
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(value)
            self.driver.find_element_by_xpath("//i[@data-testid='filter-search-icon']").click()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), '"+value+"')]")
        fprint(self, "Feed Visible - " + value)

    def test_01_QuickAddIntel_config_Indicator_IOCs(self):
        textis = ""
        fprint(self, "TC_ID: 53001 - QuickAddIntel_config_Indicator_IOCs")
        failures = []
        fprint(self, "Waiting for the New Button...")
        self.driver.find_element_by_xpath("//button[contains(text(),'New')]").click()
        fprint(self, "Clicked on the New Button")
        waitfor(self, 5, By.XPATH, "//li/div[contains(text(),'Quick Add Intel')]")
        self.driver.find_element_by_xpath("//li/div[contains(text(),'Quick Add Intel')]").click()
        fprint(self, "Clicked on the 'Quick Add Intel' option")
        waitfor(self, 10, By.XPATH, "(//div[contains(text(),'Quick Add Intel')])[1]")
        file_name = os.path.join(os.environ["PYTHONPATH"], "testdata", "quick_add_intel_data.csv")
        with open(file_name, 'r') as obj:
            data = csv.reader(obj)
            for file_data in data:
                if str(file_data[2]) == "test_FreeText":
                    waitfor(self, 10, By.XPATH, "//div[contains(text(),'Free Text')]")
                    self.driver.find_element_by_xpath("//div[contains(text(),'Free Text')]").click()
                    waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Title*']")
                    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
                    self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(file_data[2])
                    self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Enter Data']").send_keys(file_data[1])
                    self.driver.find_element_by_xpath("(//textarea[@aria-placeholder='Enter Data']//ancestor::div[3]/following-sibling::div/div)[1]").click()
                    if waitfor(self, 20, By.XPATH, "//div[@data-testid='ips']", False):
                        self.driver.find_element_by_xpath("//div[@data-testid='ips']").click()
                    else:
                        failures.append("IPs checkbox is not visible OR Remains in the Parsing state")
                elif str(file_data[2]) == "test_URLTab":
                    waitfor(self, 10, By.XPATH, "(//div/div[contains(text(),'URL')])[2]")
                    self.driver.find_element_by_xpath("(//div/div[contains(text(),'URL')])[2]").click()
                    waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Title*']")
                    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
                    self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(file_data[2])
                    self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter URL*']").send_keys(file_data[1])
                    waitfor(self, 5, By.XPATH, "//button[contains(text(),'Fetch')]")
                    self.driver.find_element_by_xpath("//button[contains(text(),'Fetch')]").click()
                    waitfor(self, 20, By.XPATH, "//span[contains(text(),'Domain(s)')]")
                    self.driver.find_element_by_xpath("//span[contains(text(),'Domain(s)')]").click()
                else:
                    waitfor(self, 10, By.XPATH, qai_ioc_type_search)
                    if Build_Version.__contains__("3."):
                        clear_field(self.driver.find_element_by_xpath(qai_ioc_type_search))
                        fprint(self, "Searching - "+file_data[0])
                        self.driver.find_element_by_xpath(qai_ioc_type_search).click()
                        self.driver.find_element_by_xpath(qai_ioc_type_search).send_keys(file_data[0])
                    else:
                        sleep(2)
                        self.driver.find_element_by_xpath("//div[@class='cy-filters__section px-1 d-flex']").click()
                        # self.driver.find_element_by_xpath("//ul//input[@placeholder='Search']").click()
                        clear_field(self.driver.find_element_by_xpath("//input[@id='main-input'][@placeholder='Search']"))
                        fprint(self, "Searching - " + file_data[0])
                        self.driver.find_element_by_xpath\
                            ("//input[@id='main-input'][@placeholder='Search']").send_keys(file_data[0])
                        self.driver.find_element_by_xpath\
                            ("//input[@type='checkbox']/ancestor::div[contains(text(), '"+file_data[0]+"')]").click()
                        sleep(2)
                    waitfor(self, 5, By.XPATH, "//div[contains(text(),'"+file_data[0]+"')]/ancestor::div[1]")
                    # self.driver.find_element_by_xpath("//div[contains(text(),'"+file_data[0]+"')]/ancestor::div[1]").click()
                    self.driver.find_element_by_xpath("//div[contains(text(),'"+file_data[0]+"')]/div[1]/div").click()
                    clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
                    self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(file_data[2])
                    self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").send_keys(file_data[1])
                self.driver.find_element_by_xpath("//button[contains(text(),'Create Intel')]").click()
                # verify_success(self, "You will be notified once the STIX package is created")
                if waitfor(self, 15, By.XPATH, "//i[@class = 'cyicon-check-o-active']", False):
                    sleep(1)
                    textis = self.driver.find_element_by_xpath("//div[contains(@class, 'cy-message__text')]").text
                    if textis == "You can view the created intel as a report object in the Threat Data module." and Build_Version.__contains__("3."):
                        fprint(self, "[Passed] Expected message is found, " + str(textis))
                        self.driver.find_element_by_xpath(
                            "//div[@class='el-notification__closeBtn el-icon-close']").click()
                        repeat = 1
                        while repeat <= 6:
                            if waitfor(self, 20, By.XPATH, "//span[contains(text(),'" + file_data[
                                2] + "')]/ancestor::td/following-sibling::td[3]//span[contains(text(),'Created')]",
                                       False):
                                fprint(self, "Created Status of intel is visible - " + file_data[2])
                                self.driver.find_element_by_xpath(
                                    "//span[contains(text(),'Quick Add History')]").click()
                                break
                            else:
                                self.driver.find_element_by_xpath("//button[contains(text(),'Refresh')]").click()
                                fprint(self, "Created Status of intel is not visible, Clicked on the Refresh Button")
                                if repeat == 6:
                                    failures.append("Created Status of intel is not visible - " + file_data[2])
                                    self.driver.find_element_by_xpath(
                                        "//span[contains(text(),'Quick Add History')]").click()
                                repeat = repeat + 1
                    elif textis == "You will be notified once the STIX package is created!":
                        fprint(self, "[Passed] Expected message is found, " + str(textis))
                        self.driver.find_element_by_xpath("//div[@class='el-notification__closeBtn el-icon-close']").click()
                        repeat = 1
                        while repeat <= 6:
                            if waitfor(self, 20, By.XPATH, "//span[contains(text(),'" + file_data[
                                2] + "')]/ancestor::td/following-sibling::td[3]//span[contains(text(),'Created')]",
                                       False):
                                fprint(self, "Created Status of intel is visible - " + file_data[2])
                                self.driver.find_element_by_xpath(
                                    "//span[contains(text(),'Quick Add History')]").click()
                                break
                            else:
                                self.driver.find_element_by_xpath("//button[contains(text(),'Refresh')]").click()
                                fprint(self, "Created Status of intel is not visible, Clicked on the Refresh Button")
                                if repeat == 6:
                                    failures.append("Created Status of intel is not visible - " + file_data[2])
                                    self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
                                repeat = repeat + 1
                    else:
                        fprint(self,
                               "[Failed] Alert found with different msg. Found: " + str(
                                   textis) + "Expected:" + "You will be notified once the STIX package is created!")
                        self.driver.find_element_by_xpath("//div[contains(text(),'"+file_data[0]+"')]/div[1]/div").click()
                        failures.append("Case Status: [Failed] Alert found but expected message is not found -"+textis)
                else:
                    fprint(self, "Getting some error in adding - "+file_data[0])
                    self.driver.find_element_by_xpath("//div[contains(text(),'"+file_data[0]+"')]/div[1]/div").click()
                    failures.append("Expected message is not found - "+textis)
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        self.assert_(failures == [], str(failures))
        sleep(600)  # waiting for 10 minutes before verification

    def test_02_verify_IPv4_quick_intel(self):
        fprint(self, "TC_ID: 53002 - verify_IPv4_quick_intel")
        self.verify_data_in_threatdata(ioc_ipv4)

    def test_03_verify_IPv6_quick_intel(self):
        fprint(self, "TC_ID: 53003 - verify_IPv6_quick_intel")
        self.verify_data_in_threatdata("2002:D4B0:6CBB:0:0:0:0:0".lower())

    def test_04_verify_Domain_quick_intel(self):
        fprint(self, "TC_ID: 53004 - verify_Domain_quick_intel")
        self.verify_data_in_threatdata("caentivage.com")

    def test_05_verify_URL_ioc_quick_intel(self):
        fprint(self, "TC_ID: 53004 - verify_Domain_quick_intel")
        self.verify_data_in_threatdata("http://178.175.16.108:34809/bin.sh")

    def test_06_verify_Email_quick_intel(self):
        fprint(self, "TC_ID: 53005 - verify_Email_quick_intel")
        self.verify_data_in_threatdata("noreply-team.googelsupport@verify-mail.pro")

    def test_07_verify_MD5_quick_intel(self):
        fprint(self, "TC_ID: 53006 - verify_MD5_quick_intel")
        self.verify_data_in_threatdata("1e2e2f39ab6988a9f3852f1ec02ab05a")

    def test_08_verify_SHA1_quick_intel(self):
        fprint(self, "TC_ID: 53007 - verify_SHA1_quick_intel")
        self.verify_data_in_threatdata("ed61f731ae7f3d238a28e90ff0b4c7d52cea508e")

    def test_09_verify_SHA224_quick_intel(self):
        fprint(self, "TC_ID: 53008 - verify_SHA224_quick_intel")
        self.verify_data_in_threatdata("6268f69784275cc9d3b2416a2c18b3cbdee3f6a0683ff817b4187821")

    def test_10_verify_SHA256_quick_intel(self):
        fprint(self, "TC_ID: 53009 - verify_SHA256_quick_intel")
        self.verify_data_in_threatdata("107d9fce05ff8296d0417a5a830d180cd46aa120ced8360df3ebfd15cb550636")

    def test_11_verify_SHA384_quick_intel(self):
        fprint(self, "TC_ID: 53010 - verify_SHA384_quick_intel")
        self.verify_data_in_threatdata("6d26f82c627c896665720938288888d1fdd3e763ab75cb8683a7e678815d0e43a38bc5960b6294af9f8f35f94a3e65b5")

    def test_12_verify_SHA512_quick_intel(self):
        fprint(self, "TC_ID: 53011 - verify_SHA512_quick_intel")
        self.verify_data_in_threatdata("77f99319def56a42462c39bea718cac8ecb95d99b07f884992ac2795528775796b952bdc1763d90b2c0310eb87e7c7fde514ce19c6fca1d09095a9a153137b05")

    def test_13_verify_SSDEEP_quick_intel(self):
        fprint(self, "TC_ID: 53012 - verify_SSDEEP_quick_intel")
        self.verify_data_in_threatdata("768:FXPkQ2Csnwhxvfhko88yb6cvXbhb7vJawOuArU1o/xnmGP:YLqvZko9ybpvrtvJa/uArU+5nNP".lower())

    def test_14_verify_FreeText_quick_intel(self):
        fprint(self, "TC_ID: 53013 - verify_FreeText_quick_intel")
        self.verify_data_in_threatdata("185.117.74.28")

    def test_15_verify_URL_quick_intel(self):
        fprint(self, "TC_ID: 53014 - verify_URL_quick_intel")
        url_data = ["stevenson-brown.com", "lynn.net", "daniels-smith.info", "pace-davis.net", "moore.com", "hunt.biz",
                "clayton-aguilar.org", "charles.com", "brown.org", "ferguson-raymond.org", "morales-foster.com",
                "herrera-freeman.com", "diaz.info", "carter-wiley.net", "washington.com", "bartlett.biz", "compton.com",
                "reese.com", "reed-cooper.com", "jordan.com"]
        for data in url_data:
            self.verify_data_in_threatdata(data)

    def test_16_create_metadata_intel_description(self):
        """
        Verify if intel can be created along with metadata
        """
        fprint(self, "TC_ID: 53016 - Test if metadata added for the object is applied")
        fprint(self, "Clicking on New")
        waitfor(self, 20, By.XPATH, "//button[text()=' New']")
        self.driver.find_element_by_xpath("//button[text()=' New']").click()
        waitfor(self, 5, By.XPATH, "//li/div[contains(text(),'Quick Add Intel')]")
        self.driver.find_element_by_xpath("//li/div[contains(text(),'Quick Add Intel')]").click()
        fprint(self, "Clicked on the 'Quick Add Intel' option")
        waitfor(self, 10, By.XPATH, "(//div[contains(text(),'Quick Add Intel')])[1]")
        fprint(self, "Filling in the name for package to be created")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").click()
        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(meta_title+"_description")
        fprint(self, "Setting the title for Indictaor object to " + sdo_title_description)
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").click()
        sleep(1)
        self.driver.find_element_by_xpath \
            ("//textarea[@aria-placeholder='Value(s)']").send_keys(sdo_title_description)
        add_metadata(self, description="meta description")
        fprint(self, "Clicking on Create Intel for data created")
        waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Create Intel')]")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Create Intel')]").click()
        if Build_Version.__contains__("3."):
            verify_success(self, "You can view the created intel as a report object in the Threat Data module")
        else:
            verify_success(self, "You will be notified once the STIX package is created")
        fprint(self, "[Passed] Request for Create Intel sent successfully")
        fprint(self, "Waiting 2 minutes for intel to get generated")
        sleep(120)
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        process_console_logs(self)

    def test_17_create_metadata_intel_tag(self):
        """
        Verify if intel can be created along with metadata
        """
        fprint(self, "TC_ID: 53024 - Test if metadata added for the object is applied")
        fprint(self, "Clicking on New")
        waitfor(self, 20, By.XPATH, "//button[text()=' New']")
        self.driver.find_element_by_xpath("//button[text()=' New']").click()
        fprint(self, "Selecting Quick Add Intel from the dropdown menu")
        waitfor(self, 5, By.XPATH, "//li/div[contains(text(),'Quick Add Intel')]")
        self.driver.find_element_by_xpath("//li/div[contains(text(),'Quick Add Intel')]").click()
        fprint(self, "Clicked on the 'Quick Add Intel' option")
        waitfor(self, 10, By.XPATH, "(//div[contains(text(),'Quick Add Intel')])[1]")
        fprint(self, "Filling in the name for package to be created")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").click()
        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(meta_title+"_tag")
        fprint(self, "Setting the title for Indictaor object to " + sdo_title_tag)
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").click()
        sleep(1)
        self.driver.find_element_by_xpath \
            ("//textarea[@aria-placeholder='Value(s)']").send_keys(sdo_title_tag)
        add_metadata(self, tag='automatetag')
        fprint(self, "Clicking on Create Intel for data created")
        waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Create Intel')]")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Create Intel')]").click()
        if Build_Version.__contains__("3."):
            verify_success(self, "You can view the created intel as a report object in the Threat Data module")
        else:
            verify_success(self, "You will be notified once the STIX package is created")
        fprint(self, "[Passed] Request for Create Intel sent successfully")
        fprint(self, "Waiting 2 minutes for intel to get generated")
        sleep(120)
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        process_console_logs(self)

    def test_18_create_metadata_intel_confidence(self):
        """
        Verify if intel can be created along with metadata
        """
        fprint(self, "TC_ID: 53025 - Test if metadata added for the object is applied")
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
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(meta_title+"_confidence")
        fprint(self, "Setting the title for Indictaor object to " + sdo_title_confidence)
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").click()
        sleep(1)
        self.driver.find_element_by_xpath \
            ("//textarea[@aria-placeholder='Value(s)']").send_keys(sdo_title_confidence)
        add_metadata(self, confidence=80)
        fprint(self, "Clicking on Create Intel for data created")
        waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Create Intel')]")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Create Intel')]").click()
        if Build_Version.__contains__("3."):
            verify_success(self, "You can view the created intel as a report object in the Threat Data module")
        else:
            verify_success(self, "You will be notified once the STIX package is created")
        fprint(self, "[Passed] Request for Create Intel sent successfully")
        fprint(self, "Waiting 2 minutes for intel to get generated")
        sleep(120)
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        process_console_logs(self)

    def test_19_create_metadata_intel_tlp(self):
        """
        Verify if intel can be created along with metadata
        """
        fprint(self, "TC_ID: 53026 - Test if metadata added for the object is applied")
        fprint(self, "Clicking on New")
        waitfor(self, 20, By.XPATH, "//button[text()=' New']")
        self.driver.find_element_by_xpath("//button[text()=' New']").click()
        waitfor(self, 5, By.XPATH, "//li/div[contains(text(),'Quick Add Intel')]")
        self.driver.find_element_by_xpath("//li/div[contains(text(),'Quick Add Intel')]").click()
        fprint(self, "Clicked on the 'Quick Add Intel' option")
        waitfor(self, 10, By.XPATH, "(//div[contains(text(),'Quick Add Intel')])[1]")
        fprint(self, "Filling in the name for package to be created")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").click()
        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(meta_title+"_tlp")
        fprint(self, "Setting the title for Indictaor object to " + sdo_title_tlp)
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").click()
        sleep(1)
        self.driver.find_element_by_xpath \
            ("//textarea[@aria-placeholder='Value(s)']").send_keys(sdo_title_tlp)
        add_metadata(self, tlp="Red")
        fprint(self, "Clicking on Create Intel for data created")
        waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Create Intel')]")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Create Intel')]").click()
        if Build_Version.__contains__("3."):
            verify_success(self, "You can view the created intel as a report object in the Threat Data module")
        else:
            verify_success(self, "You will be notified once the STIX package is created")
        fprint(self, "[Passed] Request for Create Intel sent successfully")
        fprint(self, "Waiting 2 minutes for intel to get generated")
        sleep(120)
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        process_console_logs(self)

    def test_20_verify_metadata_intel_tag(self):
        """
        Verify for metadata added to intel added via quick add
        """
        fprint(self, "TC_ID: 53017 - verify_metadata_intel_tag")
        nav_menu_main(self, 'Threat Data')
        if Build_Version.__contains__("3."):
            self.verify_data_in_threatdata(sdo_title_tag)
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                              "/ancestor::tr/td[3]//span[contains(text(),'"+sdo_title_tag+"')]")
            _ele = self.driver.find_elements_by_xpath("//span[contains(text(), '"+sdo_title_tag+"')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
        else:
            waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
            clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']"))
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(sdo_title_tag)
            self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), '"+sdo_title_tag+"')]/ancestor::tr")
            ele = self.driver.find_element_by_xpath("//span[contains(text(), '"+sdo_title_tag+"')]")
            self.driver.execute_script("arguments[0].click();", ele)
            waitfor(self, 20, By.XPATH, "//div[@data-testid='name2'][contains(text(), '"+sdo_title_tag+"')]")
        sleep(2)
        validate_tag(self, 'automatetag')

    def test_21_verify_metadata_intel_description(self):
        """
        Verify for metadata added to intel added via quick add
        """
        fprint(self, "TC_ID: 53018 - verify_metadata_intel_description")
        nav_menu_main(self, 'Threat Data')
        if Build_Version.__contains__("3."):
            self.verify_data_in_threatdata(sdo_title_description)
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                        "/ancestor::tr/td[3]//span[contains(text(),'" + sdo_title_description + "')]")
            _ele = \
            self.driver.find_elements_by_xpath("//span[contains(text(), '" + sdo_title_description + "')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
            sleep(2)
            validate_description(self, 'meta description')
        else:
            fprint(self, "Clicking on New")
            waitfor(self, 20, By.XPATH, "//button[text()=' New']")
            self.driver.find_element_by_xpath("//button[text()=' New']").click()
            fprint(self, "Selecting Quick Add Intel from the dropdown mwnu")
            waitfor(self, 5, By.XPATH, "//li/div[contains(text(),'Quick Add Intel')]")
            self.driver.find_element_by_xpath("//li/div[contains(text(),'Quick Add Intel')]").click()
            fprint(self, "Clicked on the 'Quick Add Intel' option")
            waitfor(self, 20, By.XPATH, "//button[contains(text(),'Quick Add History')]")
            self.driver.find_element_by_xpath("//button[contains(text(),'Quick Add History')]").click()
            waitfor(self, 20, By.XPATH, "(//input[@placeholder='Search or filter results'])[2]")
            sleep(2)
            self.driver.find_element_by_xpath("(//input[@placeholder='Search or filter results'])[2]").click()
            self.driver.find_element_by_xpath("(//input[@placeholder='Search or filter results'])[2]").send_keys(meta_title+"_description")
            self.driver.find_element_by_xpath("(//div[i[@data-testid='filter-search-icon']])[2]").click()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), '"+meta_title+"_description"+"')]/ancestor::td/following-sibling::td[5]")
            self.driver.find_element_by_xpath("//span[contains(text(), '"+meta_title+"_description"+"')]/ancestor::td/following-sibling::td[5]").click()
            waitfor(self, 10, By.XPATH, "//li[contains(text(),'View')]")
            self.driver.find_element_by_xpath("//li[contains(text(),'View')]").click()
            if waitfor(self, 20, By.XPATH, "//div[contains(text(),'meta description')]", False):
                fprint(self, "[Passed] Description for the SDO matches the one added")
            else:
                fprint(self, "[Failed] Description of the SDO does not match")

    def test_22_verify_metadata_intel_confidence(self):
        """
        Verify for metadata added to intel added via quick add
        """
        fprint(self, "TC_ID: 53019 - verify_metadata_intel_confidence")
        nav_menu_main(self, 'Threat Data')
        if Build_Version.__contains__("3."):
            self.verify_data_in_threatdata(sdo_title_confidence)
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                        "/ancestor::tr/td[3]//span[contains(text(),'" + sdo_title_confidence + "')]")
            _ele = \
            self.driver.find_elements_by_xpath("//span[contains(text(), '" + sdo_title_confidence + "')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
            waitfor(self, 20, By.XPATH, "//p[contains(text(), 'Confidence Score')]/button")
            self.driver.find_element_by_xpath("//p[contains(text(), 'Confidence Score')]/button").click()
        else:
            waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
            clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']"))
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(
                sdo_title_confidence)
            self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), '" + sdo_title_confidence + "')]/ancestor::tr")
            ele = self.driver.find_element_by_xpath("//span[contains(text(), '"+sdo_title_confidence+"')]")
            self.driver.execute_script("arguments[0].click();", ele)
            waitfor(self, 20, By.XPATH, "//div[@data-testid='name2'][contains(text(), '" + sdo_title_confidence + "')]")
        sleep(2)
        validate_confidence(self, '80')

    def test_23_verify_metadata_intel_tlp(self):
        """
        Verify for metadata added to intel added via quick add
        """
        fprint(self, "TC_ID: 53020 - verify_metadata_intel_tlp")
        nav_menu_main(self, 'Threat Data')
        if Build_Version.__contains__("3."):
            self.verify_data_in_threatdata(sdo_title_tlp)
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Import')]"
                                        "/ancestor::tr/td[3]//span[contains(text(),'" + sdo_title_tlp + "')]")
            _ele = \
            self.driver.find_elements_by_xpath("//span[contains(text(), '" + sdo_title_tlp + "')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Basic Details')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Basic Details')]").click()
        else:
            waitfor(self, 20, By.XPATH, "//input[@placeholder='Search or filter results']")
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
            clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']"))
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(
                sdo_title_tlp)
            self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
            waitfor(self, 20, By.XPATH, "//span[contains(text(), '" + sdo_title_tlp + "')]/ancestor::tr")
            ele = self.driver.find_element_by_xpath("//span[contains(text(), '" + sdo_title_tlp + "')]")
            self.driver.execute_script("arguments[0].click();", ele)
            waitfor(self, 20, By.XPATH, "//div[@data-testid='name2'][contains(text(), '" + sdo_title_tlp + "')]")
        sleep(2)
        validate_tlp(self, 'Red')

    def test_24_cc_quickAdd_url_and_domain(self):
        fprint(self, "TC_ID: 53021 - test_24_cc_quickAdd_url_and_domain")
        create_intel(self, type="URL", title="cc_updateTagRefset_url", value=cc_updateTagRefset_url)
        create_intel(self, type="Domain", title="cc_updateTagRefset_domain", value=cc_updateTagRefset_domain)

    def test_25_cc_verify_quickAdd_url_and_domain_in_ctix(self):
        fprint(self, "TC_ID: 53022 - test_25_cc_verify_quickAdd_url_and_domain_in_ctix")
        self.verify_data_in_threatdata(value=cc_updateTagRefset_url)
        click_on_intel(self, source="Import", value=cc_updateTagRefset_url)
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Action Taken')]/parent::a")
        self.driver.find_element_by_xpath("//div[contains(text(),'Action Taken')]/parent::a").click()
        waitfor(self, 10, By.XPATH, "//div[@data-testid='ctix_actions']//span[contains(text(),'Update Tag (Add)')]")
        waitfor(self, 10, By.XPATH, "//div[@data-testid='third_party_actions']//span[contains(text(),'Update Reference Set')]")
        fprint(self, "Verified both the actions are visible - Update Tag and Update Reference Tag")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
