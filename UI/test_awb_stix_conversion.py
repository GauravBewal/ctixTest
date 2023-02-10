import unittest
from lib.ui.analyst_workbench import click_to_process
from lib.ui.nav_threat_data import *
import json
from deepdiff import DeepDiff


stix_1dotx_filename = "stix_1dotx.txt"
stix_2dot1_filename = "stix_2dot1.txt"
stix_2dot0_filename = "stix_2dot0.txt"


class STIXConversion(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.driver = initialize_browser(self)
        login(self, Admin_Email, Admin_Password)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def click_import_file(self):
        self.driver.find_element_by_xpath("(//span[@class='cyicon-more-vertical'])[1]").click()
        try:
            waitfor(self, 10, By.XPATH, "(//span[contains(text(),'Upload a File')])[2]")
            self.driver.find_element_by_xpath("(//span[contains(text(),'Upload a File')])[2]").click()
        except:
            self.driver.find_element_by_xpath("//div/span[contains(text(),'Upload a File')]").click()

    def upload_file(self, file_name):
        waitfor(self, 5, By.XPATH, "//input[@type = 'file']")
        upload = self.driver.find_element_by_xpath("//input[@type = 'file']")
        file_path = os.path.join(os.environ["PYTHONPATH"], "testdata", "stix_conversion/" + file_name)
        fprint(self, "Uploading file... - " + file_name)
        upload.send_keys(file_path)
        # Intentionally used sleep waiting for file to be completely uploaded
        sleep(7)

    def select_version_of_input(self, version):
        waitfor(self, 5, By.XPATH, "(//span[contains(@class,'cyicon-chevron-down')]/parent::button)[1]")
        self.driver.find_element_by_xpath("(//span[contains(@class,'cyicon-chevron-down')]/parent::button)[1]").click()
        fprint(self, "Clicked on the Version dropdown of Input box")
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'"+version+"')]")
        self.driver.find_element_by_xpath("(//div[contains(text(),'"+version+"')])[2]/ancestor::li[1]").click()
        fprint(self, "Clicked on the Version - "+version)
        sleep(1)

    def select_version_of_output(self, version):
        waitfor(self, 5, By.XPATH, "(//span[contains(@class,'cyicon-chevron-down')]/parent::button)[2]")
        self.driver.find_element_by_xpath("(//span[contains(@class,'cyicon-chevron-down')]/parent::button)[2]").click()
        fprint(self, "Clicked on the Version dropdown of Output box")
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'" + version + "')]")
        self.driver.find_element_by_xpath("(//div[contains(text(),'" + version + "')])[2]/ancestor::li[1]").click()
        fprint(self, "Clicked on the Version - " + version)
        sleep(1)

    def verify_data(self, file_name):
        elem = self.driver.find_element_by_xpath("(//textarea[@aria-placeholder='Enter JSON' or @aria-placeholder='Enter XML'])[2]")
        fprint(self, "Reading the converted data...")
        actual_data = elem.get_attribute("_value")
        fprint(self, "Actual Data - " + actual_data)
        file = os.path.join(os.environ["PYTHONPATH"], "testdata", "stix_conversion/" + file_name)
        fprint(self, "Reading the expected data...")
        with open(file) as fi:
            expected = fi.read()
        fprint(self, "expected - "+expected)
        # json_actual = json.dumps(actual_data, sort_keys=True)
        # json_expected = json.dumps(expected, sort_keys=True)
        # json_actual = json.dumps(actual_data)
        # json_expected = json.dumps(expected)
        json_actual = json.loads(actual_data)
        json_expected = json.loads(expected)
        result = DeepDiff(json_actual, json_expected, ignore_order=True)
        fprint(self, "result - "+str(result))
        if len(result) == 0:
            fprint(self, "[Passed] - Getting Expected Data")
        else:
            fprint(self, "[Failed] - Not Getting Expected Data")
            self.fail("[Failed] - Not Getting Expected Data")
        # print("Keys", json_actual.keys())
        fi.close()

    def test_01_verify_stixConv_1dotx_to_2dot0(self):
        fprint(self, "TC_ID: 4012551 - test_01_verify_stixConv_1dotx_to_2dot0")
        nav_menu_main(self, "STIX conversion")
        self.click_import_file()
        self.upload_file(stix_1dotx_filename)
        click_to_process(self, "STIX conversion")
        if not waitfor(self, 10, By.XPATH, "//div[@empty='true']", False):
            fprint(self, "Data is Converted, verifying with the expected one...")
            self.verify_data(stix_2dot0_filename)
        else:
            fprint(self, "[Failed] - Converted data is not visible.")
            self.fail("[Failed] - Converted data is not visible.")

    def test_02_verify_stixConv_1dotx_to_2dot1(self):
        fprint(self, "TC_ID: 4012552 - test_02_verify_stixConv_1dotx_to_2dot1")
        nav_menu_main(self, "STIX conversion")
        self.select_version_of_output("STIX 2.1")
        self.click_import_file()
        self.upload_file(stix_1dotx_filename)
        click_to_process(self, "STIX conversion")
        if not waitfor(self, 10, By.XPATH, "//div[@empty='true']", False):
            fprint(self, "Data is Converted, verifying with the expected one...")
            self.verify_data(stix_2dot1_filename)
        else:
            fprint(self, "[Failed] - Converted data is not visible.")
            self.fail("[Failed] - Converted data is not visible.")

    def test_03_verify_stixConv_2dot1_to_2dot0(self):
        fprint(self, "TC_ID: 4012553 - test_03_verify_stixConv_2dot1_to_2dot0")
        nav_menu_main(self, "STIX conversion")
        self.select_version_of_input("STIX 2.1")
        self.click_import_file()
        self.upload_file(stix_2dot1_filename)
        click_to_process(self, "STIX conversion")
        if not waitfor(self, 10, By.XPATH, "//div[@empty='true']", False):
            fprint(self, "Data is Converted, verifying with the expected one...")
            self.verify_data("from_2dot1/"+stix_2dot0_filename)
        else:
            fprint(self, "[Failed] - Converted data is not visible.")
            self.fail("[Failed] - Converted data is not visible.")

    # Todo: Getting timestamp difference need to check how to assert without that
    # def test_04_verify_stixConv_2dot1_to_1dotx(self):
    #     fprint(self, "TC_ID: 4012554 - test_04_verify_stixConv_2dot1_to_1dotx")
    #     nav_menu_main(self, "STIX conversion")
    #     self.select_version_of_input("STIX 2.1")
    #     self.select_version_of_output("STIX 1.x")
    #     self.click_import_file()
    #     self.upload_file(stix_2dot1_filename)
    #     click_to_process(self, "STIX conversion")
    #     if not waitfor(self, 10, By.XPATH, "//div[@empty='true']", False):
    #         fprint(self, "Data is Converted, verifying with the expected one...")
    #         self.verify_data("from_2dot1/" + stix_1dotx_filename)
    #     else:
    #         fprint(self, "[Failed] - Converted data is not visible.")
    #         self.fail("[Failed] - Converted data is not visible.")

    def test_05_verify_stixConv_2dot0_to_2dot1(self):
        fprint(self, "TC_ID: 4012555 - test_05_verify_stixConv_2dot0_to_2dot1")
        nav_menu_main(self, "STIX conversion")
        self.select_version_of_output("STIX 2.1")
        self.select_version_of_input("STIX 2.0")
        self.click_import_file()
        self.upload_file(stix_2dot0_filename)
        click_to_process(self, "STIX conversion")
        if not waitfor(self, 10, By.XPATH, "//div[@empty='true']", False):
            fprint(self, "Data is Converted, verifying with the expected one...")
            self.verify_data("from_2dot0/" + stix_2dot1_filename)
        else:
            fprint(self, "[Failed] - Converted data is not visible.")
            self.fail("[Failed] - Converted data is not visible.")

    # Todo: Getting timestamp difference need to check how to assert without that
    # def test_06_verify_stixConv_2dot0_to_1dotx(self):
    #     fprint(self, "TC_ID: 4012556 - test_06_verify_stixConv_2dot0_to_1dotx")
    #     nav_menu_main(self, "STIX conversion")
    #     self.select_version_of_output("STIX 2.1")
    #     self.select_version_of_input("STIX 2.0")
    #     self.select_version_of_output("STIX 1.x")
    #     self.click_import_file()
    #     self.upload_file(stix_2dot0_filename)
    #     click_to_process(self, "STIX conversion")
    #     if not waitfor(self, 10, By.XPATH, "//div[@empty='true']", False):
    #         fprint(self, "Data is Converted, verifying with the expected one...")
    #         self.verify_data("from_2dot0/" + stix_1dotx_filename)
    #     else:
    #         fprint(self, "[Failed] - Converted data is not visible.")
    #         self.fail("[Failed] - Converted data is not visible.")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
