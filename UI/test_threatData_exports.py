import unittest
from pathlib import Path
import pandas as pd
from lib.ui.nav_threat_data import *


class ThreatDataDetailsPage(unittest.TestCase):

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

    def enable_disabled_columns(self, col_name):
        element = self.driver.find_element_by_xpath(
            "//span[contains(@class,'column-option') and normalize-space()='" + col_name + "']/i[contains(@class,'cyicon-check-circle-outline')]")
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        self.driver.find_element_by_xpath(
            "//span[contains(@class,'column-option') and normalize-space()='" + col_name + "']/i[contains(@class,'cyicon-check-circle-outline')]").click()
        fprint(self, "Column Enabled - " + col_name)

    def disable_active_columns(self, data):
        for col in data:
            if waitfor(self, 0, By.XPATH,
                       "//span[contains(@class,'column-option__active') and (normalize-space()='" + col + "')]",
                       False):
                element = self.driver.find_element_by_xpath(
                    "//span[normalize-space()='" + col + "']/i[contains(@class,'cyicon-check-circle-outline')]")
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                self.driver.find_element_by_xpath(
                    "//span[normalize-space()='" + col + "']/i[contains(@class,'cyicon-check-circle-outline')]").click()
                fprint(self, "Column Disabled - " + col)

    def visible_column(self, col_name):
        global flag
        data = []
        self.driver.find_element_by_xpath(
            "//div[@data-testaction='dropdown-link']//div[contains(@class,'cyicon-add-active')]").click()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Custom')]/parent::div//div[@class='section-columns']")
        cust_col = self.driver.find_element_by_xpath(
            "//span[contains(text(),'Custom')]/parent::div//div[@class='section-columns']")
        col_names = cust_col.find_elements(By.TAG_NAME, "span")
        for col in col_names:
            data.append(col.text)
        if flag == 0:
            fprint(self, "Disabling all Active columns")
            self.disable_active_columns(data)
            flag = flag + 1
            fprint(self, "Enabling Column - " + col_name)
            self.enable_disabled_columns(col_name)
        self.driver.find_element_by_xpath(
            "//div[@data-testaction='dropdown-link']//div[contains(@class,'cyicon-add-active')]").click()

    def test_01_verify_export_functionality(self):
        fprint(self, "TC_ID: 4011500 - Threat data SDO")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "(//button[contains(text(),'Clear Selected')])[1]")
        self.driver.find_element_by_xpath("(//button[contains(text(),'Clear Selected')])[1]").click()
        self.driver.find_element_by_xpath(
            "//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        sleep(1)
        select_threatData_filter(self, filter_name="Source", object_name="2dot1_m")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")
        waitfor(self, 20, By.XPATH, "//button[@data-testaction='open-export']")
        self.driver.find_element_by_xpath("//button[@data-testaction='open-export']").click()
        waitfor(self, 10, By.XPATH, "//li[@name='csv']")
        self.driver.find_element_by_xpath("//li[@name='csv']").click()
        verify_success(self, "Export is in progress. You will receive a notification once the export is complete")
        fprint(self, "Waiting for the 20 seconds for the file to be downloaded properly...")
        sleep(20)   # Required
        current_path = Path(__file__).parent
        files_list = glob.glob(f"{current_path}/../../reports/downloadFiles/*.csv")

        fprint(self, "Reading the downloaded file...")
        actual_file = pd.read_csv(files_list[0])
        print(self, actual_file)
        #Todo: Not including the below-mentioned column data assertion because of the dynamic value, will check from API

        if actual_file.__contains__("System Created Date"):
            exclude_columns = ["System Created Date", "System Modified Date", "Valid Until", "Valid From", "Tags"]
            print("Considered New version Columns...")
            file_path = os.path.join(os.environ["PYTHONPATH"], "testdata", "export_file_assertionData",
                                     "2dot1_m_indicator_sdo_new.csv")
        else:
            exclude_columns = ["Created Date", "Modified Date", "Valid Until", "Valid From", "Tags", "Conf Score"]
            print("Considered Old version Columns...")
            file_path = os.path.join(os.environ["PYTHONPATH"], "testdata", "export_file_assertionData",
                                     "2dot1_m_indicator_sdo.csv")
        fprint(self, "Reading the stored file..")
        expected_file = pd.read_csv(file_path)
        print("expected file - ", expected_file)
        # Debugging
        merged_df = actual_file.merge(expected_file, how = "left", indicator=True)
        uncommon_rows = merged_df[merged_df["_merge"] == "left_only"]
        print("Uncommon roes - ", uncommon_rows)
        fprint(self, "Matching the data in both of them...")
        common_dataset = pd.merge(actual_file.drop(columns=exclude_columns), expected_file.drop(columns=exclude_columns), how="inner")
        print("common_dataset", common_dataset)
        actual_rows = common_dataset.shape[0]
        print("actual_rows", actual_rows)
        if actual_rows == 8:
            fprint(self, "[PASSED] Getting correct data in the downloaded file")
        else:
            fprint(self, "[Failed] Not Getting correct data in the downloaded file")
            self.fail("[Failed] Not Getting correct data in the downloaded file")

    def test_02_csv_file(self):
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "(//button[contains(text(),'Clear Selected')])[1]")
        self.driver.find_element_by_xpath("(//button[contains(text(),'Clear Selected')])[1]").click()
        self.driver.find_element_by_xpath(
            "//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        sleep(1)
        select_threatData_filter(self, filter_name="Source", object_name="2dot1_m")
        sleep(2)
        waitfor(self, 10, By.XPATH, "//table//span[contains(text(),'Value')]")

        waitfor(self, 20, By.XPATH, "//tbody/ancestor::table")
        table = self.driver.find_element_by_xpath("//tbody/ancestor::table")
        rows = table.find_elements(By.TAG_NAME, "tr")  # get all of the rows in the table
        num_rows = (len(rows))
        feed_channels = []
        while num_rows > 0:
            row_text = table.find_elements(By.TAG_NAME, "tr")
            print("row text - ", row_text, " ", row_text[0].text)
            feed_channels.append(row_text[0].text)
            num_rows = num_rows - 1

        # for row in rows:
        #     # Get the columns (all the data from column 1)
        #     col = row.find_elements(By.TAG_NAME, "td")  # note: index start from 0, 1 and 2. Getting the data from 0.
        #     print("col - ", col, " ", col[0].text)
        #     feed_channels.append(col)

        print(feed_channels)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
