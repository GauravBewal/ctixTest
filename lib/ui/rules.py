from lib.ui.nav_app import *
from lib.common_functions import *
from selenium.webdriver.common.by import By
from lib.ui.integration_management import launch_qradar

rule_ip_pattern = "221.221.221"
tag_ip_pattern = "221.221.229"
update_tag_old_ip = tag_ip_pattern+".3"
update_tag_new_ip = tag_ip_pattern+".4"
ref_set_ip_pattern  = "221.221.222"
update_ref_set_old_ip = ref_set_ip_pattern+".5"
update_ref_set_new_ip = ref_set_ip_pattern+".6"
fp_ip_pattern = "221.221.223"
update_fp_old_ip = fp_ip_pattern+".13"
update_fp_new_ip = fp_ip_pattern+".14"
manual_ip_pattern = "221.221.224"
manual_review_old_ip = manual_ip_pattern+".15"
manual_review_new_ip = manual_ip_pattern+".16"
send_inbox_2dot_ip_pattern = "221.221.225"
send_inbox_2dot1_new_ip = send_inbox_2dot_ip_pattern+".17"
send_inbox_2dot1_old_ip = send_inbox_2dot_ip_pattern+".18"
allowed_ip_pattern = "221.221.226"
indicators_allowed_old_ip = allowed_ip_pattern+".19"
indicators_allowed_new_ip = allowed_ip_pattern+".20"
rule_domain_pattern = "default"
send_inbox_2dot0_old_domain = "default03.com"
send_inbox_2dot0_new_domain = "default04.com"
save_result_set_old_domain = "default112.com"
save_result_set_new_domain = "default122.com"
save_result_setV3_old_domain = "default132.com"
save_result_setV3_new_domain = "default142.com"
send_inbox_1dot_ip_pattern = "221.221.227"
send_inbox_1dotx_old_ip = send_inbox_1dot_ip_pattern+".30"
send_inbox_1dotx_new_ip = send_inbox_1dot_ip_pattern+".31"
coa_value = 'coa_01'
campaign_value = 'campaign_01'
intrusion_set_value = 'intrusion_set_01'
malware_value = 'zeus'
tool_value = 'tool01'
vulnerability_value = 'CVE-2022-00'
attack_pattern_value = 'phishing_01'
identity_value = 'identity01'
location_value = 'Australia'
infra_value = 'infra_01'
splunk_ip_pattern = "221.221.228"
update_splunk_lookup_old_ip = splunk_ip_pattern+".7"
update_splunk_lookup_new_ip = splunk_ip_pattern+".8"
rule_tag = "newtag-auto"
##publish values
threat_actor = "TA:00:02_publish"
vulnerability = "CVE-2022-publish"
coa = "coa_publish"
campaign = "campaign_publish"
intrusion_set = "intrusion_set_publish"
malware = "bitcoin_publish"
tool = "tool_publish"
attack_pattern = "ap_publish"
identity = "identity_publish"
location = 'Algeria'
infra = 'infra_publish'
publish_ip = "221.221.221.22"
publish_url = "https://www.systemtem.com"
publish_report = "https://www.sys123.com"
publish_md5 = "a18ca4003deb042bbee7a40f15e1970b"
publish_sha224 = "90a3ed9e32b2aaf4c61c410eb925426119e1a9dc53d4286ade99a809"
publish_sha256 = "755738e1051d65e3374bd38bad04f1de6cda492c6d516c61a64efc4164588ba3"
publish_sha384 = "fdbd8e75a67f29f701a4e040385e2e23986303ea10239211af907fcbb83578b3e417cb71ce646efd0819dd8c088de1bd"
publish_sha512 = "aed7ed7a5a0778659577e7dcf560b78a97435226bbb9e91efa7835f5e72d0d3059f3badef52ca83bbee8ec96926b02f97ad10cc722f6278e465a323c45806262"
publish_ssdeep = "24:ol9rfbzwjx5zkvbbi8rum4pp6rg5yg+q8wixhmc:qrfbzkx5l8sm4grq8wixht"
zscaler_whitelist_url_pattern = "https://demae{}smit.site"
zscaler_blacklist_url_pattern = "http://fiverr{}china.com"
csap_draft_pattern = "kontodaten{}.com"
csap_publish_pattern = "monttepaschi{}.com"
exabeam_context_pattern = "222.233.211"
phantom_playbook_pattern = "175.16.87"
phantom_playbook_v3_pattern = "175.16.90"
counter = 0


def create_basic_rule(self, name):
    """
        Function to fill in rule name
        Args:
            name: name of the rule to be created
        returns:
            None
    """
    if waitfor(self, 20, By.XPATH, "//button[contains(text(), 'New Rule')]", False):
        self.driver.find_element_by_xpath("//button[contains(text(), 'New Rule')]").click()
    if waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Enter Title*']", False):
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter Title*']").send_keys(name)
        self.driver.find_element_by_xpath("//button[normalize-space(text())='Add']").click()
    if waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Skip')]", False):
        self.driver.find_element_by_xpath("//button[contains(text(), 'Skip')]").click()
    sleep(2)
    fprint(self, "Filling in rule name")
    waitfor(self, 20, By.XPATH, "//div/preceding-sibling::div/div/div/input[@aria-placeholder='Rule Name *']")
    self.driver.find_element_by_xpath(
        "//div/preceding-sibling::div/div/div/input[@aria-placeholder='Rule Name *']").click()
    clear_field(self.driver.find_element_by_xpath(
        "//div/preceding-sibling::div/div/div/input[@aria-placeholder='Rule Name *']"))
    self.driver.find_element_by_xpath(
        "//div/preceding-sibling::div/div/div/input[@aria-placeholder='Rule Name *']").send_keys(name)
    waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Submit')]")
    fprint(self, "Clicking on Submit")
    self.driver.find_element_by_xpath("//button[contains(text(), 'Submit')]").click()


def disable_rule(self, rule_name):
    """Function to disable rule """
    nav_menu_main(self, "Rules")
    search(self, rule_name)
    waitfor(self, 20, By.XPATH, "(//span[contains(text(),'"+rule_name+"')]//ancestor::tr//span)[1]")
    ele = self.driver.find_element_by_xpath("(//span[contains(text(),'" + rule_name + "')]/ancestor::tr//span)[1]")
    action = ActionChains(self.driver).move_to_element(ele)
    action.click()
    action.perform()
    waitfor(self, 20, By.XPATH, "//button[contains(text(),'Bulk Actions')]")
    self.driver.find_element_by_xpath("//button[contains(text(),'Bulk Actions')]").click()
    if waitfor(self, 5, By.XPATH, "//li[@data-testaction='inactive-bulk']", False):
        self.driver.find_element_by_xpath("//li[@data-testaction='inactive-bulk']").click()
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Are you sure you want to deactivate')]")
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'Deactivate')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Deactivate')]").click()
    else:
        self.driver.find_element_by_xpath("//div//li[contains(text(),'Inactivate')]").click()
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Are you sure you want to inactivate')]")
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'Inactive')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Inactive')]").click()


