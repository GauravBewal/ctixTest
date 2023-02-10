import unittest
from lib.ui.nav_app import *


class NavigationTestsv2(unittest.TestCase):

    #@classmethod
    #def setUpClass(self):
    #    self.driver = initialize_browser(self)

    #@classmethod
    #def tearDownClass(self):
    #    self.driver.quit()

    @classmethod
    def setUp(self):
        self.driver = initialize_browser(self)
        login(self, Admin_Email, Admin_Password)
        clear_console_logs(self)

    def tearDown(self):
        self.driver.quit()

    def test_01_open_ctix_app_login(self):
        fprint(self, "TC_ID: 1 - Open Ctix app and login")
        #login(self, Admin_Email, Admin_Password)
        process_console_logs(self)

    def test_02_page_Reports(self):
        fprint(self, "TC_ID: 2 - Test Navigation - Reports")
        nav_menu_main(self, "Reports")

    def test_03_page_Live_Activity(self):
        fprint(self, "TC_ID: 3 - Test Navigation - Live Activity")
        nav_menu_main(self, "Live Activity")

    def test_04_page_Threat_Data(self):
        fprint(self, "TC_ID: 4 - Test Navigation - Threat Data")
        nav_menu_main(self, "Threat Data")

    def test_05_page_RSS_Feeds(self):
        fprint(self, "TC_ID: 5 - Test Navigation - RSS Feeds")
        nav_menu_main(self, "RSS Feeds")

    def test_06_page_ThreatMailbox(self):
        fprint(self, "TC_ID: 6 - Test Navigation - Threat Mailbox")
        nav_menu_main(self, "Threat Mailbox")

    def test_07_page_Twitter_Feeds(self):
        fprint(self, "TC_ID: 7 - Test Navigation - Twitter Feeds")
        nav_menu_main(self, "Twitter Feeds")

    def test_08_page_Threat_Bulletins(self):
        fprint(self, "TC_ID: 8 - Test Navigation - Threat Bulletins")
        nav_menu_main(self, "Threat Bulletins")

    def test_09_page_Intel_Packages(self):
        fprint(self, "TC_ID: 9 - Test Navigation - Intel Packages")
        nav_menu_main(self, "Intel Packages")

    def test_10_page_Threat_Visualizer(self):
        fprint(self, "TC_ID: 10 - Test Navigation - Threat Investigations")
        nav_menu_main(self, "Threat Investigations")

    def test_11_page_Threat_Actors(self):
        fprint(self, "TC_ID: 11 - Test Navigation - Threat Actors")
        nav_menu_main(self, "Threat Actors")

    def test_12_page_ATTaCK_Navigator(self):
        fprint(self, "TC_ID: 12 - Test Navigation - ATT&CK Navigator")
        nav_menu_main(self, "ATT&CK Navigator")

    def test_13_page_Fang_Defang(self):
        fprint(self, "TC_ID: 13 - Test Navigation - Fang - Defang")
        nav_menu_main(self, "Fang - Defang")

    def test_14_page_STIX_Conversion(self):
        fprint(self, "TC_ID: 14 - Test Navigation - STIX conversion")
        nav_menu_main(self, "STIX conversion")

    def test_15_page_Encode_Decode(self):
        fprint(self, "TC_ID: 15 - Test Navigation - Encode - Decode: Base64")
        nav_menu_main(self, "Encode - Decode: Base64")

    def test_16_page_CVSS_Calculator(self):
        fprint(self, "TC_ID: 16 - Test Navigation - CVSS Calculator")
        nav_menu_main(self, "CVSS Calculator")

    def test_17_page_Network_Utilities(self):
        fprint(self, "TC_ID: 17 - Test Navigation - Network Utilities")
        nav_menu_main(self, "Network Utilities")

    def test_18_page_Rules(self):
        fprint(self, "TC_ID: 18 - Test Navigation - Rules")
        nav_menu_main(self, "Rules")

    def test_19_page_Actionable_Indicators(self):
        fprint(self, "TC_ID: 19 - Test Navigation - Actionable Indicators")
        nav_menu_main(self, "Actionable Indicators")

    def test_20_page_Tasks(self):
        fprint(self, "TC_ID: 20 - Test Navigation - Tasks")
        nav_menu_main(self, "Tasks")

    def test_21_page_Create_Intel_Package(self):
        fprint(self, "TC_ID: 21 - Test Navigation - Create Intel Package")
        nav_menu_main(self, "Create Intel Package")

    def test_22_page_Intel_Inbox(self):
        fprint(self, "TC_ID: 22 - Test Navigation - Intel Inbox")
        nav_menu_main(self, "Intel Inbox")

    def test_23_page_Create_Threat_Bulletin(self):
        fprint(self, "TC_ID: 23 - Test Navigation - Create Threat Bulletin")
        nav_menu_main(self, "Create Threat Bulletin")

    def test_24_page_Saved_Searches(self):
        fprint(self, "TC_ID: 24 - Test Navigation - Saved Searches")
        nav_menu_main(self, "Saved Searches")

    def test_25_page_Domain_Fuzzer(self):
        fprint(self, "TC_ID: 25 - Test Navigation - Domain Fuzzer")
        nav_menu_main(self, "Domain Fuzzer")

    def test_26_page_Watchlist_Alerts(self):
        fprint(self, "TC_ID: 26 - Test Navigation - Watchlist Alerts")
        nav_menu_main(self, "Watchlist Alerts")

    def test_27_page_Manual_Review(self):
        fprint(self, "TestCase: 27 - Test Navigation - Manual Review")
        nav_menu_main(self, "Manual Review")

    def test_28_page_Indicators_Allowed(self):
        fprint(self, "TC_ID: 28 - Test Navigation - Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")

    def test_29_page_Watchlist(self):
        fprint(self, "TC_ID: 29 - Test Navigation - Watchlist")
        nav_menu_main(self, "Watchlist")

    def test_30_page_Tags(self):
        fprint(self, "TC_ID: 30 - Test Navigation - Tags")
        nav_menu_main(self, "Tags")

    def test_31_page_Background_Tasks(self):
        fprint(self, "TC_ID: 31 - Test Navigation - Background Tasks")
        nav_menu_main(self, "Background Tasks")

    def test_32_page_Dashboards(self):
        fprint(self, "TC_ID: 32 - Test Navigation - Dashboards")
        nav_menu_main(self, "Dashboards")

    def test_33_page_User_Management(self):
        fprint(self, "TC_ID: 33 - Test Navigation - User Management")
        nav_menu_admin(self, "User Management")

    def test_34_page_Integration_Management(self):
        fprint(self, "TC_ID: 34 - Test Navigation - Integration Management")
        nav_menu_admin(self, "Integration Management")

    def test_35_page_Enrichment_Management(self):
        fprint(self, "TC_ID: 35 - Test Navigation - Enrichment Management")
        nav_menu_admin(self, "Enrichment Management")

    def test_36_page_Certificates(self):
        fprint(self, "TC_ID: 36 - Test Navigation - Certificates")
        nav_menu_admin(self, "Certificates")

    def test_37_page_License_Management(self):
        fprint(self, "TC_ID: 37 - Test Navigation - License Management")
        nav_menu_admin(self, "License Management")

    def test_38_page_Followed_Data(self):
        fprint(self, "TC_ID: 38 - Test Navigation - Followed Data")
        nav_menu_admin(self, "Followed Data")

    def test_39_page_Configuration(self):
        fprint(self, "TC_ID: 39 - Test Navigation - Configuration")
        nav_menu_admin(self, "Configuration")

    def test_40_page_STIX_Collections(self):
        fprint(self, "TC_ID: 40 - Test Navigation - STIX Collections")
        nav_menu_admin(self, "STIX Collections")

    def xtest_41_page_Organization_Type(self):
        fprint(self, "TC_ID: 41 - Test Navigation - Organization Type")
        nav_menu_admin(self, "Organization Type")

    def test_42_page_Confidence_Score(self):
        fprint(self, "TC_ID: 42 - Test Navigation - Confidence Score")
        nav_menu_admin(self, "Confidence Score")

    def test_43_page_Console_Status(self):
        fprint(self, "TC_ID: 43 - Test Navigation - Console Status")
        nav_menu_admin(self, "Console Status")


