import unittest
from lib.ui.nav_app import *
from lib.ui.nav_threat_data import verify_data_in_threatdata


class ThreatInvestigation(unittest.TestCase):

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

    # This function helps in clicking a particular indicator
    def click_helper(self, val):
        waitfor(self, 3, By.XPATH, f"//li[contains(@data-node,'{val}')]")
        fprint(self, f"Clicked on {val}")
        self.driver.find_element_by_xpath(f"//li[contains(@data-node,'{val}')]").click()

    # This function helps in adding a particular value of a type
    def addValue_helper(self, val, key):
        waitfor(self, 3, By.XPATH, f"//input[@aria-placeholder = 'Enter {val}']")
        fprint(self, f"Provided value of {val}")
        self.driver.find_element_by_xpath(f"//input[@aria-placeholder = 'Enter {val}']").send_keys(f"{key}")
        fprint(self, f"{val} added on canvas")
        self.driver.find_element_by_xpath(f"//input[@aria-placeholder = 'Enter {val}']").send_keys(Keys.ENTER)

    # This function will helps in clicking on create new button
    def click_on_create_new(self):

        if waitfor(self, 4, By.XPATH, "//button[contains(text(), 'Create New')]", False):
            self.driver.find_element_by_xpath("//button[contains(text(), 'Create New')]").click()
        elif waitfor(self, 1, By.XPATH, "//span[contains(text(), 'Create New')]", False):
            self.driver.find_element_by_xpath("//span[contains(text(), 'Create New')]").click()
        if waitfor(self, 10, By.XPATH, "//input[@aria-placeholder='Enter Title*']", False):
            self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter Title*']").click()
            self.driver.find_element_by_xpath("//input[@aria-placeholder='Enter Title*']").send_keys("tmp_title")
            self.driver.find_element_by_xpath("//button[normalize-space(text())='Add']").click()
            fprint(self, "Clicked on add as this is the first canvas")
        fprint(self, "Clicked on Create New Button")

    # This function helps in adding title to canvas
    def add_Title(self, title):
        self.skip_walk_through()
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Untitled Canvas*']")
        fprint(self, "Providing the title of the canvas")
        clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Untitled Canvas*']"))
        self.driver.find_element_by_xpath("//input[@placeholder='Untitled Canvas*']").send_keys(f"{title}")

    # This function helps in skipping walk through is prompted
    def skip_walk_through(self):
        if waitfor(self, 2, By.XPATH, "//button[contains(text(),'SKIP')]", False):
            fprint(self, "Skipping the walkthrough")
            self.driver.find_element_by_xpath("//button[contains(text(),'SKIP')]").click()
            waitfor(self, 2, By.XPATH, "//button[contains(text(),'OK, GOT IT')]")
            fprint(self, "Clicked on Ok got it")
            self.driver.find_element_by_xpath("//button[contains(text(),'OK, GOT IT')]").click()

    # This function helps in clikcing on add node
    def click_on_add_node(self):
        waitfor(self, 3, By.XPATH, "//div[@id='sidebar-add']")
        fprint(self, "Clicked on add node")
        self.driver.find_element_by_xpath("//div[@id='sidebar-add']").click()

    # This function helps in clicking on Other SDO(s) option
    def click_on_other_sdo(self):
        waitfor(self, 2, By.XPATH, "//div / span[contains(text(), 'Other SDO(s)')]")
        fprint(self, "Clicked on other sdo(s)")
        self.driver.find_element_by_xpath("//div / span[contains(text(), 'Other SDO(s)')]").click()

    # This function helps in saving and creating intel
    def save_create_intel(self):
        waitfor(self, 3, By.XPATH, "//div[@id='visualizer-walkthrough']")
        fprint(self, "Clicked on three dot for creating intel")
        self.driver.find_element_by_xpath("//div[@id='visualizer-walkthrough']").click()

        waitfor(self, 3, By.XPATH, "//li[contains(text(),'Create Intel in CTIX')]")
        fprint(self, "Clicked on create intel in CTIX")
        self.driver.find_element_by_xpath("//li[contains(text(),'Create Intel in CTIX')]").click()

        verify_success(self, "You can view the created intel as a report object in the Threat Data module")
        sleep(.2)   # required multiple alerts coming up
        verify_success(self, "Canvas saved successfully")

    # This function helps in verifying whether intel is created or not
    def verfiy_intel_is_created_or_not(self, title):
        nav_menu_main(self, "Threat Investigations")
        waitfor(self, 3, By.XPATH, "//*[contains(text(),'Intel History')]")
        fprint(self, "Clicked on intel history")
        self.driver.find_element_by_xpath("//*[contains(text(),'Intel History')]").click()
        if waitfor(self, 20, By.XPATH, f"(//span[contains(text(),'{title}')]/ancestor::td/following-sibling::td[3]//span[contains(text(),'Created')])[1]", False):
            fprint(self, "[Passed] Intel is successfully created")
        else:
            fprint(self, "[Failed] Intel is not created, there must be some error occured")
            self.fail("[Failed] Intel is not created, there must be some error occured")
        waitfor(self, 3, By.XPATH, "//span[@data-testaction='slider-close']")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()

    def test_01_intel_creation_with_IPv4(self):
        fprint(self, "\n----------- TC_ID: 77001 Creating intel with IPv4")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("IPv4_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_helper('ipv4')
        self.addValue_helper('IPv4', "89.163.249.192")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("IPv4_canvas")

    def test_02_intel_creation_with_IPv6(self):
        fprint(self, "\n----------- TC_ID: 77002 Creating intel with IPv6")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("IPv6_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_helper('ipv6')
        self.addValue_helper('IPv6', "f8c6:f44b:9bc7:97e9:0b1c:3d03:3a9d:ee20")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("IPv6_canvas")

    def test_03_intel_creation_with_Domain(self):
        fprint(self, "\n----------- TC_ID: 77003 Creating intel with Domain")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Domain_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_helper('domain')
        self.addValue_helper('Domain', "daily.automation.com")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Domain_canvas")

    def test_04_intel_creation_with_URL(self):
        fprint(self, "\n----------- TC_ID: 77004 Creating intel with URL")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("URL_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_helper('url')
        self.addValue_helper('URL', "http://malicousurl.in/4712/")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("URL_canvas")

    def test_05_intel_creation_with_MD5(self):
        fprint(self, "\n----------- TC_ID: 77005 Creating intel with MD5")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("MD5_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_helper('MD5')
        self.addValue_helper('MD5', "29db482da7696f9343a34566affc6905")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("MD5_canvas")

    def test_06_intel_creation_with_SHA1(self):
        fprint(self, "\n----------- TC_ID: 77006 Creating intel with SHA1")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("SHA1_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_helper('SHA-1')
        self.addValue_helper('SHA1', "ec69154b36a9918db3c7fb4013a2fe1a1ab4ee62")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("SHA1_canvas")

    def test_07_intel_creation_with_SHA224(self):
        fprint(self, "\n----------- TC_ID: 77007 Creating intel with SHA224")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("SHA224_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_helper('SHA-224')
        self.addValue_helper('SHA224', "c94056a762dae7eb92f1f454b7fa5779f1cc8e863195b594874a0a3d")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("SHA224_canvas")

    def test_08_intel_creation_with_SHA256(self):
        fprint(self, "\n----------- TC_ID: 77008 Creating intel with SHA256")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("SHA256_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_helper('SHA-256')
        self.addValue_helper('SHA256', "6471f3898e63c2a9af25284253dc087dfda94809182c45728b3adc40e238c7f6")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("SHA256_canvas")

    def test_09_intel_creation_with_SHA384(self):
        fprint(self, "\n----------- TC_ID: 77009 Creating intel with SHA384")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("SHA384_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_helper('SHA-384')
        self.addValue_helper('SHA384',"ce0f53a859f335458d10302403daa678cc205d737871b0636e369269f318ac53ee651472f138c78c280ca2c6ab8a3b46")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("SHA384_canvas")

    def test_10_intel_creation_with_SHA512(self):
        fprint(self, "\n----------- TC_ID: 77010 Creating intel with SHA512")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("SHA512_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_helper('SHA-512')
        self.addValue_helper('SHA512',"6ffe33597b55cd4bac3c6856ce3ac7b6b5b317df5e023fe69eb06683305531db8332d540cb78d28873bc28955a6707bdf5a094c7fafe0c6f1b549c1f97dfc44b")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("SHA512_canvas")

    def test_11_intel_creation_with_SSDEEP(self):
        fprint(self, "\n----------- TC_ID: 77011 Creating intel with SSDEEP")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("SSDEEP_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_helper('SSDEEP')
        self.addValue_helper('SSDEEP',"12288:grph3cRII/cjTP3xTPutUKlJDJN9wqvZVayjkMiOlGQf3q:grphMf/cP3xaUKldpFRVayAMrl5q")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("SSDEEP_canvas")

    def test_12_intel_creation_with_Email(self):
        fprint(self, "\n----------- TC_ID: 77012 Creating intel with Email")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Email_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_helper('email')
        self.addValue_helper('Email', "abcdeokf@gmail.com")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Email_canvas")

    def test_13_intel_creation_with_Port(self):
        fprint(self, "\n----------- TC_ID: 77013 Creating intel with Port")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Port_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_helper('port')
        self.addValue_helper('Port', "59999")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Port_canvas")

    def test_14_intel_creation_with_Mutex(self):
        fprint(self, "\n----------- TC_ID: 77014 Creating intel with Mutex")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Mutex_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_helper('mutex')
        self.addValue_helper('Mutex', "HS_Mutex")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Mutex_canvas")

    def test_15_intel_creation_with_ASN(self):
        fprint(self, "\n----------- TC_ID: 77015 Creating intel with ASN")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("ASN_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_helper('autonomous-system')
        self.addValue_helper('ASN', "AS21699")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("ASN_canvas")

    def test_16_intel_creation_with_Vulnerability(self):
        fprint(self, "\n----------- TC_ID: 77016 Creating intel with Vulnerability")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Vulnerability_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_on_other_sdo()
        self.click_helper('vulnerability')
        self.addValue_helper('Vulnerability', "CVE-1999-0090")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Vulnerability_canvas")

    def test_17_intel_creation_with_Malware(self):
        fprint(self, "\n----------- TC_ID: 77017 Creating intel with Malware")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Malware_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_on_other_sdo()
        self.click_helper('malware')
        self.addValue_helper('Malware', "Ursnif")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Malware_canvas")

    def test_18_intel_creation_with_Campaign(self):
        fprint(self, "\n----------- TC_ID: 77018 Creating intel with Campaign")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Campaign_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_on_other_sdo()
        self.click_helper('campaign')
        self.addValue_helper('Campaign', "CredentialHarvesting")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Campaign_canvas")

    def test_19_intel_creation_with_Threat_Actor(self):
        fprint(self, "\n----------- TC_ID: 77019 Creating intel with Threat Actor")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Threat Actor_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_on_other_sdo()
        self.click_helper('threat-actor')
        self.addValue_helper('Threat Actor', "Dropping Elephant")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Threat Actor_canvas")

    def test_20_intel_creation_with_Intrusion_Set(self):
        fprint(self, "\n----------- TC_ID: 77020 Creating intel with Intrusion Set")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Intrusion Set_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_on_other_sdo()
        self.click_helper('intrusion-set')
        self.addValue_helper("Intrusion Set", "intrusion-set :24/12/2021 02:36:16")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Intrusion Set_canvas")

    def test_21_intel_creation_with_Attack_Pattern(self):
        fprint(self, "\n----------- TC_ID: 77021 Creating intel with Attack Pattern")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Attack Pattern_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_on_other_sdo()
        self.click_helper('attack-pattern')
        self.addValue_helper('Attack Pattern', "democratic")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Attack Pattern_canvas")

    def test_22_intel_creation_with_Course_of_Action(self):
        fprint(self, "\n----------- TC_ID: 77022 Creating intel with Course of Action")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Course of Action_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_on_other_sdo()
        self.click_helper('course-of-action')
        self.addValue_helper('Course of Action', "number-COA")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Course of Action_canvas")

    def test_23_intel_creation_with_Identity(self):
        fprint(self, "\n----------- TC_ID: 77023 Creating intel with Identity")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Identity_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_on_other_sdo()
        self.click_helper('identity')
        self.addValue_helper('Identity', "Mark-Identity")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Identity_canvas")

    def test_24_intel_creation_with_Kill_Chain(self):
        fprint(self, "\n----------- TC_ID: 77024 Creating intel with Kill Chain")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Kill Chain_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_on_other_sdo()
        self.click_helper('kill_chain')
        self.addValue_helper('Kill Chain', "misp-category")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Kill Chain_canvas")

    def test_25_intel_creation_with_Tool(self):
        fprint(self, "\n----------- TC_ID: 77025 Creating intel with Tool")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Tool_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_on_other_sdo()
        self.click_helper('tool')
        self.addValue_helper('Tool', "VNC")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Tool_canvas")

    def test_26_intel_creation_with_Infrastructure(self):
        fprint(self, "\n----------- TC_ID: 77026 Creating intel with Infrastructure")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Infrastructure_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_on_other_sdo()
        self.click_helper('infrastructure')
        self.addValue_helper('Infrastructure', "Flask-Security: Flask-Security")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Infrastructure_canvas")

    def test_27_intel_creation_with_Malware_Analysis(self):
        fprint(self, "\n----------- TC_ID: 77027 Creating intel with Malware Analysis")
        nav_menu_main(self, "Threat Investigations")
        self.click_on_create_new()
        self.add_Title("Malware Analysis_canvas")
        self.skip_walk_through()
        self.click_on_add_node()
        self.click_on_other_sdo()
        self.click_helper('malware-analysis')
        self.addValue_helper('Malware Analysis', "test_mal_ana")
        self.save_create_intel()
        self.verfiy_intel_is_created_or_not("Malware Analysis_canvas")

    def test_28_verify_IPv4(self):
        fprint(self, "\n----------- TC_ID: 77028 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, '89.163.249.192', 'Import')

    def test_29_verify_IPv6(self):
        fprint(self, "\n----------- TC_ID: 77029 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'f8c6:f44b:9bc7:97e9:0b1c:3d03:3a9d:ee20', 'Import')

    def test_30_verify_Domain(self):
        fprint(self, "\n----------- TC_ID: 77030 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'daily.automation.com', 'Import')

    def test_31_verify_URL(self):
        fprint(self, "\n----------- TC_ID: 77031 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'http://malicousurl.in/4712/', 'Import')

    def test_32_verify_MD5(self):
        fprint(self, "\n----------- TC_ID: 77032 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, '29db482da7696f9343a34566affc6905', 'Import')

    def test_33_verify_SHA1(self):
        fprint(self, "\n----------- TC_ID: 77033 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'ec69154b36a9918db3c7fb4013a2fe1a1ab4ee62', 'Import')

    def test_34_verify_SHA224(self):
        fprint(self, "\n----------- TC_ID: 77034 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'c94056a762dae7eb92f1f454b7fa5779f1cc8e863195b594874a0a3d', 'Import')

    def test_35_verify_SHA256(self):
        fprint(self, "\n----------- TC_ID: 77035 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, '6471f3898e63c2a9af25284253dc087dfda94809182c45728b3adc40e238c7f6', 'Import')

    def test_36_verify_SHA384(self):
        fprint(self, "\n----------- TC_ID: 77036 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'ce0f53a859f335458d10302403daa678cc205d737871b0636e369269f318ac53ee651472f138c78c280ca2c6ab8a3b46', 'Import')

    def test_37_verify_SHA512(self):
        fprint(self, "\n----------- TC_ID: 77037 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, '6ffe33597b55cd4bac3c6856ce3ac7b6b5b317df5e023fe69eb06683305531db8332d540cb78d28873bc28955a6707bdf5a094c7fafe0c6f1b549c1f97dfc44b', 'Import')

    def test_38_verify_SSDEEP(self):
        fprint(self, "\n----------- TC_ID: 77038 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, '12288:grph3cRII/cjTP3xTPutUKlJDJN9wqvZVayjkMiOlGQf3q:grphMf/cP3xaUKldpFRVayAMrl5q', 'Import')

    def test_39_verify_Email(self):
        fprint(self, "\n----------- TC_ID: 77039 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'abcdeokf@gmail.com', 'Import')

    def test_40_verify_Port(self):
        fprint(self, "\n----------- TC_ID: 77040 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, '59999', 'Import')

    def test_41_verify_Mutex(self):
        fprint(self, "\n----------- TC_ID: 77041 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'HS_Mutex', 'Import')

    def test_42_verify_ASN(self):
        fprint(self, "\n----------- TC_ID: 77042 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'AS21699', 'Import')

    def test_43_verify_Vulnerability(self):
        fprint(self, "\n----------- TC_ID: 77043 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'CVE-1999-0090', 'Import')

    def test_44_verify_Malware(self):
        fprint(self, "\n----------- TC_ID: 77044 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'Ursnif', 'Import')

    def test_45_verify_Campaign(self):
        fprint(self, "\n----------- TC_ID: 77045 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'CredentialHarvesting', 'Import')

    def test_46_verify_Threat_Actor(self):
        fprint(self, "\n----------- TC_ID: 77046 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'Dropping Elephant', 'Import')

    def test_47_verify_Intrusion_Set(self):
        fprint(self, "\n----------- TC_ID: 77047 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'intrusion-set :24/12/2021 02:36:16', 'Import')

    def test_48_verify_Attack_Pattern(self):
        fprint(self, "\n----------- TC_ID: 77048 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'democratic', 'Import')

    def test_49_verify_Course_Of_Action(self):
        fprint(self, "\n----------- TC_ID: 77049 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'number-COA', 'Import')

    def test_50_verify_Identity(self):
        fprint(self, "\n----------- TC_ID: 77050 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'Mark-Identity', 'Import')

    def test_51_verify_Tool(self):
        fprint(self, "\n----------- TC_ID: 77051 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'VNC', 'Import')

    def test_52_verify_Infrastructure(self):
        fprint(self, "\n----------- TC_ID: 77052 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'Flask-Security: Flask-Security', 'Import')

    def test_53_verify_Malware_Analysis(self):
        fprint(self, "\n----------- TC_ID: 77053 Verifying intel visibility in threat data")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, 'test_mal_ana', 'Import')


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