def add_source(self, **kwargs):
    """
    Funtion to fill in source and collection in rules

    kwargs:
        source: Source for feeds on which rule is to be run
        collection: Collection of the selected source
        isall: if all sources and collection are to be selected
    """
    isall = kwargs.get('isall', None)
    source = kwargs.get("source", None)
    collection = kwargs.get("collection", None)
    if Build_Version.__contains__("3."):
        if isall:
            waitfor(self, 20, By.XPATH,
                    "//span[span[contains(text(), 'All Sources & Collections')]]/preceding-sibling::span/input")
            self.driver.find_element_by_xpath(
                "//span[span[contains(text(), 'All Sources & Collections')]]/preceding-sibling::span/input").click()
        else:
            sleep(2)
            self.driver.find_element_by_xpath("//div[p[contains(text(), 'Source and Collection')]]").click()
            waitfor(self, 10, By.XPATH, "//input[@aria-placeholder='Source and Collection']")
            self.driver.find_element_by_xpath("//input[@aria-placeholder='Source and Collection']").send_keys(source)
            waitfor(self, 20, By.XPATH, "//span[span[contains(text(), '"+source[:20]+"')]]/preceding-sibling::span/input")
            sleep(1)
            self.driver.find_element_by_xpath\
                ("//span[span[contains(text(), '"+source[:20]+"')]]/preceding-sibling::span").click()
            waitfor(self, 20, By.XPATH, "//span[span[contains(text(), '"+collection+"')]]/preceding-sibling::span/input")
            sleep(1)
            self.driver.find_element_by_xpath\
                ("//div[div/span[span[contains(text(), '"+collection+"')]]/preceding-sibling::span]").click()
    else:
        if isall:
            waitfor(self, 20, By.XPATH, "//span[span[contains(text(), 'Allow all Sources')]]/preceding-sibling::span")
            self.driver.find_element_by_xpath\
                ("//span[span[contains(text(), 'Allow all Sources')]]/preceding-sibling::span").click()
        else:
            waitfor(self, 20, By.XPATH, "//a[contains(text(), 'Intel Packages')]")
            self.driver.find_element_by_xpath("//a[contains(text(), 'Intel Packages')]").click()
            fprint(self, "Selecting Source for rule execution")
            sleep(1)
            waitfor(self, 20, By.XPATH, "//div[div/span[text()=' Source ']]")
            self.driver.find_element_by_xpath("//div[div/span[text()=' Source ']]").click()
            sleep(2)
            self.driver.find_element_by_xpath("//input[@placeholder='Search']").send_keys(source)
            waitfor(self, 20, By.XPATH, "//li//div[contains(text(), '"+source+"')]")
            self.driver.find_element_by_xpath("//li//div[contains(text(), '"+source+"')]").click()
            fprint(self, "Selecting collection to run rule upon")
            if collection == 'Select All':
                self.driver.find_element_by_xpath("//span[text()='All Collections']/preceding-sibling::span/span").click()
            else:
                waitfor(self, 20, By.XPATH, "//div[div/span[text()=' Collection ']]")
                self.driver.find_element_by_xpath("//div[div/span[text()=' Collection ']]").click()
                self.driver.find_element_by_xpath("//input[@placeholder='Search']").send_keys(collection)
                waitfor(self, 20, By.XPATH, "//li//div[contains(text(), '"+collection+"')]")
                self.driver.find_element_by_xpath("//li//div[contains(text(), '"+collection+"')]").click()
            sleep(10)


def add_condition_title(self, value):
    """
    Add condition for IP check in rule

    Args:
        value: value of ioc to be added in condition
    """
    sleep(1)
    fprint(self, "Selecting Condition from left panel")
    waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Conditions')]]")
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Conditions')]]").click()
    fprint(self, "Selecting Indicators from Conditions")
    waitfor(self, 20, By.XPATH, "//a[contains(text(), 'Indicator')]")
    self.driver.find_element_by_xpath("//a[contains(text(), 'Indicator')]").click()
    fprint(self, "Selecting Rule Type")
    waitfor(self, 20, By.XPATH, "//div/span[contains(text(), 'Rule Type')]")
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Rule Type')]]/following-sibling::div/div").click()
    fprint(self, "Adding title for indicator in Rule")
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Search ...']")
    self.driver.find_element_by_xpath("//input[@placeholder='Search ...']").send_keys("TITLE")
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'TITLE')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'TITLE')]").click()
    fprint(self, "Selecting CONTAINS as Selector")
    waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Selector')]]")
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Selector')]]/following-sibling::div/div").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'CONTAINS')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'CONTAINS')]").click()
    fprint(self, "Adding IP/Domain pattern to be checked")
    waitfor(self, 20, By.XPATH, "//div[input[@aria-placeholder='Value ']]")
    self.driver.find_element_by_xpath("//div[input[@aria-placeholder='Value ']]").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Value ']").send_keys(value)
    if Build_Version.__contains__("3."):
        if waitfor(self, 1, By.XPATH, "//span[span[contains(text(), 'Select Object for Actioning')]]/preceding-sibling::span/input[@value='false']", False):
            fprint(self, "Selecting Object for actioning checkbox")
            self.driver.find_element_by_xpath("//span[span[contains(text(), 'Select Object for Actioning')]]"
                                              "/preceding-sibling::span").click()
        #waitfor(self, 20, By.XPATH, "//div/span[contains(text(), 'Select Object')]")
        #self.driver.find_element_by_xpath("//div[span[contains(text(), 'Select Object')]]/following-sibling::div[div/span]").click()
        #fprint(self, "Selecting Indicator for actioning")
        #waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'Indicator')]")
        #self.driver.find_element_by_xpath("//li//div[contains(text(), 'Indicator')]").click()
    sleep(10)


def add_condition_indicators(self, type):
    """
     Add condition for indicator check in rule
    """
    if Build_Version.__contains__("3."):
        sleep(1)
        fprint(self, "Selecting Condition from left panel")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Conditions')]]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Conditions')]]").click()
        fprint(self, "Selecting Indicators from Conditions")
        waitfor(self, 20, By.XPATH, "//a[contains(text(), 'Indicator')]")
        self.driver.find_element_by_xpath("//a[contains(text(), 'Indicator')]").click()
        fprint(self, "Selecting Rule Type")
        waitfor(self, 20, By.XPATH, "//div/span[contains(text(), 'Rule Type')]")
        self.driver.find_element_by_xpath(
            "//div[span[contains(text(), 'Rule Type')]]/following-sibling::div/div").click()
        fprint(self, "Adding "+type+" as Rule type")
        waitfor(self, 20, By.XPATH, "//input[@placeholder='Search ...']")
        self.driver.find_element_by_xpath("//input[@placeholder='Search ...']").send_keys(type)
        waitfor(self, 20, By.XPATH, "//li//div[text() = '"+type+"']")
        self.driver.find_element_by_xpath("//li//div[text() = '"+type+"']").click()
        fprint(self, "Selecting ALL as Selector")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Selector')]]")
        self.driver.find_element_by_xpath(
            "//div[span[contains(text(), 'Selector')]]/following-sibling::div/div").click()
        waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'ALL')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(), 'ALL')]").click()
        if waitfor(self, 1, By.XPATH, "//span[span[contains(text(), 'Select Object for Actioning')]]/preceding-sibling::span/input[@value='false']", False):
            fprint(self, "Selecting Object for actioning checkbox")
            self.driver.find_element_by_xpath("//span[span[contains(text(), 'Select Object for Actioning')]]"
                                              "/preceding-sibling::span").click()
    else:
        fprint(self, "2.9")


def add_condition_domain_objects(self, object_type):
    """
    Add condition for SDO check in rule
    """
    if Build_Version.__contains__("3."):
        sleep(1)
        fprint(self, "Selecting Condition from left panel")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Conditions')]]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Conditions')]]").click()
        fprint(self, "Selecting "+object_type+" from Conditions")
        waitfor(self, 20, By.XPATH, "//a[contains(text(), '"+object_type+"')]")
        self.driver.find_element_by_xpath("//a[contains(text(), '"+object_type+"')]").click()
        fprint(self, "Selecting Rule Type")
        waitfor(self, 20, By.XPATH, "//div/span[contains(text(), 'Rule Type')]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Rule Type')]]/following-sibling::div/div").click()
        fprint(self, "Adding ALL as Rule type")
        waitfor(self, 20, By.XPATH, "//input[@placeholder='Search ...']")
        self.driver.find_element_by_xpath("//input[@placeholder='Search ...']").send_keys("ALL")
        waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'ALL')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(), 'ALL')]").click()
        if waitfor(self, 1, By.XPATH, "//span[span[contains(text(), 'Select Object for Actioning')]]/preceding-sibling::span/input[@value='false']", False):
            fprint(self, "Selecting Object for actioning checkbox")
            self.driver.find_element_by_xpath("//span[span[contains(text(), 'Select Object for Actioning')]]/preceding-sibling::span").click()
        if object_type == 'Report':
            waitfor(self, 20, By.XPATH, "//div[span[normalize-space()='Select Object']]")
            waitfor(self, 20, By.XPATH, "(//div[span[contains(text(),'Select Object')]]/following-sibling::div/div)[2]")
            # ele = self.driver.find_element_by_xpath("(//div[span[contains(text(),'Select Object')]]/following-sibling::div/div)[2]")
            # self.driver.execute_script("arguments[0].scrollIntoView(true);", ele)
            self.driver.find_element_by_xpath("(//div[span[contains(text(),'Select Object')]]/following-sibling::div/div)[2]").click()
            waitfor(self, 20, By.XPATH, "//div[contains(text(),'Indicator')]")
            self.driver.find_element_by_xpath("//div[contains(text(),'Indicator')]").click()
    else:
        fprint(self, "2.9")


