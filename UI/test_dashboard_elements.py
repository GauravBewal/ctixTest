import unittest
from lib.ui.dashboard_elements import *


class Dashboard(unittest.TestCase):

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

    @classmethod
    def test_01_Intel_Package(self):
        Herocard_Visible(self, "Intel Packages")

    def test_02_Domain_Objects(self):
       Herocard_Visible(self, "Domain Objects")

    def test_03_Blocked_Indicators(self):
        Herocard_Visible(self, "Blocked Indicators")

    def test_04_High_Confidence_Indicators(self):
        Herocard_Visible(self, "High Confidence Indicators")

    def test_05_Deprecated_Indicators(self):
        Herocard_Visible(self,"Deprecated Indicators")

    def test_06_Allowed_Indicators(self):
        Herocard_Visible(self, "Allowed Indicators")

    def test_07_False_Positive_Indicators(self):
        Herocard_Visible(self, "False Positive Indicators")

    def test_08_Top_Geography_IP(self):
        Herocard_Visible(self,"Top Geography - IP")

    def test_10_sources_Vs_Iocs(self):
        sources_Vs_Iocs(self,"API Feeds")

    def test_11_Domain_Objects_vs_Source(self):
        widgets(self,"Domain Objects vs Source")

    def test_12_Confidence_Score_Vs_TLP(self):
        widgets(self,"Confidence Score Vs TLP")

    def test_13_TLP_Vs_All_IOCs(self):
        TLP_Vs_All_IOCs(self, "All IOCs")

    def test_14_Timeline_for_all_countries(self):
       Timeline_for_all_countries(self, "All Countries")

    def test_15_TLD_Distribution(self):
        widgets(self, "TLD Distribution")

    def test_16_recurring_tags(self):
        widgets(self, "Top 5 recurring tags")

    def test_17_IP_Distribution_by_Country(self):
        widgets(self,"IP Distribution by Country")

    def test_18_User_status(self):
        widgets(self, "User status")

    def test_20_TLP_Red(self):
        Herocard_Visible(self,"TLP Red - Domain Objects")

    def test_21_TLP_Amber(self):
        Herocard_Visible(self, "TLP Amber - Domain Objects")

    def test_24_test_Indicator_vs_Timeline(self):
        Indicator_vs_Timeline(self,"Indicator")









if __name__ == '__main__':
    unittest.main(testRunner=reporting())




