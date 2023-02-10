import unittest
from lib.ui.nav_app import *
from lib.ui.nav_threat_data import click_on_intel, verify_data_in_threatdata
from lib.ui.import_intel import select_format,navigate_to_import_intel,select_collection,import_file

class AttackNavigator(unittest.TestCase):

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

    def switch_category(self, category):
        """
            Function to switch between Mobile and Enterprise
            args:
                category: can either be Mobile or Enterprise
        """
        waitfor(self, 20, By.XPATH, "//h1[span]/div/div/button")
        self.driver.find_element_by_xpath("//h1[span]/div/div/button").click()
        waitfor(self, 20, By.XPATH, "//li/span[contains(text(),'" + category + "')]")
        self.driver.find_element_by_xpath("//li/span[contains(text(),'" + category + "')]").click()
        sleep(2)

    def open_mitre_and_read(self, category):
        """
            Function to read from MITRE all available tactics and techniques
            args:
                category: can either be Mobile or Enterprise
            returns:
                main_dict: dictionary containing all tactics and techniques
        """
        self.driver.maximize_window()
        self.driver.execute_script("window.open('https://attack.mitre.org/techniques/" + category + "/');")
        fprint(self, "Redirecting to MITRE")
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        sleep(10)
        main_dict = {}
        ele = self.driver.find_elements_by_xpath("//div[@id='" + category + "-body']/div/div[contains(@class,'sidenav-head')]")
        for i in ele:
            all = i.find_elements(By.XPATH, ".//following-sibling::div/div/div/a")
            _sub_dict = dict()
            for ii in all:
                _sub_dict[ii.get_attribute("text").strip()] = []
                final_layer = ii.find_elements(By.XPATH, ".//parent::div/following-sibling::div/div/div/a")
                for iii in final_layer:
                    _sub_dict[ii.get_attribute("text").strip()].append(iii.get_attribute("text").strip())
            main_dict[i.text] = _sub_dict
        return main_dict

    def validate_techniques(self, TTP_dict, headers, deprecated_techniques):
        """
            Function to pick each technique and validate its presence under ATT&CK navigator
            args:
                TTP_dict: Dictionary containing all Tactics and underlying techniques
                headers: list of Tactics in ATT&CK Navigator
                deprecated_techniques: list of MITRE deprecated techniques
            returns:
                fails: List of techniques missing under ATT&CK Navigator if any
        """
        fails = []
        for num, header in enumerate(headers):
            fprint(self, header.text)
            if header.text in ["Network Effects", "Remote Service Effects"]:
                continue
            for keys, values in TTP_dict[header.text].items():
                if len(values) == 0:
                    fprint(self, "Validating " + header.text + " -> " + keys.encode("ascii", "ignore").decode())
                    if keys in deprecated_techniques:
                        fprint(self, header.text + " -> " + keys.encode("ascii", "ignore").decode() + " is deprecated")
                        continue
                    elif waitfor(self, 10, By.XPATH,
                                 "//tbody/tr/td['" + str(
                                     num + 1) + "']/table/tr/td//*[normalize-space(text())='" + keys + "']",
                                 False):
                        fprint(self, "Validated " + header.text + " -> " + keys.encode("ascii", "ignore").decode())
                    elif waitfor(self, 10, By.XPATH,
                                 "//tbody/tr/td['" + str(
                                     num + 1) + "']/table/tr/td//*[contains(text(),'" + keys[:39] + "')]",
                                 False):
                        fprint(self, "Validated " + header.text + " -> " + keys.encode("ascii", "ignore").decode())
                    else:
                        fprint(self,
                               "[Failed] " + header.text + " -> " + keys.encode("ascii",
                                                                                "ignore").decode() + " not found")
                        fails.append(header.text + " -> " + keys.encode("ascii", "ignore").decode())
                else:
                    for i in values:
                        fprint(self, "Validating " + header.text + " -> " + keys.encode("ascii",
                                                                                        "ignore").decode() + " -> " + i.encode(
                            "ascii", "ignore").decode())
                        if i in deprecated_techniques:
                            fprint(self,
                                   header.text + " -> " + keys.encode("ascii", "ignore").decode() + " -> " + i.encode(
                                       "ascii", "ignore").decode() + " is deprecated")
                            continue
                        elif waitfor(self, 10, By.XPATH, "//tbody/tr/td['" + str(num + 1) +
                                                         "']/table/tr[td//child::*[contains(text(), '" + i +
                                                         "')]][td//child::*[contains(text(), '" + keys + "')]]", False):
                            fprint(self, "Validated " + header.text + " -> " + keys.encode("ascii",
                                                                                           "ignore").decode() + " -> " + i.encode(
                                "ascii", "ignore").decode())
                        elif waitfor(self, 10, By.XPATH, "//tbody/tr/td['" + str(num + 1) +
                                                         "']/table/tr[td//child::*[contains(text(), '" + i[:39] +
                                                         "')]][td//child::*[contains(text(), '" + keys[:39] + "')]]",
                                     False):
                            fprint(self, "Validated " + header.text + " -> " + keys.encode("ascii",
                                                                                           "ignore").decode() + " -> " + i.encode(
                                "ascii", "ignore").decode())
                        else:
                            fprint(self, "[Failed ]" + header.text + " -> " + keys.encode("ascii",
                                                                                          "ignore").decode() + " -> " + i.encode(
                                "ascii", "ignore").decode() + " not found")
                            fails.append(
                                header.text + " -> " + keys.encode("ascii", "ignore").decode() + " -> " + i.encode(
                                    "ascii",
                                    "ignore").decode())
        return fails

    def test_01_attackNavigator_pageLoad(self):
        """
            Testcase to validate if ATT&CK Navigator page is loading
        """
        fprint(self, "TC_ID: 2001 - ATT&CK Navigator_PageLoad" + uniquestr)
        nav_menu_main(self, "ATT&CK Navigator")
        waitfor(self, 5, By.XPATH, "//*[contains(text(),'Native API')]")
        fprint(self, "AttackNavigator - Enterprise Technology Native API found")
        fprint(self, "AttackNavigator - Enterprise PageLoad is verified")
        self.driver.find_element_by_xpath("//i[@class='cyicon-chevron-down']").click()
        fprint(self, "AttackNavigator - clicked on chevron")
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'Mobile')]/ancestor::li[@id='list-item-1']")
        sleep(0.2)
        self.driver.find_element_by_xpath("//span[contains(text(),'Mobile')]/ancestor::li[@id='list-item-1']").click()
        fprint(self, "AttackNavigator - Clicked on Mobile option")
        waitfor(self, 5, By.XPATH, "//*[contains(text(),'Broadcast Receivers')]")
        fprint(self, "AttackNavigator - Mobile Technology Broadcast Receivers found")
        process_console_logs(self)
        fprint(self, "AttackNavigator - Mobile PageLoad is verified")

    def test_02_attacknavigator_addmitrelayer_mobile(self):
        """
            Testcase to verify if new MITRE Layer can be added under ATT&CK Navigator -> Mobile
        """
        fprint(self, "TC_ID: 2002 - ATT&CK Navigator_Add Layer")
        set_value("AddLayer_Mobile", "M" + uniquestr[-4:])
        nav_menu_main(self, "ATT&CK Navigator")
        self.switch_category(category="Mobile")
        waitfor(self, 20, By.XPATH, "//span[contains(@class,'cyicon-add')]")
        self.driver.find_element_by_xpath("//span[contains(@class,'cyicon-add')]").click()
        if waitfor(self, 20, By.XPATH, "//li[contains(text(), 'New MITRE Layer')]", False):
            self.driver.find_element_by_xpath("//li[contains(text(), 'New MITRE Layer')]").click()
        fprint(self, "Moving to Search Bar")
        _ele = self.driver.find_element_by_xpath("//div[@data-testid='search-filter']/input")
        ActionChains(self.driver).move_to_element(_ele).perform()
        sleep(2)  # needed
        fprint(self, "Mobile - ATT&CK Navigator_Clicked on Add Layer")
        fprint(self, "Type Layer Text: " + get_value("AddLayer_Mobile"))
        if Build_Version.__contains__("3."):
            self.driver.find_element_by_xpath("//div[contains(text(), 'Layer 1')]").click()
            waitfor(self, 20, By.XPATH, "//div[div[contains(text(),'Layer 1')]]//button")
            self.driver.find_element_by_xpath("//div[div[contains(text(),'Layer 1')]]//button").click()
            sleep(2)
            waitfor(self, 20, By.XPATH, "//li[@data-testid='rename']")
            self.driver.find_element_by_xpath("//li[@data-testid='rename']").click()
            waitfor(self, 20, By.XPATH, "//div[@data-testid='name-input']")
            self.driver.find_element_by_xpath("//div[@data-testid='name-input']").click()
            clear_field(self.driver.find_element_by_xpath("//div[@data-testid='name-input']/input"))
            self.driver.find_element_by_xpath("//div[@data-testid='name-input']/input"). \
                send_keys(get_value('AddLayer_Mobile'))
            self.driver.find_element_by_xpath("//div[@data-testid='name-input']/input").send_keys(Keys.ENTER)
            sleep(1)
        else:
            sleep(5)
            self.driver.find_element_by_xpath("//div[@data-testid='title-input']/input").send_keys(
                get_value("AddLayer_Mobile"))
            self.driver.find_element_by_xpath("//div[@data-testid='title-input']/input").send_keys(Keys.ENTER)
            fprint(self, "Click on Save Button")
        self.driver.find_element_by_xpath("(//button[contains(text(),'Save')])[1]").click()
        verify_success(self, "Layer created successfully")

    def test_03_attacknavigator_addmitrelayer_enterprise(self):
        """
            Testcase to verify if new MITRE Layer can be added under ATT&CK Navigator -> Enterprise
        """
        fprint(self, "TC_ID: 2003 - ATT&CK Navigator_Add MITRE Layer Enterprise")
        set_value("AddLayer_Enterprise", "E" + uniquestr[-4:])
        nav_menu_main(self, "ATT&CK Navigator")
        self.switch_category(category="Enterprise")
        waitfor(self, 20, By.XPATH, "//span[contains(@class,'cyicon-add')]")
        self.driver.find_element_by_xpath("//span[contains(@class,'cyicon-add')]").click()
        if waitfor(self, 20, By.XPATH, "//li[contains(text(), 'New MITRE Layer')]", False):
            self.driver.find_element_by_xpath("//li[contains(text(), 'New MITRE Layer')]").click()
        fprint(self, "Moving to Search Bar")
        _ele = self.driver.find_element_by_xpath("//div[@data-testid='search-filter']/input")
        ActionChains(self.driver).move_to_element(_ele).perform()
        sleep(2)  # needed
        fprint(self, "Enterprise - ATT&CK Navigator_Clicked on Add New MITRE Layer")
        fprint(self, "Type Layer Text: " + get_value("AddLayer_Enterprise"))
        if Build_Version.__contains__("3."):
            self.driver.find_element_by_xpath("//div[contains(text(), 'Layer 1')]").click()
            waitfor(self, 20, By.XPATH, "//div[div[contains(text(),'Layer 1')]]//button")
            self.driver.find_element_by_xpath("//div[div[contains(text(),'Layer 1')]]//button").click()
            sleep(2)
            waitfor(self, 20, By.XPATH, "//li[@data-testid='rename']")
            self.driver.find_element_by_xpath("//li[@data-testid='rename']").click()
            waitfor(self, 20, By.XPATH, "//div[@data-testid='name-input']")
            self.driver.find_element_by_xpath("//div[@data-testid='name-input']").click()
            clear_field(self.driver.find_element_by_xpath("//div[@data-testid='name-input']/input"))
            self.driver.find_element_by_xpath("//div[@data-testid='name-input']/input"). \
                send_keys(get_value('AddLayer_Enterprise'))
            self.driver.find_element_by_xpath("//div[@data-testid='name-input']/input").send_keys(Keys.ENTER)
            sleep(1)
        else:
            sleep(5)
            self.driver.find_element_by_xpath("//div[@data-testid='title-input']/input").send_keys(
                get_value("AddLayer_Enterprise"))
            self.driver.find_element_by_xpath("//div[@data-testid='title-input']/input").send_keys(Keys.ENTER)
            fprint(self, "Click on Save Button")
        self.driver.find_element_by_xpath("(//button[contains(text(),'Save')])[1]").click()
        verify_success(self, "Layer created successfully")

    def test_04_attacknavigator_editmitreLayer_enterprise(self):
        """
            Testcase to verify if new MITRE Layer can be edited for backgroundcolor under ATT&CK Navigator -> Enterprise
        """
        fprint(self, "TC_ID: 2004 - ATT&CK Navigator_Edit Mitre Layer Enterprise" + get_value("AddLayer_Enterprise"))
        nav_menu_main(self, "ATT&CK Navigator")
        self.switch_category(category="Enterprise")
        if (self.driver.find_element_by_xpath(
                "//*[contains(text(),'" + get_value("AddLayer_Enterprise") + "')]")).is_displayed():
            fprint(self, "ATT&CK Navigator_Identified the added layer")
            self.driver.find_element_by_xpath(
                "//*[contains(text(),'" + get_value("AddLayer_Enterprise") + "')]").click()
            sleep(0.2)
        waitfor(self, 5, By.XPATH, "(//span[@class='cyicon-more-vertical'])[2]")
        self.driver.find_element_by_xpath("(//span[@class='cyicon-more-vertical'])[2]").click()
        fprint(self, "ATT&CK Navigator_Clicked on layer action option")
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Edit')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Edit')]").click()
        fprint(self, "ATT&CK Navigator_Clicked on layer edit option")
        self.driver.find_element_by_xpath \
            ("//span[following-sibling::*[contains(text(), 'Drive-by Compromise')]]/div/span[input]").click()
        self.driver.find_element_by_xpath("//button/span/span/i").click()
        waitfor(self, 20, By.XPATH, "(//li/span[contains(@style,'background')])[2]")
        self.driver.find_element_by_xpath("(//li/span[contains(@style,'background')])[2]").click()
        waitfor(self, 5, By.XPATH, "(//button[contains(text(),'Save')])[1]")
        self.driver.find_element_by_xpath("(//button[contains(text(),'Save')])[1]").click()
        verify_success(self, "updated successfully")
        fprint(self, "ATT&CK Navigator_Edit Layer " + get_value("AddLayer_Enterprise") + " for Enterprise is verified")

    def test_05_attacknavigator_editmitreLayer_mobile(self):
        """
            Testcase to verify if new MITRE Layer can be edited for backgroundcolor under ATT&CK Navigator -> Mobile
        """
        fprint(self, "TC_ID: 2005 - ATT&CK Navigator_Edit Mitre Layer Mobile" + get_value("AddLayer_Mobile"))
        nav_menu_main(self, "ATT&CK Navigator")
        self.switch_category(category="Mobile")
        if (self.driver.find_element_by_xpath(
                "//*[contains(text(),'" + get_value("AddLayer_Mobile") + "')]")).is_displayed():
            fprint(self, "ATT&CK Navigator_Identified the added layer")
            self.driver.find_element_by_xpath("//*[contains(text(),'" + get_value("AddLayer_Mobile") + "')]").click()
            sleep(0.2)
        waitfor(self, 5, By.XPATH, "(//span[@class='cyicon-more-vertical'])[2]")
        self.driver.find_element_by_xpath("(//span[@class='cyicon-more-vertical'])[2]").click()
        fprint(self, "ATT&CK Navigator_Clicked on layer action option")
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Edit')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Edit')]").click()
        fprint(self, "ATT&CK Navigator_Clicked on layer edit option")
        waitfor(self, 10, By.XPATH, "//span[following-sibling::*[contains(text(), 'Drive-By Compromise')]]/div/span[input]")
        self.driver.find_element_by_xpath \
            ("//span[following-sibling::*[contains(text(), 'Drive-By Compromise')]]/div/span[input]").click()
        self.driver.find_element_by_xpath("//button/span/span/i").click()
        waitfor(self, 20, By.XPATH, "(//li/span[contains(@style,'background')])[2]")
        self.driver.find_element_by_xpath("(//li/span[contains(@style,'background')])[2]").click()
        waitfor(self, 5, By.XPATH, "(//button[contains(text(),'Save')])[1]")
        self.driver.find_element_by_xpath("(//button[contains(text(),'Save')])[1]").click()
        verify_success(self, "updated successfully")
        fprint(self, "ATT&CK Navigator_Edit Layer " + get_value("AddLayer_Mobile") + " for Mobile is verified")

    def test_06_validate_attack_ttp_with_mitre(self):
        """
            Testcase to validate if all TTP in MITRE are listed under ATT&CK Navigator
        """
        fprint(self, "TC_ID: 2006: Validating if all techniques are present under ATT&CK Navigator")
        deprecated_techniques = ["Launchd"]
        TTP_dict = self.open_mitre_and_read(category="enterprise")
        handles = self.driver.window_handles
        fprint(self, "Redirecting back to CTIX")
        self.driver.switch_to.window(handles[0])
        nav_menu_main(self, 'ATT&CK Navigator')
        self.switch_category(category="Enterprise")
        waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Expand Sub-techniques')]")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Expand Sub-techniques')]").click()
        sleep(5)
        headers = self.driver.find_elements_by_xpath("//table/thead/th/div/div/span[1]")
        fails = self.validate_techniques(TTP_dict, headers, deprecated_techniques)
        if len(fails) != 0:
            self.assert_(fails == [], str(fails))
        else:
            fprint(self, "[Passed] All Techniques are listed under ATT&CK Navigator")

    def test_07_validate_attack_ttp_with_mitre_mobile(self):
        """
            Testcase to validate if all TTP in MITRE mobile are listed under ATT&CK Navigator
        """
        fprint(self, "TC_ID: 2007: Validating if all techniques are present under ATT&CK Navigator")
        deprecated_techniques = ["Launchd"]
        TTP_dict = self.open_mitre_and_read(category="mobile")
        handles = self.driver.window_handles
        fprint(self, "Redirecting back to CTIX")
        self.driver.switch_to.window(handles[0])
        nav_menu_main(self, 'ATT&CK Navigator')
        self.switch_category(category="Mobile")
        waitfor(self, 20, By.XPATH, "//button[contains(text(), 'Expand Sub-techniques')]")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Expand Sub-techniques')]").click()
        sleep(5)
        headers = self.driver.find_elements_by_xpath("//table/thead/th/div/div/span[1]")
        fails = self.validate_techniques(TTP_dict, headers, deprecated_techniques)
        if len(fails) != 0:
            self.assert_(fails == [], str(fails))
        else:
            fprint(self, "[Passed] All Techniques are listed under ATT&CK Navigator")

    def test_08_attacknavigator_deletemitrelayer_enterprise(self):
        """
            Testcase to validate that MITRE layer under ATT&CK Navigator -> Enterprise can be deleted
        """
        fprint(self, "TC_ID: 2008 - ATT&CK Navigator_Delete Mitre Layer Enterprise" + get_value("AddLayer_Enterprise"))
        nav_menu_main(self, "ATT&CK Navigator")
        self.switch_category(category="Enterprise")
        if (self.driver.find_element_by_xpath(
                "//*[contains(text(),'" + get_value("AddLayer_Enterprise") + "')]")).is_displayed():
            fprint(self, "ATT&CK Navigator_Identified the added layer")
            self.driver.find_element_by_xpath(
                "//*[contains(text(),'" + get_value("AddLayer_Enterprise") + "')]").click()
            sleep(0.2)
        waitfor(self, 5, By.XPATH, "(//span[@class='cyicon-more-vertical'])[2]")
        self.driver.find_element_by_xpath("(//span[@class='cyicon-more-vertical'])[2]").click()
        fprint(self, "ATT&CK Navigator_Clicked on layer action option")
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Delete')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Delete')]").click()
        sleep(0.2)
        fprint(self, "ATT&CK Navigator_Clicked on layer Delete option")
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Delete')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Delete')]").click()
        verify_success(self, "Layer deleted successfully")
        fprint(self, "ATT&CK Navigator_Delete Mitre Layer for Enterprise is verified")
        self.switch_category(category="Enterprise")
        if waitfor(self, 20, By.XPATH, "//*[contains(text(),'" + get_value("AddLayer_Enterprise") + "')]", False):
            fprint(self,
                   "[FAILED] " + get_value("AddLayer_Enterprise") + " failed to be deleted under ATT&CK Navigator")
            raise Exception(
                "[FAILED] " + get_value("AddLayer_Enterprise") + " failed to be deleted under ATT&CK Navigator")
        else:
            fprint(self, "[PASSED] " + get_value("AddLayer_Enterprise") +
                   "Enterprise Mitre layer is successfully deleted from ATT&CK Navigator")

    def test_09_attacknavigator_deletemitrelayer_mobile(self):
        """
            Testcase to validate if MITRE layer under ATT&CK Navigator -> Mobile can be deleted
        """
        fprint(self, "TC_ID: 2009 - ATT&CK Navigator_Delete Mitre Layer Mobile" + get_value("AddLayer_Mobile"))
        nav_menu_main(self, "ATT&CK Navigator")
        self.switch_category(category="Mobile")
        if (self.driver.find_element_by_xpath(
                "//*[contains(text(),'" + get_value("AddLayer_Mobile") + "')]")).is_displayed():
            fprint(self, "ATT&CK Navigator_Identified the added layer")
            self.driver.find_element_by_xpath("//*[contains(text(),'" + get_value("AddLayer_Mobile") + "')]").click()
            sleep(0.2)
        waitfor(self, 5, By.XPATH, "(//span[@class='cyicon-more-vertical'])[2]")
        self.driver.find_element_by_xpath("(//span[@class='cyicon-more-vertical'])[2]").click()
        fprint(self, "ATT&CK Navigator_Clicked on layer action option")
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Delete')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Delete')]").click()
        sleep(0.2)
        fprint(self, "ATT&CK Navigator_Clicked on layer Delete option")
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Delete')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Delete')]").click()
        verify_success(self, "Layer deleted successfully")
        fprint(self, "ATT&CK Navigator_Delete Mitre Layer for Mobile is verified")
        self.switch_category(category="Mobile")
        if waitfor(self, 20, By.XPATH, "//*[contains(text(),'" + get_value("AddLayer_Mobile") + "')]", False):
            fprint(self, "[FAILED] " + get_value("AddLayer_Mobile") + " failed to be deleted under ATT&CK Navigator")
            raise Exception("[FAILED] " + get_value("AddLayer_Mobile") + " failed to be deleted under ATT&CK Navigator")
        else:
            fprint(self,
                   "[PASSED] " + get_value(
                       "AddLayer_Mobile") + "Mobile Mitre layer is successfully deleted from ATT&CK Navigator")

    def test_10_attacknavigator_addcustombaselayer_mobile(self):
        """
            Testcase to verify if new custom base Layer can be added under ATT&CK Navigator -> Mobile
        """
        fprint(self, "TC_ID: 2010 - ATT&CK Navigator_Add Custom Base Layer Mobile")
        set_value("AddCustomBaseLayer_Mobile", "CBM" + uniquestr[-4:])
        nav_menu_main(self, "ATT&CK Navigator")
        self.switch_category(category="Mobile")
        waitfor(self, 20, By.XPATH, "//span[contains(@class,'cyicon-add')]")
        self.driver.find_element_by_xpath("//span[contains(@class,'cyicon-add')]").click()
        if waitfor(self, 20, By.XPATH, "//li[contains(text(), 'New Custom Base Layer')]", False):
            self.driver.find_element_by_xpath("//li[contains(text(), 'New Custom Base Layer')]").click()
            fprint(self, "Moving to Search Bar")
            _ele = self.driver.find_element_by_xpath("//div[@data-testid='search-filter']/input")
            ActionChains(self.driver).move_to_element(_ele).perform()
        sleep(2)  # needed
        fprint(self, "Mobile - ATT&CK Navigator_Clicked on Add New Custom Base Layer")
        fprint(self, "Type Layer Text: " + get_value("AddCustomBaseLayer_Mobile"))
        if Build_Version.__contains__("3."):
            self.driver.find_element_by_xpath("//div[contains(text(), 'Layer 1')]").click()
            waitfor(self, 20, By.XPATH, "//div[div[contains(text(),'Layer 1')]]//button")
            self.driver.find_element_by_xpath("//div[div[contains(text(),'Layer 1')]]//button").click()
            sleep(2)
            waitfor(self, 20, By.XPATH, "//li[@data-testid='rename']")
            self.driver.find_element_by_xpath("//li[@data-testid='rename']").click()
            waitfor(self, 20, By.XPATH, "//div[@data-testid='name-input']")
            self.driver.find_element_by_xpath("//div[@data-testid='name-input']").click()
            clear_field(self.driver.find_element_by_xpath("//div[@data-testid='name-input']/input"))
            self.driver.find_element_by_xpath("//div[@data-testid='name-input']/input"). \
                send_keys(get_value('AddCustomBaseLayer_Mobile'))
            self.driver.find_element_by_xpath("//div[@data-testid='name-input']/input").send_keys(Keys.ENTER)
            sleep(1)
        else:
            sleep(5)
        self.driver.find_element_by_xpath("(//button[contains(text(),'Save')])[1]").click()
        verify_success(self, "Layer created successfully")
        fprint(self,
               "[PASSED] " + get_value(
                   "AddCustomBaseLayer_Mobile") + "Mobile Custom Base layer is successfully Created")

    def test_11_attacknavigator_addcustombaselayer_enterprise(self):
        """
            Testcase to verify if new custom base Layer can be added under ATT&CK Navigator -> Enterprise
        """
        fprint(self, "TC_ID: 2011 - ATT&CK Navigator_Add Custom Base Layer Enterprise")
        set_value("AddCustomBaseLayer_Enterprise", "CBE" + uniquestr[-4:])
        nav_menu_main(self, "ATT&CK Navigator")
        self.switch_category(category="Enterprise")
        waitfor(self, 20, By.XPATH, "//span[contains(@class,'cyicon-add')]")
        self.driver.find_element_by_xpath("//span[contains(@class,'cyicon-add')]").click()
        if waitfor(self, 20, By.XPATH, "//li[contains(text(), 'New Custom Base Layer')]", False):
            self.driver.find_element_by_xpath("//li[contains(text(), 'New Custom Base Layer')]").click()
        fprint(self, "Moving to Search Bar")
        _ele = self.driver.find_element_by_xpath("//div[@data-testid='search-filter']/input")
        ActionChains(self.driver).move_to_element(_ele).perform()
        sleep(2)  # needed
        fprint(self, "Enterprise - ATT&CK Navigator_Clicked on Add New Custom Base Layer")
        fprint(self, "Type Layer Text: " + get_value("AddCustomBaseLayer_Enterprise"))
        if Build_Version.__contains__("3."):
            self.driver.find_element_by_xpath("//div[contains(text(), 'Layer 1')]").click()
            waitfor(self, 20, By.XPATH, "//div[div[contains(text(),'Layer 1')]]//button")
            self.driver.find_element_by_xpath("//div[div[contains(text(),'Layer 1')]]//button").click()
            sleep(2)
            waitfor(self, 20, By.XPATH, "//li[@data-testid='rename']")
            self.driver.find_element_by_xpath("//li[@data-testid='rename']").click()
            waitfor(self, 20, By.XPATH, "//div[@data-testid='name-input']")
            self.driver.find_element_by_xpath("//div[@data-testid='name-input']").click()
            clear_field(self.driver.find_element_by_xpath("//div[@data-testid='name-input']/input"))
            self.driver.find_element_by_xpath("//div[@data-testid='name-input']/input"). \
                send_keys(get_value('AddCustomBaseLayer_Enterprise'))
            self.driver.find_element_by_xpath("//div[@data-testid='name-input']/input").send_keys(Keys.ENTER)
            sleep(1)
        else:
            sleep(5)
            self.driver.find_element_by_xpath("//div[@data-testid='title-input']/input").send_keys(
                get_value("AddCustomBaseLayer_Enterprise"))
            self.driver.find_element_by_xpath("//div[@data-testid='title-input']/input").send_keys(Keys.ENTER)
            fprint(self, "Click on Save Button")
        self.driver.find_element_by_xpath("(//button[contains(text(),'Save')])[1]").click()
        verify_success(self, "Layer created successfully")
        fprint(self,
               "[PASSED] " + get_value(
                   "AddCustomBaseLayer_Enterprise") + "Enterprise Custom Base layer is successfully Created")

    def test_12_attacknavigator_editcustombaseLayer_enterprise(self):
        """
            Testcase to verify if new custom base Layer can be edited for backgroundcolor under ATT&CK Navigator -> Enterprise
        """
        fprint(self,
               "TC_ID: 2012 - ATT&CK Navigator_Edit Layer Enterprise" + get_value("AddCustomBaseLayer_Enterprise"))
        nav_menu_main(self, "ATT&CK Navigator")
        self.switch_category(category="Enterprise")
        if (self.driver.find_element_by_xpath(
                "//*[contains(text(),'" + get_value("AddCustomBaseLayer_Enterprise") + "')]")).is_displayed():
            fprint(self, "ATT&CK Navigator_Identified the added custom base layer")
            self.driver.find_element_by_xpath(
                "//*[contains(text(),'" + get_value("AddCustomBaseLayer_Enterprise") + "')]").click()
            sleep(0.2)
        waitfor(self, 5, By.XPATH, "(//span[@class='cyicon-more-vertical'])[2]")
        self.driver.find_element_by_xpath("(//span[@class='cyicon-more-vertical'])[2]").click()
        fprint(self, "ATT&CK Navigator_Clicked on layer action option")
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Edit')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Edit')]").click()
        fprint(self, "ATT&CK Navigator_Clicked on layer edit option")
        waitfor(self, 10, By.XPATH, "//span[following-sibling::*[contains(text(), 'Drive-by Compromise')]]/div/span[input]")
        self.driver.find_element_by_xpath \
            ("//span[following-sibling::*[contains(text(), 'Drive-by Compromise')]]/div/span[input]").click()
        self.driver.find_element_by_xpath("//button/span/span/i").click()
        waitfor(self, 20, By.XPATH, "(//li/span[contains(@style,'background')])[2]")
        self.driver.find_element_by_xpath("(//li/span[contains(@style,'background')])[2]").click()
        waitfor(self, 5, By.XPATH, "(//button[contains(text(),'Save')])[1]")
        self.driver.find_element_by_xpath("(//button[contains(text(),'Save')])[1]").click()
        verify_success(self, "updated successfully")
        fprint(self, "ATT&CK Navigator_Edit Custom Base Layer " + get_value(
            "AddCustomBaseLayer_Enterprise") + " for Enterprise is verified")

    def test_13_attacknavigator_editcustombaseLayer_mobile(self):
        """
            Testcase to verify if new custom base Layer can be edited for backgroundcolor under ATT&CK Navigator -> Mobile
        """
        fprint(self,
               "TC_ID: 2013 - ATT&CK Navigator_Edit custom base Layer Mobile" + get_value("AddCustomBaseLayer_Mobile"))
        nav_menu_main(self, "ATT&CK Navigator")
        self.switch_category(category="Mobile")
        if (
                self.driver.find_element_by_xpath(
                    "//*[contains(text(),'" + get_value("AddCustomBaseLayer_Mobile") + "')]")).is_displayed():
            fprint(self, "ATT&CK Navigator_Identified the added layer")
        self.driver.find_element_by_xpath(
            "//*[contains(text(),'" + get_value("AddCustomBaseLayer_Mobile") + "')]").click()
        sleep(0.2)
        waitfor(self, 5, By.XPATH, "(//span[@class='cyicon-more-vertical'])[2]")
        self.driver.find_element_by_xpath("(//span[@class='cyicon-more-vertical'])[2]").click()
        fprint(self, "ATT&CK Navigator_Clicked on layer action option")
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Edit')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Edit')]").click()
        fprint(self, "ATT&CK Navigator_Clicked on layer edit option")
        waitfor(self, 10, By.XPATH, "//span[following-sibling::*[contains(text(), 'Drive-By Compromise')]]/div/span[input]")
        self.driver.find_element_by_xpath \
            ("//span[following-sibling::*[contains(text(), 'Drive-By Compromise')]]/div/span[input]").click()
        self.driver.find_element_by_xpath("//button/span/span/i").click()
        waitfor(self, 20, By.XPATH, "(//li/span[contains(@style,'background')])[2]")
        self.driver.find_element_by_xpath("(//li/span[contains(@style,'background')])[2]").click()
        waitfor(self, 5, By.XPATH, "(//button[contains(text(),'Save')])[1]")
        self.driver.find_element_by_xpath("(//button[contains(text(),'Save')])[1]").click()
        verify_success(self, "updated successfully")
        fprint(self, "ATT&CK Navigator_Edit Custom Base Layer " + get_value(
            "AddCustomBaseLayer_Mobile") + " for Mobile is verified")

    def test_14_attacknavigator_deletecustombaselayer_enterprise(self):
        """
            Testcase to validate that custom base layer under ATT&CK Navigator -> Enterprise can be deleted
        """
        fprint(self, "TC_ID: 2014 - ATT&CK Navigator_Delete Custom Base Layer Enterprise" + get_value(
            "AddCustomBaseLayer_Enterprise"))
        nav_menu_main(self, "ATT&CK Navigator")
        self.switch_category(category="Enterprise")
        if (self.driver.find_element_by_xpath(
                "//*[contains(text(),'" + get_value("AddCustomBaseLayer_Enterprise") + "')]")).is_displayed():
            fprint(self, "ATT&CK Navigator_Identified the added layer")
        self.driver.find_element_by_xpath(
            "//*[contains(text(),'" + get_value("AddCustomBaseLayer_Enterprise") + "')]").click()
        sleep(0.2)
        waitfor(self, 5, By.XPATH, "(//span[@class='cyicon-more-vertical'])[2]")
        self.driver.find_element_by_xpath("(//span[@class='cyicon-more-vertical'])[2]").click()
        fprint(self, "ATT&CK Navigator_Clicked on layer action option")
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Delete')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Delete')]").click()
        sleep(0.2)
        fprint(self, "ATT&CK Navigator_Clicked on layer Delete option")
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Delete')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Delete')]").click()
        verify_success(self, "Layer deleted successfully")
        fprint(self, "ATT&CK Navigator_Delete Layer for Enterprise is verified")
        self.switch_category(category="Enterprise")
        if waitfor(self, 20, By.XPATH, "//*[contains(text(),'" + get_value("AddLayer_Enterprise") + "')]", False):
            fprint(self, "[FAILED] " + get_value(
                "AddCustomBaseLayer_Enterprise") + " failed to be deleted under ATT&CK Navigator")
            raise Exception("[FAILED] " + get_value(
                "AddCustomBaseLayer_Enterprise") + " failed to be deleted under ATT&CK Navigator")
        else:
            fprint(self, "[PASSED] " + get_value(
                "AddCustomBaseLayer_Enterprise") + " Custom Base layer is successfully deleted from ATT&CK Navigator")

    def test_15_attacknavigator_deletecustombaselayer_mobile(self):
        """
            Testcase to validate if custom base layer under ATT&CK Navigator -> Mobile can be deleted
        """
        fprint(self, "TC_ID: 2015 - ATT&CK Navigator_Delete custom base Layer" + get_value("AddCustomBaseLayer_Mobile"))
        nav_menu_main(self, "ATT&CK Navigator")
        self.switch_category(category="Mobile")
        if (
                self.driver.find_element_by_xpath(
                    "//*[contains(text(),'" + get_value("AddCustomBaseLayer_Mobile") + "')]")).is_displayed():
            fprint(self, "ATT&CK Navigator_Identified the added custom base layer")
        self.driver.find_element_by_xpath(
            "//*[contains(text(),'" + get_value("AddCustomBaseLayer_Mobile") + "')]").click()
        sleep(0.2)
        waitfor(self, 5, By.XPATH, "(//span[@class='cyicon-more-vertical'])[2]")
        self.driver.find_element_by_xpath("(//span[@class='cyicon-more-vertical'])[2]").click()
        fprint(self, "ATT&CK Navigator_Clicked on custom base layer action option")
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Delete')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Delete')]").click()
        sleep(0.2)
        fprint(self, "ATT&CK Navigator_Clicked on custom base layer Delete option")
        waitfor(self, 5, By.XPATH, "//button[contains(text(),'Delete')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Delete')]").click()
        verify_success(self, "Layer deleted successfully")
        fprint(self, "ATT&CK Navigator_Delete Layer for Mobile is verified")
        self.switch_category(category="Mobile")
        if waitfor(self, 20, By.XPATH, "//*[contains(text(),'" + get_value("AddLayer_Mobile") + "')]", False):
            fprint(self, "[FAILED] " + get_value(
                "AddCustomBaseLayer_Mobile") + " failed to be deleted under ATT&CK Navigator")
            raise Exception(
                "[FAILED] " + get_value("AddCustomBaseLayer_Mobile") + " failed to be deleted under ATT&CK Navigator")
        else:
            fprint(self, "[PASSED] " + get_value(
                "AddCustomBaseLayer_Mobile") + "Custom Base layer is successfully deleted from ATT&CK Navigator")

    def test_16_attacknavigator_addcustomtechnique_Enterprise(self):
        """
            Testcase to validate if custom technique under ATT&CK Navigator-> Enterprise can be added
            To Verify if the technique is added under Custom Base Layer
            To Verify if Att&ck Pattern SDO is created in threat data
            To Verify if Tactics are selected under Associate with MITRE Tactic
        """
        url_domain = APP_URL.split(".")
        fprint(self, "TC_ID: 2016 - ATT&CK Navigator_Add Custom technique under Enterprise")
        set_value("AddCustomtechnique_Enterprise", "CTE" + uniquestr[-4:])
        nav_menu_main(self, "ATT&CK Navigator")
        self.switch_category(category="Enterprise")
        waitfor(self, 20, By.XPATH, "//button[@data-testaction='customTechniques-button']")
        self.driver.find_element_by_xpath("//button[@data-testaction='customTechniques-button']").click()
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Custom Technique')]")
        fprint(self, "Enterprise - ATT&CK Navigator_Add Custom technique slider is opened")
        self.driver.find_element_by_xpath("//input[@name='name']").click()
        fprint(self, "Type Layer Text: " + get_value("AddCustomtechnique_Enterprise"))
        self.driver.find_element_by_xpath("//input[@name='name']"). \
            send_keys(get_value('AddCustomtechnique_Enterprise'))
        self.driver.find_element_by_xpath("//div[@data-testid='tactics']").click()
        sleep(1)
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Reconnaissance')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Reconnaissance')] ").click()
        self.driver.find_element_by_xpath("(//button[contains(text(),'Save')])[2]").click()
        verify_success(self, "Custom Technique created successfully")
        fprint(self, "[PASSED] " + get_value(
            "AddCustomtechnique_Enterprise") + " Enterprise custom technique is successfully Created")
        waitfor(self, 20, By.XPATH, "//div[contains(text(),' Custom Base Layer')]")
        self.driver.find_element_by_xpath("//div[contains(text(),' Custom Base Layer')]").click()
        self.driver.find_element_by_xpath("//input[@name='searchbar']").click()
        self.driver.find_element_by_xpath("//input[@name='searchbar']").send_keys(
            get_value('AddCustomtechnique_Enterprise'))
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'" + get_value('AddCustomtechnique_Enterprise') + "')]")
        fprint(self, "Enterprise - ATT&CK Navigator_Add Custom technique is found in custom base layer")
        nav_menu_main(self, "Threat Data")
        fprint(self, "Searching for the Feed under attack pattern - " + get_value("AddCustomtechnique_Enterprise"))
        verify_data_in_threatdata(self, get_value('AddCustomtechnique_Enterprise'), (url_domain[0])[8:])
        fprint(self, "attack custom technique as SDO is Visible - ")
        sleep(1)
        click_on_intel(self, (url_domain[0])[8:], get_value('AddCustomtechnique_Enterprise'))
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Associate with MITRE Tactics')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Associate with MITRE Tactics')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Enterprise Matrix')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Enterprise Matrix')]").click()
        waitfor(self, 20, By.XPATH, "//*[contains(text(),'Reconnaissance')]/ancestor::li/div/div/span/input[@value='true']")
        fprint(self, "[PASSED] : custom technique has the Reconnaissance checkbox selected under Associate with MITRE Tactic in details page ")

    def test_17_attacknavigator_statscountonmitre_Enterprise(self):
        """
             Testcase to validate if Object Stats count is increasing after import which has relation with att&ck
        """
        fprint(self, "TC_ID: 2017 - ATT&CK Navigator_Object Stats on Mitre under Enterprise")
        fprint(self, "Verifying that import Intel page is loading ")
        select_format(self,format_name='STIX 2.1')
        fprint(self, "format in import intel is selected ")
        select_collection(self, collection_name='Free Text')
        import_file(self, file_name='attackstats.json')
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        sleep(3)#needed so that stats will reflect on attack navigator after import
        nav_menu_main(self, "ATT&CK Navigator")
        self.switch_category(category="Enterprise")
        waitfor(self, 20, By.XPATH, "//button[contains(text(),'Count by')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Count by')]").click()
        waitfor(self, 20, By.XPATH, "//div[@data-testid='checkbox']")
        checkboxes = self.driver.find_elements_by_xpath("//div[@data-testid='checkbox']")
        [checkbox.click() for checkbox in checkboxes]
        waitfor(self, 20, By.XPATH, "//span[@class='cyicon-sort']")
        self.driver.find_element_by_xpath("//span[@class='cyicon-sort']").click()
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Descending')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Descending')]").click()
        self.driver.find_element_by_xpath("//input[@name='searchbar']").click()
        self.driver.find_element_by_xpath("//input[@name='searchbar']").send_keys("Trusted Relationship")
        waitfor(self, 20, By.XPATH, "//span[@class='cyicon-indicator']/following-sibling::span[contains(text(),'1')]")
        fprint(self, "Indicator count is seen on mitre grid")
        waitfor(self, 20, By.XPATH, "//span[@class='cyicon-malware']/following-sibling::span[contains(text(),'1')]")
        fprint(self, "malware count is seen on mitre grid")
        waitfor(self, 20, By.XPATH, "//span[@class='cyicon-threat-actor']/following-sibling::span[contains(text(),'1')]")
        fprint(self, "threat-actor count is seen on mitre grid")

if __name__ == '__main__':
    unittest.main(testRunner=reporting())