def add_action_update_tag(self, tagname):
    """
    Function to add action update tag to selected intel

    Args:
        tagname: name of the tag to be added
    """
    sleep(1)
    rule_prefix = "(//div[text()='Update Tag']/ancestor::form)[2]"
    if not waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Update Tag')]", False):
        fprint(self, "Selecting Actions from left panel")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
        fprint(self, "Selecting Update Tag as action")
        waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Update Tag')]")
    self.driver.find_element_by_xpath("//a[contains(text(), 'Update Tag')]").click()
    fprint(self, "Selecting CTIX as application")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Application')]")
    self.driver.find_element_by_xpath\
        ("//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, rule_prefix+"//li//div[contains(text(), 'CTIX')]")
    self.driver.find_element_by_xpath(rule_prefix+"//li//div[contains(text(), 'CTIX')]").click()
    fprint(self, "Selrcting account to be worked upon")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
    self.driver.find_element_by_xpath\
        (rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'default account')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'default account')]").click()
    fprint(self, "Selecting operation to be carried out")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Operation')]")
    self.driver.find_element_by_xpath\
        (rule_prefix+"//div[span[contains(text(), 'Operation')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[div[contains(text(), 'Add')]]")
    self.driver.find_element_by_xpath("//li//div[div[contains(text(), 'Add')]]").click()
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Tags')]")
    fprint(self, "Selecting "+tagname+" as tag")
    self.driver.find_element_by_xpath\
        (rule_prefix+"//div[span[contains(text(), 'Tags')]]/following-sibling::div[div/span]").click()
    sleep(2)
    self.driver.find_element_by_xpath("//form//input[@placeholder='Search']").send_keys(tagname)
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), '"+tagname+"')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), '"+tagname+"')]").click()


def add_action_update_false_positive(self):
    """
        Function to add action update false positive to selected intel
    """
    rule_prefix = "(//div[text()='Update False Positive']/ancestor::form)[2]"
    if Build_Version.__contains__("3."):
        sleep(1)
        if not waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Update False Positive')]", False):
            fprint(self, "Selecting Actions from left panel")
            waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
            self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
            fprint(self, "Selecting Update false positive as action")
            waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Update False Positive')]")
        self.driver.find_element_by_xpath("//a[contains(text(), 'Update False Positive')]").click()
        fprint(self, "Selecting CTIX as application")
        waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Application')]")
        self.driver.find_element_by_xpath(rule_prefix+"//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
        waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'CTIX')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(), 'CTIX')]").click()
        fprint(self, "Selecting account to be worked upon")
        waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
        self.driver.find_element_by_xpath \
            (rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
        waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'default account')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(), 'default account')]").click()
        fprint(self, "Selecting False Positive status to be carried out")
        waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Update False Positive Status')]")
        self.driver.find_element_by_xpath \
                (rule_prefix+"//div[span[contains(text(), 'Update False Positive')]]/following-sibling::div[div/span]").click()
        waitfor(self, 20, By.XPATH, "//li//div[div[contains(text(), 'Mark')]]")
        self.driver.find_element_by_xpath("//li//div[div[contains(text(), 'Mark')]]").click()
    else:
        fprint(self, "2.9")


def add_action_send_inbox(self,source_name,collection):
    """
        Function to add action send inbox for 2dot
    """
    rule_prefix = "(//div[text()='Send Inbox']/ancestor::form)[2]"
    if not waitfor(self, 20, By.XPATH, "//a[contains(text(), 'Send Inbox')]", False):
        fprint(self, "Selecting Actions from left panel")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
        fprint(self, "Selecting send inbox as action")
        waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Send Inbox')]")
    self.driver.find_element_by_xpath("//a[contains(text(), 'Send Inbox')]").click()
    fprint(self, "Selecting CTIX as application")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Application')]")
    self.driver.find_element_by_xpath(
        rule_prefix+"//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'CTIX')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'CTIX')]").click()
    fprint(self, "Selecting account to be worked upon")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
    self.driver.find_element_by_xpath(
        rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'default account')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'default account')]").click()
    fprint(self, "Selecting Analyser - Fast & Light")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Analyser')]")
    self.driver.find_element_by_xpath(
        rule_prefix+"//div[span[contains(text(), 'Analyser')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'Fast & Light')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'Fast & Light')]").click()
    fprint(self, "Selecting Source")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Source')]")
    self.driver.find_element_by_xpath(
        rule_prefix+"//div[span[contains(text(), 'Source')]]/following-sibling::div[div/span]").click()
    self.driver.find_element_by_xpath("//div/span[contains(text(), 'Source')]//following::input[@placeholder='Search']").send_keys(source_name)
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), '"+source_name+"')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), '"+source_name+"')]").click()
    fprint(self,"Selecting Collection")
    waitfor(self,20,By.XPATH,rule_prefix+"//div/span[contains(text(), 'Collection')]")
    self.driver.find_element_by_xpath(
        rule_prefix+"//div[span[contains(text(), 'Collection')]]/following-sibling::div[div/span]").click()
    self.driver.find_element_by_xpath("//div/span[contains(text(), 'Collection')]//following::input[@placeholder='Search']").send_keys(collection)
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), '"+collection+"')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), '"+collection+"')]").click()


def add_action_publish_collection(self, collection_list=["col_1.x", "col_2.0", "col_2.1"]):
    rule_prefix = "(//div[text()='Publish To Collection']/ancestor::form)[2]"
    if not waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Publish To Collection')]", False):
        fprint(self, "Selecting Actions from left panel")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
        fprint(self, "Selecting Publish To Collection as action")
        waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Publish To Collection')]")
    self.driver.find_element_by_xpath("//a[contains(text(), 'Publish To Collection')]").click()
    fprint(self, "Selecting CTIX as application")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Application')]")
    self.driver.find_element_by_xpath(rule_prefix+"//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
    fprint(self, "Clicked on the Application dropdown")
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'CTIX')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'CTIX')]").click()
    fprint(self, "Selecting account to be worked upon")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
    self.driver.find_element_by_xpath(rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'default account')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'default account')]").click()
    fprint(self, "Selecting Analyser - Fast & Light")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Analyser')]")
    self.driver.find_element_by_xpath(rule_prefix+"//div[span[contains(text(), 'Analyser')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'Fast & Light')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'Fast & Light')]").click()
    # Need to improve below statements by using parameterized function
    # fprint(self, "Selecting Default account to send Email")
    # waitfor(self, 20, By.XPATH, "//div/span[contains(text(), 'Send Email')]")
    # self.driver.find_element_by_xpath("//div[span[contains(text(), 'Send Email')]]/following-sibling::div[div/span]").click()
    # waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'System Default')]")
    # self.driver.find_element_by_xpath("//li//div[contains(text(), 'System Default')]").click()
    fprint(self, "Selecting Server Collections")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Server Collection')]")
    self.driver.find_element_by_xpath(rule_prefix+"//div[span[contains(text(), 'Server Collection')]]/following-sibling::div[div/span]").click()
    for collection in collection_list:
        clear_field(self.driver.find_element_by_xpath("//div[span[normalize-space(text())='Server Collection']]/following-sibling::div//input"))
        self.driver.find_element_by_xpath("//div[span[normalize-space(text())='Server Collection']]/following-sibling::div//input").send_keys(collection)
        waitfor(self, 20, By.XPATH, f"//li//div[contains(text(), '{collection}')]")
        self.driver.find_element_by_xpath(f"//li//div[contains(text(), '{collection}')]").click()


