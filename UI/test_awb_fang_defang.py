import unittest

from lib.ui.analyst_workbench import verify_data, click_to_process
from lib.ui.nav_threat_data import *

fang_data = "Automation@123.12__abb"
expected_fang_data_manual = "Automation(at)123[.]12__abb"
expected_defang_data_importFile = "IPV4 - 23[.]154[.]177[.]62, IPV6 - 807b:9334:64f7:f23b:cb9a:7877:2113:7282, Domain - hXXps://swisscpprivate2[.]com/, Email - mailcius(at)dizzydom2[.]com"
filename = "fang_defang_txt.txt"


class FangDefang(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.driver = initialize_browser(self)
        login(self, Admin_Email, Admin_Password)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def test_01_verify_fang_defang(self):
        fprint(self, "TC_ID: 4012551 - test_01_verify_fang_defang")
        nav_menu_main(self, "Fang - Defang")
        self.driver.find_element_by_xpath("(//textarea[@aria-placeholder='Type (or paste) data here'])[1]").click()
        self.driver.find_element_by_xpath("(//textarea[@aria-placeholder='Type (or paste) data here'])[1]").send_keys(fang_data)
        fprint(self, "Entered the Fang data - "+fang_data)
        click_to_process(self, module="Fang - Defang")
        if not waitfor(self, 5, By.XPATH, "//div[@empty='true']", False):
            fprint(self, "Data is Fanged, verifying with the expected one...")
            verify_data(self, exp_data=expected_fang_data_manual)
        else:
            fprint(self, "[Failed] - Defanged data is not visible.")

    def test_02_verify_fang_defang_by_importFile(self):
        fprint(self, "TC_ID: 4012552 - test_02_verify_fang_defang_by_importFile")
        nav_menu_main(self, "Fang - Defang")
        self.driver.find_element_by_xpath("(//span[@class='cyicon-more-vertical'])[1]").click()
        try:
            waitfor(self, 10, By.XPATH, "(//span[contains(text(),'Upload a File')])[2]")
            self.driver.find_element_by_xpath("(//span[contains(text(),'Upload a File')])[2]").click()
        except:
            self.driver.find_element_by_xpath("(//div[contains(text(),'Upload a File')])[2]").click()
        waitfor(self, 5, By.XPATH, "//input[@type = 'file']")
        upload = self.driver.find_element_by_xpath("(//input[@type = 'file'])[1]")
        file_path = os.path.join(os.environ["PYTHONPATH"], "testdata", "fang_defang/"+filename)
        fprint(self, "Uploading file... - "+filename)
        upload.send_keys(file_path)
        # Intentionally used sleep waiting for file to be completely uploaded
        sleep(10)
        click_to_process(self, module="Fang - Defang")
        if not waitfor(self, 5, By.XPATH, "//div[@empty='true']", False):
            fprint(self, "Data is Fanged, verifying with the expected one...")
            verify_data(self, exp_data=expected_defang_data_importFile)
        else:
            fprint(self, "[Failed] - Defanged data is not visible.")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