class NavigationTestsv3(unittest.TestCase):

    @classmethod
    def setUp(self):
        self.driver = initialize_browser(self)
        login(self, Admin_Email, Admin_Password)
        clear_console_logs(self)

    def tearDown(self):
        self.driver.quit()

    def test_01_open_ctix_app_login(self):
        fprint(self, "TC_ID: 1 - Open Ctix app and login")
        #login(self, Admin_Email, Admin_Password)
        process_console_logs(self)

    def test_02_page_Reports(self):
        fprint(self, "TC_ID: 2 - Test Navigation - Reports")
        nav_menu_main(self, "Reports")

    def test_04_page_Threat_Data(self):
        fprint(self, "TC_ID: 4 - Test Navigation - Threat Data")
        nav_menu_main(self, "Threat Data")

    def test_05_page_RSS_Feeds(self):
        fprint(self, "TC_ID: 5 - Test Navigation - RSS Feeds")
        nav_menu_main(self, "RSS Feeds")

    def test_06_page_ThreatMailbox(self):
        fprint(self, "TC_ID: 6 - Test Navigation - Threat Mailbox")
        nav_menu_main(self, "Threat Mailbox")

    # def test_07_page_Twitter_Feeds(self):
    #     fprint(self, "TC_ID: 7 - Test Navigation - Twitter Feeds")
    #     nav_menu_main(self, "Twitter Feeds")

    def test_10_page_Threat_Visualizer(self):
        fprint(self, "TC_ID: 10 - Test Navigation - Threat Investigations")
        nav_menu_main(self, "Threat Investigations")

    def test_18_page_Rules(self):
        fprint(self, "TC_ID: 18 - Test Navigation - Rules")
        nav_menu_main(self, "Rules")

    def test_20_page_Tasks(self):
        fprint(self, "TC_ID: 20 - Test Navigation - Tasks")
        nav_menu_main(self, "Tasks")

    def test_28_page_Indicators_Allowed(self):
        fprint(self, "TC_ID: 28 - Test Navigation - Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")

    def test_30_page_Tags(self):
        fprint(self, "TC_ID: 30 - Test Navigation - Tags")
        nav_menu_main(self, "Tags")

    def test_32_page_Dashboards(self):
        fprint(self, "TC_ID: 32 - Test Navigation - Dashboards")
        nav_menu_main(self, "Dashboards")

    def test_33_page_User_Management(self):
        fprint(self, "TC_ID: 33 - Test Navigation - User Management")
        nav_menu_admin(self, "User Management")

    def test_34_page_Integration_Management(self):
        fprint(self, "TC_ID: 34 - Test Navigation - Integration Management")
        nav_menu_admin(self, "Integration Management")

    def test_35_page_Enrichment_Management(self):
        fprint(self, "TC_ID: 35 - Test Navigation - Enrichment Management")
        nav_menu_admin(self, "Enrichment Management")

    def test_36_page_Certificates(self):
        fprint(self, "TC_ID: 36 - Test Navigation - Certificates")
        nav_menu_admin(self, "Certificates")

    def test_37_page_License_Management(self):
        fprint(self, "TC_ID: 37 - Test Navigation - License Management")
        nav_menu_admin(self, "License Management")

    def test_39_page_Configuration(self):
        fprint(self, "TC_ID: 39 - Test Navigation - Configuration")
        nav_menu_admin(self, "Configuration")

    def test_40_page_STIX_Collections(self):
        fprint(self, "TC_ID: 40 - Test Navigation - STIX Collections")
        nav_menu_admin(self, "STIX Collections")

    def test_42_page_Confidence_Score(self):
        fprint(self, "TC_ID: 42 - Test Navigation - Confidence Score")
        nav_menu_admin(self, "Confidence Score")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