def add_action_update_ref_set(self, set_name):
    """
    Function to add action update reference set

    Args:
        set_name: name of reference set to be used
    returns:
        None
    """
    rule_prefix = "(//div[text()='Update Reference Set']/ancestor::form)[2]"
    if not waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Update Reference Set')]", False):
        fprint(self, "Selecting Actions from left panel")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
        fprint(self, "Selecting Update Reference Set as action")
        waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Update Reference Set')]")
    self.driver.find_element_by_xpath("//a[contains(text(), 'Update Reference Set')]").click()
    fprint(self, "Selecting QRadar as application")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Application')]")
    self.driver.find_element_by_xpath \
        (rule_prefix+"//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
    if waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'Qradar')]", False):
        self.driver.find_element_by_xpath("//li//div[contains(text(), 'Qradar')]").click()
    elif waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'QRadar')]"):
        self.driver.find_element_by_xpath("//li//div[contains(text(), 'QRadar')]").click()
    fprint(self, "Selecting account to be worked upon")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
    self.driver.find_element_by_xpath \
        (rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'qrad')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'qrad')]").click()
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Reference Data Set')]")
    fprint(self, "Selecting "+set_name+" as reference set")
    self.driver.find_element_by_xpath\
        (rule_prefix+"//div[span[contains(text(), 'Reference Data Set')]]/following-sibling::div[div/span]").click()
    sleep(2)
    #Todo: Selector required here, request from shivam
    self.driver.find_element_by_xpath("//div[@class='cy-select-search']/input[@placeholder='Search']").send_keys(set_name)
    waitfor(self, 40, By.XPATH, "//li//div[contains(text(), '"+set_name+"')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), '"+set_name+"')]").click()
    fprint(self, "Selecting operation to be carried out")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Operation')]")
    self.driver.find_element_by_xpath\
        (rule_prefix+"//div[span[contains(text(), 'Operation')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[div[contains(text(), 'Add')]]")
    self.driver.find_element_by_xpath("//li//div[div[contains(text(), 'Add')]]").click()


def add_action_manual_review(self):
    """
    Function to add action update manual review
    """
    rule_prefix = "(//div[text()='Manual Review']/ancestor::form)[2]"
    if Build_Version.__contains__("3."):
        if not waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Manual Review')]", False):
            fprint(self, "Selecting Actions from left panel")
            waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
            self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
            fprint(self, "Selecting Manual Review as actions")
            waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Manual Review')]")
        self.driver.find_element_by_xpath("//a[contains(text(), 'Manual Review')]").click()
        fprint(self, "Selecting CTIX as application")
        waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Application')]")
        self.driver.find_element_by_xpath(
            rule_prefix+"//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
        waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'CTIX')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(), 'CTIX')]").click()
        fprint(self, "Selecting account to be worked upon")
        waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
        self.driver.find_element_by_xpath \
            (rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
        waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'default account')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(), 'default account')]").click()


def add_action_indicators_allowed(self):

    """
    Function to add action update indicators allowed
    """
    rule_prefix = "(//div[text()='Update Indicators Allowed']/ancestor::form)[2]"
    if Build_Version.__contains__("3."):
        if not waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Update Indicators Allowed')]", False):
            fprint(self, "Selecting Actions from left panel")
            waitfor(self, 30, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
            self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
            fprint(self, "Selecting Update Indicators Allowed as actions")
            waitfor(self, 20, By.XPATH, "//a[contains(text(), 'Update Indicators Allowed')]")
        self.driver.find_element_by_xpath("//a[contains(text(), 'Update Indicators Allowed')]").click()
        fprint(self, "Selecting CTIX as application")
        waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Application')]")
        self.driver.find_element_by_xpath(
            rule_prefix+"//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
        waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'CTIX')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(), 'CTIX')]").click()
        fprint(self, "Selecting account to be worked upon")
        waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
        self.driver.find_element_by_xpath \
            (rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
        waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'default account')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(), 'default account')]").click()
        waitfor(self, 20, By.XPATH, rule_prefix+"//div[span[contains(text(), 'Operation')]]")
        fprint(self, "Selecting Add as operation")
        self.driver.find_element_by_xpath \
            (rule_prefix+"//div[span[contains(text(), 'Operation')]]/following-sibling::div[div/span]").click()
        waitfor(self, 20, By.XPATH, "//li//div[div[contains(text(), 'Add')]]")
        self.driver.find_element_by_xpath("//li//div[div[contains(text(), 'Add')]]").click()
    else:
        fprint(self, "2.x")


