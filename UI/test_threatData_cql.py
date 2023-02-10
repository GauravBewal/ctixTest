import unittest

from lib.ui.nav_app import *
from lib.ui.quick_add import quick_create_ip, create_intel
from lib.ui.nav_tableview import *


class CQL(unittest.TestCase):

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

    ipv4 = "15.15.14.13"
    ipv6 = "6e50:dddd:6774:a2ee:517a:a656:90ad:25fc"
    domain = "automationgupta.com"
    url = "http://www.example.com/index.html"
    email = "shinchan@abc.com"
    md5 = "8b394d62da771c85fb875769c2b07472"
    sha1 = "f420a7dc060275f50d223bafe5fb66ce4ac8b5e4"
    sha224 = "4ab7e1ef817b888e3f421f0a8c2b44409c75a15cdb5ed412cfb247c4"
    sha256 = "e362f707920a68c263c0dddea633ecf6a29de610d381af547344e7c9fb238032"
    sha384 = "f799041290a3922d1e8537a8bb3f4eef6f309cc920e6fa1cbe6e12a3567c8adf3720568dab38126f9da0596bb8684f2e"
    ssdeep = "1536:cicoo8zayon9/exffmetin9vu+oaygy/jqbjakerwwk:hdo8gnefntindloajy/jqnlezk"

    def click_cql(self):
        nav_menu_main(self, "Threat Data")
        waitfor(self, 10, By.XPATH, "//button//span[normalize-space()='CQL']")
        self.driver.find_element_by_xpath("//button//span[normalize-space()='CQL']").click()
        fprint(self, "[Passed]-clicked on the cql button successfully")
        if waitfor(self, 5, By.XPATH, "//div[@aria-hidden='true']/ul[contains(@class,'cy-cql__suggestions')]", False):
            waitfor(self, 5, By.XPATH, "//textarea[@placeholder='Search Query']")
            self.driver.find_element_by_xpath("//textarea[@placeholder='Search Query']").click()
        fprint(self, "[Passed]-clicked on search query")

    def select_initial_steps_(self):
        self.select_from_dropdown("Object Type")
        self.select_from_dropdown("=")
        self.select_from_dropdown("Indicator")
        self.select_from_dropdown("AND")
        self.select_from_dropdown("IOC Type")
        self.select_from_dropdown("=")

    def select_from_dropdown(self, val):
        waitfor(self, 10, By.XPATH, "(//li/span/span[contains(text(), '" + val + "')])[1]")
        self.driver.find_element_by_xpath("(//li/span/span[contains(text(), '" + val + "')])[1]").click()
        fprint(self, f"[Passed]-clicked on the {val}")

    def verify_data(self, val):
        self.driver.find_element_by_xpath("//textarea[@placeholder='Search Query']").send_keys(Keys.RETURN)
        waitfor(self, 10, By.XPATH, "//span[contains(@class,'cyicon-search')]")
        self.driver.find_element_by_xpath("//span[contains(@class,'cyicon-search')]").click()
        fprint(self, "[Passed]-clicked on the search Icon")
        waitfor(self, 20, By.XPATH, "(//span[contains(text(),'" + val + "')])[1]")

    def test_01_verify_ipv4_and_source_threat_mailbox(self):
        """ Test case to verify that ipv4 is received from the threat mailbox"""
        fprint(self, "TC_ID 1671: Checking that the CQl is working for the IPV4 that is created from threat mailbox ")
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("Ipv4 addr")
        self.select_from_dropdown("AND")
        self.select_from_dropdown("Source")
        self.select_from_dropdown("=")
        self.select_from_dropdown("AUTOMATESTIN")
        self.verify_data("23.154.177.6")
        fprint(self, "[Passed]- The CQL filter is working fine for the ioc type ipv4 and source as threat mailbox")

    def test_02_verify_ipv6_and_source_threat_mailbox(self):
        """ test case to verify that cql is woking fine for ipv6 received from threat mailbox"""
        fprint(self, "TC_ID 1672: Checking that the CQl is working for the IPV6 that is created from threat mailbox ")
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("Ipv6 addr")
        self.select_from_dropdown("AND")
        self.select_from_dropdown("Source")
        self.select_from_dropdown("=")
        self.select_from_dropdown("AUTOMATESTIN")
        self.verify_data("807b:9334:64f7:f23b:cb9a:7877:2113:7281")
        fprint(self, "[Passed]-working fine for ipv6 that is received from threat mailbox")

    def test_03_verify_domain_threat_mailbox(self):
        """ Test case to verify that the cql is working fine for the domain"""
        fprint(self, "TC_ID 1673: Checking that the CQl is working for the Domain that is created from threat mailbox ")
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("Domain")
        self.select_from_dropdown("AND")
        self.select_from_dropdown("Source")
        self.select_from_dropdown("=")
        self.select_from_dropdown("AUTOMATESTIN")
        self.verify_data("dizzydom.com")
        fprint(self, "[Passed]-working fine for domain that is received from threat mailbox")

    def test_04_verify_email_threat_mailbox(self):
        """ test case to verify that cql is working fine for the url"""
        fprint(self, "TC_ID 1674: Checking that the CQl is working for the Email that is created from threat mailbox ")
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("Email addr")
        self.select_from_dropdown("AND")
        self.select_from_dropdown("Source")
        self.select_from_dropdown("=")
        self.select_from_dropdown("AUTOMATESTIN")
        self.verify_data("mailcius@dizzydom.com")
        fprint(self, "[Passed]-working fine for email that is received from threat mailbox")

    def test_05_verify_sha1_threat_mailbox(self):
        """ test case to verify that cql is working fine for sha1"""
        fprint(self, "TC_ID 1675: Checking that the CQl is working for the SHA1 that is created from threat mailbox ")
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("SHA1")
        self.select_from_dropdown("AND")
        self.select_from_dropdown("Source")
        self.select_from_dropdown("=")
        self.select_from_dropdown("AUTOMATESTIN")
        self.verify_data("9f01d4442c495c7128649b98201187bc0c58dedd")
        fprint(self, "[Passed]-working fine for SHA1 that is received from threat mailbox")

    def test_06_verify_sha224_threat_mailbox(self):
        """ Test case to verify that cql is working fine for sha 224"""
        fprint(self, "TC_ID 1676: Checking that the CQl is working for the SHA224 that is created from threat mailbox ")
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("SHA224")
        self.select_from_dropdown("AND")
        self.select_from_dropdown("Source")
        self.select_from_dropdown("=")
        self.select_from_dropdown("AUTOMATESTIN")
        self.verify_data("bb72629638f93433d05aaed0b89fd07ce26f104fda143554ed7075ea")
        fprint(self, "[Passed]-working fine for SHA224 that is received from threat mailbox")

    def test_07_verify_sha256_threat_mailbox(self):
        """ Test case to verify that cql is working fine for sha 256"""
        fprint(self, "TC_ID 1677: Checking that the CQl is working for the SHA256 that is created from threat mailbox ")
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("SHA256")
        self.select_from_dropdown("AND")
        self.select_from_dropdown("Source")
        self.select_from_dropdown("=")
        self.select_from_dropdown("AUTOMATESTIN")
        self.verify_data("cf8b68b779c4e716eceed5dad7003d280eba96c11f3d7868d59f2dcae5500067")
        fprint(self, "[Passed]-working fine for SHA256 that is received from threat mailbox")

    def test_08_verify_sha384_threat_mailbox(self):
        """ Test case to verify that cql is working fine for sha 384"""
        fprint(self, "TC_ID 1678: Checking that the CQl is working for the SHA384 that is created from threat mailbox ")
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("SHA384")
        self.select_from_dropdown("AND")
        self.select_from_dropdown("Source")
        self.select_from_dropdown("=")
        self.select_from_dropdown("AUTOMATESTIN")
        self.verify_data(
            "1e3b3705af320ac1c99d21d798ff363a6c0674bbef43e77e3a87388f79a28c56ff1e68b5c5eb67f3aa732f61aea54338")
        fprint(self, "[Passed]-working fine for SHA384 that is received from threat mailbox")

    def test_09_verify_sha512_threat_mailbox(self):
        """ Test case to verify that cql is working fine for sha 512"""
        fprint(self, "TC_ID 1679: Checking that the CQl is working for the SHA512 that is created from threat mailbox ")
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("SHA512")
        self.select_from_dropdown("AND")
        self.select_from_dropdown("Source")
        self.select_from_dropdown("=")
        self.select_from_dropdown("AUTOMATESTIN")
        self.verify_data("9ed22e3da0d6d58193489cdbd3e0d181cfc631598de26bb0e17bb8874e6cf2")
        fprint(self, "[Passed]-working fine for SHA512 that is received from threat mailbox")

    def test_10_verify_MD5_threat_mailbox(self):
        """ test case to verify that CQL is working fine for MD5 received from threat Mailbox"""
        fprint(self, "TC_ID 16710: Checking that the CQl is working for the MD5 that is created from threat mailbox ")
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("MD5")
        self.select_from_dropdown("AND")
        self.select_from_dropdown("Source")
        self.select_from_dropdown("=")
        self.select_from_dropdown("AUTOMATESTIN")
        self.verify_data("c95fdb7e8ec18534b549dba339688353")
        fprint(self, "[Passed]-working fine for MD5 that is received from threat mailbox")

    def test_11_verify_SSDEEP_threat_mailbox(self):
        """ test case to verify that CQL is working fine for SSDEEP received from threat Mailbox"""
        fprint(self,
               "TC_ID 16711: Checking that the CQl is working for the SSDEEP that is created from threat mailbox ")
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("SSDEEP")
        self.select_from_dropdown("AND")
        self.select_from_dropdown("Source")
        self.select_from_dropdown("=")
        self.select_from_dropdown("AUTOMATESTIN")
        self.verify_data("1536:Z1QbFJL5JcH5tSHWDUITshqd4XQNX27H1z:QFJl9OU3z")
        fprint(self, "[Passed]-working fine for SSDEEP that is received from threat mailbox")

    def test_12_verify_URL_threat_mailbox(self):
        """ test case to verify that CQL is working fine for URL received from threat Mailbox"""
        fprint(self,
               "TC_ID 16712: Checking that the CQl is working for the URL that is created from threat mailbox ")
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("URL")
        self.select_from_dropdown("AND")
        self.select_from_dropdown("Source")
        self.select_from_dropdown("=")
        self.select_from_dropdown("AUTOMATESTIN")
        self.verify_data("https://swisscpprivate.com")
        fprint(self, "[Passed]-working fine for URL that is received from threat mailbox")

    def test_13_verify_quick_create_ipv4(self):
        """ Test case to verify that the indicator that is created by quick create ip is visible under CQL"""
        fprint(self,
               "TC_ID 16713:Test case to verify that the data that is created under quick create Ip is visible under CQL")
        quick_create_ip(self, self.ipv4, self.ipv4)
        self.click_cql()
        sleep(5)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("Ipv4 addr")
        self.verify_data(self.ipv4)
        fprint(self, "[Passed]- The ipv4 created is visible under the CQL")

    def test_14_verify_quick_create_ipv6(self):
        """ Test case to verify that the indicator that is created by quick create ip is visible under CQL"""
        fprint(self,
               "TC_ID 16714:Test case to verify that the data that is created under quick create Ip is visible under CQL")
        create_intel(self, 'IPv6', self.ipv6, self.ipv6)
        self.click_cql()
        sleep(5)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("Ipv6 addr")
        self.verify_data(self.ipv6)
        fprint(self, "[Passed]- The ipv6 created is visible under the CQL")

    def test_15_verify_quick_create_domain(self):
        """ Test case to verify that the domain object which is created by quick create ip is visible under CQL"""
        fprint(self,
               "TC_ID 16715:Test case to verify that the domain object which is created by quick create ip is visible under CQL")
        create_intel(self, 'Domain', self.domain, self.domain)
        self.click_cql()
        sleep(5)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("Domain")
        self.verify_data(self.domain)
        fprint(self, "[Passed]-The domain created is visible under CQL")

    def test_16_verify_quick_create_url(self):
        """ Test case to verify that the url created by quick create IP is visible under CQL"""
        fprint(self, "TC_ID:16716:Test case to verify that the url created by quick create IP is visible under CQL")
        create_intel(self, "URL", self.url, self.url)
        self.click_cql()
        sleep(5)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("URL")
        self.verify_data(self.url)
        fprint(self, "[Passed]-The url created is visible under CQL")

    def test_17_verify_quick_create_email(self):
        """ Test case to verify that the email address that is created using quick create ip is visible under CQL"""
        fprint(self,
               "TC_ID 16717: to verify that the email address that is created using quick create ip is visible under CQL")
        create_intel(self, "Email Address", self.email, self.email)
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("Email addr")
        self.verify_data(self.email)
        fprint(self, "[Passed]-The email created is visible under CQL")

    def test_18_verify_quick_create_md5(self):
        """ Test case to verify that md5 that is created by quick add is visible under cql"""
        fprint(self, "TC_ID 16718: to verify that md5 that is created by quick add is visible under cql")
        create_intel(self, "MD5", self.md5, self.md5)
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("MD5")
        self.verify_data(self.md5)
        fprint(self, "[Passed]-The md5 created is visible under CQL")

    def test_19_verify_quick_create_sha1(self):
        """ Test cast to verify that sha1 that is created by quick add is visible under cql"""
        fprint(self, "TC_ID 16719:  to verify that sha1 that is created by quick add is visible under cql ")
        create_intel(self, "SHA1", self.sha1, self.sha1)
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("SHA1")
        self.verify_data(self.sha1)
        fprint(self, "[Passed]-The sha1 created is visible under CQL")

    def test_20_verify_quick_create_sha224(self):
        """ Test case to verify that sha224 that is created by quick add is visible under cql"""
        fprint(self, "TC_ID 16720: to verify that sha224 that is created by quick add is visible under cql")
        create_intel(self, "SHA224", self.sha224, self.sha224)
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("SHA224")
        self.verify_data(self.sha224)
        fprint(self, "[Passed]-The sha224 created is visible under CQL")

    def test_21_verify_quick_create_sha256(self):
        """ Test case to verify that sha256 that is created using quick add is visible under cql"""
        fprint(self, "TC_ID 16721:to verify that sha256 that is created by quick add is visible under cql ")
        create_intel(self, "SHA256", self.sha256, self.sha256)
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("SHA256")
        self.verify_data(self.sha256)
        fprint(self, "[Passed]-The sha256 created is visible under CQL")

    def test_22_verify_quick_create_sha384(self):
        """ Test case to verify that sha384 that is created using quick add is visible under cql"""
        fprint(self, "TC_ID 16722:to verify that sha384 that is created by quick add is visible under cql ")
        create_intel(self, "SHA384", self.sha384, self.sha384)
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("SHA384")
        self.verify_data(self.sha384)
        fprint(self, "[Passed]-The sha384 created is visible under CQL")

    def test_23_verify_quick_create_ssdeep(self):
        """ Test case to verify that ssdeep that is created using quickadd is visible under cql"""
        fprint(self, "TC_ID 16723:to verify that ssdeep that is created by quick add is visible under cql ")
        create_intel(self, "SSDEEP", self.ssdeep, self.ssdeep)
        self.click_cql()
        sleep(2)  # mandatory
        self.select_initial_steps_()
        self.select_from_dropdown("SSDEEP")
        self.verify_data(self.ssdeep)
        fprint(self, "[Passed]-The ssdeep created is visible under CQL")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())