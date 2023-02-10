import unittest
from pathlib import Path
import pandas as pd
from lib.ui.nav_app import *
from lib.ui.nav_threat_data import bulk_ioc_lookup_upload_file

show_button_expected_data_list = ['3a-d6-75-e8-c7-7f', '91:93:c3:e5:ab:99', 'http://www.pena.com/',
                                  'https://guzman.org/', 'b92c:1aa8:a6bf:2b8c:407f:f669:eb88:b23d',
                                  'e0-16-52-55-21-e1', '186.10.48.26', '9.14.109.95']
download_expected_data_list = ['www.pena.com', 'guzman.org']
file_name = "ioc_lookup.csv"


class GlobalIOCLookup(unittest.TestCase):

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

    def test_01_global_search(self):
        """
        Testing if global search is working as expected
        """
        fprint(self, "\n---------- TC_ID 1: Validating if global search is loading ----------")
        nav_menu_main(self, "Dashboards")
        fprint(self, "Clicking on global search")
        self.driver.find_element_by_xpath("//ul/li[a/i][1]").click()
        waitfor(self, 2, By.XPATH,
                "//button//ancestor::div/preceding-sibling::div[contains(text(), 'Global Search')]")
        waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='Search here']")
        self.driver.refresh()
        fprint(self, "[PASSED] Global search slider is working as expected")
        process_console_logs(self)

    def test_02_ioc_lookup(self):
        """
        Testing if IOC lookup page is loading
        """
        fprint(self, "\n---------- TC_ID 1: Validating if IOC lookup is loading ----------")
        nav_menu_main(self, "Dashboards")
        fprint(self, "Clicking on global search")
        self.driver.find_element_by_xpath("//ul/li[a/i][1]").click()
        waitfor(self, 2, By.XPATH, "//button[contains(text(),'IOC Lookup')]")
        fprint(self, "Clicking on IOC lookup")
        self.driver.find_element_by_xpath("//button[contains(text(),'IOC Lookup')]").click()
        waitfor(self, 2, By.XPATH, "//h1[contains(text(), 'IOC Lookup')]")
        waitfor(self, 2, By.XPATH, "//input[@aria-placeholder='Search IOCs']")
        fprint(self, "IOC lookup page loaded successfully")
        process_console_logs(self)


class IOCLookup(unittest.TestCase):
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

    def test_01_verify_existing_IOCs(self):
        fprint(self, "TC_ID: 4012331 - test_01_verify_existing_IOCs")
        nav_menu_main(self, "Threat Data")
        file = os.path.join(os.environ["PYTHONPATH"], "testdata", "ioc_lookup/" + file_name)
        bulk_ioc_lookup_upload_file(self, fileName=file)
        fprint(self, "[Passed] - Upload of File is successful")
        self.driver.find_element_by_xpath("//button[contains(text(),'Show')]").click()
        fprint(self, "Clicked on the Show button and waiting for the 2 seconds...")
        sleep(2)
        table = self.driver.find_element_by_xpath("(//table[@class='el-table__body']/tbody)[2]")
        rows = table.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
        feed_channels_list = []
        fprint(self, "Reading all the data from the visible Table...")
        for row in rows:
            col = row.find_elements(By.TAG_NAME, "td")[2]
            feed_channels_list.append(col.text)
        fprint(self, "Comparing the data that is Fetched from the CTIX with the Expected one...")
        if show_button_expected_data_list.sort() == feed_channels_list.sort():
            fprint(self, "[Passed] - Getting all the Expected data in Existing data")
        else:
            fprint(self, "[Failed] - Not Getting all the Expected data in the Existing data")
            self.fail("[Failed] - Not Getting all the Expected data in the Existing data")

    def test_02_verify_downloaded_IOCs(self):
        fprint(self, "TC_ID: 4012332 - test_02_verify_downloaded_IOCs")
        nav_menu_main(self, "Threat Data")
        file = os.path.join(os.environ["PYTHONPATH"], "testdata", "ioc_lookup/" + file_name)
        bulk_ioc_lookup_upload_file(self, fileName=file)
        fprint(self, "[Passed] - Upload of File is successful")
        self.driver.find_element_by_xpath("//span[contains(text(),'Download CSV')]/parent::button").click()
        fprint(self, "Clicked on the Download button, now waiting for the 10 seconds for the file to be downloaded...")
        sleep(10)
        current_path = Path(__file__).parent
        files_list = glob.glob(f"{current_path}/../../reports/downloadFiles/lookup_export.csv")
        fprint(self, "Reading the downloaded file...")
        df_actual_file = pd.read_csv(files_list[0])
        as_list = df_actual_file["IOC Value"].tolist()
        print("Getting - ", as_list)
        sorted_actual_file_list = sorted(as_list)
        print("sorted_actual_file_list - ", sorted_actual_file_list)
        expected_data = sorted(download_expected_data_list)

        if expected_data == sorted_actual_file_list:
            fprint(self, "[Passed] - Getting all the Expected data in Downloaded File")
        else:
            fprint(self, "[Failed] - Not Getting all the Expected data in the Downloaded File")
            self.fail("[Failed] - Not Getting all the Expected data in the Downloaded File")

    def test_03_verify_cancel_bulkIOCs(self):
        fprint(self, "TC_ID: 4012333 - test_03_verify_cancel_bulkIOCs")
        nav_menu_main(self, "Threat Data")
        file = os.path.join(os.environ["PYTHONPATH"], "testdata", "ioc_lookup/" + file_name)
        bulk_ioc_lookup_upload_file(self, fileName=file)
        fprint(self, "[Passed] - Upload of File is successful")
        self.driver.find_element_by_xpath("//span[@class='cyicon-cross-o-active']/parent::button").click()
        fprint(self, "Clicked on the cancel button")
        sleep(2)
        if waitfor(self, 2, By.XPATH, "//button[contains(text(),'Show')]", False):
            fprint(self, "[Failed] - Cancel Bulk IOC is not working fine")
            self.fail("[Failed] - Cancel Bulk IOC is not working fine")
        else:
            fprint(self, "[Passed] - Cancel Bulk IOC is working fine")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
