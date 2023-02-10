import unittest
from lib.ui.nav_app import *
from lib.ui.nav_threat_data import verify_data_in_threatdata


class ImportIntel(unittest.TestCase):

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

    def navigate_to_import_intel(self):
        waitfor(self, 5, By.XPATH, '//button[contains(text(), "New")]')
        fprint(self, 'Clicked on "+ New" button')
        self.driver.find_element_by_xpath('//button[contains(text(), "New")]').click()

        waitfor(self, 5, By.XPATH, '//li/div[contains(text(), "Import Intel")]')
        fprint(self, 'Clicked on Import Intel')
        self.driver.find_element_by_xpath('//li/div[contains(text(), "Import Intel")]').click()

        waitfor(self, 5, By.XPATH, '//div[contains(text(), "Intel History")]')
        fprint(self, "[Passed] Import Intel Page is loaded successfully")

    def select_format(self, format_name):
        self.navigate_to_import_intel()
        waitfor(self, 5, By.XPATH, '(//div[@data-testaction="close"])[1]')
        fprint(self, "Clicking on file format dropdown")
        self.driver.find_element_by_xpath('(//div[@data-testaction="close"])[1]').click()

        waitfor(self, 5, By.XPATH, f'(//div[contains(text(), "{format_name}")])[1]')
        fprint(self, f"Clicked on {format_name} format")
        self.driver.find_element_by_xpath(f'(//div[contains(text(), "{format_name}")])[1]').click()

    def select_collection(self, collection_name):
        waitfor(self, 5, By.XPATH, '(//div[@data-testaction="close"])[2]')
        fprint(self, "Clicking on file collection dropdown")
        self.driver.find_element_by_xpath('(//div[@data-testaction="close"])[2]').click()

        waitfor(self, 5, By.XPATH, '(//input[@name="search-input"])[2]')
        self.driver.find_element_by_xpath('(//input[@name="search-input"])[2]').send_keys(collection_name)

        waitfor(self, 5, By.XPATH, f'(//div[contains(text(), "{collection_name}")])[1]')
        fprint(self, f"Clicked on the collection {collection_name}")
        self.driver.find_element_by_xpath(f'(//div[contains(text(), "{collection_name}")])[1]').click()

    def import_file(self, file_name):
        waitfor(self, 5, By.XPATH, "//input[@type = 'file']")
        upload = self.driver.find_element_by_xpath("//input[@type = 'file']")
        file_path = os.path.join(os.environ["PYTHONPATH"], "testdata", f"import_intel/{file_name}")
        fprint(self, f"Uploaded {file_name}")
        upload.send_keys(file_path)
        # Intentionally used sleep waiting for file to be completely uploaded
        sleep(10)

        waitfor(self, 5, By.XPATH, '//button[contains(text(), "Import")]')
        fprint(self, "Clicked on import button")
        self.driver.find_element_by_xpath('//button[contains(text(), "Import")]').click()
        verify_success(self, 'File imported successfully')

    def verify_status_intel_history(self, title):
        self.navigate_to_import_intel()
        for i in range(1, 6):
            waitfor(self, 5, By.XPATH, '//button[contains(text(), "Refresh")]')
            self.driver.find_element_by_xpath('//button[contains(text(), "Refresh")]').click()
            sleep(8)
            if waitfor(self, 5, By.XPATH,f"(//span[contains(text(),'{title}')]/ancestor::td/following-sibling::td[3]//span[contains(text(),'Created')])[1]",False):
                fprint(self, "[Passed] Status is visible as created")
                return
            elif waitfor(self, 5, By.XPATH,f"(//span[contains(text(),'{title}')]/ancestor::td/following-sibling::td[3]//span[contains(text(),'CREATED')])[1]",False):
                fprint(self, "[Passed] Status is visible as created")
                return
        fprint(self, "[Failed] Status is not visible as created, there must be some error occured")
        self.fail("[Failed] Status is not visible as created, there must be some error occured")

    def test_01_verify_page_loading(self):
        fprint(self, "\n------ TC_ID: 81001 Verifying that import Intel page is loading ------")
        self.navigate_to_import_intel()

    def test_02_verify_file_formats(self):
        fprint(self, "\n------ TC_ID: 81002 Verifying that All expected file formats are available in the dropdown ------")

        # Some more file formats might be added in next build
        expected_formats = {'STIX 1.x', 'STIX 2.0', 'STIX 2.1', 'STIX 1.x URL', 'MISP', 'MAEC 4.1', 'CSV (Recorded Future)', 'Open IOC', 'FREE TEXT', 'PDF'}
        visible_formats  = set()

        self.navigate_to_import_intel()
        waitfor(self, 5, By.XPATH, '(//div[@data-testaction="close"])[1]')
        fprint(self, "Clicking on file format dropdown")
        self.driver.find_element_by_xpath('(//div[@data-testaction="close"])[1]').click()

        for i in range(1, 11):
            waitfor(self, 5, By.XPATH, "//div[@name='text']")
            file_format = str(self.driver.find_element_by_xpath(f"(//div[@name='text'])[{i}]").text)
            print(file_format)
            visible_formats.add(file_format)

        fprint(self, "Verifying the visible formats with expected formats")
        for val in expected_formats:
            if val not in visible_formats:
                fprint(self, f"[Failed] , The format {val} is not available in the dropdown")
                break
        else:
            fprint(self, "[Passed] All expected formats are visible")

    def test_03_verify_source_collections(self):
        fprint(self, "\n------ TC_ID: 81003 Verifying that All expected source collections are available in the dropdown ------")
        # one bug is raised for collection's naming,  after that it will be implemented
        self.fail()

    def test_04_verify_alert_message(self):
        fprint(self, "\n------ TC_ID: 81004 Verifying the alert message for mandatory fields ------")

        self.navigate_to_import_intel()
        waitfor(self, 5, By.XPATH, '//button[contains(text(), "Import")]')
        fprint(self, "Clicking directly on import button so that alerts gets visible for the respective fields")
        self.driver.find_element_by_xpath('//button[contains(text(), "Import")]').click()

        waitfor(self, 5, By.XPATH, '//div[contains(text(), "Format is required")]')
        fprint(self, "[Passed] Alert present for the file format")

        waitfor(self, 5, By.XPATH, '//div[contains(text(), "Collection is required")]')
        fprint(self, "[Passed] Alert present for the collection")

        waitfor(self, 5, By.XPATH, '//div[contains(text(), "File is required")]')
        fprint(self, "[Passed] Alert present for the Upload File")

    def test_05_import_stix1_dot_x_file(self):
        fprint(self, "\n------ TC_ID: 81005 Verifying STIX 1.X files can be imported successfully ------")
        self.select_format('STIX 1.x')
        self.select_collection('Free Text')
        self.import_file('STIX-1.x.xml')

    def test_06_verify_stix1_dot_x_file_intel_history_status(self):
        fprint(self, "\n------ TC_ID: 81006 Verifying the status of STIX 1.X files in intel history ------")
        self.verify_status_intel_history('STIX-1.x.xml')

    def test_07_import_stix2_dot_0_file(self):
        fprint(self, "\n------ TC_ID: 81007 Verifying STIX 2.0 files can be imported successfully ------")
        self.select_format('STIX 2.0')
        self.select_collection('Free Text')
        self.import_file('STIX-2.0.json')

    def test_08_verify_stix2_dot_0_file_intel_history_status(self):
        fprint(self, "\n------ TC_ID: 81008 Verifying the status of STIX 2.0 files in intel history ------")
        self.verify_status_intel_history('STIX-2.0.json')

    def test_09_import_stix2_dot_1_file(self):
        fprint(self, "\n------ TC_ID: 81009 Verifying STIX 2.1 files can be imported successfully ------")
        self.select_format('STIX 2.1')
        self.select_collection('Free Text')
        self.import_file('STIX-2.1.json')

    def test_10_verify_stix2_dot_1_file_intel_history_status(self):
        fprint(self, "\n------ TC_ID: 81010 Verifying the status of STIX 2.1 files in intel history ------")
        self.verify_status_intel_history('STIX-2.1.json')

    def test_11_import_stix1_dot_x_URL(self):
        fprint(self, "\n------ TC_ID: 81011 Verifying STIX 1.X url can be imported successfully ------")
        self.select_format('STIX 1.x URL')
        self.select_collection('Free Text')
        waitfor(self, 5, By.XPATH, '//input[@aria-placeholder="Enter File Url *"]')
        self.driver.find_element_by_xpath('//input[@aria-placeholder="Enter File Url *"]').send_keys('https://stixproject.github.io/documentation/idioms/malicious-url/indicator-for-malicious-url.xml')
        waitfor(self, 5, By.XPATH, '//button[contains(text(), "Import")]')
        fprint(self, "Clicked on import button")
        self.driver.find_element_by_xpath('//button[contains(text(), "Import")]').click()
        verify_success(self, 'File imported successfully')

    def test_12_verify_stix1_dot_x_URL_intel_history_status(self):
        fprint(self, "\n------ TC_ID: 81012 Verifying the status of STIX 1.X URL in intel history ------")
        self.verify_status_intel_history('indicator-for-malicious-url.xml')

    def test_13_import_MISP_file(self):
        fprint(self, "\n------ TC_ID: 81013 Verifying MISP files can be imported successfully ------")
        self.select_format('MISP')
        self.select_collection('Free Text')
        self.import_file('MISP.json')

    def test_14_verify_MISP_file_intel_history_status(self):
        fprint(self, "\n------ TC_ID: 81014 Verifying the status of MISP files in intel history ------")
        self.verify_status_intel_history('MISP.json')

    def test_15_import_MAEC4_dot_1_file(self):
        fprint(self, "\n------ TC_ID: 81015 Verifying MAEC 4.1 files can be imported successfully ------")
        self.select_format('MAEC 4.1')
        self.select_collection('Free Text')
        self.import_file('MAEC-4.1.xml')

    def test_16_verify_MAEC4_dot_1_file_intel_history_status(self):
        fprint(self, "\n------ TC_ID: 81016 Verifying the status of MAEC 4.1 files in intel history ------")
        self.verify_status_intel_history('MAEC-4.1.xml')

    def test_17_import_CSV_RF_file(self):
        fprint(self, "\n------ TC_ID: 81017 Verifying CSV RF files can be imported successfully ------")
        self.select_format('CSV (Recorded Future)')
        self.select_collection('Free Text')
        self.import_file('CSV(Recorded Future).csv')

    def test_18_verify_CSV_RF_file_intel_history_status(self):
        fprint(self, "\n------ TC_ID: 81018 Verifying the status of CSV RF files in intel history ------")
        self.verify_status_intel_history('CSV(Recorded Future).csv')

    def test_19_import_Open_IOC_file(self):
        fprint(self, "\n------ TC_ID: 81019 Verifying Open IOC files can be imported successfully ------")
        self.select_format('Open IOC')
        self.select_collection('Free Text')
        self.import_file('OPEN IOC.xml')

    def test_20_verify_Open_IOC_file_intel_history_status(self):
        fprint(self, "\n------ TC_ID: 81020 Verifying the status of Open IOC files in intel history ------")
        self.verify_status_intel_history('OPEN IOC.xml')

    def test_21_import_Free_Text_file(self):
        fprint(self, "\n------ TC_ID: 81021 Verifying Free Text files can be imported successfully ------")
        self.select_format('FREE TEXT')
        self.select_collection('Free Text')
        self.import_file('Free Text.txt')

    def test_22_verify_Free_Text_file_intel_history_status(self):
        fprint(self, "\n------ TC_ID: 81022 Verifying the status of Free Text files in intel history ------")
        self.verify_status_intel_history('Free Text.txt')

    def test_23_import_PDF_file(self):
        fprint(self, "\n------ TC_ID: 81023 Verifying PDF files can be imported successfully ------")
        self.select_format('PDF')
        self.select_collection('Free Text')
        self.import_file('PDF.pdf')

    def test_24_verify_PDF_file_intel_history_status(self):
        fprint(self, "\n------ TC_ID: 81024 Verifying the status of PDF files in intel history ------")
        self.verify_status_intel_history('PDF.pdf')
        waitfor(self, 3, By.XPATH, '//span[@data-testaction="slider-close"]')
        self.driver.find_element_by_xpath('//span[@data-testaction="slider-close"]').click()

    def test_25_verify_stix1_dot_x_file_threat_data(self):
        fprint(self, "\n------ TC_ID: 81025 Verifying intel visibility in threat data ------")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'hsldne.com', 'Import')

    def test_26_verify_stix2_dot_0_file_threat_data(self):
        fprint(self, "\n------ TC_ID: 81026 Verifying intel visibility in threat data ------")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'xhs4z9arb backdoor', 'Import')
        verify_data_in_threatdata(self, 'http://xhs4z9arb.cn/5054/', 'Import')

    def test_27_verify_stix2_dot_1_file_threat_data(self):
        fprint(self, "\n------ TC_ID: 81027 Verifying intel visibility in threat data ------")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, '10.0.0.0', 'Import')

    def test_28_verify_stix1_dot_x_URL_threat_data(self):
        fprint(self, "\n------ TC_ID: 81028 Verifying intel visibility in threat data ------")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'http://x4z9arb.cn/4712', 'Import')

    def test_29_verify_MISP_file_threat_data(self):
        fprint(self, "\n------ TC_ID: 81029 Verifying intel visibility in threat data ------")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'https://researchcenter.paloaltonetworks.com/2017/11/unit42-new-malware-with-ties-to-sunorcal-discovered/', 'Import')
        verify_data_in_threatdata(self, 'HSCIRCL', 'Import')
        verify_data_in_threatdata(self, 'observed-data--5a0a9ade-3b60-4fbb-87d2-4628950d210f', 'Import')
        verify_data_in_threatdata(self, 'Testing MISP', 'Import')

    def test_30_verify_MAEC4_dot_1_file_threat_data(self):
        fprint(self, "\n------ TC_ID: 81030 Verifying intel visibility in threat data ------")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'Poison Ivy Variant v4392-acc', 'Import')

    def test_31_verify_CSV_RF_file_threat_data(self):
        fprint(self, "\n------ TC_ID: 81031 Verifying intel visibility in threat data ------")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, '176.10.99.200', 'Import')
        verify_data_in_threatdata(self, 'Historical Honeypot Sighting', 'Import')

    def test_32_verify_Open_IOC_file_threat_data(self):
        fprint(self, "\n------ TC_ID: 81032 Verifying intel visibility in threat data ------")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'HKEY_LOCAL_MACHINE\\\\SOFTWARE\\\\Microsoft\\\\Linux\\\\CurrentVersion\\\\Internet Settings\\\\Zones\\\\4', 'Import')
        verify_data_in_threatdata(self, 'cmi4432.sys', 'Import')

    def test_33_verify_Free_Text_file_threat_data(self):
        fprint(self, "\n------ TC_ID: 81033 Verifying intel visibility in threat data ------")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, '29.231.21.211', 'Import')

    def test_34_verify_PDF_file_threat_data(self):
        fprint(self, "\n------ TC_ID: 81034 Verifying intel visibility in threat data ------")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'hsmail@gmail.com', 'Import')
        verify_data_in_threatdata(self, 'h.s@gmail.com', 'Import')


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
