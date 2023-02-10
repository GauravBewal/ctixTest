import unittest
from lib.ui.quick_add import *
from lib.ui.nav_threat_data import get_threat_data

append_time = int(datetime.datetime.now().timestamp())
SDO_TITLE = "test_creation"+str(append_time)
all_sdo = get_object_details(csv_file="quick_add_sdo_list.csv")


class QuickAddSdo(unittest.TestCase):

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

    def test_01_quick_add_create_sdo(self):
        """
        Verify if Quick Add Create Intel is working for all SDO
        """
        fprint(self, "TC_ID: 9001 - verify_intel_creation")
        fprint(self, "----------- Verifying Quick Add Intel Creation is working ----------")
        title = SDO_TITLE+"_intel"
        add_sdo_from_csv(self, title=SDO_TITLE, intel_type='intel')
        fprint(self, 'Waiting 3 minutes for data to be created in history')
        sleep(180)
        if Build_Version.__contains__("3."):
            wait_for_history(self, title=SDO_TITLE, intel_type='intel')
            waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']")
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        else:
            sleep(60)
            quick_add_redirect(self, title=SDO_TITLE, intel_type="intel")
            validate_redirect_package_page(self, title=title)
            validate_package_objects(self)
        fprint(self, 'Waiting 2 minutes before threat data validation')
        sleep(120)
        process_console_logs(self)

    def test_02_quick_add_draft_sdo(self):
        """
        Verify if Quick Add Draft is working for all SDO
        """
        fprint(self, "TC_ID: 9002 - verify draft creation")
        fprint(self, "----------- Verifying Quick Add Draft creation is working ----------")
        add_sdo_from_csv(self, title=SDO_TITLE, intel_type='draft')
        quick_add_redirect(self, title=SDO_TITLE, intel_type="draft")
        sleep(2)
        fprint(self, "Clicking on Edit from dropdown")
        waitfor(self, 20, By.XPATH, "//li[contains(text(), 'Edit')]")
        self.driver.find_element_by_xpath("//li[contains(text(), 'Edit')]/span").click()
        waitfor(self, 20, By.XPATH, "//div[contains(text(), '"+SDO_TITLE+"_draft')]")
        fprint(self, "[Passed] Detailed page for draft has loaded successfully")
        validate_draft_objects(self)
        sleep(300)
        process_console_logs(self)

    def test_03_validate_vulnerability(self):
        """
        Verify if Vulnerability Object is added successfully
        """
        fprint(self, "TC_ID: 9003 - Test Vulnerability Object in Threat Data")
        global all_sdo
        sdo_type = "Vulnerability"
        if Build_Version.__contains__("3."):
            verify_threatdata_name(self, sdo_type, all_sdo[sdo_type]+"_intel", "Import")
        else:
            get_threat_data(self, sdo_type, all_sdo[sdo_type]+"_intel")
        process_console_logs(self)

    def test_04_validate_malware(self):
        """
        Verify if Malware Object is added successfully
        """
        fprint(self, "TC_ID: 9004 - Test Malware Object in Threat Data")
        global all_sdo
        sdo_type = "Malware"
        if Build_Version.__contains__("3."):
            verify_threatdata_name(self, sdo_type, all_sdo[sdo_type]+"_intel", "Import")
        else:
            get_threat_data(self, sdo_type, all_sdo[sdo_type]+"_intel")
        process_console_logs(self)

    def test_05_validate_campaign(self):
        """
        Verify if Campaign Object is added successfully
        """
        fprint(self, "TC_ID: 9005 - Test Campaign Object in Threat Data")
        global all_sdo
        sdo_type = "Campaign"
        if Build_Version.__contains__("3."):
            verify_threatdata_name(self, sdo_type, all_sdo[sdo_type]+"_intel", "Import")
        else:
            get_threat_data(self, sdo_type, all_sdo[sdo_type]+"_intel")
        process_console_logs(self)

    def test_06_validate_threat_actor(self):
        """
        Verify if Threat Actor Object is added successfully
        """
        fprint(self, "TC_ID: 9006 - Test Threat Actor Object in Threat Data")
        global all_sdo
        sdo_type = "Threat Actor"
        if Build_Version.__contains__("3."):
            verify_threatdata_name(self, sdo_type, all_sdo[sdo_type]+"_intel", "Import")
        else:
            get_threat_data(self, sdo_type, all_sdo[sdo_type]+"_intel")
        process_console_logs(self)

    def test_07_validate_intrusion_set(self):
        """
        Verify if Intrusion Set Object is added successfully
        """
        fprint(self, "TC_ID: 9007 - Test Intrusion Set Object in Threat Data")
        global all_sdo
        sdo_type = "Intrusion Set"
        if Build_Version.__contains__("3."):
            verify_threatdata_name(self, sdo_type, all_sdo[sdo_type]+"_intel", "Import")
        else:
            get_threat_data(self, sdo_type, all_sdo[sdo_type]+"_intel")
        process_console_logs(self)

    def test_08_validate_attack_pattern(self):
        """
        Verify if Attack Pattern Object is added successfully
        """
        fprint(self, "TC_ID: 9008 - Test Attack Pattern Object in Threat Data")
        global all_sdo
        sdo_type = "Attack Pattern"
        if Build_Version.__contains__("3."):
            verify_threatdata_name(self, sdo_type, all_sdo[sdo_type]+"_intel", "Import")
        else:
            get_threat_data(self, sdo_type, all_sdo[sdo_type]+"_intel")
        process_console_logs(self)

    def test_09_validate_coa(self):
        """
        Verify if Course of Action Object is added successfully
        """
        fprint(self, "TC_ID: 9009 - Test Course of Action Object in Threat Data")
        global all_sdo
        sdo_type = "Course of Action"
        if Build_Version.__contains__("3."):
            verify_threatdata_name(self, sdo_type, all_sdo[sdo_type]+"_intel", "Import")
        else:
            get_threat_data(self, sdo_type, all_sdo[sdo_type]+"_intel")
        process_console_logs(self)

    def test_10_validate_identity(self):
        """
        Verify if Identity Object is added successfully
        """
        fprint(self, "TC_ID: 9010 - Test Identity Object in Threat Data")
        global all_sdo
        sdo_type = "Identity"
        if Build_Version.__contains__("3."):
            verify_threatdata_name(self, sdo_type, all_sdo[sdo_type]+"_intel", "Import")
        else:
            get_threat_data(self, sdo_type, all_sdo[sdo_type]+"_intel")
        process_console_logs(self)

    def test_11_validate_tool(self):
        """
        Verify if Tool Object is added successfully
        """
        fprint(self, "TC_ID: 9011 - Test Tool Object in Threat Data")
        global all_sdo
        sdo_type = "Tool"
        if Build_Version.__contains__("3."):
            verify_threatdata_name(self, sdo_type, all_sdo[sdo_type]+"_intel", "Import")
        else:
            get_threat_data(self, sdo_type, all_sdo[sdo_type]+"_intel")
        process_console_logs(self)

    def test_12_validate_infrastructure(self):
        """
        Verify if Infrastructure Object is added successfully
        """
        fprint(self, "TC_ID: 9012 - Test Infrastructure Object in Threat Data")
        global all_sdo
        sdo_type = "Infrastructure"
        if Build_Version.__contains__("3."):
            verify_threatdata_name(self, sdo_type, all_sdo[sdo_type]+"_intel", "Import")
        else:
            get_threat_data(self, sdo_type, all_sdo[sdo_type]+"_intel")
        process_console_logs(self)

    def test_13_validate_malware_analysis(self):
        """
        Verify if Malware Analysis Object is added successfully
        """
        fprint(self, "TC_ID: 9013 - Test Malware Analysis Object in Threat Data")
        global all_sdo
        sdo_type = "Malware Analysis"
        if Build_Version.__contains__("3."):
            verify_threatdata_name(self, sdo_type, all_sdo[sdo_type]+"_intel", "Import")
        else:
            get_threat_data(self, sdo_type, all_sdo[sdo_type]+"_intel")
        process_console_logs(self)

    def test_14_quick_add_create_location(self):
        """
            Verify if intel with location object can be created
        """
        fprint(self, "TC_ID: 9014 - verify_intel_creation")
        fprint(self, "----------- Verifying Quick Add Intel Creation is working ----------")
        title = SDO_TITLE + "_location"
        sleep(1)
        fprint(self, "Clicking on New")
        waitfor(self, 20, By.XPATH, "//button[text()=' New']")
        self.driver.find_element_by_xpath("//button[text()=' New']").click()
        fprint(self, "Selecting Quick Add Intel from the dropdown mwnu")
        waitfor(self, 20, By.XPATH, "//li/*[contains(text(), 'Quick Add Intel')]")
        sleep(2)
        self.driver.find_element_by_xpath("//li/*[contains(text(), 'Quick Add Intel')]").click()
        waitfor(self, 20, By.XPATH, "//div/div[contains(text(), 'Quick Add Intel')]")
        fprint(self, "Clicking on Domain Objects panel under quick add")
        sleep(2)
        self.driver.find_element_by_xpath("//div/span[contains(text(), 'Domain Objects')]").click()
        fprint(self, "Filling in the name for package to be created")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").click()
        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(title)
        sleep(2)
        fprint(self, "Selecting Location from list of SDO")
        self.driver.find_element_by_xpath("//div/div[contains(text(), 'Location')]").click()
        sleep(1)
        fprint(self, "Clicking on checkbox for Location")
        self.driver.find_element_by_xpath("//div[contains(text(), 'Location')]//span").click()
        sleep(1)
        fprint(self, "Selecting Latitude - Longitude from the radio options")
        waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Latitude - Longitude')]")
        self.driver.find_element_by_xpath("//div[contains(text(), 'Latitude - Longitude')]").click()
        waitfor(self, 10, By.XPATH, "//input[@name='latitude']")
        fprint(self, "Setting the value of latitude")
        clear_field(self.driver.find_element_by_xpath("//input[@name='latitude']"))
        self.driver.find_element_by_xpath("//input[@name='latitude']").click()
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name='latitude']").send_keys("30")
        fprint(self, "Setting the value for longitude")
        clear_field(self.driver.find_element_by_xpath("//input[@name='longitude']"))
        self.driver.find_element_by_xpath("//input[@name='longitude']").click()
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name='longitude']").send_keys("40")
        fprint(self, 'Waiting 3 minutes for data to be created in history')
        fprint(self, "Clicking on Create Intel for data created")
        waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Create Intel')]")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Create Intel')]").click()
        if Build_Version.__contains__("3."):
            verify_success(self, "You can view the created intel as a report object in the Threat Data module")
        else:
            verify_success(self, "You will be notified once the STIX package is created")
        fprint(self, "[Passed] Request for Create Intel sent successfully")
        waitfor(self, 20, By.XPATH, "//span[contains(text(), 'Quick Add History')]")
        sleep(180)
        if Build_Version.__contains__("3."):
            wait_for_history(self, title=title, intel_type='intel')
            waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']")
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        else:
            sleep(60)
            quick_add_redirect(self, title=title, intel_type="intel")
            validate_redirect_package_page(self, title=title)
            validate_package_objects(self)
        fprint(self, 'Waiting 2 minutes before threat data validation')
        sleep(120)
        process_console_logs(self)

    def test_15_validate_location(self):
        """
        Verify if Location Object is added successfully
        """
        fprint(self, "TC_ID: 9015 - Test Malware Analysis Object in Threat Data")
        if Build_Version.__contains__("3."):
            verify_threatdata_name(self, "Location", "30.0 and 40.0", "Import")
        else:
            get_threat_data(self, "Location", "30.0 and 40.0")
        process_console_logs(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
