import unittest
from lib.ui.nav_threat_data import *

domain = "google.com"
record_type = ['A', 'AAAA', 'NS', 'SOA', 'MX', 'TXT', 'CAA']
certificate_anlys_section = ['ssl_info', 'subject', 'issuer', 'certificate chain', 'certificate_chain-0',
                             'certificate_chain-1', 'certificate_chain-2', 'extensions']

failures = []


class NetworkUtilities(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.driver = initialize_browser(self)
        login(self, Admin_Email, Admin_Password)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def verify_data_on_page(self, section, value):
        if waitfor(self, 20, By.XPATH, "//div[contains(text(),'"+section+"')]/parent::div//div[contains(text(),'"+value+"')]", False):
            fprint(self, value+" is visible under section "+section)
        else:
            fprint(self, "[Falied] - "+value+" is visible under section "+section)
            failures.append("[Falied] - "+value+" is visible under section "+section)

    def select_recent_search_query(self, searched_domain):
        self.driver.find_element_by_xpath("//span[@data-testid='ioc_value' and contains(text(),'"+searched_domain+"')]").click()
        fprint(self, "Clicked on the Query - "+searched_domain)

    def search_for_domain(self, domain):
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Enter Domain or IP']")
        self.driver.find_element_by_xpath("//input[@placeholder='Enter Domain or IP']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Enter Domain or IP']").send_keys(domain)
        self.driver.find_element_by_xpath("//span[@data-testaction='search-icon']").click()

    def test_01_verify_whois_report(self):
        fprint(self, "TC_ID: 4012571 - test_01_verify_whois_report")
        nav_menu_main(self, "Network Utilities")
        if waitfor(self, 1, By.XPATH, "//span[@data-testid='ioc_value' and contains(text(),'"+domain+"')]", False):
            self.select_recent_search_query(searched_domain=domain)
        else:
            self.search_for_domain(domain=domain)

        # Verification in WHOIS Report

        waitfor(self, 60, By.XPATH, "//div[contains(text(),'Domain Name')]/parent::div//div[contains(text(),'"+domain+"')]")
        self.verify_data_on_page(section="ioc key", value=domain)
        self.driver.find_element_by_xpath("//div[contains(text(),'result')]").click()
        self.verify_data_on_page(section="Admin Country", value="US")
        self.verify_data_on_page(section="Registrar WHOIS Server", value="whois.markmonitor.com")
        self.verify_data_on_page(section="Domain Name", value=domain)
        self.verify_data_on_page(section="Admin Email", value="Select Request Email Form at https://domains.markmonitor.com/whois/google.com")
        self.verify_data_on_page(section="Domain Status", value="serverDeleteProhibited (https://www.icann.org/epp#serverDeleteProhibited)")
        self.verify_data_on_page(section="Tech Email", value="Select Request Email Form at https://domains.markmonitor.com/whois/google.com")
        self.verify_data_on_page(section="Registrant Email", value="Select Request Email Form at https://domains.markmonitor.com/whois/google.com")
        self.assert_(failures == [], str(failures))

    def test_02_verify_DNS_record(self):
        fprint(self, "TC_ID: 4012572 - test_02_verify_DNS_record")
        nav_menu_main(self, "Network Utilities")
        if waitfor(self, 1, By.XPATH, "//span[@data-testid='ioc_value' and contains(text(),'" + domain + "')]", False):
            self.select_recent_search_query(searched_domain=domain)
        else:
            self.search_for_domain(domain=domain)
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'DNS Records')]/parent::li")
        self.driver.find_element_by_xpath("//div[contains(text(),'DNS Records')]/parent::li").click()

        # Verification in DNS Record
        for data in record_type:
            if waitfor(self, 5, By.XPATH, "//span[@data-testid='record_type' and contains(text(),'"+data+"')]", False):
                fprint(self, "Record type is visible - "+data)
            else:
                fprint(self, "[Failed] - Record type is not visible - "+data)
                failures.append("[Failed] - Record type is not visible - "+data)
        self.assert_(failures == [], str(failures))

    def test_03_verify_certificate_analysis(self):
        fprint(self, "TC_ID: 4012573 - test_03_verify_certificate_analysis")
        nav_menu_main(self, "Network Utilities")
        if waitfor(self, 1, By.XPATH, "//span[@data-testid='ioc_value' and contains(text(),'" + domain + "')]", False):
            self.select_recent_search_query(searched_domain=domain)
        else:
            self.search_for_domain(domain=domain)
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Certificate Analysis')]/parent::li")
        self.driver.find_element_by_xpath("//div[contains(text(),'Certificate Analysis')]/parent::li").click()

        # Verification in Certificate Analyst
        for data in certificate_anlys_section:
            if waitfor(self, 5, By.XPATH, "//div[contains(text(),'"+data+"')]", False):
                fprint(self, "Certificate Analyst Sections is visible - "+data)
            else:
                fprint(self, "[Failed] - Certificate Analyst Sections is not visible - "+data)
                failures.append("Certificate Analyst Sections is not visible - "+data)

        self.assert_(failures == [], str(failures))

    def test_04_verify_traceroute(self):
        fprint(self, "TC_ID: 4012574 - test_04_verify_traceroute")
        nav_menu_main(self, "Network Utilities")
        if waitfor(self, 1, By.XPATH, "//span[@data-testid='ioc_value' and contains(text(),'" + domain + "')]", False):
            self.select_recent_search_query(searched_domain=domain)
        else:
            self.search_for_domain(domain=domain)
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Traceroute')]/parent::li")
        self.driver.find_element_by_xpath("//div[contains(text(),'Traceroute')]/parent::li").click()

        # Verification in Traceroute
        waitfor(self, 20, By.XPATH, "//pre")
        page_text = self.driver.find_element_by_xpath("//pre").text
        if str(page_text).__contains__(domain):
            fprint(self, "[Passed] - Getting data in Traceroute")
        else:
            fprint(self, "[Failed] - Getting data in Traceroute")
            self.fail("[Failed] - Getting data in Traceroute")

    def test_05_verify_ping(self):
        fprint(self, "TC_ID: 4012575 - test_05_verify_ping")
        nav_menu_main(self, "Network Utilities")
        if waitfor(self, 1, By.XPATH, "//span[@data-testid='ioc_value' and contains(text(),'" + domain + "')]", False):
            self.select_recent_search_query(searched_domain=domain)
        else:
            self.search_for_domain(domain=domain)
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Ping')]/parent::li")
        self.driver.find_element_by_xpath("//div[contains(text(),'Ping')]/parent::li").click()

        # Verification in Ping
        self.verify_data_on_page(section="destination", value=domain)
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'packet')]")
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'rtt')]")
        fprint(self, "[Passed] - All Expected sections are visible")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