def add_action_save_result_set(self, tagname, threat_data_object):
    """
    Function to add action save result set
    """
    rule_prefix = "(//div[text()='Save Result Set']/ancestor::form)[2]"
    if Build_Version.__contains__("3."):
        if not waitfor(self, 10, By.XPATH, "//a[normalize-space()='Save Result Set']", False):
            fprint(self, "selection actions from left panel")
            waitfor(self, 10, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
            self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
            fprint(self, "selecting save result set as actions")
            waitfor(self, 10, By.XPATH, "//a[normalize-space()='Save Result Set']")
        self.driver.find_element_by_xpath("//a[normalize-space()='Save Result Set']").click()
        fprint(self, "selecting CTIX as application")
        waitfor(self, 10, By.XPATH, rule_prefix+"//div[span[contains(text(), 'Application')]]")
        self.driver.find_element_by_xpath\
            (rule_prefix+"//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
        waitfor(self, 10, By.XPATH, "//li//div[contains(text(), 'CTIX')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(), 'CTIX')]").click()
        fprint(self, "Selecting account to be worked upon")
        waitfor(self, 10, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
        self.driver.find_element_by_xpath \
            (rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
        waitfor(self, 10, By.XPATH, "//li//div[contains(text(), 'default account')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(), 'default account')]").click()
        fprint(self, "Selecting Tag")
        waitfor(self, 10, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Tags')]")
        self.driver.find_element_by_xpath \
            (rule_prefix+"//div[span[contains(text(), 'Tags')]]/following-sibling::div[div/span]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//form//input[@placeholder='Search']").send_keys(tagname)
        waitfor(self, 20, By.XPATH, "//li//div[contains(text(), '" + tagname + "')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(), '" + tagname + "')]").click()
        self.driver.find_element_by_xpath \
            ("//div[span[contains(text(), 'Tags')]]/following-sibling::div[div/span]").click()
        fprint(self, "Selecting Threat Data Objects")
        waitfor(self, 10, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Threat Data Objects')]")
        self.driver.find_element_by_xpath \
            (rule_prefix+"//div[span[contains(text(), 'Threat Data Objects')]]/following-sibling::div[div/span]").click()
        fprint(self, "Selecting indicators as Threat Data Objects")
        waitfor(self, 10, By.XPATH, "//li//div[contains(text(), '"+ threat_data_object +"')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(), '"+threat_data_object+"')]").click()
        waitfor(self, 10, By.XPATH, "//button[text()='Save']")
    else:
        fprint(self, "2.x")


def add_action_save_result_setV3(self, tagname):
    """
    Function to add action save result set
    """
    rule_prefix = "(//div[text()='Save Result Set V3']/ancestor::form)[2]"
    if Build_Version.__contains__("3."):
        if not waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Save Result Set V3')]", False):
            fprint(self, "selection actions from left panel")
            waitfor(self, 10, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
            self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
            fprint(self, "selecting save result set as actions")
            waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Save Result Set V3')]")
        self.driver.find_element_by_xpath("//a[contains(text(), 'Save Result Set V3')]").click()
        fprint(self, "selecting CTIX as application")
        waitfor(self, 10, By.XPATH, rule_prefix+"//div[span[contains(text(), 'Application')]]")
        self.driver.find_element_by_xpath\
            (rule_prefix+"//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
        waitfor(self, 10, By.XPATH, "//li//div[contains(text(), 'CTIX')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(), 'CTIX')]").click()
        fprint(self, "Selecting account to be worked upon")
        waitfor(self, 10, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
        self.driver.find_element_by_xpath \
            (rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
        waitfor(self, 10, By.XPATH, "//li//div[contains(text(), 'default account')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(), 'default account')]").click()
        fprint(self, "Selecting Tag")
        waitfor(self, 10, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Tags')]")
        self.driver.find_element_by_xpath \
            (rule_prefix+"//div[span[contains(text(), 'Tags')]]/following-sibling::div[div/span]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//form//input[@placeholder='Search']").send_keys(tagname)
        waitfor(self, 20, By.XPATH, "//li//div[contains(text(), '" + tagname + "')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(), '" + tagname + "')]").click()
    else:
        fprint(self, "2.x")


def add_action_update_lookup_table(self, table_name):
    """
        Function to add action to update lookup table
    """
    rule_prefix = "(//div[text()='Update Lookup Table']/ancestor::form)[2]"
    if not waitfor(self, 20, By.XPATH, "//a[contains(text(), 'Update Lookup Table')]", False):
        fprint(self, "Selecting Actions from left panel")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
        fprint(self, "Selecting Update Lookup Table as action")
        waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Update Lookup Table')]")
    self.driver.find_element_by_xpath("//a[contains(text(), 'Update Lookup Table')]").click()
    fprint(self, "Selecting Splunk as application")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Application')]")
    self.driver.find_element_by_xpath \
        (rule_prefix+"//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'Splunk')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'Splunk')]").click()
    fprint(self, "Selecting account to be worked upon")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
    self.driver.find_element_by_xpath \
        (rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'splunk')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'splunk')]").click()
    waitfor(self, 20, By.XPATH, rule_prefix+"//div[div[span[contains(text(), 'Lookup Table')]]]")
    self.driver.find_element_by_xpath(rule_prefix+"//div[div[span[contains(text(), 'Lookup Table')]]]").click()
    waitfor(self, 20, By.XPATH, "//input[@name='search-input'][@placeholder='Search']")
    self.driver.find_element_by_xpath("//input[@name='search-input'][@placeholder='Search']").send_keys(table_name)
    waitfor(self, 20, By.XPATH, "//div[contains(text(), '"+table_name+"')]")
    self.driver.find_element_by_xpath("//div[contains(text(), '"+table_name+"')]").click()
    waitfor(self, 20, By.XPATH, rule_prefix+"//div[div[span[contains(text(), 'Fields')]]]")
    self.driver.find_element_by_xpath(rule_prefix+"//div[div[span[contains(text(), 'Fields')]]]").click()
    _fields = self.driver.find_elements_by_xpath("//ul[@id='dropdown-list']/li")
    for i in _fields:
        fprint(self, "Clicking on "+i.text)
        i.click()
    sleep(5)


def check_splunk_fields(self, **kwargs):
    """
        Function to validate fields populated in splunk
        kwargs:
            criticality: criticality of the provided IOC
            cyware_score: Confidence Score of the provided IOC
            severity: severity of the provided IOC
            tlp: TLP of the provided IOC
            type: Type of IOC provided
            value: title or name of the IOC
    """
    fails = []
    criticality = kwargs.get("criticality", "UNKNOWN")
    cyware_score = kwargs.get("cyware_score", "UNKNOWN")
    severity = kwargs.get("severity", "UNKNOWN")
    tlp = kwargs.get("tlp")
    type = kwargs.get("type")
    value = kwargs.get("value")
    value_list = [cyware_score, severity, tlp, type, value]
    fprint(self, "Clicking on Lookup Editor")
    waitfor(self, 20, By.XPATH, "//div[@data-appid='lookup_editor']")
    sleep(5)    # required
    self.driver.find_element_by_xpath("//div[@data-appid='lookup_editor']").click()
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Filter by name']")
    fprint(self, "Searching for created lookup table")
    self.driver.find_element_by_xpath("//input[@placeholder='Filter by name']").send_keys(get_value("Splunk Lookup"))
    waitfor(self, 20, By.XPATH, "//a[text()='" + get_value("Splunk Lookup") + "']")
    sleep(2)
    fprint(self, "Clicking on created lookup table")
    self.driver.find_element_by_xpath("//a[text()='" + get_value("Splunk Lookup") + "']").click()
    waitfor(self, 20, By.XPATH, "//h2[contains(text(), '" + get_value("Splunk Lookup") + "')]")
    clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Search lookup']"))
    fprint(self, "Searching for value in Splunk Lookup")
    self.driver.find_element_by_xpath("//input[@placeholder='Search lookup']").send_keys(value)
    _theads = self.driver.find_elements_by_xpath("//thead/tr/td")[1:]
    _tbody = self.driver.find_elements_by_xpath("//tbody/tr/td")[1:]
    if len(_tbody) == 0:
        fprint(self, "No Entry for "+value+" found")
        for i in _theads:
            fails.append(i.text)
    for i, j, k in zip(_theads, _tbody, value_list):
        fprint(self, "Value for " + i.text + " is set as " + j.text)
        if j.text == "UNKNOWN" and i.text not in ['Severity', 'Criticality', 'Cyware Score']:
            fails.append(i.text)
        elif j.text != str(k):
            fails.append(i.text)
    return fails


def add_action_cortex_trigger_playbook(self, **kwargs):
    """
        Function to add action for trigger playbook on CORTEX SOAR
        kwargs:
            v3: Version of Trigger playbook
    """
    v3 = kwargs.get("v3", False)
    _action_name = 'Trigger Playbook'
    if v3:
        _action_name = 'Trigger Playbook V3'
    rule_prefix = f"(//div[text()='{_action_name}']/ancestor::form)[2]"
    sleep(1)
    if not waitfor(self, 10, By.XPATH, "//a[text()='"+_action_name+"']", False):
        fprint(self, "Selecting Actions from left panel")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
        fprint(self, "Selecting Update Tag as action")
        waitfor(self, 10, By.XPATH, "//a[text()='"+_action_name+"']")
    self.driver.find_element_by_xpath("//a[text()='"+_action_name+"']").click()
    fprint(self, "Selecting CORTEX-SOAR as application")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Application')]")
    self.driver.find_element_by_xpath\
        (rule_prefix+"//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'CORTEX-XSOAR')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'CORTEX-XSOAR')]").click()
    fprint(self, "Selecting account to be worked upon")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
    self.driver.find_element_by_xpath\
        (rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'cortex')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'cortex')]").click()
    fprint(self, "Selecting Event to be worked upon")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Event')]")
    self.driver.find_element_by_xpath\
        (rule_prefix+"//div[span[contains(text(), 'Event')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Event')]]/following-sibling::div/input")
    sleep(5)    # required
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Event')]]/following-sibling::div/input").\
        send_keys(get_value("CORTEX_INCIDENT"))
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), '"+get_value("CORTEX_INCIDENT")+"')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), '"+get_value("CORTEX_INCIDENT")+"')]").click()
    if not v3:
        waitfor(self, 20, By.XPATH, "//div/span[contains(text(), 'Threat Data Objects')]")
        fprint(self, "Selecting Indicator as IOC")
        self.driver.find_element_by_xpath\
            ("//div[span[contains(text(), 'Threat Data Objects')]]/following-sibling::div[div/span]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//li[div/div/div[text()='indicators']]").click()

def add_action_zscaler(self, **kwargs):
    """
        Function to add action to be run in ZScaler
        kwargs:
            action: name of the action (whitelist or blacklist)
    """
    action = kwargs.get("action")
    _action_name = "Update Whitelist URLs"
    _action_name2 = "Update Zscaler Allowlist Url"
    if action == 'blacklist':
        _action_name = "Update Blacklist URL"
        _action_name2 = "Update Zscaler Denylist Url"
    if not waitfor(self, 5, By.XPATH, "//a[contains(text(), '" + _action_name + "')]", False):
        fprint(self, "Selecting Actions from left panel")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
    elif not waitfor(self, 5, By.XPATH, "//a[contains(text(), '" + _action_name2 + "')]", False):
        fprint(self, "Selecting Actions from left panel")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
    fprint(self, "Selecting Update Whitelist URLs as action")
    if action == 'whitelist':
        if waitfor(self, 10, By.XPATH, "//a[contains(text(), '" + _action_name + "')]", False):
            self.driver.find_element_by_xpath("//a[contains(text(), '" + _action_name + "')]").click()
        else:
            self.driver.find_element_by_xpath("//a[contains(text(), 'Update Zscaler Allowlist Url')]").click()
            _action_name = "Update Zscaler Allowlist Url"
    elif action == 'blacklist':
        if waitfor(self, 10, By.XPATH, "//a[contains(text(), '" + _action_name + "')]", False):
            self.driver.find_element_by_xpath("//a[contains(text(), '" + _action_name + "')]").click()
        else:
            self.driver.find_element_by_xpath("//a[contains(text(), 'Update Zscaler Denylist Url')]").click()
            _action_name = "Update Zscaler Denylist Url"
    rule_prefix = f"(//div[text()='{_action_name}']/ancestor::form)[2]"
    fprint(self, "Selecting Zscaler Network Security as application")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Application')]")
    self.driver.find_element_by_xpath \
        (rule_prefix+"//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'Zscaler Network Security')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'Zscaler Network Security')]").click()
    fprint(self, "Selecting account to be worked upon")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
    self.driver.find_element_by_xpath \
        (rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'zscaler')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'zscaler')]").click()
    fprint(self, "Selecting Operation to be performed")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Operation')]")
    self.driver.find_element_by_xpath \
        (rule_prefix+"//div[span[contains(text(), 'Operation')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Operation')]]/following-sibling::div/input")
    sleep(5)  # required
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Operation')]]/following-sibling::div/input"). \
        send_keys("Add")
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'Add')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'Add') and @name='text']").click()


