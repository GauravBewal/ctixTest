import unittest
from lib.ui.fs_stix import *
from lib.ui.nav_tableview import *
from lib.ui.nav_threat_data import *


class IntegrationStix2dot1(unittest.TestCase):

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

    def choose_previous_date(self):
        fprint(self, "Selecting date from the calender")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),' Select Start Time ')]/ancestor::div[1]/preceding::div[1]")
        self.driver.find_element_by_xpath("//span[contains(text(),' Select Start Time ')]/ancestor::div[1]/preceding::div[1]").click()
        if waitfor(self, 5, By.XPATH, "(//td[@class='available today current']/preceding::td[1])[1]", False):
            self.driver.find_element_by_xpath("(//td[@class='available today current']/preceding::td[1])[1]").click()
            fprint(self, "Selected Yesterday's date")
        elif waitfor(self, 5, By.XPATH, "//td[@class='available today current']/ancestor::tr/preceding::tr[1]/td[7]", False):
            self.driver.find_element_by_xpath(
                "//td[@class='available today']/ancestor::tr/preceding::tr[1]/td[7]").click()
            fprint(self, "Selected Yesterday's date")
        else:
            fprint(self, "Going back to previous month")
            self.driver.find_element_by_xpath("//button[@aria-label='Previous Month']").click()
            waitfor(self, 5, By.XPATH, "//td[@class='next-month']")
            self.driver.find_element_by_xpath("//td[@class='next-month']").click()
            fprint(self, "Selected previous month date")

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
        waitfor(self, 5, By.XPATH, "//div[text()='STIX 2.1']")
        self.driver.find_element_by_xpath("//div[text()='STIX 2.1']").click()
        fprint(self, "STIX version - STIX 2.1")
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

    def test_01_adding_STIXSource_2dot1_manualPoll(self):
        fprint(self, "TC_ID: 5001 - Adding_STIXSource_2dot1_verify_manual_polling")
        self.adding_STIXSource('2dot1_m',
                               'https://orion.cywareqa.com/3a46ca11-b015-4b12-8a8c-1d73e726d171/taxii2/',
                               '3a46ca11-b015-4b12-8a8c-1d73e726d171', '7c3ea97b-6d07-45a4-9c0f-295ee70a6599')
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        fprint(self, "Searching the STIX Source - 2dot1_m")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("2dot1_m")
        self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
        waitfor(self, 5, By.XPATH, "//p[contains(text(),'2dot1_m')]")
        fprint(self, "Getting the added STIX Source - 2dot1_m")
        # Clicked on the action menu
        self.driver.find_element_by_xpath("//p[contains(text(),'2dot1_m')]//ancestor::div[1]/div[2]").click()
        fprint(self, 'Clicked on the action menu')
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'View Collections')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'View Collections')]").click()
        fprint(self, "Clicked on the View Collections")
        waitfor(self, 5, By.XPATH, "//button[@data-testid='action']")
        fprint(self, "Inside of - Collections of 2dot1_m")
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

    def test_02_adding_STIXSource_2dot1_automaticPoll(self):
        fprint(self, "TC_ID: 5002 - adding_STIXSource_2dot1_verify_automatic_polling")
        self.adding_STIXSource('2dot1_a',
                               'https://orion.cywareqa.com/265025a6-d7dc-4fba-8c83-eb1f8da15d49/taxii2/',
                               '265025a6-d7dc-4fba-8c83-eb1f8da15d49', 'cf150b5b-a3d5-440d-8379-03580d5e1e7f')
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        fprint(self, "Searching the STIX Source - 2dot1_a")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("2dot1_a")
        self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
        waitfor(self, 5, By.XPATH, "//p[contains(text(),'2dot1_a')]")
        fprint(self, "Getting the added STIX Source - 2dot1_a")
        # Clicked on the action menu
        self.driver.find_element_by_xpath("//p[contains(text(),'2dot1_a')]//ancestor::div[1]/div[2]").click()
        fprint(self, 'Clicked on the action menu')
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'View Collections')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'View Collections')]").click()
        fprint(self, "Clicked on the View Collections")
        waitfor(self, 5, By.XPATH, "//button[@data-testid='action']")
        fprint(self, "Inside of - Collections of 2dot1_a")
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
        fprint(self, "Waiting for the 15 minutes to data get polled...")
        sleep(900)

    # Only for CTIX Version 3.0
    def test_03_adding_STIXSource_2dot1_manualPoll(self):
        fprint(self, "TC_ID: 5003 - adding_STIXSource_2dot1_manualPoll")
        self.adding_STIXSource('2dot1_m',
                               'https://orion.cywareqa.com/3a46ca11-b015-4b12-8a8c-1d73e726d171/taxii2/',
                               '3a46ca11-b015-4b12-8a8c-1d73e726d171', '7c3ea97b-6d07-45a4-9c0f-295ee70a6599')
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        fprint(self, "Searching the STIX Source - 2dot1_m")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("2dot1_m")
        self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
        waitfor(self, 5, By.XPATH, "//p[contains(text(),'2dot1_m')]")
        fprint(self, "Getting the added STIX Source - 2dot1_m")
        self.driver.find_element_by_xpath("//p[contains(text(),'2dot1_m')]").click()
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
        # process_console_logs(self)
        # fprint(self, "Waiting for the 15 minutes to data get polled...")
        # sleep(900)

    # Worked for both 3.0 and previous versions
    def test_04_verify_2dot1_manual_polledData_indicator(self):
        fprint(self, "TC_ID: 5004 - verify_2dot1_manual_polledData_indicator")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Indicator")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        if Build_Version.__contains__("3."):
            verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_indicator_3dotx.csv")
        else:
            verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_indicator.csv")
        fprint(self, "[Passed] Found all the Indicator data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_05_verify_2dot1_manual_polledData_threatActor(self):
        fprint(self, "TC_ID: 5005 - verify_2dot1_manual_polledData_threatActor")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Threat Actor")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_threat_actor.csv")
        fprint(self, "[Passed] Found all the Threat Actor data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_06_verify_2dot1_manual_polledData_vulnerability(self):
        fprint(self, "TC_ID: 5006 - verify_2dot1_manual_polledData_vulnerability")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Vulnerability")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_vulnerability.csv")
        fprint(self, "[Passed] Found all the Vulnerability data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_07_verify_2dot1_manual_polledData_report(self):
        fprint(self, "TC_ID: 5007 - verify_2dot1_manual_polledData_report")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Report")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_report.csv")
        fprint(self, "[Passed] Found all the Report data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_08_verify_2dot1_manual_polledData_malware(self):
        fprint(self, "TC_ID: 5008 - verify_2dot1_manual_polledData_malware")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Malware")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_malware.csv")
        fprint(self, "[Passed] Found all the Malware data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    # Not getting correct data to compare with, getting some hash or some part of hash.
    def test_09_verify_2dot1_manual_polledData_location(self):
        fprint(self, "TC_ID: 5009 - verify_2dot1_manual_polledData_location")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Location")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_location.csv")
        fprint(self, "[Passed] Found all the Location data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_10_verify_2dot1_manual_polledData_intrusionSet(self):
        fprint(self, "TC_ID: 5010 - verify_2dot1_manual_polledData_intrusionSet")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Intrusion Set")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_intrusion_set.csv")
        fprint(self, "[Passed] Found all the Intrusion Set data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_11_verify_2dot1_manual_polledData_identity(self):
        fprint(self, "TC_ID: 5011 - verify_2dot1_manual_polledData_identity")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Identity")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_identity.csv")
        fprint(self, "[Passed] Found all the Identity data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_12_verify_2dot1_manual_polledData_courseOfAction(self):
        fprint(self, "TC_ID: 5012 - verify_2dot1_manual_polledData_courseOfAction")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Course of Action")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_course_of_action.csv")
        fprint(self, "[Passed] Found all the Course Of Action data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_13_verify_2dot1_manual_polledData_campaign(self):
        fprint(self, "TC_ID: 5013 - verify_2dot1_manual_polledData_campaign")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Campaign")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_campaign.csv")
        fprint(self, "[Passed] Found all the Campaign data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_14_verify_2dot1_manual_polledData_attackPattern(self):
        fprint(self, "TC_ID: 5014 - verify_2dot1_manual_polledData_attackPattern")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Attack Pattern")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_attack_pattern.csv")
        fprint(self, "[Passed] Found all the Attack Pattern data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_15_verify_2dot1_manual_polledData_infrastructure(self):
        fprint(self, "TC_ID: 5015 - verify_2dot1_manual_polledData_infrastructure")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Infrastructure")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_infrastructure.csv")
        fprint(self, "[Passed] Found all the Infrastructure data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_16_verify_2dot1_manual_polledData_tool(self):
        fprint(self, "TC_ID: 5016 - verify_2dot1_manual_polledData_tool")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Tool")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_tool.csv")
        fprint(self, "[Passed] Found all the Tool data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_17_verify_2dot1_manual_polledData_opinion(self):
        fprint(self, "TC_ID: 5017 - verify_2dot1_manual_polledData_opinion")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Opinion")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_opinion.csv")
        fprint(self, "[Passed] Found all the Opinion data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    def test_18_verify_2dot1_manual_polledData_malware_analysis(self):
        fprint(self, "TC_ID: 5018 - verify_2dot1_manual_polledData_malware_analysis")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Malware Analysis")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_malware_analysis.csv")
        fprint(self, "[Passed] Found all the Malware Analysis data, in Manual Polling")

    # Worked for both 3.0 and previous versions
    # Need to add it back in ui_v3.txt
    # def test_19_verify_2dot1_manual_polledData_observed_data(self):
    #     fprint(self, "TC_ID: 5019 - verify_2dot1_manual_polledData_observed_data")
    #     if Build_Version.__contains__("3."):
    #         nav_menu_main(self, "Threat Data")
