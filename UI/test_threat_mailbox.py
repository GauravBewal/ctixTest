import json
import unittest
from lib.ui.indicators_allowed import allowed_indi_search
from lib.ui.nav_app import *
from lib.ui.nav_threat_data import verify_data_in_threatdata, validate_all_metadata
from lib.ui.threat_mailbox import *
from pathlib import Path

class ThreatMailbox(unittest.TestCase):

    email_path = os.path.join(os.environ["PYTHONPATH"], "testdata", "threat_mailbox_data.json")
    email_data = json.loads(Path(email_path).read_text().replace("\n", ''))
    POP_TITLE = "POPTESTIN"
    POP_USERNAME = "poptestin@gmail.com"
    POP_PASSWORD = "mphmupnithemmjpo"
    POP_DOMAIN = "pop.gmail.com"
    IMAP_TITLE = "AUTOMATESTIN"
    IMAP_USERNAME = "jetraikar@gmail.com"   # Warning: Not to be used for manual testing at all
    IMAP_PASSWORD = "vmrhhnpijwgqnlel"     # Warning: Not to be used for manual testing at all
    IMAP_DOMAIN = "imap.gmail.com"

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

    def test_01_add_mail_source(self):
        """
            Adding POP 3 account to threat Mailbox
        """
        fprint(self, "\n----------- TC_ID 9501 : Adding an IMAP account to Threat Mailbox -----------")
        nav_menu_main(self, "Threat Mailbox")
        fprint(self, "Opened Threat Mailbox")
        if waitfor(self, 20, By.XPATH, "//div[@role='button']/span/button[text()]", False):
            self.driver.find_element_by_xpath("//div[@role='button']/span/button[text()]").click()
            sleep(2)
            if waitfor(self, 20, By.XPATH, "//div/*[contains(text(),'"+self.POP_TITLE+"')]", False):
                self.driver.find_element_by_xpath("//div/*[contains(text(),'"+self.POP_TITLE+"')]").click()
                sleep(1)
                self.driver.find_element_by_xpath("//div/span/button/i[@class='cyicon-more-vertical']").click()
                waitfor(self, 20, By.XPATH, "//li[contains(text(),'Remove Configuration')]")
                sleep(1)
                self.driver.find_element_by_xpath("//li[contains(text(),'Remove Configuration')]").click()
                fprint(self, "Clicked on remove Configuration")
                waitfor(self, 20, By.XPATH, "//button[@data-testalert='confirm-delete']")
                sleep(1)
                self.driver.find_element_by_xpath("//button[@data-testalert='confirm-delete']").click()
                verify_success(self, "Threat mail account deleted successfully")
                self.driver.find_element_by_xpath("//div[@role='button']/span/button[text()]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(),'Add New Account')]").click()
        add_email_source(self, title=self.POP_TITLE, username=self.POP_USERNAME, password=self.POP_PASSWORD,
                         domain=self.POP_DOMAIN, type="POP 3", auto_create=False)
        self.driver.refresh()
        fprint(self, "Verifying if mail account is added")
        waitfor(self, 20, By.XPATH, "//div[@role='button']/span/button[text()]")
        self.driver.find_element_by_xpath("//div[@role='button']/span/button[text()]").click()
        waitfor(self, 20, By.XPATH, "//div/*[contains(text(),'"+self.POP_TITLE+"')]")
        self.driver.find_element_by_xpath("//div/*[contains(text(),'"+self.POP_TITLE+"')]").click()
        fprint(self, "[PASSED] Mail account added successfully")
        process_console_logs(self)

    def test_02_refresh_mail(self):
        """
        Refreshing the page for new intel
        """
        fprint(self, "\n----------- TC_ID 9502: Refresh the page for mailbox intel -----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        self.driver.refresh()
        waitfor(self, 20, By.XPATH, "//div[@role='button']/span/button[text()]")
        self.driver.find_element_by_xpath("//div[@role='button']/span/button[text()]").click()
        waitfor(self, 20, By.XPATH, "//div/*[contains(text(),'"+self.POP_TITLE+"')]")
        self.driver.find_element_by_xpath("//div/*[contains(text(),'"+self.POP_TITLE+"')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(), 'Inbox')]//ancestor::a/span/i")
        self.driver.find_element_by_xpath("//span[contains(text(), 'Inbox')]//ancestor::a/span/i").click()
        fprint(self, "Clicking on refresh button")
        self.driver.find_element_by_xpath("//div[button[@type='button'][contains(text(), 'Refresh')]]"
                                          "[preceding-sibling::span]").click()
        fprint(self, "[PASSED] Refresh action performed successfully")
        self.driver.find_element_by_xpath("//span[contains(text(), 'Inbox')]//ancestor::a/span/i").click()
        process_console_logs(self)

    def test_03_edit_mail_source(self):
        """
        Editing mailbox source details
        """
        fprint(self, "\n----------- TC_ID 9503: Editing the added mail source -----------")
        nav_menu_main(self, "Threat Mailbox")
        self.driver.refresh()
        waitfor(self, 20, By.XPATH, "//div[@role='button']/span/button[text()]")
        self.driver.find_element_by_xpath("//div[@role='button']/span/button[text()]").click()
        waitfor(self, 20, By.XPATH, "//div/*[contains(text(),'"+self.POP_TITLE+"')]")
        self.driver.find_element_by_xpath("//div/*[contains(text(),'"+self.POP_TITLE+"')]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//div/span/button/i[@class='cyicon-more-vertical']").click()
        fprint(self, "Clicking on Edit Configuration for the mailbox")
        waitfor(self, 20, By.XPATH, "//li[contains(text(),'Edit Configuration')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Edit Configuration')]").click()
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Email Configuration')]")
        fprint(self, "Clearing and updating Client Name")
        client_name = self.driver.find_element_by_xpath("//input[@aria-placeholder='Client Name *']")
        client_name.click()
        clear_field(client_name)
        client_name.send_keys(self.POP_TITLE+"edited")
        fprint(self, "Filling in configuration password")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Password *']").click()
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Password *']").send_keys(self.POP_PASSWORD)
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        verify_success(self, "updated successfully")
        sleep(3)
        fprint(self, "[PASSED] Email Configuration updates saved")
        self.driver.refresh()
        waitfor(self, 20, By.XPATH, "//div[@role='button']/span/button[text()]")
        self.driver.find_element_by_xpath("//div[@role='button']/span/button[text()]").click()
        fprint(self, "Verifying the updated Configuration client name")
        waitfor(self, 20, By.XPATH, "//div/*[contains(text(),'"+self.POP_TITLE+"edited')]")
        self.driver.find_element_by_xpath("//div/*[contains(text(),'"+self.POP_TITLE+"edited')]").click()
        fprint(self, "[PASSED] Client name of configuration updated successfully")
        process_console_logs(self)

    def test_04_add_imap_account(self):
        """
        Adding IMAP account to Threat Mailbox
        """
        fprint(self, "\n----------- TC_ID 9504 : Adding an IMAP account to Threat Mailbox -----------")
        nav_menu_main(self, "Threat Mailbox")
        fprint(self, "Opened Threat Mailbox")
        if waitfor(self, 20, By.XPATH, "//div[@role='button']/span/button[text()]", False):
            self.driver.find_element_by_xpath("//div[@role='button']/span/button[text()]").click()
            sleep(2)
            if waitfor(self, 20, By.XPATH, "//div/*[contains(text(),'" + self.IMAP_TITLE + "')]", False):
                self.driver.find_element_by_xpath("//div/*[contains(text(),'" + self.IMAP_TITLE + "')]").click()
                sleep(1)
                self.driver.find_element_by_xpath("//div/span/button/i[@class='cyicon-more-vertical']").click()
                waitfor(self, 20, By.XPATH, "//li[contains(text(),'Remove Configuration')]")
                sleep(1)
                self.driver.find_element_by_xpath("//li[contains(text(),'Remove Configuration')]").click()
                fprint(self, "Clicked on remove Configuration")
                waitfor(self, 20, By.XPATH, "//button[@data-testalert='confirm-delete']")
                sleep(1)
                self.driver.find_element_by_xpath("//button[@data-testalert='confirm-delete']").click()
                verify_success(self, "Threat mail account deleted successfully")
                self.driver.find_element_by_xpath("//div[@role='button']/span/button[text()]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(),'Add New Account')]").click()
        add_email_source(self, title=self.IMAP_TITLE, username=self.IMAP_USERNAME, password=self.IMAP_PASSWORD,
                         domain=self.IMAP_DOMAIN, type="IMAP", auto_create=True)
        self.driver.refresh()
        fprint(self, "Verifying if mail account is added")
        waitfor(self, 20, By.XPATH, "//div[@role='button']/span/button[text()]")
        self.driver.find_element_by_xpath("//div[@role='button']/span/button[text()]").click()
        waitfor(self, 20, By.XPATH, "//div/*[contains(text(),'" + self.IMAP_TITLE + "')]")
        self.driver.find_element_by_xpath("//div/*[contains(text(),'" + self.IMAP_TITLE + "')]").click()
        fprint(self, "[PASSED] Mail account added successfully")
        process_console_logs(self)

    def test_05_parse_and_create_domain_imap_body(self):
        """
        TestCase to validate if all Domain Objects are parsed from the IMAP mail body and create Intel
        """
        fprint(self, "\n---------- TC_ID 9505: Parse and create Domain from POP mail body ----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_IOC_TYPES")
        parse_and_select(self, domain='IMAP', mail='imap_body', ioctype='Domains')
        create_selected_intel(self)
        process_console_logs(self)

    def test_06_parse_and_create_registry_imap_body(self):
        """
        TestCase to validate if all Domain Objects are parsed from the IMAP mail body and create Intel
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9506: Parse and create Registry Key from IMAP mail body ----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_IOC_TYPES")
        parse_and_select(self, domain='IMAP', mail='imap_body', ioctype='Registry Keys')
        create_selected_intel(self)
        process_console_logs(self)

    def test_07_parse_and_create_asn_imap_body(self):
        """
        TestCase to validate if all ASN Objects are parsed from the IMAP mail body and create Intel
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9507: Parse and create ASN from IMAP mail body ----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_IOC_TYPES")
        parse_and_select(self, domain='IMAP', mail='imap_body', ioctype='ASN')
        create_selected_intel(self)
        process_console_logs(self)

    def test_08_parse_and_create_url_imap_body(self):
        """
        TestCase to validate if all URL Objects are parsed from the IMAP mail body and create Intel
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9508: Parse and create URL from IMAP mail body ----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_IOC_TYPES")
        parse_and_select(self, domain='IMAP', mail='imap_body', ioctype='URLs')
        create_selected_intel(self)
        process_console_logs(self)

    def test_09_parse_and_create_sha256_imap_body(self):
        """
        TestCase to validate if all SHA256 Objects are parsed from the IMAP mail body and create Intel
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9509: Parse and create SHA256 from IMAP mail body ----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_IOC_TYPES")
        parse_and_select(self, domain='IMAP', mail='imap_body', ioctype='SHA256')
        create_selected_intel(self)
        process_console_logs(self)

    def test_10_parse_and_create_md5_imap_body(self):
        """
        TestCase to validate if all MD5 Objects are parsed from the IMAP mail body and create Intel
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9510: Parse and create MD5 from IMAP mail body ----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_IOC_TYPES")
        parse_and_select(self, domain='IMAP', mail='imap_body', ioctype='MD5')
        create_selected_intel(self)
        process_console_logs(self)

    def test_11_parse_and_create_email_imap_body(self):
        """
        TestCase to validate if all Email Objects are parsed from the IMAP mail body and create Intel
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9511: Parse and create Email from IMAP mail body ----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_IOC_TYPES")
        parse_and_select(self, domain='IMAP', mail='imap_body', ioctype='Emails')
        create_selected_intel(self)
        process_console_logs(self)

    def test_12_parse_and_create_sha1_imap_body(self):
        """
        TestCase to validate if all SHA1 Objects are parsed from the IMAP mail body and create Intel
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9512: Parse and create SHA1 from IMAP mail body ----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_IOC_TYPES")
        parse_and_select(self, domain='IMAP', mail='imap_body', ioctype='SHA1')
        create_selected_intel(self)
        process_console_logs(self)

    def test_13_parse_and_create_sha224_imap_body(self):
        """
        TestCase to validate if all SHA224 Objects are parsed from the IMAP mail body and create Intel
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9513: Parse and create SHA224 from IMAP mail body ----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_IOC_TYPES")
        parse_and_select(self, domain='IMAP', mail='imap_body', ioctype='SHA224')
        create_selected_intel(self)
        process_console_logs(self)

    def test_14_parse_and_create_sha384_imap_body(self):
        """
        TestCase to validate if all SHA384 Objects are parsed from the IMAP mail body and create Intel
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9514: Parse and create SHA384 from IMAP mail body ----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_IOC_TYPES")
        parse_and_select(self, domain='IMAP', mail='imap_body', ioctype='SHA384')
        create_selected_intel(self)
        process_console_logs(self)

    def test_15_parse_and_create_sha512_imap_body(self):
        """
        TestCase to validate if all SHA512 Objects are parsed from the IMAP mail body and create Intel
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9515: Parse and create SHA512 from IMAP mail body ----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_IOC_TYPES")
        parse_and_select(self, domain='IMAP', mail='imap_body', ioctype='SHA512')
        create_selected_intel(self)
        process_console_logs(self)

    def test_16_parse_and_create_ssdeep_imap_body(self):
        """
        TestCase to validate if all SSDeep Objects are parsed from the IMAP mail body and create Intel
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9516: Parse and create SSDeep from IMAP mail body ----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_IOC_TYPES")
        parse_and_select(self, domain='IMAP', mail='imap_body', ioctype='SSDeep')
        create_selected_intel(self)
        process_console_logs(self)

    def test_17_parse_and_create_cveid_imap_body(self):
        """
        TestCase to validate if all CVE ID Objects are parsed from the IMAP mail body and create Intel
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9517: Parse and create CVE ID from IMAP mail body ----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_IOC_TYPES")
        parse_and_select(self, domain='IMAP', mail='imap_body', ioctype='CVE ID')
        create_selected_intel(self)
        process_console_logs(self)

    def test_18_parse_and_create_ipv6_imap_body(self):
        """
        TestCase to validate if all ipv6 Objects are parsed from the IMAP mail body and create Intel
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9518: Parse and create IPv6 from IMAP mail body ----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_IOC_TYPES")
        parse_and_select(self, domain='IMAP', mail='imap_body', ioctype='IPv6')
        create_selected_intel(self)
        process_console_logs(self)

    def test_19_parse_and_create_ipv4_imap_body(self):
        """
        TestCase to validate if all ipv4 Objects are parsed from the IMAP mail body and create Intel
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9519: Parse and create IPv4 from IMAP mail body ----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_IOC_TYPES")
        add_metadata(self, confidence_score="0")
        parse_and_select(self, domain='IMAP', mail='imap_body', ioctype='IPv4')
        create_selected_intel(self)
        process_console_logs(self)

    def test_20_verify_domain_imap_body(self):
        """
        Testcase to validate Domain creation from IMAP account
        """
        fprint(self, "\n---------- TC_ID 9520: Verify domain creation from IMAP mail body ----------")
        nav_menu_main(self, 'Threat Data')
        for i in self.email_data["IMAP"]["imap_body"]["Domains"]:
            verify_data_in_threatdata(self, i, self.IMAP_TITLE)

    def test_21_verify_registry_key_imap_body(self):
        """
        Testcase to validate Registry Keys creation from IMAP account
        """
        fprint(self, "\n---------- TC_ID 9521: Verify Registry Key creation from IMAP mail body ----------")
        nav_menu_main(self, 'Threat Data')
        for i in self.email_data["IMAP"]["imap_body"]["Registry Keys"]:
            verify_data_in_threatdata(self, i, self.IMAP_TITLE)

    def test_22_verify_asn_imap_body(self):
        """
        Testcase to validate ASN creation from IMAP account
        """
        fprint(self, "\n---------- TC_ID 9522: Verify ASN creation from IMAP mail body ----------")
        nav_menu_main(self, 'Threat Data')
        for i in self.email_data["IMAP"]["imap_body"]["ASN"]:
            verify_data_in_threatdata(self, "AS"+i, self.IMAP_TITLE)

    def test_23_verify_url_imap_body(self):
        """
        Testcase to validate URL creation from IMAP account
        """
        fprint(self, "\n---------- TC_ID 9523: Verify URL creation from IMAP mail body ----------")
        nav_menu_main(self, 'Threat Data')
        for i in self.email_data["IMAP"]["imap_body"]["URLs"]:
            verify_data_in_threatdata(self, i, self.IMAP_TITLE)

    def test_24_verify_email_imap_body(self):
        """
        Testcase to validate Email creation from IMAP account
        """
        fprint(self, "\n---------- TC_ID 9524: Verify Email creation from IMAP mail body ----------")
        nav_menu_main(self, 'Threat Data')
        for i in self.email_data["IMAP"]["imap_body"]["Emails"]:
            verify_data_in_threatdata(self, i, self.IMAP_TITLE)

    def test_25_verify_sha512_imap_body(self):
        """
        Testcase to validate SHA512 creation from IMAP account
        """
        fprint(self, "\n---------- TC_ID 9525: Verify SHA512 creation from IMAP mail body ----------")
        nav_menu_main(self, 'Threat Data')
        for i in self.email_data["IMAP"]["imap_body"]["SHA512"]:
            verify_data_in_threatdata(self, i, self.IMAP_TITLE)

    def test_26_verify_sha256_imap_body(self):
        """
        Testcase to validate SHA256 creation from IMAP account
        """
        fprint(self, "\n---------- TC_ID 9526: Verify SHA256 creation from IMAP mail body ----------")
        nav_menu_main(self, 'Threat Data')
        for i in self.email_data["IMAP"]["imap_body"]["SHA256"]:
            verify_data_in_threatdata(self, i, self.IMAP_TITLE)

    def test_27_verify_sha1_imap_body(self):
        """
        Testcase to validate SHA1 creation from IMAP account
        """
        fprint(self, "\n---------- TC_ID 9527: Verify SHA1 creation from IMAP mail body ----------")
        nav_menu_main(self, 'Threat Data')
        for i in self.email_data["IMAP"]["imap_body"]["SHA1"]:
            verify_data_in_threatdata(self, i, self.IMAP_TITLE)

    def test_28_verify_md5_imap_body(self):
        """
        Testcase to validate MD5 creation from IMAP account
        """
        fprint(self, "\n---------- TC_ID 9528: Verify MD5 creation from IMAP mail body ----------")
        nav_menu_main(self, 'Threat Data')
        for i in self.email_data["IMAP"]["imap_body"]["MD5"]:
            verify_data_in_threatdata(self, i, self.IMAP_TITLE)

    def test_29_verify_sha224_imap_body(self):
        """
        Testcase to validate SHA224 creation from IMAP account
        """
        fprint(self, "\n---------- TC_ID 9529: Verify SHA224 creation from IMAP mail body ----------")
        nav_menu_main(self, 'Threat Data')
        for i in self.email_data["IMAP"]["imap_body"]["SHA224"]:
            verify_data_in_threatdata(self, i, self.IMAP_TITLE)

    def test_30_verify_sha384_imap_body(self):
        """
        Testcase to validate SHA384 creation from IMAP account
        """
        fprint(self, "\n---------- TC_ID 9530: Verify SHA384 creation from IMAP mail body ----------")
        nav_menu_main(self, 'Threat Data')
        for i in self.email_data["IMAP"]["imap_body"]["SHA384"]:
            verify_data_in_threatdata(self, i, self.IMAP_TITLE)

    def test_31_verify_ssdeep_imap_body(self):
        """
        Testcase to validate SSDeep creation from IMAP account
        """
        fprint(self, "\n---------- TC_ID 9531: Verify SSDeep creation from IMAP mail body ----------")
        nav_menu_main(self, 'Threat Data')
        for i in self.email_data["IMAP"]["imap_body"]["SSDeep"]:
            verify_data_in_threatdata(self, i, self.IMAP_TITLE)

    def test_32_verify_cveid_imap_body(self):
        """
        Testcase to validate CVE ID creation from IMAP account
        """
        fprint(self, "\n---------- TC_ID 9532: Verify CVE-ID creation from IMAP mail body ----------")
        nav_menu_main(self, 'Threat Data')
        for i in self.email_data["IMAP"]["imap_body"]["CVE ID"]:
            verify_data_in_threatdata(self, i, self.IMAP_TITLE)

    def test_33_verify_ipv6_imap_body(self):
        """
        Testcase to validate IPv6 creation from IMAP account
        """
        fprint(self, "\n---------- TC_ID 9533: Verify IPv6 creation from IMAP mail body ----------")
        nav_menu_main(self, 'Threat Data')
        for i in self.email_data["IMAP"]["imap_body"]["IPv6"]:
            verify_data_in_threatdata(self, i, self.IMAP_TITLE)

    def test_34_verify_ipv4_imap_body(self):
        """
        Testcase to validate IPv4 creation from IMAP account
        """
        fprint(self, "\n---------- TC_ID 9534: Verify IPv4 creation from IMAP mail body ----------")
        nav_menu_main(self, 'Threat Data')
        for i in self.email_data["IMAP"]["imap_body"]["IPv4"]:
            verify_data_in_threatdata(self, i, self.IMAP_TITLE)

    def test_35_delete_email_configuration(self):
        """
        TestCase to delete created mailbox configuration
        """
        fprint(self, "\n----------- TC_ID 9535: Deleting the Created Email Configuration -----------")
        nav_menu_main(self, "Threat Mailbox")
        self.driver.refresh()
        waitfor(self, 20, By.XPATH, "//div[@role='button']/span/button[text()]")
        self.driver.find_element_by_xpath("//div[@role='button']/span/button[text()]").click()
        waitfor(self, 20, By.XPATH, "//div/*[contains(text(),'"+self.POP_TITLE+"')]")
        sleep(1)
        self.driver.find_element_by_xpath("//div/*[contains(text(),'"+self.POP_TITLE+"')]").click()
        fprint(self, "Clicking on action button for email configuration")
        sleep(1)
        self.driver.find_element_by_xpath("//div/span/button/i[@class='cyicon-more-vertical']").click()
        waitfor(self, 20, By.XPATH, "//li[contains(text(),'Remove Configuration')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Remove Configuration')]").click()
        fprint(self, "Clicked on remove Configuration")
        waitfor(self, 20, By.XPATH, "//button[@data-testalert='confirm-delete']")
        self.driver.find_element_by_xpath("//button[@data-testalert='confirm-delete']").click()
        fprint(self, "Clicked on confirm Delete pop up")
        verify_success(self, "Threat mail account deleted successfully")
        fprint(self, "[PASSED] Selected configuration is deleted successfully")
        self.driver.refresh()
        process_console_logs(self)

    def test_36_validate_selective_intel_creation(self):
        """
        Testcase to validate if only selective data is being auto created
        """
        fprint(self, "\n----------- TC_ID 9536: Validating selective intel creation from mailbox -----------")
        nav_menu_main(self, "Threat Data")
        if get_value("selective_intel"):
            pattern = get_value("auto_mail_pattern")
            for i, k in self.email_data["IMAP"]["selective_intel"].items():
                if pattern in i:
                    verify_data_in_threatdata(self, k[0], self.IMAP_TITLE)
            verify_data_in_threatdata(self, "auto_selective", self.IMAP_TITLE)
            waitfor(self, 20, By.XPATH, f"//span[contains(text(),'{self.IMAP_TITLE}')]"
                                        "/ancestor::tr/td[3]//span[contains(text(),'auto_selective')]")
            sleep(2)
            _ele = self.driver.find_elements_by_xpath(
                "//span[contains(text(), 'auto_selective')]//ancestor::tr")[1]
            ActionChains(self.driver).click(_ele).perform()
            waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Relations')]")
            self.driver.find_element_by_xpath("//div[contains(text(), 'Relations')]").click()
            waitfor(self, 10, By.XPATH, "//span[contains(text(),'Indicator')]/following-sibling::span[text()='5']")
            self.driver.find_element_by_xpath("//*[span[contains(text(),'Indicator')]/"
                                              "following-sibling::span[text()='5']]").click()
            self.driver.find_element_by_xpath("//button[span[normalize-space(text())='Table']]").click()
            for i, k in self.email_data["IMAP"]["selective_intel"].items():
                if pattern in i:
                    waitfor(self, 20, By.XPATH, f"//span[normalize-space(text())='{k[0]}']")
        else:
            fprint(self, "Feature not supported in the version being run upon")

    def test_37_create_intel_metadata_report(self):
        """
        Testcase to create intel with varied metadata applied for report only
        """
        fprint(self, "\n----------- TC_ID 9537: Create intel with metadata only added to Report -----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        object_types = ["IPv4", "URLs", "Domains"]
        load_mail(self, account_name=self.IMAP_TITLE, subject="auto_selective")
        waitfor(self, 20, By.XPATH, "//div[span/span/span[normalize-space(text())='partial_select.txt']]/"
                                    "preceding-sibling::span")
        self.driver.find_element_by_xpath("//div[span/span/span[normalize-space(text())='partial_select.txt']]/"
                                          "preceding-sibling::span").click()
        create_intel_metadata(self, object_types=object_types, title='meta_report_obj', confidence=20, TLP="Green",
                              tag="meta_to_report", only_report=True)
        process_console_logs(self)

    def test_38_create_intel_metadata_all(self):
        """
        Testcase to create intel with varied metadata applied for report only
        """
        fprint(self, "\n----------- TC_ID 9538: Create intel with metadata for all objects -----------")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        object_types = ["IPv6", "Emails", "MD5"]
        load_mail(self, account_name=self.IMAP_TITLE, subject="auto_selective")
        waitfor(self, 20, By.XPATH, "//div[span/span/span[normalize-space(text())='partial_select.txt']]/"
                                    "preceding-sibling::span")
        self.driver.find_element_by_xpath("//div[span/span/span[normalize-space(text())='partial_select.txt']]/"
                                          "preceding-sibling::span").click()
        create_intel_metadata(self, object_types=object_types, title='metadata_all_obj', confidence=60, TLP="Red",
                              tag="meta_to_all", only_report=False)
        process_console_logs(self)

    def test_39_validate_metadata_report_obj(self):
        """
        Testcase to validate if metadata only applied to report
        """
        fprint(self, "\n----------- TC_ID 9539: Validate if metadata is only applied to report -----------")
        nav_menu_main(self, "Threat Data")
        for i, k in self.email_data["IMAP"]["selective_intel"].items():
            if i in ["IPv4", "URLs", "Domains"]:
                verify_data_in_threatdata(self, k[0], self.IMAP_TITLE)
                validate_all_metadata(self, source=self.IMAP_TITLE, object=k[0], tlp='None', confidence="0")
                self.driver.find_element_by_xpath("//span[@class='cy-page__back-button']").click()
        verify_data_in_threatdata(self, "meta_report_obj", self.IMAP_TITLE)
        validate_all_metadata(self, source=self.IMAP_TITLE, object="meta_report_obj", tlp='Green', tag='meta_to_report')

    def test_40_validate_metadata_all_obj(self):
        """
        Testcase to validate if metadata applied to all objects
        """
        fprint(self, "\n----------- TC_ID 9540: Validate if metadata is applied to all objects -----------")
        nav_menu_main(self, "Threat Data")
        for i, k in self.email_data["IMAP"]["selective_intel"].items():
            if i in ["IPv6", "Emails", "MD5"]:
                verify_data_in_threatdata(self, k[0], self.IMAP_TITLE)
                validate_all_metadata(self, source=self.IMAP_TITLE, object=k[0], tlp='Red', confidence="60", tag='meta_to_all')
                self.driver.find_element_by_xpath("//span[@class='cy-page__back-button']").click()
        verify_data_in_threatdata(self, "metadata_all_obj", self.IMAP_TITLE)
        validate_all_metadata(self, source=self.IMAP_TITLE, object="metadata_all_obj", tlp='Red', tag='meta_to_all')

    def test_41_create_intel_mail_pdf(self):
        """
            Testcase to validate if all data in pdf file can be parsed and created successfully
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9541: Parse and create IPv4 from IMAP mail body ----------")
        fails = []
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_FILE_TYPES")
        add_metadata(self, confidence_score="0")
        read_mail_file(self, "all_pdf.pdf")
        for i in self.email_data["IMAP"]["imap_file_pdf"].keys():
            try:
                parse_and_select(self, domain='IMAP', mail='imap_file_pdf', ioctype=i)
            except Exception:
                fails.append(i)
                fprint(self, f"Object type {i} failed to get created")
        create_selected_intel(self)
        if len(fails) > 0:
            fprint(self, "Intel creation failed for "+", ".join(fails))
            self.fail("Not all expected intel could be created")
        else:
            fprint(self, "All expected intel was parsed and created successfully")

    def test_42_create_intel_mail_txt(self):
        """
            Testcase to validate if all data in txt file can be parsed and created successfully
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9542: Parse and create IPv4 from IMAP mail body ----------")
        fails = []
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_FILE_TYPES")
        add_metadata(self, confidence_score="0")
        read_mail_file(self, "all_txt.txt")
        for i in self.email_data["IMAP"]["imap_file_txt"].keys():
            try:
                parse_and_select(self, domain='IMAP', mail='imap_file_txt', ioctype=i)
            except Exception:
                fails.append(i)
                fprint(self, f"Object type {i} failed to get created")
        create_selected_intel(self)
        if len(fails) > 0:
            fprint(self, "Intel creation failed for "+", ".join(fails))
            self.fail("Not all expected intel could be created")
        else:
            fprint(self, "All expected intel was parsed and created successfully")

    def test_43_create_intel_mail_docx(self):
        """
            Testcase to validate if all data in docx file can be parsed and created successfully
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9543: Parse and create IPv4 from IMAP mail body ----------")
        fails = []
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_FILE_TYPES")
        add_metadata(self, confidence_score="0")
        read_mail_file(self, "all_docx.docx")
        for i in self.email_data["IMAP"]["imap_file_docx"].keys():
            try:
                parse_and_select(self, domain='IMAP', mail='imap_file_docx', ioctype=i)
            except Exception:
                fails.append(i)
                fprint(self, f"Object type {i} failed to get created")
        create_selected_intel(self)
        if len(fails) > 0:
            fprint(self, "Intel creation failed for "+", ".join(fails))
            self.fail("Not all expected intel could be created")
        else:
            fprint(self, "All expected intel was parsed and created successfully")

    def test_44_create_intel_mail_xlsx(self):
        """
            Testcase to validate if all data in xlsx file can be parsed and created successfully
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9544: Parse and create IPv4 from IMAP mail body ----------")
        fails = []
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_FILE_TYPES")
        add_metadata(self, confidence_score="0")
        read_mail_file(self, "all_xlsx.xlsx")
        for i in self.email_data["IMAP"]["imap_file_xlsx"].keys():
            try:
                parse_and_select(self, domain='IMAP', mail='imap_file_xlsx', ioctype=i)
            except Exception:
                fails.append(i)
                fprint(self, f"Object type {i} failed to get created")
        create_selected_intel(self)
        if len(fails) > 0:
            fprint(self, "Intel creation failed for "+", ".join(fails))
            self.fail("Not all expected intel could be created")
        else:
            fprint(self, "All expected intel was parsed and created successfully")

    def test_45_create_intel_mail_csv(self):
        """
            Testcase to validate if all data in csv file can be parsed and created successfully
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9545: Parse and create IPv4 from IMAP mail body ----------")
        fails = []
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_FILE_TYPES")
        add_metadata(self, confidence_score="0")
        read_mail_file(self, "all_csv.csv")
        for i in self.email_data["IMAP"]["imap_file_csv"].keys():
            try:
                parse_and_select(self, domain='IMAP', mail='imap_file_csv', ioctype=i)
            except Exception:
                fails.append(i)
                fprint(self, f"Object type {i} failed to get created")
        create_selected_intel(self)
        if len(fails) > 0:
            fprint(self, "Intel creation failed for "+", ".join(fails))
            self.fail("Not all expected intel could be created")
        else:
            fprint(self, "All expected intel was parsed and created successfully")

    def test_46_create_intel_mail_zip(self):
        """
            Testcase to validate if all data in zip file can be parsed and created successfully
        """
        self.driver.refresh()
        sleep(5)
        fprint(self, "\n---------- TC_ID 9546: Parse and create IPv4 from IMAP mail body ----------")
        fails = []
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="ALL_FILE_TYPES")
        add_metadata(self, confidence_score="0")
        read_mail_file(self, "all_zip.zip")
        for i in self.email_data["IMAP"]["imap_file_zip"].keys():
            try:
                parse_and_select(self, domain='IMAP', mail='imap_file_zip', ioctype=i)
            except Exception:
                fails.append(i)
                fprint(self, f"Object type {i} failed to get created")
        create_selected_intel(self)
        if len(fails) > 0:
            fprint(self, "Intel creation failed for "+", ".join(fails))
            self.fail("Not all expected intel could be created")
        else:
            fprint(self, "All expected intel was parsed and created successfully")

    def test_47_verify_imap_pdf_data(self):
        """
        Testcase to validate intel creation from pdf attachment
        """
        fprint(self, "\n---------- TC_ID 9547: Verify Intel creation from pdf attachment ----------")
        nav_menu_main(self, 'Threat Data')
        fails = []
        for ioc_type, value_list in self.email_data["IMAP"]["imap_file_pdf"].items():
            for value in value_list:
                if ioc_type == "ASN":
                    value = "AS"+value
                try:
                    fprint(self, f"Seardhing for {value} in Threat Data")
                    verify_data_in_threatdata(self, value, self.IMAP_TITLE)
                except:
                    fails.append(value)
                    fprint(self, f"{ioc_type} with value {value} not found")
        if len(fails) > 0:
            self.fail("Failed as data listed below was not found in Threat Data \n"+"\n".join(fails))
        else:
            fprint(self, "All Expected Data is created successfully")

    def test_48_verify_imap_txt_data(self):
        """
        Testcase to validate intel creation from txt attachment
        """
        fprint(self, "\n---------- TC_ID 9548: Verify Intel creation from txt attachment ----------")
        nav_menu_main(self, 'Threat Data')
        fails = []
        for ioc_type, value_list in self.email_data["IMAP"]["imap_file_txt"].items():
            for value in value_list:
                if ioc_type == "ASN":
                    value = "AS"+value
                try:
                    fprint(self, f"Seardhing for {value} in Threat Data")
                    verify_data_in_threatdata(self, value, self.IMAP_TITLE)
                except:
                    fails.append(value)
                    fprint(self, f"{ioc_type} with value {value} not found")
        if len(fails) > 0:
            self.fail("Failed as data listed below was not found in Threat Data \n"+"\n".join(fails))
        else:
            fprint(self, "All Expected Data is created successfully")

    def test_49_verify_imap_docx_data(self):
        """
        Testcase to validate intel creation from docx attachment
        """
        fprint(self, "\n---------- TC_ID 9549: Verify Intel creation from docx attachment ----------")
        nav_menu_main(self, 'Threat Data')
        fails = []
        for ioc_type, value_list in self.email_data["IMAP"]["imap_file_docx"].items():
            for value in value_list:
                if ioc_type == "ASN":
                    value = "AS"+value
                try:
                    fprint(self, f"Seardhing for {value} in Threat Data")
                    verify_data_in_threatdata(self, value, self.IMAP_TITLE)
                except:
                    fails.append(value)
                    fprint(self, f"{ioc_type} with value {value} not found")
        if len(fails) > 0:
            self.fail("Failed as data listed below was not found in Threat Data \n"+"\n".join(fails))
        else:
            fprint(self, "All Expected Data is created successfully")

    def test_50_verify_imap_xlsx_data(self):
        """
        Testcase to validate intel creation from xlsx attachment
        """
        fprint(self, "\n---------- TC_ID 9550: Verify Intel creation from xlsx attachment ----------")
        nav_menu_main(self, 'Threat Data')
        fails = []
        for ioc_type, value_list in self.email_data["IMAP"]["imap_file_xlsx"].items():
            for value in value_list:
                if ioc_type == "ASN":
                    value = "AS"+value
                try:
                    fprint(self, f"Seardhing for {value} in Threat Data")
                    verify_data_in_threatdata(self, value, self.IMAP_TITLE)
                except:
                    fails.append(value)
                    fprint(self, f"{ioc_type} with value {value} not found")
        if len(fails) > 0:
            self.fail("Failed as data listed below was not found in Threat Data \n"+"\n".join(fails))
        else:
            fprint(self, "All Expected Data is created successfully")

    def test_51_verify_imap_csv_data(self):
        """
        Testcase to validate intel creation from csv attachment
        """
        fprint(self, "\n---------- TC_ID 9551: Verify Intel creation from csv attachment ----------")
        nav_menu_main(self, 'Threat Data')
        fails = []
        for ioc_type, value_list in self.email_data["IMAP"]["imap_file_csv"].items():
            for value in value_list:
                if ioc_type == "ASN":
                    value = "AS"+value
                try:
                    fprint(self, f"Seardhing for {value} in Threat Data")
                    verify_data_in_threatdata(self, value, self.IMAP_TITLE)
                except:
                    fails.append(value)
                    fprint(self, f"{ioc_type} with value {value} not found")
        if len(fails) > 0:
            self.fail("Failed as data listed below was not found in Threat Data \n"+"\n".join(fails))
        else:
            fprint(self, "All Expected Data is created successfully")

    def test_52_verify_imap_zip_data(self):
        """
        Testcase to validate intel creation from zip attachment
        """
        fprint(self, "\n---------- TC_ID 9552: Verify Intel creation from zip attachment ----------")
        nav_menu_main(self, 'Threat Data')
        fails = []
        for ioc_type, value_list in self.email_data["IMAP"]["imap_file_zip"].items():
            for value in value_list:
                if ioc_type == "ASN":
                    value = "AS"+value
                try:
                    fprint(self, f"Seardhing for {value} in Threat Data")
                    verify_data_in_threatdata(self, value, self.IMAP_TITLE)
                except:
                    fails.append(value)
                    fprint(self, f"{ioc_type} with value {value} not found")
        if len(fails) > 0:
            self.fail("Failed as data listed below was not found in Threat Data \n"+"\n".join(fails))
        else:
            fprint(self, "All Expected Data is created successfully")

    def test_53_add_to_allowed(self):
        """
            Testcase to validate if allow indicators from mailbox is working as expected
        """
        fprint(self, "\n ------------ TC_ID 9553: Add Indicators to allowed from mailbox ------------\n")
        nav_menu_main(self, "Threat Mailbox")
        fails = []
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        nav_menu_main(self, "Threat Mailbox")
        load_mail(self, account_name=self.IMAP_TITLE, subject="allow_indicators", action="Allow")
        for i in self.email_data["IMAP"]["imap_allow_ioc"].keys():
            try:
                parse_and_select(self, domain='IMAP', mail='imap_allow_ioc', ioctype=i)
            except Exception:
                fails.append(i)
                fprint(self, f"Object type {i} failed to get selected")
        self.driver.find_element_by_xpath("//button[text()='Save']").click()
        verify_success(self, " added successfully")

    def test_54_verify_allowed_mail_ioc(self):
        """
            Validate if all indicators marked are added to allowed
        """
        fprint(self, "\n ------------ TC_ID 9554: Validate if all indicators marked are added to allowed ------------\n")
        fails = []
        nav_menu_main(self, "Indicators Allowed")
        for ioc_type, value in self.email_data["IMAP"]["imap_allow_ioc"].items():
            for i in value:
                try:
                    allowed_indi_search(self, value=i)
                except:
                    fails.append(i)
        if len(fails)>0:
            fprint(self, "Indicators allow failed for \n"+"\n".join(fails))
        else:
            fprint(self, "All selected indicators are allowed successfully")

    def test_55_unlock_protected_pdf_wrong_pass(self):
        """
            Testcase to validate if wrong password can be used to access protected file
        """
        fprint(self, "\n -------- TC_ID 9555: verify flow of wrong password on a protected file  -------- \n")
        nav_menu_main(self, "Threat Mailbox")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        load_mail(self, account_name=self.IMAP_TITLE, subject="complex_protected_data", action="View")
        _lock_icon_xpath = "//span[normalize-space(text())='password_pdf.pdf']/following-sibling::span/i[contains" \
                           "(@class, 'cyicon-lock')]"
        if waitfor(self, 2, By.XPATH, _lock_icon_xpath):
            fprint(self, "Lock icon is being displayed for the protected file")
        self.driver.find_element_by_xpath(_lock_icon_xpath).click()
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Enter Password *']")
        fprint(self, "Entering wrong password for the file")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter Password *']").send_keys("wrong_pass")
        self.driver.find_element_by_xpath("//button[text()='Submit']").click()
        verify_success(self, "Incorrect Password")

    def test_56_unlock_protected_pdf_right_pass(self):
        """
            Validate if password protected file can not be accessed with right password
        """
        fprint(self, "\n -------- TC_ID 9556: Validate right pass for protected file ------------- \n")
        _actual_pass = 'rightpass123'
        nav_menu_main(self, "Threat Mailbox")
        if waitfor(self, 20, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        load_mail(self, account_name=self.IMAP_TITLE, subject="complex_protected_data", action="View")
        _lock_icon_xpath = "//span[normalize-space(text())='password_pdf.pdf']/following-sibling::span/i[contains" \
                           "(@class, 'cyicon-lock')]"
        if waitfor(self, 2, By.XPATH, _lock_icon_xpath):
            fprint(self, "Lock icon is being displayed for the protected file")
        self.driver.find_element_by_xpath(_lock_icon_xpath).click()
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Enter Password *']")
        fprint(self, "Entering wrong password for the file")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter Password *']").send_keys(_actual_pass)
        self.driver.find_element_by_xpath("//button[text()='Submit']").click()
        verify_success(self, "You will be notified once the parsing of attachment is completed")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