def add_action_exabeam(self):
    """
        Function to add Update Context table action to rule
    """
    _action_name = "Update Context Table"
    rule_prefix = f"(//div[text()='{_action_name}']/ancestor::form)[2]"
    if not waitfor(self, 20, By.XPATH, "//a[contains(text(), '" + _action_name + "')]", False):
        fprint(self, "Selecting Actions from left panel")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
        fprint(self, "Selecting Update Context Table as action")
        waitfor(self, 20, By.XPATH, "//a[contains(text(), '" + _action_name + "')]")
    self.driver.find_element_by_xpath("//a[contains(text(), '" + _action_name + "')]").click()
    fprint(self, "Selecting Exabeam as application")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Application')]")
    self.driver.find_element_by_xpath \
        (rule_prefix+"//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'Exabeam')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'Exabeam')]").click()
    fprint(self, "Selecting account to be worked upon")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
    self.driver.find_element_by_xpath \
        (rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'exabeam')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'exabeam')]").click()
    _table_name = get_value("ex_context_table")
    fprint(self, "Selecting Context Table to be used as - "+_table_name)
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Context Tables')]")
    self.driver.find_element_by_xpath \
        (rule_prefix+"//div[span[contains(text(), 'Context Tables')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Context Tables')]]/following-sibling::div/input")
    sleep(5)  # required
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Context Tables')]]/following-sibling::div/input"). \
        send_keys(_table_name)
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), '"+_table_name+"')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), '"+_table_name+"')]").click()


def add_action_splunk_phantom(self, **kwargs):
    """
        Function to add action for trigger playbook Splunk Phantom
        kwargs:
            v3: Version of Trigger playbook
    """
    v3 = kwargs.get("v3", False)
    _action_name = 'Trigger Playbook'
    if v3:
        _action_name = 'Trigger Playbook V3'
    rule_prefix = f"(//div[text()='{_action_name}']/ancestor::form)[2]"
    sleep(1)
    if not waitfor(self, 20, By.XPATH, "//a[normalize-space(text())= '"+_action_name+"']", False):
        fprint(self, "Selecting Actions from left panel")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
        fprint(self, "Selecting Update Tag as action")
        waitfor(self, 10, By.XPATH, "//a[normalize-space(text())= '"+_action_name+"']")
    self.driver.find_element_by_xpath("//a[normalize-space(text())= '"+_action_name+"']").click()
    fprint(self, "Selecting CORTEX-SOAR as application")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Application')]")
    self.driver.find_element_by_xpath\
        (rule_prefix+"//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'Splunk Phantom')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'Splunk Phantom')]").click()
    fprint(self, "Selecting account to be worked upon")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
    self.driver.find_element_by_xpath\
        (rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'phantom')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'phantom')]").click()
    fprint(self, "Selecting Event to be worked upon")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Event')]")
    self.driver.find_element_by_xpath\
        (rule_prefix+"//div[span[contains(text(), 'Event')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Event')]]/following-sibling::div/input")
    sleep(5)    # required
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Event')]]/following-sibling::div/input").\
        send_keys("events")
    waitfor(self, 20, By.XPATH, rule_prefix+"//li//div[contains(text(), 'events')]")
    self.driver.find_element_by_xpath(rule_prefix+"//li//div[contains(text(), 'events')]").click()
    if not v3:
        waitfor(self, 20, By.XPATH, "//div/span[contains(text(), 'Threat Data Objects')]")
        fprint(self, "Selecting Indicator as IOC")
        self.driver.find_element_by_xpath\
            ("//div[span[contains(text(), 'Threat Data Objects')]]/following-sibling::div[div/span]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//li[div/div/div[text()='indicators']]").click()


def add_action_csap(self, **kwargs):
    """
        Function to add action for create CSAP Alert action
        kwargs:
            action: publish type draft/published
    """
    _action = kwargs.get("action")
    _group_name = get_value("csap_recipient_group")
    _category_name = get_value("csap_category_name")
    rule_prefix = f"(//div[text()='Create CSAP Alert']/ancestor::form)[2]"
    if not waitfor(self, 20, By.XPATH, "//a[contains(text(), 'Create CSAP Alert')]", False):
        fprint(self, "Selecting Actions from left panel")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
        fprint(self, "Selecting Create CSAP Alert as action")
        waitfor(self, 10, By.XPATH, "//a[contains(text(), 'Create CSAP Alert')]")
    self.driver.find_element_by_xpath("//a[contains(text(), 'Create CSAP Alert')]").click()
    fprint(self, "Selecting CSAP as application")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Application')]")
    self.driver.find_element_by_xpath \
        (rule_prefix+"//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'CSAP')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'CSAP')]").click()
    fprint(self, "Selecting account to be worked upon as csap")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
    self.driver.find_element_by_xpath \
        (rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'csap')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'csap')]").click()
    fprint(self, f"Setting Group name to {_group_name}")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div[div[span[contains(text(), 'Group')]]]")
    self.driver.find_element_by_xpath(rule_prefix+"//div[div[span[contains(text(), 'Group')]]]").click()
    for i in range(5):
        if waitfor(self, 10, By.XPATH, "//div[normalize-space(text())='No results found']", False):
            self.driver.find_element_by_xpath(rule_prefix + "//div[div[span[contains(text(), 'Group')]]]").click()
        else:
            break
    waitfor(self, 20, By.XPATH, "//input[@name='search-input'][@placeholder='Search']")
    self.driver.find_element_by_xpath("//input[@name='search-input'][@placeholder='Search']").send_keys(_group_name)
    waitfor(self, 20, By.XPATH, "//div[contains(text(), '" + _group_name + "')]")
    self.driver.find_element_by_xpath("//div[contains(text(), '" + _group_name + "')]").click()
    self.driver.find_element_by_xpath("//div[div/div/div[text()='"+_group_name+"']]//following-sibling::"
                                      "div/div[@data-testaction='close']").click()
    fprint(self, f"Setting status as {_action}")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div[div[span[contains(text(), 'Status')]]]")
    self.driver.find_element_by_xpath(rule_prefix+"//div[div[span[contains(text(), 'Status')]]]").click()
    waitfor(self, 20, By.XPATH, "//div[contains(text(), '" + _action + "')]")
    self.driver.find_element_by_xpath("//div[contains(text(), '" + _action + "')]").click()
    fprint(self, f"Setting Category name to {_category_name}")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div[div[span[contains(text(), 'Category')]]]")
    self.driver.find_element_by_xpath(rule_prefix+"//div[div[span[contains(text(), 'Category')]]]").click()
    for i in range(5):
        if waitfor(self, 10, By.XPATH, "//div[normalize-space(text())='No results found']", False):
            self.driver.find_element_by_xpath(rule_prefix+"//div[div[span[contains(text(), 'Category')]]]").click()
        else:
            break
    waitfor(self, 20, By.XPATH, "//input[@name='search-input'][@placeholder='Search']")
    self.driver.find_element_by_xpath("//input[@name='search-input'][@placeholder='Search']").send_keys(_category_name)
    waitfor(self, 20, By.XPATH, "//div[contains(text(), '" + _category_name + "')]")
    self.driver.find_element_by_xpath("//div[contains(text(), '" + _category_name + "')]").click()
    sleep(5)