#     #         beforeVerifying_PolledData(self, "Observed Data")
    #     else:
    #         fprint(self, "Navigating to the Threat Data")
    #         nav_menu_main(self, "Threat Data")
    #     verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_manual_observed_data.csv")
    #     fprint(self, "[Passed] Found all the 'Observed Data' data, in Automatic Polling")

    # Only for CTIX Version 3.0
    def test_20_v3_adding_STIXSource_2dot1_automaticPoll(self):
        fprint(self, "TC_ID: 5020 - adding_STIXSource_2dot1_automaticPoll")
        self.adding_STIXSource('2dot1_a',
                               'https://orion.cywareqa.com/265025a6-d7dc-4fba-8c83-eb1f8da15d49/taxii2/',
                               '265025a6-d7dc-4fba-8c83-eb1f8da15d49', 'cf150b5b-a3d5-440d-8379-03580d5e1e7f')
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        fprint(self, "Searching the STIX Source - 2dot1_a")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("2dot1_a")
        self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
        waitfor(self, 5, By.XPATH, "//p[contains(text(),'2dot1_a')]")
        fprint(self, "Getting the added STIX Source - 2dot1_a")
        self.driver.find_element_by_xpath("//p[contains(text(),'2dot1_a')]").click()
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
    def test_21_verify_2dot1_automatic_polledData_malware(self):
        fprint(self, "TC_ID: 5021 - verify_2dot1_automatic_polledData_malware")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Malware")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_malware.csv")
        fprint(self, "[Passed] Found all the Malware data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_22_verify_2dot1_automatic_polledData_vulnerability(self):
        fprint(self, "TC_ID: 5022 - verify_2dot1_automatic_polledData_vulnerability")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Vulnerability")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_vulnerability.csv")
        fprint(self, "[Passed] Found all the Vulnerability data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_23_verify_2dot1_automatic_polledData_attackPattern(self):
        fprint(self, "TC_ID: 5023 - verify_2dot1_automatic_polledData_attackPattern")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Attack Pattern")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_attack_pattern.csv")
        fprint(self, "[Passed] Found all the Attack Pattern data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_24_verify_2dot1_automatic_polledData_identity(self):
        fprint(self, "TC_ID: 5024 - verify_2dot1_automatic_polledData_identity")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Identity")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_identity.csv")
        fprint(self, "[Passed] Found all the Identity data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_25_verify_2dot1_automatic_polledData_infrastructure(self):
        fprint(self, "TC_ID: 5025 - verify_2dot1_automatic_polledData_infrastructure")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Infrastructure")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_infrastructure.csv")
        fprint(self, "[Passed] Found all the Infrastructure data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_26_verify_2dot1_automatic_polledData_campaign(self):
        fprint(self, "TC_ID: 5026 - verify_2dot1_automatic_polledData_campaign")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Campaign")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_campaign.csv")
        fprint(self, "[Passed] Found all the Campaign data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_27_verify_2dot1_automatic_polledData_course_of_action(self):
        fprint(self, "TC_ID: 5027 - verify_2dot1_automatic_polledData_course_of_action")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Course of Action")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_course_of_action.csv")
        fprint(self, "[Passed] Found all the Course Of Action data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_28_verify_2dot1_automatic_polledData_indicator(self):
        fprint(self, "TC_ID: 5028 - verify_2dot1_automatic_polledData_indicator")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Indicator")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        if Build_Version.__contains__("3."):
            verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_indicator_3dotx.csv")
        else:
            verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_indicator.csv")
        fprint(self, "[Passed] Found all the Indicator data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_29_verify_2dot1_automatic_polledData_intrusion_set(self):
        fprint(self, "TC_ID: 5029 - verify_2dot1_automatic_polledData_intrusion_set")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Intrusion Set")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_intrusion_set.csv")
        fprint(self, "[Passed] Found all the Intrusion Set data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_30_verify_2dot1_automatic_polledData_location(self):
        fprint(self, "TC_ID: 5030 - verify_2dot1_automatic_polledData_location")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Location")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_location.csv")
        fprint(self, "[Passed] Found all the Location data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_31_verify_2dot1_automatic_polledData_malware_analysis(self):
        fprint(self, "TC_ID: 5031 - verify_2dot1_automatic_polledData_malware_analysis")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Malware Analysis")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_malware_analysis.csv")
        fprint(self, "[Passed] Found all the Malware Analysis data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    # Need to add it back in ui_v3.txt
    # def test_32_verify_2dot1_automatic_polledData_observed_data(self):
    #     fprint(self, "TC_ID: 5032 - verify_2dot1_automatic_polledData_observed_data")
    #     if Build_Version.__contains__("3."):
    #         nav_menu_main(self, "Threat Data")
#     #         beforeVerifying_PolledData(self, "Observed Data")
    #     else:
    #         fprint(self, "Navigating to the Threat Data")
    #         nav_menu_main(self, "Threat Data")
    #     verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_observed_data.csv")
    #     fprint(self, "[Passed] Found all the 'Observed Data' data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_33_verify_2dot1_automatic_polledData_opinion(self):
        fprint(self, "TC_ID: 5033 - verify_2dot1_automatic_polledData_opinion")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Opinion")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_opinion.csv")
        fprint(self, "[Passed] Found all the Opinion data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_34_verify_2dot1_automatic_polledData_report(self):
        fprint(self, "TC_ID: 5034 - verify_2dot1_automatic_polledData_report")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Report")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_report.csv")
        fprint(self, "[Passed] Found all the Report data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_35_verify_2dot1_automatic_polledData_threat_actor(self):
        fprint(self, "TC_ID: 5035 - verify_2dot1_automatic_polledData_threat_actor")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Threat Actor")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_threat_actor.csv")
        fprint(self, "[Passed] Found all the Threat Actor data, in Automatic Polling")

    # Worked for both 3.0 and previous versions
    def test_36_verify_2dot1_automatic_polledData_tool(self):
        fprint(self, "TC_ID: 5036 - verify_2dot1_automatic_polledData_tool")
        if Build_Version.__contains__("3."):
            nav_menu_main(self, "Threat Data")
            # beforeVerifying_PolledData(self, "Tool")
        else:
            fprint(self, "Navigating to the Threat Data")
            nav_menu_main(self, "Threat Data")
        verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_tool.csv")
        fprint(self, "[Passed] Found all the Tool data, in Automatic Polling")

    def test_37_delete_STIXSource_2dot1(self):
        fprint(self, "TC_ID: 5037 - delete_STIXSource_2dot1")
        """
        This Case will fail when source "test_STIX_SourceName" is not already there
        """
        source_name = ["2dot1_m", "2dot1_a"]
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

    # Worked for 3.0 only
    def test_38_verify_2dot1_manual_polledData_observable(self):
        fprint(self, "TC_ID: 5038 - verify_2dot1_manual_polledData_observable")
        nav_menu_main(self, "Threat Data")
        # beforeVerifying_PolledData(self, "Observable")
        verify_polleddata_in_threatdata(self, "2dot1_m", "stix2dot1/threatdata_manual_observable.csv")
        fprint(self, "[Passed] Found all the Observable data, in Manual Polling")

    # Worked for 3.0 only
    def test_39_verify_2dot1_automatic_polledData_observable(self):
        fprint(self, "TC_ID: 5039 - verify_2dot1_automatic_polledData_observable")
        nav_menu_main(self, "Threat Data")
        # beforeVerifying_PolledData(self, "Observable")
        verify_polleddata_in_threatdata(self, "2dot1_a", "stix2dot1/threatdata_automatic_observable.csv")
        fprint(self, "[Passed] Found all the Observable data, in Manual Polling")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
