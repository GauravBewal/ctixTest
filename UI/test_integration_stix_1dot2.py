import unittest
from lib.ui.fs_stix import *
from lib.ui.nav_tableview import *
from lib.ui.nav_threat_data import *


class IntegrationStix1dot2(unittest.TestCase):

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

    def adding_STIXSource(self, sourcename, url, username, password):
        fprint(self, "Test Data - Source Name: " + sourcename)
        fprint(self, "Test Data - Source URL: " + url)
        fprint(self, "Test Data - Source Username: " + username)
        fprint(self, "Test Data - Source Password: " + password)
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected to the Integration Management page successfully")
        fprint(self, "Checking for the 'Add Stix Source' button")
        if Build_Version.__contains__("3."):
            waitfor(self, 2, By.XPATH, "(//button[contains(text(),'STIX Source')])[1]")
            fprint(self, "Button found, now clicking on it")
            self.driver.find_element_by_xpath("(//button[contains(text(),'STIX Source')])[1]").click()
        else:
            waitfor(self, 2, By.XPATH, "//button[contains(text(),'Add STIX Source')]")
            fprint(self, "Button found, now clicking on it")
            self.driver.find_element_by_xpath("//button[contains(text(),'Add STIX Source')]").click()
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Source Name *']")
        fprint(self, "Adding Configuration Details : ")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Source Name *']").send_keys(sourcename)
        fprint(self, "Source Name - "+sourcename)
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description *']").send_keys("test_STIX_Description")
        fprint(self, "Source Description - test_STIX_Description")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Discovery Service URL *']").send_keys(url)
        fprint(self, "Discovery Service URL - "+url)
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Confidence *']").send_keys("70")
        fprint(self, "Confidence Score - 70")
        self.driver.find_element_by_xpath("(//div[@name='taxii_option'])[1]").click()
        waitfor(self, 5, By.XPATH, "//div[text()='STIX 1.x']")
        self.driver.find_element_by_xpath("//div[text()='STIX 1.x']").click()
        fprint(self, "STIX version - STIX 1.x")
        self.driver.find_element_by_xpath("(//div[@name='category'])[1]").click()
        waitfor(self, 20, By.XPATH, "//div[text()='Community Feeds']")
        sleep(2)
        self.driver.find_element_by_xpath("//div[text()='Community Feeds']").click()
        fprint(self, "Category - Community Feeds")
        self.driver.find_element_by_xpath("(//div[@name='authentication_type'])[1]").click()
        waitfor(self, 5, By.XPATH, "//div[text()='Basic']")
        self.driver.find_element_by_xpath("//div[text()='Basic']").click()
        fprint(self, "Authentication Tyoe - Basic")
        waitfor(self, 5, By.XPATH, "//input[@name='username']")
        self.driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
        fprint(self, "Entered Username")
        self.driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
        fprint(self, "Entered Password")
        if Build_Version.__contains__("3."):
            self.driver.find_element_by_xpath("//button[@data-testid='save-custom-sources']").click()
        else:
            self.driver.find_element_by_xpath("//button[@data-testid='save-sources']").click()
        fprint(self, "Clicked on the Save Source Button")
        verify_success(self, "Source created successfully")
        # process_console_logs(self)

        # ToDo: Handle the case when source is already exist. Getting an error - "Host name already exists"

    def test_01_adding_STIXSource_1dot2_manualPoll(self):
        fprint(self, "TC_ID: 55001 - Adding_STIXSource_1dot2_verify_manual_polling")
        self.adding_STIXSource('1dot2_m',
                               'https://orion.cywareqa.com/taxii/1/c6e50796-a185-4344-830f-5c83d32dac45/taxii/',
                               'c6e50796-a185-4344-830f-5c83d32dac45', '22cbfe35-8d96-42a8-903e-38cf8c993c31')
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        fprint(self, "Searching the STIX Source - 1dot2_m")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("1dot2_m")
        self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
        waitfor(self, 5, By.XPATH, "//p[contains(text(),'1dot2_m')]")
        fprint(self, "Getting the added STIX Source - 1dot2_m")
        # Clicked on the action menu
        self.driver.find_element_by_xpath("//p[contains(text(),'1dot2_m')]//ancestor::div[1]/div[2]").click()
        fprint(self, 'Clicked on the action menu')
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'View Collections')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'View Collections')]").click()
        fprint(self, "Clicked on the View Collections")
        waitfor(self, 5, By.XPATH, "//button[@data-testid='action']")
        fprint(self, "Inside of - Collections of 1dot2_m")
        self.driver.find_element_by_xpath("//button[@data-testid='action']").click()
        fprint(self, "Clicked on the Action menu")
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Edit Poll Configuration')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Edit Poll Configuration')]").click()
        fprint(self, "Clicked on the Edit Poll Configuration option")
        choose_previous_date(self)
        waitfor(self, 5, By.XPATH, "//button[text()='Update']")
        self.driver.find_element_by_xpath("//button[text()='Update']").click()
        fprint(self, "Clicked on the Update Button")
        verify_success(self, "updated successfully")
        sleep(2)
        click_on_actions_item(self, "collection_0", "Poll Now")
        fprint(self, "Clicked on the Poll Now option")
        verify_success(self, "updated successfully")
        process_console_logs(self)
        fprint(self, "Waiting for the 15 minutes...")
        sleep(900)

    def test_02_adding_STIXSource_1dot2_automaticPoll(self):
        fprint(self, "TC_ID: 55002 - adding_STIXSource_1dot2_verify_automatic_polling")
        self.adding_STIXSource('1dot2_a',
                               'https://orion.cywareqa.com/taxii/1/a8bcd3d5-a756-4b75-a5a1-6f134e2e639b/taxii/',
                               'a8bcd3d5-a756-4b75-a5a1-6f134e2e639b', 'e42860f4-df2a-4f48-95c6-b806c038d186')
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        fprint(self, "Searching the STIX Source - 1dot2_a")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("1dot2_a")
        self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
        waitfor(self, 5, By.XPATH, "//p[contains(text(),'1dot2_a')]")
        fprint(self, "Getting the added STIX Source - 1dot2_a")
        # Clicked on the action menu
        self.driver.find_element_by_xpath("//p[contains(text(),'1dot2_a')]//ancestor::div[1]/div[2]").click()
        fprint(self, 'Clicked on the action menu')
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'View Collections')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'View Collections')]").click()
        fprint(self, "Clicked on the View Collections")
        waitfor(self, 5, By.XPATH, "//button[@data-testid='action']")
        fprint(self, "Inside of - Collections of 1dot2_a")
        self.driver.find_element_by_xpath("//button[@data-testid='action']").click()
        fprint(self, "Clicked on the Action menu")
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Edit Poll Configuration')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Edit Poll Configuration')]").click()
        fprint(self, "Clicked on the Edit Poll Configuration option")
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Automatic')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Automatic')]").click()
        choose_previous_date(self)
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Frequency (seconds)']")
        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Frequency (seconds)']"))
        fprint(self, "Setting Frequency of 10 seconds")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Frequency (seconds)']").send_keys("10")
        self.driver.find_element_by_xpath("//button[text()='Update']").click()
        fprint(self, "Clicked on the Update Button")
        verify_success(self, "updated successfully")
        process_console_logs(self)
        fprint(self, "Waiting for the 15 minutes...")
        sleep(900)

    # Only for CTIX Version 3.0
    def test_03_adding_STIXSource_1dot2_manualPoll(self):
        fprint(self, "TC_ID: 55003 - adding_STIXSource_1dot2_manualPoll")
        self.adding_STIXSource('1dot2_m',
                               'https://orion.cywareqa.com/taxii/1/c6e50796-a185-4344-830f-5c83d32dac45/taxii/',
                               'c6e50796-a185-4344-830f-5c83d32dac45', '22cbfe35-8d96-42a8-903e-38cf8c993c31')
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        fprint(self, "Searching the STIX Source - 1dot2_m")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("1dot2_m")
        self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
        waitfor(self, 5, By.XPATH, "//p[contains(text(),'1dot2_m')]")
        fprint(self, "Getting the added STIX Source - 1dot2_m")
        self.driver.find_element_by_xpath("//p[contains(text(),'1dot2_m')]").click()
        click_on_actions_item(self, "collection_0", "Edit Poll Configuration")
        fprint(self, "Clicked on the Edit Poll Configuration option")
        choose_previous_date(self)
        waitfor(self, 5, By.XPATH, "//button[text()='Update']")
        self.driver.find_element_by_xpath("//button[text()='Update']").click()
        fprint(self, "Clicked on the Update Button")
        verify_success(self, "updated successfully")
        sleep(2)
        click_on_actions_item(self, "collection_0", "Poll Now")
        fprint(self, "Clicked on the Poll Now option")
        verify_success(self, "updated successfully")
        process_console_logs(self)
        # fprint(self, "Waiting for the 15 minutes to data get polled...")
        # sleep(900)

    # Worked for both 3.0 and previous versions
    def test_04_verify_1dot2_manual_polledData_indicator(self):
        fprint(self, "TC_ID: 55004 - verify_1dot2_manual_polledData_indicator")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
          # beforeVerifying_PolledData(self, "Indicator")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_m", "stix1dot2/threatdata_manual_indicator.csv")
        fprint(self, "[Passed] Found all the Indicator data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_05_verify_1dot2_manual_polledData_threatActor(self):
        fprint(self, "TC_ID: 55005 - verify_1dot2_manual_polledData_threatActor")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Threat Actor")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_m", "stix1dot2/threatdata_manual_threat_actor.csv")
        fprint(self, "[Passed] Found all the Threat Actor data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_06_verify_1dot2_manual_polledData_vulnerability(self):
        fprint(self, "TC_ID: 55006 - verify_1dot2_manual_polledData_vulnerability")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Vulnerability")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_m", "stix1dot2/threatdata_manual_vulnerability.csv")
        fprint(self, "[Passed] Found all the Vulnerability data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_07_verify_1dot2_manual_polledData_report(self):
        fprint(self, "TC_ID: 55007 - verify_1dot2_manual_polledData_report")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Report")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_m", "stix1dot2/threatdata_manual_report.csv")
        fprint(self, "[Passed] Found all the Report data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_12_verify_1dot2_manual_polledData_courseOfAction(self):
        fprint(self, "TC_ID: 55012 - verify_1dot2_manual_polledData_courseOfAction")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Course of Action")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_m", "stix1dot2/threatdata_manual_course_of_action.csv")
        fprint(self, "[Passed] Found all the Course Of Action data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_13_verify_1dot2_manual_polledData_campaign(self):
        fprint(self, "TC_ID: 55013 - verify_1dot2_manual_polledData_campaign")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Campaign")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_m", "stix1dot2/threatdata_manual_campaign.csv")
        fprint(self, "[Passed] Found all the Campaign data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_13_verify_1dot2_manual_polledData_incident(self):
        fprint(self, "TC_ID: 55013 - verify_1dot2_manual_polledData_incident")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Incident")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_m", "stix1dot2/threatdata_manual_incident.csv")
        fprint(self, "[Passed] Found all the Incident data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_13_verify_1dot2_manual_polledData_ttp(self):
        fprint(self, "TC_ID: 55013 - verify_1dot2_manual_polledData_ttp")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "TTP")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_m", "stix1dot2/threatdata_manual_ttp.csv")
        fprint(self, "[Passed] Found all the TTP data, in Manual Polling")

    # Only for CTIX Version 3.0
    def test_20_v3_adding_STIXSource_1dot2_automaticPoll(self):
        fprint(self, "TC_ID: 55020 - adding_STIXSource_1dot2_automaticPoll")
        self.adding_STIXSource('1dot2_a',
                               'https://orion.cywareqa.com/taxii/1/a8bcd3d5-a756-4b75-a5a1-6f134e2e639b/taxii/',
                               'a8bcd3d5-a756-4b75-a5a1-6f134e2e639b', 'e42860f4-df2a-4f48-95c6-b806c038d186')
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        fprint(self, "Searching the STIX Source - 1dot2_a")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("1dot2_a")
        self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
        waitfor(self, 5, By.XPATH, "//p[contains(text(),'1dot2_a')]")
        fprint(self, "Getting the added STIX Source - 1dot2_a")
        self.driver.find_element_by_xpath("//p[contains(text(),'1dot2_a')]").click()
        click_on_actions_item(self, "collection_0", "Edit Poll Configuration")
        fprint(self, "Clicked on the Edit Poll Configuration option")
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Automatic')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Automatic')]").click()
        choose_previous_date(self)
        # waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Frequency (seconds)']")
        # clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Frequency (seconds)']"))
        # fprint(self, "Setting Frequency of 10 seconds")
        # self.driver.find_element_by_xpath("//input[@aria-placeholder='Frequency (seconds)']").send_keys("10")
        self.driver.find_element_by_xpath("//button[text()='Update']").click()
        fprint(self, "Clicked on the Update Button")
        verify_success(self, "updated successfully")
        process_console_logs(self)
        # fprint(self, "Waiting for the 15 minutes to data get polled...")
        # sleep(900)

    # Worked for both 3.0 and previous versions
    def test_22_verify_1dot2_automatic_polledData_vulnerability(self):
        fprint(self, "TC_ID: 55022 - verify_1dot2_automatic_polledData_vulnerability")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Vulnerability")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_a", "stix1dot2/threatdata_automatic_vulnerability.csv")
        fprint(self, "[Passed] Found all the Vulnerability data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_26_verify_1dot2_automatic_polledData_campaign(self):
        fprint(self, "TC_ID: 55026 - verify_1dot2_automatic_polledData_campaign")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Campaign")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_a", "stix1dot2/threatdata_automatic_campaign.csv")
        fprint(self, "[Passed] Found all the Campaign data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_27_verify_1dot2_automatic_polledData_course_of_action(self):
        fprint(self, "TC_ID: 55027 - verify_1dot2_automatic_polledData_course_of_action")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Course of Action")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_a", "stix1dot2/threatdata_automatic_course_of_action.csv")
        fprint(self, "[Passed] Found all the Course Of Action data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_28_verify_1dot2_automatic_polledData_indicator(self):
        fprint(self, "TC_ID: 55028 - verify_1dot2_automatic_polledData_indicator")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Indicator")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_a", "stix1dot2/threatdata_automatic_indicator.csv")
        fprint(self, "[Passed] Found all the Indicator data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_34_verify_1dot2_automatic_polledData_report(self):
        fprint(self, "TC_ID: 55034 - verify_1dot2_automatic_polledData_report")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Report")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_a", "stix1dot2/threatdata_automatic_report.csv")
        fprint(self, "[Passed] Found all the Report data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_35_verify_1dot2_automatic_polledData_threat_actor(self):
        fprint(self, "TC_ID: 55035 - verify_1dot2_automatic_polledData_threat_actor")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Threat Actor")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_a", "stix1dot2/threatdata_automatic_threat_actor.csv")
        fprint(self, "[Passed] Found all the Threat Actor data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_13_verify_1dot2_automatic_polledData_incident(self):
        fprint(self, "TC_ID: 55013 - verify_1dot2_automatic_polledData_incident")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Incident")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_a", "stix1dot2/threatdata_automatic_incident.csv")
        fprint(self, "[Passed] Found all the Incident data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_13_verify_1dot2_automatic_polledData_ttp(self):
        fprint(self, "TC_ID: 55013 - verify_1dot2_automatic_polledData_ttp")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "TTP")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_m", "stix1dot2/threatdata_automatic_ttp.csv")
        fprint(self, "[Passed] Found all the TTP data, in Manual Polling")

    def test_37_delete_STIXSource_1dot2(self):
        fprint(self, "TC_ID: 55037 - delete_STIXSource_1dotX")
        """
        This Case will fail when source "test_STIX_SourceName" is not already there
        """
        source_name = ["1dot2_m", "1dot2_a"]
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected to the Integration Management page successfully")
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        fprint(self, "Search Bar is visible")
        for stix_source in source_name:
            fprint(self, "Searching the STIX Source - "+stix_source)
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
            self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys(stix_source)
            self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
            if waitfor(self, 5, By.XPATH, "//p[contains(text(),'"+stix_source+"')]", False):
                remove_stix_source(self, stix_source)
            else:
                fprint(self, "STIX Source not Found - "+stix_source)

    # Worked for both 3.0 and previous versions
    def test_38_verify_1dot2_automatic_polledData_malware(self):
        fprint(self, "TC_ID: 55038 - verify_1dot2_automatic_polledData_malware")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Malware")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_a", "stix1dot2/threatdata_automatic_malware.csv")
        fprint(self, "[Passed] Found all the Malware data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_39_verify_1dot2_automatic_polledData_attackPattern(self):
        fprint(self, "TC_ID: 55039 - verify_1dot2_automatic_polledData_attack_pattern")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Attack Pattern")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_a", "stix1dot2/threatdata_automatic_attack_pattern.csv")
        fprint(self, "[Passed] Found all the Attack Pattern data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_40_verify_1dot2_automatic_polledData_infrastructure(self):
        fprint(self, "TC_ID: 55040 - verify_1dot2_automatic_polledData_infrastructure")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Infrastructure")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_a", "stix1dot2/threatdata_automatic_infrastructure.csv")
        fprint(self, "[Passed] Found all the Infrastructure data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_41_verify_1dot2_automatic_polledData_identity(self):
        fprint(self, "TC_ID: 55041 - verify_1dot2_automatic_polledData_identity")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Identity")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "1dot2_a", "stix1dot2/threatdata_automatic_identity.csv")
        fprint(self, "[Passed] Found all the Identity data, in Automatic Polling")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())