def add_action_csol(self, event, type="Trigger Playbook"):
    """
        Function to add action for trigger playbook of CSOL
    """
    rule_prefix = f"(//div[text()='{type}']/ancestor::form)[2]"
    if not waitfor(self, 10, By.XPATH, "//a[text()='"+type+"']", False):
        fprint(self, "Selecting Actions from left panel")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Actions')]]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Actions')]]").click()
        fprint(self, "Selecting "+type+" as action")
        waitfor(self, 10, By.XPATH, "//a[text()='"+type+"']")
    self.driver.find_element_by_xpath("//a[text()='"+type+"']").click()
    fprint(self, "Selecting CSOL as application")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Application')]")
    self.driver.find_element_by_xpath(rule_prefix+"//div[span[contains(text(), 'Application')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'CO')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'CO')]").click()
    fprint(self, "Selecting account to be worked upon")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Account')]")
    self.driver.find_element_by_xpath(rule_prefix+"//div[span[contains(text(), 'Account')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'CSOL')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'CSOL')]").click()
    fprint(self, "Selecting Event - citx_action")
    waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Event')]")
    self.driver.find_element_by_xpath(rule_prefix+"//div[span[contains(text(), 'Event')]]/following-sibling::div[div/span]").click()
    waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Event')]]/following-sibling::div/input")
    sleep(5)    # required
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Event')]]/following-sibling::div/input").send_keys(event)
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), '"+event+"')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), '"+event+"')]").click()
    if type == "Trigger Playbook":
        waitfor(self, 20, By.XPATH, rule_prefix+"//div/span[contains(text(), 'Threat Data Objects')]")
        fprint(self, "Selecting Indicator as IOC")
        self.driver.find_element_by_xpath(rule_prefix+"//div[span[contains(text(), 'Threat Data Objects')]]/following-sibling::div[div/span]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//li[div/div/div[text()='indicators']]").click()


def add_condition_tag(self, value):
    """
    Add condition for Tag check in rule
    Args:
        value: value of tag to be added in condition
    """
    sleep(1)
    fprint(self, "Selecting Condition from left panel")
    waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Conditions')]]")
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Conditions')]]").click()
    fprint(self, "Selecting Indicators from Conditions")
    waitfor(self, 20, By.XPATH, "//a[contains(text(), 'Indicator')]")
    self.driver.find_element_by_xpath("//a[contains(text(), 'Indicator')]").click()
    fprint(self, "Selecting Rule Type")
    waitfor(self, 20, By.XPATH, "//div/span[contains(text(), 'Rule Type')]")
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Rule Type')]]/following-sibling::div/div").click()
    self.driver.find_element_by_xpath("//input[@name='search-input']").send_keys("TAGS")
    waitfor(self, 5, By.XPATH, "//div[@name='text' and contains(text(),'TAGS')]")
    self.driver.find_element_by_xpath("//div[@name='text' and contains(text(),'TAGS')]").click()
    fprint(self, "Selecting EQUAL as Selector")
    waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Selector')]]")
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Selector')]]/following-sibling::div/div").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'EQUAL')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'EQUAL')]").click()
    fprint(self, "Adding Tag name to be checked")
    waitfor(self, 20, By.XPATH, "//span[contains(text(),'Value')]")
    self.driver.find_element_by_xpath("//span[contains(text(),'Value')]/parent::div/following-sibling::div[2]/div[@data-testaction='close']").click()
    self.driver.find_element_by_xpath("//input[@name='search-input']").send_keys(value)
    waitfor(self, 10, By.XPATH, "//div[@name='text' and contains(text(),'"+value+"')]")
    self.driver.find_element_by_xpath("//div[@name='text' and contains(text(),'"+value+"')]").click()
    if Build_Version.__contains__("3."):
        if waitfor(self, 1, By.XPATH, "//span[span[contains(text(), 'Select Object for Actioning')]]/preceding-sibling::span/input[@value='false']", False):
            fprint(self, "Selecting Object for actioning checkbox")
            self.driver.find_element_by_xpath("//span[span[contains(text(), 'Select Object for Actioning')]]"
                                              "/preceding-sibling::span").click()


def run_rule_for_previous_feeds(self):
    waitfor(self, 20, By.XPATH, "//div[contains(text(), 'Run Rule')]")
    fprint(self, "Filling in Start Date and Time")
    self.driver.find_elements_by_xpath("//div[@mintime='10:00:00']/input")[0].click()
    sleep(2)
    self.driver.find_element_by_xpath("//td[div/span][@class='available today']").click()
    sleep(2)
    self.driver.find_element_by_xpath("//td[div/span][@class='available today current']").click()
    if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-expand']", False):
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-expand']").click()
    else:
        self.driver.find_element_by_xpath("//div[normalize-space(text())='Run Rule']").click()
    sleep(2)
    fprint(self, "Filling in End Date and Time")
    self.driver.find_elements_by_xpath("//div[@mintime='10:00:00']/input")[1].click()
    sleep(2)
    self.driver.find_element_by_xpath("//td[@class='available today']/div").click()
    if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-collapse']", False):
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-collapse']").click()
    else:
        self.driver.find_element_by_xpath("//div[normalize-space(text())='Run Rule']").click()
    sleep(2)
    fprint(self, "Clicking on run")
    self.driver.find_element_by_xpath("//button[contains(text(), 'Run')]").click()
    sleep(60)   # Increases the sleep time to 60 seconds


def add_condition_confidence_score(self, comparator, value):
    """
    Function to add condition to handle confidence score

    params:
        comparator: specifies the condition to be added
        value: specifies the value to be used in the condition
    """
    sleep(1)
    fprint(self, "Selecting Condition from left panel")
    waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Conditions')]]")
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Conditions')]]").click()
    fprint(self, "Selecting Indicators from Conditions")
    waitfor(self, 20, By.XPATH, "//a[contains(text(), 'Indicator')]")
    self.driver.find_element_by_xpath("//a[contains(text(), 'Indicator')]").click()
    fprint(self, "Selecting Rule Type")
    waitfor(self, 20, By.XPATH, "//div/span[contains(text(), 'Rule Type')]")
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Rule Type')]]/following-sibling::div/div").click()
    fprint(self, "Adding title for indicator in Rule")
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Search ...']")
    self.driver.find_element_by_xpath("//input[@placeholder='Search ...']").send_keys("CTIX CONFIDENCE SCORE")
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'CTIX CONFIDENCE SCORE')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'CTIX CONFIDENCE SCORE')]").click()
    fprint(self, f"Selecting {comparator} as Selector")
    waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Selector')]]")
    self.driver.find_element_by_xpath(
        "//div[span[contains(text(), 'Selector')]]/following-sibling::div/div").click()
    waitfor(self, 20, By.XPATH, f"//li//div[text()='{comparator}']")
    self.driver.find_element_by_xpath(f"//li//div[text()='{comparator}']").click()
    fprint(self, "Adding Value to be used for confidence score")
    waitfor(self, 20, By.XPATH, "//div[input[@aria-placeholder='Value ']]")
    self.driver.find_element_by_xpath("//div[input[@aria-placeholder='Value ']]").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Value ']").send_keys(value)
    if waitfor(self, 1, By.XPATH, "//span[span[contains(text(), 'Select Object for Actioning')]]/preceding-sibling::span/input[@value='false']", False):
        fprint(self, "Selecting Object for actioning checkbox")
        self.driver.find_element_by_xpath("//span[span[contains(text(), 'Select Object for Actioning')]]")

