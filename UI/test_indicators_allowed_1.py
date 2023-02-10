
import unittest


from lib.ui.nav_app import *
from lib.ui.nav_threat_data import verify_data_in_threatdata, click_on_intel
from lib.ui.quick_add import quick_create_ip
from lib.ui.nav_tableview import *



class IndicatorAllowed(unittest.TestCase):

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

    def quick_create_intel(self, name, ioc_type, ioc_value):
        fprint(self, "Waiting for the New Button...")
        self.driver.find_element_by_xpath("//button[contains(text(),'New')]").click()
        fprint(self, "Clicked on the New Button")
        waitfor(self, 5, By.XPATH, "//li/div[contains(text(),'Quick Add Intel')]")
        self.driver.find_element_by_xpath("//li/div[contains(text(),'Quick Add Intel')]").click()
        fprint(self, "Clicked on the 'Quick Add Intel' option")
        waitfor(self, 5, By.XPATH, qai_ioc_type_search)
        sleep(5)
        fprint(self, "Searching - " + ioc_type)
        waitfor(self, 5, By.XPATH, "//input[@name='searchbar']")
        self.driver.find_element_by_xpath("//input[@name='searchbar']").click()
        clear_field(self.driver.find_element_by_xpath("//input[@name='searchbar']"))
        self.driver.find_element_by_xpath("//input[@name='searchbar']").send_keys(ioc_type)
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'" + ioc_type + "')]/ancestor::div[1]")
        self.driver.find_element_by_xpath("//div[contains(text(),'" + ioc_type + "')]/div[1]/div").click()
        clear_field(self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']"))
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys(name)
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Value(s)']").send_keys(ioc_value)
        fprint(self, "Clicking on Create Intel for data created")
        waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Create Intel')]")
        sleep(2)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Create Intel')]").click()
        if Build_Version.__contains__("3."):
            verify_success(self, "You can view the created intel as a report object in the Threat Data module")
        else:
            verify_success(self, "You will be notified once the STIX package is created", 15)
        fprint(self, "[Passed] Request for Create Intel sent successfully")
        fprint(self, "Waiting for intel to be with Created Status")
        repeat = 1
        while repeat <= 6:
            if waitfor(self, 10, By.XPATH,
                       "//span[contains(text(),'" + name + "')]/ancestor::td/following-sibling::td[3]//span[contains(text(),'Created')]",
                       False):
                fprint(self, "[Passed] Created Status of intel is visible - " + name)
                self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
                break
            else:
                fprint(self, "Created Status of intel is not visible, Clicking on the Refresh Button")
                sleep(20)
                self.driver.find_element_by_xpath("//button[contains(text(),'Refresh')]").click()
                fprint(self, "Clicked on the Refresh Button")
                if repeat == 6:
                    fprint(self, "going to quick add history")
                    self.driver.find_element_by_xpath("//span[contains(text(),'Quick Add History')]").click()
                    fprint(self, "[Failed] Intel is not found with Created Status")
                repeat = repeat + 1
                sleep(30)
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_01_ADD_Indicator_IPV4_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 10091 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath("//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  #//input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the  IPV4 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Address (IPv4)").click()
        else:
            self.driver.find_element_by_xpath("//div[contains(text(),'Ipv4')]").click()
        fprint(self, "Verifying the IPV4 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys('12.12.12.43')# //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_6')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_02_ADD_Indicator_IPV6_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 10092 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath("//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  #//input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the IPv6 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Address (IPv6)").click()
        else:
            self.driver.find_element_by_xpath("//div[contains(text(),'Ipv6')]").click()
        fprint(self, "Verifying the IPV6 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys('e5b2:b240:5121:710a:1f2c:51c7:0964:58fb')# //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_7')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_03_ADD_Indicator_ASN_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 10093 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the ASN is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" // div[contains(text(), 'ASN Number')]").click()
        else:
            self.driver.find_element_by_xpath("//div[contains(text(),'ASN')]").click()
        fprint(self, "Verifying the ASN address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'AS122')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_8')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_04_ADD_Indicator_Email_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 10094 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the Email is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Email Address')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'E-mail')]").click()
        fprint(self, "Verifying the Email address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'abc@gmail.com')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_9')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_05_ADD_Indicator_MD5_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 10095 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the MD5 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Hash (MD5')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'MD5')]").click()
        fprint(self, "Verifying the MD5 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            '9a5fa5c5f3915b2297a1c379be9979f0')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_10')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_06_ADD_Indicator_SHA1_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 10096 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the SHA1 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Hash (SHA1)')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'SHA1')]").click()
        fprint(self, "Verifying the SHA1 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'ef6adfb8326f6942360631f882e144293ff8e893')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_11')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_07_ADD_Indicator_SHA256_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 10097 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the SHA256 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Hash (SHA256)')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'SHA256')]").click()
        fprint(self, "Verifying the SHA256 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'e58ec15691a649185ae4c84650e90a4432b7c5a2b171350781222f6aa0a96309')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_12')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_08_ADD_Indicator_SHA224_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 10098 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the SHA224 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Hash (SHA224)')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'SHA224')]").click()
        fprint(self, "Verifying the SHA224 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'ED5E2B4B33AD1CDB1C6E0783E3BE83ADFC81522DB59D9FC028650476')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_13')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_09_ADD_Indicator_SHA384_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 10099 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the SHA384 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Hash (SHA384)')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'SHA384')]").click()
        fprint(self, "Verifying the SHA384 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'd509ef5002c939d41666ceb5116b4d4fa787a5ab5e9574ab3bb157e0c7583d6cb4d04e249e86ec62eb5ce4bfad2d1c9b')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_14')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_10_ADD_Indicator_SHA512_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 100910 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the SHA512 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Hash (SHA512)')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'SHA512')]").click()
        fprint(self, "Verifying the SHA512 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'e909fcc01220bc7ebd328e616e3b4d75e5a58508b63f0b7d7d4a797b020a486a1edc257ae982c08d1b1404a1bb36378a3cffd541c511dda89a85df3fdaf2c465')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_15')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_11_ADD_Indicator_SSDEEP_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 100911 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the SSDEEP is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Hash (SSDEEP)')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'SSDEEP')]").click()
        fprint(self, "Verifying the SSDEEP address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            '1536:Z1QbFJL5JcH5tSHWDUITshqd4XQNX27H1z:QFJl9OU35')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_16')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_12_ADD_Indicator_URL_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 100912 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the URL is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'URL')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'URL')]").click()
        fprint(self, "Verifying the URL address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'https://pypi.org/project/ssdeep/')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_17')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_13_ADD_Indicator_Domain_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 100913 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the Domain is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Domain')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'Domain')]").click()
        fprint(self, "Verifying the Domain address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'test_ind_allowed.com')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_18')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_14_ADD_Indicator_CIDR_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 100914 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the CIDR is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'CIDR')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'CIDR')]").click()
        fprint(self, "Verifying the CIDR address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            '12.13.14.35/24')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_19')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_15_ADD_Indicator_Mutex_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 100915 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the Mutex is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Mutex Name')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'Mutex')]").click()
        fprint(self, "Verifying the Mutex address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'somemutex3')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_20')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_16_ADD_Indicator_User_Agents_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 100916 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the User_Agents is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'User Agent name')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'User Agents')]").click()
        fprint(self, "Verifying the User Agent address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'useragent_1')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_21')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_17_ADD_Indicator_Registry_Key_to_Allowed_indicator(self):
        fprint(self, "TC_ID: 100917 - Verify_Indicators Allowed")
        nav_menu_main(self, "Indicators Allowed")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the Registry_Key is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Win Registry Key')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'Registry Key')]").click()
        fprint(self, "Verifying the Registry_Key address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\erroneous3')
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_22')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")

    def test_18_Create_indicator_using_quick_add(self):
        fprint(self, "TC_ID: 100918 - Verify_Indicators Allowed")
        self.driver.refresh()
        sleep(5)
        quick_create_ip(self, "12.12.12.43", "saubhagya_6")
        fprint(self, "Clicking on New")
        waitfor(self, 20, By.XPATH, "//button[text()=' New']")
        self.driver.find_element_by_xpath("//button[text()=' New']").click()
        fprint(self, "Selecting Quick Add Intel from the dropdown menu")
        waitfor(self, 20, By.XPATH, "//li/*[contains(text(), 'Quick Add Intel')]")
        sleep(2)
        self.driver.find_element_by_xpath("//li/*[contains(text(), 'Quick Add Intel')]").click()
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'Quick Add History')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Quick Add History')]").click()
        if Build_Version.__contains__("3."):
            waitfor(self, 10, By.XPATH, "(//span[contains(text(),'saubhagya_6')]/ancestor::td/following-sibling::td[3]//span[contains(text(),'Created')])[1]")
            fprint(self, "[Passed] The Indicator is being created in the case of CTIX Version 3")
        else:
            waitfor(self, 10, By.XPATH, "(//span[contains(text(),'saubhagya_6')]/ancestor::td/following-sibling::td[3]//span[contains(text(),'Failed')])[1]")
            fprint(self, "[Passed] The indicator is not added in the case of the CTIX version 2.x, if it is added to the allowed indicator")

    def test_19_v3_verify_threatdata_state_added_to_allowed_indicator(self):
        fprint(self, "TC_ID: 100919 - Verify_Indicators Allowed")
        self.driver.refresh()
        sleep(5)
        nav_menu_main(self, 'Threat Data')
        fprint(self, "send the value of Ip value to be searched in the test case")
        self.driver.find_element_by_xpath("(//input[contains(@placeholder,'Search')])[4]").send_keys('12.12.12.43')
        fprint(self, "clicking on the search button")
        sleep(4)
        fprint(self, "Clicking on the indicator that needs to be searched")
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'12.12.12.43')])[1]")
        ele = self.driver.find_element_by_xpath("(//span[contains(text(),'12.12.12.43')])[1]")
        action=ActionChains(self.driver).move_to_element(ele)
        action.click()
        action.perform()
        fprint(self, "Checking for the overview page is being loaded or not")
        waitfor(self, 10, By.XPATH ,"//div[normalize-space()='Overview']")
        fprint(self,"clicking on the Indicators allowed in Quick Actions")
        self.driver.find_element_by_xpath("//span[normalize-space()='Indicator Allowed']").click()
        fprint(self,"Verifying that allowed indicator is being Clicked")
        fprint(self, "checking if the text is Remove from the allowed indicators")
        sleep(10)
        waitfor(self,10, By.XPATH, "//span[normalize-space()='Remove from Indicator Allowed']")
        fprint(self, "[Passed], It is giving the right result which is expected")

    def test_20_remove_from_allowed_indicator(self):
        fprint(self, "TC_ID: 100920 - Verify_Indicators Allowed")
        self.driver.refresh()
        sleep(5)
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that search bar is being used or not")
        self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys("12.12.12.43")
        self.driver.find_element_by_xpath("//*[@data-testid='filter-search-icon']").click()
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'12.12.12.43')])[1]")
        click_on_actions_item(self, '12.12.12.43', 'Remove')
        sleep(10)
        self.driver.find_element_by_xpath("//button[normalize-space()='Yes, Remove']").click()
        verify_success(self, "deleted successfully")

    def test_21_Verify_unfollow_working_fine(self):
        fprint(self, "TC_ID: 100921 - Verify Unfollow Functionality")
        self.driver.refresh()
        sleep(5)
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()
        fprint(self, "Verifying that the  IPV4 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Address (IPv4)").click()
        else:
            self.driver.find_element_by_xpath("//div[contains(text(),'Ipv4')]").click()
        fprint(self, "Verifying the IPV4 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            '12.22.22.41')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Unfollow_functionality')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        self.driver.refresh()
        sleep(10)
        fprint(self, "Verifying that search bar is being used or not")
        self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys("12.22.22.41")
        self.driver.find_element_by_xpath("//*[@data-testid='filter-search-icon']").click()
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'12.22.22.41')])[1]")
        click_on_actions_item(self, '12.22.22.41', 'Unfollow')
        verify_success(self, "Indicator details updated successfully")
        fprint(self, '[Passed]-Indicators Unfollowed succesfully')

    def test_22_Verify_Follow_Working_Fine(self):
        fprint(self, "TC_ID: 100922 - Verify follow Functionality")
        self.driver.refresh()
        sleep(5)
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that search bar is being used or not")
        self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys("12.22.22.41")
        self.driver.find_element_by_xpath("//*[@data-testid='filter-search-icon']").click()
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'12.22.22.41')])[1]")
        click_on_actions_item(self, '12.22.22.41', 'Follow')
        verify_success(self, "Indicator details updated successfully")
        fprint(self, '[Passed]-Indicators followed succesfully')

    def test_23_Verify_if_Added_Through_Threat_Data(self):
        fprint(self, "TC_ID: 100923 - Verify_Indicators Allowed")
        self.driver.refresh()
        sleep(5)
        quick_create_ip(self, "13.13.13.12", "Test_threat")
        verify_data_in_threatdata(self, "13.13.13.12", "Import")
        # sleep(20)
        fprint(self, "send the value of Ip value to be searched in the test case")
        # self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys('13.13.13.12')
        # fprint(self, "clicking on the search button")
        # sleep(4)
        # fprint(self, "Clicking on the indicator that needs to be searched")
        click_on_intel(self, "Import", "13.13.13.12")
        # waitfor(self, 10, By.XPATH, "(//span[contains(text(),'13.13.13.12')])[1]")
        # ele = self.driver.find_element_by_xpath("(//span[contains(text(),'13.13.13.12')])[1]")
        # action = ActionChains(self.driver).move_to_element(ele)
        # action.click()
        # action.perform()
        fprint(self, "Checking for the overview page is being loaded or not")
        waitfor(self, 10, By.XPATH, "//div[normalize-space()='Overview']")
        fprint(self, "clicking on the Indicators allowed in Quick Actions")
        self.driver.find_element_by_xpath("//span[normalize-space()='Indicator Allowed']").click()
        fprint(self, "Verifying that allowed indicator is being Clicked")
        fprint(self, "Clicking On Add To allowed Indicators")
        waitfor(self, 10, By.XPATH, "//span[normalize-space()='Add to Indicator Allowed']")
        self.driver.find_element_by_xpath("//span[normalize-space()='Add to Indicator Allowed']").click()
        fprint(self, "clicked on add to allowed Indicator")
        waitfor(self, 10, By.XPATH, "//textarea[ @placeholder='Enter Reason']")
        self.driver.find_element_by_xpath("//textarea[ @placeholder='Enter Reason']").send_keys("testing")
        fprint(self, "Enter the reason in add to allowed indicators")
        self.driver.find_element_by_xpath("(//span[ @class='cy-text-f12'])[2]").click()
        fprint(self, "Clicked on the save Button")
        verify_success(self, "Objects added to Indicators Allowed successfully")
        self.driver.refresh()
        sleep(5)
        fprint(self, "clicking on the Indicators allowed in Quick Actions")
        self.driver.find_element_by_xpath("//span[normalize-space()='Indicator Allowed']").click()
        fprint(self, "Verifying that allowed indicator is being Clicked")
        fprint(self, "checking if the text is Remove from the allowed indicators")
        sleep(10)
        waitfor(self, 10, By.XPATH, "//span[normalize-space()='Remove from Indicator Allowed']")
        fprint(self, "[Passed], It is giving the right result which is expected")
        nav_menu_main(self, "Indicators Allowed")
        self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys("13.13.13.12")
        self.driver.find_element_by_xpath("//*[@data-testid='filter-search-icon']").click()
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'13.13.13.12')])[1]")
        fprint(self, "Passed - Indicator is present in the indicators allowed.")

    def test_24_Verify_Intel_Cannot_Added_Wrong_Value(self):
        fprint(self, "TC_ID: 100924 - Verify that Intel cannot be added by providing the wrong value")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()
        fprint(self, "Verifying that the  IPV4 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Address (IPv4)").click()
        else:
            self.driver.find_element_by_xpath("//div[contains(text(),'Ipv4')]").click()
        fprint(self, "Verifying the IPV4 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            '12.33.44.44.')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Testing')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "The Indicator Type and Values do not match. Please enter valid Indicators.")
        fprint(self, "Passed - Indicator Cannot be added if we provide the wrong value")

    def test_25_Verify_Created_Include_URl(self):
        fprint(self, "TC_ID: 100925 - Verify that the URL should be added to indicators allowed")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()
        fprint(self, "Verifying that the  IPV4 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Address (IPv4)").click()
        else:
            self.driver.find_element_by_xpath("//div[contains(text(),'Ipv4')]").click()
        fprint(self, "Verifying the IPV4 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys('21.44.111.88')
        self.driver.find_element_by_xpath("//span[@class='cy-switch-input-wrapper sm secondary in-active']").click()
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Testing')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "added successfully")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        sleep(10)
        self.quick_create_intel('Include_URL', 'URL', 'http://21.44.111.88/user')
        nav_menu_main(self, 'Threat Data')
        fprint(self, "send the value of Ip value to be searched in the test case")
        self.driver.find_element_by_xpath("(//input[contains(@placeholder,'Search')])[4]").send_keys('http://21.44.111.88/user')
        fprint(self, "clicking on the search button")
        sleep(4)
        fprint(self, "Clicking on the indicator that needs to be searched")
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'http://21.44.111.88/user')])[1]")
        ele = self.driver.find_element_by_xpath("(//span[contains(text(),'http://21.44.111.88/user')])[1]")
        action = ActionChains(self.driver).move_to_element(ele)
        action.click()
        action.perform()
        fprint(self, "Checking for the overview page is being loaded or not")
        waitfor(self, 10, By.XPATH, "//div[normalize-space()='Overview']")
        fprint(self, "clicking on the Indicators allowed in Quick Actions")
        self.driver.find_element_by_xpath("//span[normalize-space()='Indicator Allowed']").click()
        fprint(self, "Verifying that allowed indicator is being Clicked")
        fprint(self, "checking if the text is Remove from the allowed indicators")
        sleep(10)
        waitfor(self, 10, By.XPATH, "//span[normalize-space()='Remove from Indicator Allowed']")
        fprint(self, "[Passed], It is giving the right result which is expected")

    def test_26_Verify_Wrong_Ipv4_Cannot_Be_Added(self):
        """
        Test case to verify the wrong value of ipv4 cannot be added
        """
        fprint(self, "TC_ID: 100926 - Verify that wrong value of ipv4 cannot be added")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()
        fprint(self, "Verifying that the  IPV4 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Address (IPv4)").click()
        else:
            self.driver.find_element_by_xpath("//div[contains(text(),'Ipv4')]").click()
        fprint(self, "Verifying the IPV4 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            '12.3.4.5.')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Testing_Wrong_value')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "The Indicator Type and Values do not match. Please enter valid Indicators.")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_27_Verify_Wrong_Ipv6_Cannot_Be_Added(self):
        """
        Test case to verify the wrong value of ipv4 cannot be added
        """
        fprint(self, "TC_ID: 100927 - Verify that wrong value of ipv6 cannot be added")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()
        fprint(self, "Verifying that the IPv6 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Address (IPv6)").click()
        else:
            self.driver.find_element_by_xpath("//div[contains(text(),'Ipv6')]").click()
        fprint(self, "Verifying the IPV6 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'e5b2:b240:5121:710a:1f2c:51c7:58fb::')
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Testing_wrong_value')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "The Indicator Type and Values do not match. Please enter valid Indicators.")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_28_Verify_Wrong_ASN_Cannot_Be_Added(self):
        """
        test case to verify that the wrong value of ASn cannot be added
        """
        fprint(self, "TC_ID: 100928 - Verify that wrong value of ASN cannot be added")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()
        fprint(self, "Verifying that the ASN is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" // div[contains(text(), 'ASN Number')]").click()
        else:
            self.driver.find_element_by_xpath("//div[contains(text(),'ASN')]").click()
        fprint(self, "Verifying the ASN address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'Test')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Test_wrong_value')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "The Indicator Type and Values do not match. Please enter valid Indicators.")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_29_Verify_Wrong_email_Cannot_Be_Added(self):
        """
        test case to verify that the wrong email cannot be added
        """
        fprint(self, "TC_ID: 100929 -test case to verify that the wrong email cannot be added ")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the Email is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Email Address')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'E-mail')]").click()
        fprint(self, "Verifying the Email address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'abcgmail.com')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Test Wrong value')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "The Indicator Type and Values do not match. Please enter valid Indicators.")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_30_Verify_Wrong_MD5_Cannot_Be_Added(self):
        """
        Test case to verify that the wrong md5 cannot be added
        """
        fprint(self, "TC_ID: 100930 -Test case to verify that the wrong md5 cannot be added")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the MD5 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Hash (MD5')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'MD5')]").click()
        fprint(self, "Verifying the MD5 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            '9a5fa5c5f3915b2297a1c379be997dx,kmxc9f0')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Test Wrong value')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "The Indicator Type and Values do not match. Please enter valid Indicators.")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_31_Verify_Wrong_SHA1_Cannot_Be_Added(self):
        """
        test case to verify that the wrong value of the sha1 cannot be added
        """
        fprint(self, "TC_ID: 100931 - Test case to verify that the wrong value of the Sha 1 cannot be added ")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the SHA1 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Hash (SHA1)')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'SHA1')]").click()
        fprint(self, "Verifying the SHA1 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'ef6adfb8326f6942360631f882e144.,,293ff8e893')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Test_wrong_value')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "The Indicator Type and Values do not match. Please enter valid Indicators.")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_32_Verify_Wrong_sha256_Cannot_be_added(self):
        """
        Test Case to verify that the wrong value of the sha 256 cannot be added
        """
        fprint(self, "TC_ID: 100932 - Test Case to verify that the wrong value of the sha 256 cannot be added")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the SHA256 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Hash (SHA256)')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'SHA256')]").click()
        fprint(self, "Verifying the SHA256 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'e58ec15691a649185ae4c84650e90a4432b7c5a2b171350781222f6lfllf,,,,aa0a96309')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_12')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "The Indicator Type and Values do not match. Please enter valid Indicators.")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_33_Verify_Wrong_Sha224_Cannot_Be_Added(self):
        """
        Test case to verify that the wrong value of sha 224 cannot be added
        """
        fprint(self, "TC_ID: 100933 - Test case to verify that the wrong value of sha 224 cannot be added ")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the SHA224 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Hash (SHA224)')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'SHA224')]").click()
        fprint(self, "Verifying the SHA224 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'ED5E2B4B33AD1CDB1C6E0783E3BE83ADFC81522DB59D9F,.kl.,C028650476')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Saubhagya_13')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "The Indicator Type and Values do not match. Please enter valid Indicators.")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_34_Verify_Wrong_sha384_Cannot_Be_Added(self):
        """
        Test case to verify the wrong value of the sha384 cannot be added
        """
        fprint(self, "TC_ID: 100934 - Test case to verify the wrong value of the sha384 cannot be added ")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()
        fprint(self, "Verifying that the SHA384 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Hash (SHA384)')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'SHA384')]").click()
        fprint(self, "Verifying the SHA384 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'd509ef5002c939d41666ceb5116b4d4fa787a5ab5e9574ab3bb157e0c7583d6cb4d04,,.e249e86ec62eb5ce4bfad2d1c9b')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Test wrong value ')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "The Indicator Type and Values do not match. Please enter valid Indicators.")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_35_Verify_Wrong_Sha512_Cannot_Be_Added(self):
        """
        Test case to verify that the wrong value of the sha512 cannot be added
        """
        fprint(self, "TC_ID: 100935 - Test case to verify that the wrong value of the sha512 cannot be added ")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the SHA512 is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Hash (SHA512)')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'SHA512')]").click()
        fprint(self, "Verifying the SHA512 address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'e909fcc01220bc7ebd328e616e3b4d75e5a58508b63f0b7d7d4a797b020a486a1edc257ae,,.982c08d1b1404a1bb36378a3cffd541c511dda89a85df3fdaf2c465')
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Test wrong value')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "The Indicator Type and Values do not match. Please enter valid Indicators.")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_36_Verify_Wrong_SSDEEP_Cannot_Be_Added(self):
        """
        Test Case to verify that the Wrong value of ssdeep cannot be added
        """
        fprint(self, "TC_ID: 100936 - Verify that the wrong ssdeep cannot be added ")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the SSDEEP is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'Hash (SSDEEP)')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'SSDEEP')]").click()
        fprint(self, "Verifying the SSDEEP address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'dev.com')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Test wrong value ')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "The Indicator Type and Values do not match. Please enter valid Indicators.")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_37_Verify_Wrong_URL_Cannot_Be_Added(self):
        """
        Test case to verify that the wrong value of the url cannot be added
        """
        fprint(self, "TC_ID: 100937 - Test case to verify that the wrong value of the url cannot be added")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()
        fprint(self, "Verifying that the URL is clickable or not ")
        if Build_Version.__contains__("2."):
            self.driver.find_element_by_xpath(" //div[contains(text(),'URL')]").click()
        else:
            self.driver.find_element_by_xpath("// div[contains(text(),'URL')]").click()
        fprint(self, "Verifying the URL address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys("https:?\pypi.org\project\ssdeep")  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Test Wrong value')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "The Indicator Type and Values do not match. Please enter valid Indicators.")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_38_Verify_Wrong_Domain_Cannot_Be_Added(self):
        """
        Test case to verify that the wrong value of the domain cannot be added
        """
        fprint(self, "TC_ID: 100938 - Test case to verify that the wrong value of the domain cannot be added")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the Domain is clickable or not ")
        self.driver.find_element_by_xpath("// div[contains(text(),'Domain')]").click()
        fprint(self, "Verifying the Domain address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            'test_ind_allowed?.?com')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Test wrong value')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "The Indicator Type and Values do not match. Please enter valid Indicators.")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_39_Verify_Wrong_CIDR_Cannot_Be_Added(self):
        """
        Test case to verify that the wrong CIDR range cannot be added
        """
        fprint(self, "TC_ID: 100939 - Test case to verify that the wrong value of the CIDR cannot be added")
        nav_menu_main(self, "Indicators Allowed")
        fprint(self, "Verifying that the Add Indicator button is clickable or not ")
        waitfor(self, 15, By.XPATH, "//button[normalize-space()='Add to Allowed Indicators']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add to Allowed Indicators']").click()
        waitfor(self, 15, By.XPATH, "//div[contains(text(),'Add to Allowed Indicators')]")
        fprint(self, "Verifying the drop down menu is clickable or not ")
        self.driver.find_element_by_xpath(
            "//span[normalize-space()='Select Type *']/ancestor::div[@tabindex]").click()  # //input[@placeholder='Search ...']   //span[@class='cyicon-chevron-down ']
        fprint(self, "Verifying that the CIDR is clickable or not ")
        self.driver.find_element_by_xpath("// div[contains(text(),'CIDR')]").click()
        fprint(self, "Verifying the CIDR address is added")
        self.driver.find_element_by_xpath("//textarea[contains(@aria-placeholder, 'Indicator')]").send_keys(
            '12.13.14.35/34')  # //input
        fprint(self, "Verifying the reason is added")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Reason']").send_keys('Testing Wrong value')
        fprint(self, "verifying that ADD button is clickable or not")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        verify_success(self, "The Indicator Type and Values do not match. Please enter valid Indicators.")
        fprint(self, "Closing the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
