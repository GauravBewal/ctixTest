import unittest
from lib.ui.nav_app import *


class WatchlistAlerts(unittest.TestCase):

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

    def test_01_WatchlistAlerts_PageLoad(self):
        fprint(self, "TC_ID: 1 - Watchlist Alerts" + uniquestr)
        nav_menu_main(self, "Watchlist Alerts")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(),'Watchlist Alerts')]")
        fprint(self, "TC_ID: 1 - Watchlist Alerts - Watchlist Alerts Page Load is verified")

    #This will not work for new instance hence, commenting for now
    def Ctest_02_WatchlistAlerts_OverviewHeader(self):
        fprint(self, "TC_ID: 2 - Watchlist Alerts" + uniquestr)
        nav_menu_main(self, "Watchlist Alerts")
        waitfor(self, 5, By.XPATH, "//div[@data-testid = 'overview-Occurrences']")
        fprint(self, "TC_ID: 2 - Watchlist Alerts - overview-Occurrences is seen")
        waitfor(self, 5, By.XPATH, "//div[@data-testid = 'overview-Last Active']")
        fprint(self, "TC_ID: 2 - Watchlist Alerts - overview-Last Active is seen")
        waitfor(self, 5, By.XPATH, "//div[@data-testid = 'overview-Created On']")
        fprint(self, "TC_ID: 2 - Watchlist Alerts - overview-Created On is seen")

        fprint(self, "TC_ID: 2 - Watchlist Alerts - OverviewHeader is verified")

if __name__ == '__main__':
    unittest.main(testRunner=reporting())