def add_condition_ioc_All(self, ioc_type):
    """
         Add condition for specific ioc type and Selector:ALL in rule
    """
    global counter
    print("counter - ", counter)
    if Build_Version.__contains__("3."):
        sleep(1)
        if counter == 0:
            fprint(self, "Selecting Condition from left panel")
            waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Conditions')]]")
            self.driver.find_element_by_xpath("//div[span[contains(text(), 'Conditions')]]").click()
            fprint(self, "Selecting Indicators from Conditions")
            waitfor(self, 20, By.XPATH, "//a[contains(text(), 'Indicator')]")
            self.driver.find_element_by_xpath("//a[contains(text(), 'Indicator')]").click()
        fprint(self, "Selecting Rule Type")

        if counter == 0:
            waitfor(self, 20, By.XPATH, "//div/span[contains(text(), 'Rule Type')]")
            self.driver.find_element_by_xpath(
                "//div[span[contains(text(), 'Rule Type')]]/following-sibling::div/div[@data-testaction='close']").click()
        else:
            waitfor(self, 20, By.XPATH, "(//div/span[contains(text(), 'Rule Type')])[2]")
            self.driver.find_element_by_xpath(
                "(//div[span[contains(text(), 'Rule Type')]]/following-sibling::div/div[@data-testaction='close'])[2]").click()
        fprint(self, "Adding DOMAIN as Rule type")
        waitfor(self, 20, By.XPATH, "//input[@placeholder='Search ...']")
        self.driver.find_element_by_xpath("//input[@placeholder='Search ...']").send_keys(ioc_type)
        waitfor(self, 20, By.XPATH, "//li//div[text() = '"+ioc_type+"']")
        self.driver.find_element_by_xpath("//li//div[text() = '"+ioc_type+"']").click()
        fprint(self, "Selecting ALL as Selector")

        if counter == 0:
            waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Selector')]]")
            self.driver.find_element_by_xpath(
                "//div[span[contains(text(), 'Selector')]]/following-sibling::div/div").click()
            waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'ALL')]")
            self.driver.find_element_by_xpath("//li//div[contains(text(), 'ALL')]").click()
        else:
            waitfor(self, 20, By.XPATH, "(//div[span[contains(text(), 'Selector')]])[2]")
            self.driver.find_element_by_xpath(
                "(//div[span[contains(text(), 'Selector')]]/following-sibling::div/div[@data-testaction='close'])[2]").click()
            waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'ALL')]")
            self.driver.find_element_by_xpath("//li//div[contains(text(), 'ALL')]").click()
        if waitfor(self, 1, By.XPATH,
                   "//span[span[contains(text(), 'Select Object for Actioning')]]/preceding-sibling::span/input[@value='false']",
                   False):
            fprint(self, "Selecting Object for actioning checkbox")
            self.driver.find_element_by_xpath("//span[span[contains(text(), 'Select Object for Actioning')]]"
                                              "/preceding-sibling::span").click()
        counter = counter + 1
    else:
        fprint(self, "2.9")


def add_condition_indicator_all(self):
    """
            Add condition for Indicator ALL in rule
       """
    if Build_Version.__contains__("3."):
        sleep(1)
        fprint(self, "Selecting Condition from left panel")
        waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Conditions')]]")
        self.driver.find_element_by_xpath("//div[span[contains(text(), 'Conditions')]]").click()
        fprint(self, "Selecting Indicators from Conditions")
        waitfor(self, 20, By.XPATH, "//a[contains(text(), 'Indicator')]")
        self.driver.find_element_by_xpath("//a[contains(text(), 'Indicator')]").click()
        fprint(self, "Selecting Rule Type")
        waitfor(self, 20, By.XPATH, "//div/span[contains(text(), 'Rule Type')]")
        self.driver.find_element_by_xpath(
            "//div[span[contains(text(), 'Rule Type')]]/following-sibling::div/div").click()
        fprint(self, "Adding ALL as Rule type")
        waitfor(self, 20, By.XPATH, "//input[@placeholder='Search ...']")
        self.driver.find_element_by_xpath("//input[@placeholder='Search ...']").send_keys("ALL")
        waitfor(self, 20, By.XPATH, "//li//div[text() = 'ALL']")
        self.driver.find_element_by_xpath("//li//div[text() = 'ALL']").click()
        if waitfor(self, 1, By.XPATH,
                   "//span[span[contains(text(), 'Select Object for Actioning')]]/preceding-sibling::span/input[@value='false']",
                   False):
            fprint(self, "Selecting Object for actioning checkbox")
            self.driver.find_element_by_xpath("//span[span[contains(text(), 'Select Object for Actioning')]]"
                                              "/preceding-sibling::span").click()
    else:
        fprint(self, "2.9")


def select_operator(self, operator):
    """
    For Selecting the Operator between multiple operators
    """
    fprint(self, "Waiting for the Select Operator Link")
    waitfor(self, 5, By.XPATH, "//span[contains(text(),'Select Operator')]")
    self.driver.find_element_by_xpath("//span[contains(text(),'Select Operator')]").click()
    fprint(self, "Visible Clicked on it")
    waitfor(self, 5, By.XPATH, "//div[contains(text(),'"+operator+"')]/parent::li")
    try:
        self.driver.find_element_by_xpath("//div[contains(text(),'"+operator+"')]/parent::li").click()
    except:
        #   For handling third condition operator
        fprint(self, "Trying to click on the second occurrence")
        self.driver.find_element_by_xpath("(//div[contains(text(),'"+operator+"')]/parent::li)[2]").click()
    fprint(self, "Selected Operator - "+operator)


def search_object(self, value):
    waitfor(self, 10, By.XPATH, "//form//input[@placeholder='Search']")
    self.driver.find_element_by_xpath("//form//input[@placeholder='Search']").send_keys(value)


def verify_in_qradar(self, refset_name):
    fprint(self, "Launching QRadar")
    self.driver = launch_qradar(self)
    fprint(self, "Selecting Reference Set Management")
    waitfor(self, 60, By.XPATH, "html//table[@title='Reference Set Management']/tr/td/div")
    self.driver.find_element_by_xpath("html//table[@title='Reference Set Management']/tr/td/div").click()
    handles = self.driver.window_handles
    self.driver.switch_to.window(handles[1])
    sleep(10)
    fprint(self, "Searching for the created reference set")
    self.driver.find_element_by_xpath("//span[contains(text(), 'Input name')]/ancestor::div[input]").click()
    self.driver.find_element_by_xpath("//span[contains(text(), 'Input name')]/preceding-sibling::input").send_keys(refset_name)
    sleep(5)
    self.driver.find_element_by_xpath("//span[@title='Input name']").click()
    fprint(self, "Clikcing on the created reference set")
    waitfor(self, 60, By.XPATH, "//td[contains(text(), '"+refset_name+"')]")
    self.driver.find_element_by_xpath("//td[contains(text(), '"+refset_name+"')]").click()


def add_condition_report_title(self, report_title):
    """
        Function to add condition based on Report Title
    """
    sleep(1)
    fprint(self, "Selecting Condition from left panel")
    waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Conditions')]]")
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Conditions')]]").click()
    fprint(self, "Selecting Indicators from Conditions")
    waitfor(self, 20, By.XPATH, "//a[contains(text(), 'Report')]")
    self.driver.find_element_by_xpath("//a[contains(text(), 'Report')]").click()
    fprint(self, "Selecting Rule Type")
    fprint(self, "Selecting Rule Type")
    waitfor(self, 20, By.XPATH, "//div/span[contains(text(), 'Rule Type')]")
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Rule Type')]]/following-sibling::div/div").click()
    fprint(self, "Adding title for indicator in Rule")
    waitfor(self, 20, By.XPATH, "//input[@placeholder='Search ...']")
    self.driver.find_element_by_xpath("//input[@placeholder='Search ...']").send_keys("TITLE")
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'TITLE')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'TITLE')]").click()
    fprint(self, "Selecting CONTAINS as Selector")
    waitfor(self, 20, By.XPATH, "//div[span[contains(text(), 'Selector')]]")
    self.driver.find_element_by_xpath("//div[span[contains(text(), 'Selector')]]/following-sibling::div/div").click()
    waitfor(self, 20, By.XPATH, "//li//div[contains(text(), 'CONTAINS')]")
    self.driver.find_element_by_xpath("//li//div[contains(text(), 'CONTAINS')]").click()
    fprint(self, "Adding IP/Domain pattern to be checked")
    waitfor(self, 20, By.XPATH, "//div[input[@aria-placeholder='Value ']]")
    self.driver.find_element_by_xpath("//div[input[@aria-placeholder='Value ']]").click()
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Value ']").send_keys(report_title)
    waitfor(self, 20, By.XPATH, "//div[span[normalize-space()='Select Object']]")
    waitfor(self, 20, By.XPATH, "(//div[span[contains(text(),'Select Object')]]/following-sibling::div/div)[2]")
    self.driver.find_element_by_xpath(
        "(//div[span[contains(text(),'Select Object')]]/following-sibling::div/div)[2]").click()
    waitfor(self, 20, By.XPATH, "//div[contains(text(),'Indicator')]")
    self.driver.find_element_by_xpath("//div[contains(text(),'Indicator')]").click()
    _dropdown = self.driver.find_element_by_xpath("//ul[@id='dropdown-list']")
    verical_ordinate = 50
    for i in range(0, 6):
        self.driver.execute_script("arguments[0].scrollTop = arguments[1]", _dropdown, verical_ordinate)
        verical_ordinate += 500
        time.sleep(1)
    self.driver.find_element_by_xpath("//li//div[contains(text(),'Report')]").click()
