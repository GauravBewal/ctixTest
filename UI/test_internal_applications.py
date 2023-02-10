import unittest
from lib.ui.integration_management import *


class InternalApplications(unittest.TestCase):

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

    def test_20_configure_QRADAR(self):
        """
        Checking if Qradar account can be added successfully
        """
        fprint(self, "TC_ID: 71003 - verify configure")
        nav_menu_admin(self, "Integration Management")
        waitfor(self, 20, By.XPATH, "//a/span[contains(text(), 'Internal Applications')]")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Internal Applications')]").click()
        fprint(self, "Clicking on SIEM tools")
        waitfor(self, 20, By.XPATH, "//div[p[contains(text(), 'Security Information and Event')]]")
        self.driver.find_element_by_xpath("//div[p[contains(text(), 'Security Information and Event')]]").click()
        sleep(2)
        fprint(self, "Adding New QRADAR Account")
        add_qradar_account(self)
        manage_actions(self)
        sleep(2)
        process_console_logs(self)

    def test_21_create_reference_set_in_QRADAR(self):
        """
        Testcase to create a reference set in qradar
        """
        fprint(self, "TC_ID: 71002 - verify create reference set")
        fprint(self, "Launching QRadar")
        set_value("REFERENCE_SET_NAME", "auto" + str(datetime.datetime.now())[-4:])
        self.driver = launch_qradar(self)
        fprint(self, "Clicking on Reference Set Management")
        waitfor(self, 60, By.XPATH, "html//table[@title='Reference Set Management']/tr/td/div")
        self.driver.find_element_by_xpath("html//table[@title='Reference Set Management']/tr/td/div").click()
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        fprint(self, "Clicking on new for Reference set creation")
        waitfor(self, 60, By.XPATH, "//span[@title='New']")
        sleep(60)
        self.driver.find_element_by_xpath("//span[@title='New']").click()
        waitfor(self, 60, By.XPATH, "//div[span[contains(text(), 'New Reference Collection')]]")
        fprint(self, "Filling in the name for Reference Set creation")
        self.driver.find_element_by_xpath("//input[@id='set.name']").send_keys(get_value("REFERENCE_SET_NAME"))
        fprint(self, "Clicking on add")
        self.driver.find_element_by_xpath("//span[@id='set.button.add']").click()
        sleep(10)

    def test_22_delete_reference_set_in_QRADAR(self):
        """
        Function to delete reference set from qradar
        """
        fprint(self, "TC_ID: 71003 - verify delete reference set")
        fprint(self, "Launching Qradar")
        self.driver = launch_qradar(self)
        fprint(self, "Clicking on Reference Set Management")
        waitfor(self, 60, By.XPATH, "html//table[@title='Reference Set Management']/tr/td/div")
        self.driver.find_element_by_xpath("html//table[@title='Reference Set Management']/tr/td/div").click()
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[1])
        sleep(60)
        fprint(self, "Filling in the name of the reference set yto be searched")
        self.driver.find_element_by_xpath("//span[contains(text(), 'Input name')]/ancestor::div[input]").click()
        self.driver.find_element_by_xpath("//span[contains(text(), 'Input name')]/preceding-sibling::input").send_keys(
            get_value("REFERENCE_SET_NAME"))
        sleep(5)
        fprint(self, "Clicking on created reference set")
        self.driver.find_element_by_xpath("//span[@title='Input name']").click()
        waitfor(self, 60, By.XPATH, "//td[contains(text(), '" + get_value("REFERENCE_SET_NAME") + "')]")
        self.driver.find_element_by_xpath("//td[contains(text(), '" + get_value("REFERENCE_SET_NAME") + "')]").click()
        sleep(2)
        fprint(self, "Clicking on delete")
        self.driver.find_element_by_xpath("//span[@title='Delete']").click()
        waitfor(self, 60, By.XPATH, "//div[contains(text(), 'Confirm Deletion')]")
        sleep(10)
        fprint(self, "Clicking on confirm Deletion in Qradar")
        waitfor(self, 60, By.XPATH, "//span[@id='dataDeletionLoadingDialog_btn_deleteBtn']")
        self.driver.find_element_by_xpath("//span[@id='dataDeletionLoadingDialog_btn_deleteBtn']").click()

    def test_23_configure_splunk(self):
        """
            Testcase to validate if splunk can be configured in CTIX
        """
        fprint(self, "TC_ID: 71004: Testing if splunk can be configured successfully")
        nav_menu_admin(self, "Integration Management")
        waitfor(self, 20, By.XPATH, "//a/span[contains(text(), 'Internal Applications')]")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Internal Applications')]").click()
        fprint(self, "Clicking on SIEM tools")
        waitfor(self, 20, By.XPATH, "//div[p[contains(text(), 'Security Information and Event')]]")
        self.driver.find_element_by_xpath("//div[p[contains(text(), 'Security Information and Event')]]").click()
        sleep(2)
        fprint(self, "Adding Splunk Account")
        add_splunk_account(self)
        manage_actions(self)
        sleep(2)
        process_console_logs(self)

    def test_24_create_splunk_lookup_table(self):
        """
            Testcase to add a new lookup table in splunk
        """
        fprint(self, "TC_ID: 71005: Testing if Lookup table is created successfully in Splunk")
        main_driver = launch_splunk(self)
        try:
            set_value("Splunk Lookup", "splnk" + uniquestr[-4:] + ".csv")
            waitfor(self, 20, By.XPATH, "//div[@data-appid='lookup_editor']")
            sleep(5)  # required
            self.driver.find_element_by_xpath("//div[@data-appid='lookup_editor']").click()
            fprint(self, "Opening Lookup Editor")
            waitfor(self, 20, By.XPATH, "//a[contains(text(), 'Create a New Lookup')][span]")
            self.driver.find_element_by_xpath("//a[contains(text(), 'Create a New Lookup')][span]").click()
            fprint(self, "Clicking on Create a New Lookup")
            sleep(2)
            waitfor(self, 20, By.XPATH, "//a[text()='CSV lookup']")
            fprint(self, "Clicking on CSV Lookup")
            self.driver.find_element_by_xpath("//a[text()='CSV lookup']").click()
            waitfor(self, 20, By.XPATH, "//h2[contains(text(),'New Lookup')]")
            fprint(self, "Clicked on New Lookup")
            self.driver.find_element_by_xpath("//input[@data-test='textbox']").click()
            self.driver.find_element_by_xpath("//input[@data-test='textbox']").send_keys(get_value("Splunk Lookup"))
            fprint(self, "Filling in name for the splunk lookup")
            self.driver.find_element_by_xpath("//button/span/span[contains(text(), 'Select')]").click()
            waitfor(self, 20, By.XPATH, "//input[@placeholder='filter']")
            fprint(self, "Filling in Search and Reporting under filters")
            self.driver.find_element_by_xpath("//input[@placeholder='filter']").send_keys("Search & Reporting")
            waitfor(self, 20, By.XPATH, "//button[span/span[text()='Search']]")
            self.driver.find_element_by_xpath("//button[span/span[text()='Search']]").click()
            fields = ['Value', 'Cyware Score', 'Type', 'TLP', 'Severity', 'Criticality']
            for num, field in enumerate(fields):
                _ele = self.driver.find_element_by_xpath("//td[@title='Column" + str(num + 1) + "']")
                _ele.click()
                ActionChains(self.driver).context_click(_ele).perform()
                sleep(2)
                fprint(self, "Adding a new column for " + field)
                self.driver.find_element_by_xpath("//a[text()='Rename this column']").click()
                _alert = self.driver.switch_to.alert
                _alert.send_keys(field)
                sleep(2)
                _alert.accept()
                sleep(2)
            self.driver.find_element_by_xpath("//button[text()='Save Lookup']").click()
            fprint(self, "Saving the created Lookup Table")
            waitfor(self, 20, By.XPATH, "//h2[contains(text(), '" + get_value("Splunk Lookup") + "')]")
        finally:
            main_driver.quit()

    def test_25_delete_splunk_lookup_table(self):
        """
            Testcase to delete the created Lookup Table
        """
        fprint(self, "TC_ID: 71006: Testing if Lookup table is deleted successfully in Splunk")
        main_driver = launch_splunk(self)
        try:
            waitfor(self, 20, By.XPATH, "//div[@data-appid='lookup_editor']")
            sleep(5)
            self.driver.find_element_by_xpath("//div[@data-appid='lookup_editor']").click()
            fprint(self, "Opening Lookup Editor")
            waitfor(self, 20, By.XPATH, "//input[@placeholder='Filter by name']")
            self.driver.find_element_by_xpath("//input[@placeholder='Filter by name']").send_keys(get_value("Splunk Lookup"))
            fprint(self, "Searching for the created lookup table")
            sleep(2)
            fprint(self, "Clicking on delete for the created lookup table")
            self.driver.find_element_by_xpath("//a[@data-name='" + get_value("Splunk Lookup") + "'][text()='Delete']").click()
            waitfor(self, 20, By.XPATH, "//td[@class='delete-lookup-name'][text()='" + get_value("Splunk Lookup") + "']")
            fprint(self, "Clicking on Yes, Delete from the prompt")
            self.driver.find_element_by_xpath("//a[text()='Yes, Delete']").click()
            sleep(2)
            fprint(self, "Searching to check if the lookup table is deleted successfully")
            clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Filter by name']"))
            self.driver.find_element_by_xpath("//input[@placeholder='Filter by name']").send_keys(get_value("Splunk Lookup"))
            if waitfor(self, 5, By.XPATH, "//a[@data-name='" + get_value("Splunk Lookup") + "']", False):
                raise Exception("Lookup Table " + get_value("Splunk Lookup") + " failed to get deleted")
            else:
                fprint(self, "Lookup Table " + get_value("Splunk Lookup") + " deleted successfully")
        finally:
            main_driver.quit()

    def test_26_configure_cortex_soar(self):
        """
            Testcase to check if Cortex SOAR account can be added
        """
        fprint(self, "TC_ID: 71007: Testing if CORTEX SOAR account can be added")
        nav_menu_admin(self, "Integration Management")
        waitfor(self, 20, By.XPATH, "//a/span[contains(text(), 'Internal Applications')]")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Internal Applications')]").click()
        fprint(self, "Clicking on SIEM tools")
        waitfor(self, 20, By.XPATH, "//div[p[contains(text(), 'Security Orchestration Automation Response')]]")
        self.driver.find_element_by_xpath("//div[p[contains(text(), 'Security Orchestration Automation Response')]]") \
            .click()
        sleep(2)
        fprint(self, "Adding CORTEX SOAR Account")
        add_cortex_soar_account(self)
        manage_actions(self)

    def test_27_create_cortex_soar_incident(self):
        """
            Testcase to add an instance in CORTEX SOAR
        """
        fprint(self, "TC_ID: 71008: Testing if CORTEX SOAR incident can be added")
        set_value("CORTEX_INCIDENT", "cortex" + uniquestr[-4:])
        launch_cortex_soar(self)
        waitfor(self, 20, By.XPATH, "//div[span[text()='New Incident Type']]")
        self.driver.find_element_by_xpath("//div[span[text()='New Incident Type']]").click()
        waitfor(self, 20, By.XPATH, "//label/span[text()='Name']")
        sleep(2)  # required
        self.driver.find_element_by_xpath("//label[span[text()='Name']]/following-sibling::div/input"). \
            send_keys(get_value("CORTEX_INCIDENT"))
        self.driver.find_element_by_xpath("//button[span/span[text()='Save']]").click()
        sleep(2)
        waitfor(self, 20, By.XPATH, "//input[@placeholder='Search in table...']")
        self.driver.find_element_by_xpath("//input[@placeholder='Search in table...']").send_keys(
            get_value("CORTEX_INCIDENT"))
        if waitfor(self, 20, By.XPATH, "//div[@title='" + get_value("CORTEX_INCIDENT") + "']"):
            fprint(self, "[PASSED] Cortex Incident " + get_value("CORTEX_INCIDENT") + " created successfully")

    def test_28_delete_cortex_soar_incident(self):
        """
            Function to delete the created incident from CORTEX SOAR
        """
        fprint(self, "TC_ID: 71009: Testing if CORTEX SOAR incident can be deleted")
        launch_cortex_soar(self)
        waitfor(self, 20, By.XPATH, "//input[@placeholder='Search in table...']")
        self.driver.find_element_by_xpath("//input[@placeholder='Search in table...']").send_keys(
            get_value("CORTEX_INCIDENT"))
        if waitfor(self, 20, By.XPATH, "//div[@title='" + get_value("CORTEX_INCIDENT") + "']"):
            fprint(self, "[PASSED] Cortex Incident " + get_value("CORTEX_INCIDENT") + " present")
        waitfor(self, 20, By.XPATH, "//input[@type='checkbox'][@class='checkbox-cell-input']")
        self.driver.find_element_by_xpath("//input[@type='checkbox'][@class='checkbox-cell-input']").click()
        waitfor(self, 20, By.XPATH, "//div[span[text()='Delete']]")
        sleep(2)  # required
        self.driver.find_element_by_xpath("//div[span[text()='Delete']]").click()
        waitfor(self, 20, By.XPATH, "//span[text()='Delete incident type?']")
        self.driver.find_element_by_xpath("//button[span/span[text()='Yes, I know what I am doing']]").click()
        waitfor(self, 20, By.XPATH, "//span[text()='No Results. Check your search syntax.']")
        fprint(self, "[PASSED] Created Incident " + get_value("CORTEX_INCIDENT") + " deleted successfully")

    def test_29_configure_zscaler(self):
        """
            Testcase to configure Zscaler and check if working
        """
        fprint(self, "TC_ID: 71010: Testing if Zscalar account can be added")
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        get_zscaler_key(self)
        self.driver.switch_to.window(self.driver.window_handles[0])
        nav_menu_admin(self, "Integration Management")
        waitfor(self, 20, By.XPATH, "//a/span[contains(text(), 'Internal Applications')]")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Internal Applications')]").click()
        fprint(self, "Clicking on Network Security")
        waitfor(self, 20, By.XPATH, "//div[p[contains(text(), 'Network Security')]]")
        self.driver.find_element_by_xpath("//div[p[contains(text(), 'Network Security')]]").click()
        sleep(2)
        fprint(self, "Adding ZScaler Account")
        add_zscaler_account(self)
        manage_actions(self)

    def test_30_configure_exabeam(self):
        """
            Testcase to configure Exabeam on CTIX
        """
        fprint(self, "TC_ID: 71011 - Testcase to configure EXABEAM on CTIX")
        nav_menu_admin(self, "Integration Management")
        waitfor(self, 20, By.XPATH, "//a/span[contains(text(), 'Internal Applications')]")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Internal Applications')]").click()
        fprint(self, "Clicking on SIEM tools")
        waitfor(self, 20, By.XPATH, "//div[p[contains(text(), 'Security Information and Event')]]")
        self.driver.find_element_by_xpath("//div[p[contains(text(), 'Security Information and Event')]]").click()
        sleep(2)
        add_exabeam_account(self)
        manage_actions(self)

    def test_31_create_exabeam_context_table(self):
        """
            Testcase to create new context table on Exabeam
        """
        set_value("ex_context_table", "exabeam" + uniquestr[-4:])
        fprint(self, "TC_ID: 71012 - Testcase to add a new context Table in Exabeam")
        launch_exabeam(self)
        fprint(self, "Clicking on add new context table button")
        self.driver.find_element_by_xpath("//div[i[text()='add']]").click()
        waitfor(self, 20, By.XPATH, "//div[text()='New Context Table']")
        self.driver.find_element_by_xpath("//input[@name='contextTableName']").send_keys(get_value("ex_context_table"))
        waitfor(self, 20, By.XPATH, "//button[@data-toggle='dropdown']")
        self.driver.find_element_by_xpath("//button[@data-toggle='dropdown']").click()
        fprint(self, "Selecting Key Only from the dropdown")
        waitfor(self, 20, By.XPATH, "//li[a/span[text()='Key Only']]")
        self.driver.find_element_by_xpath("//li[a/span[text()='Key Only']]").click()
        fprint(self, "Clicking on save button")
        self.driver.find_element_by_xpath("//span[text()='SAVE']").click()
        waitfor(self, 120, By.XPATH, "//div[text()='" + get_value("ex_context_table") + "']")

    def test_32_delete_exabeam_context_table(self):
        """
            Testcase to delete the created context table from Exabeam
        """
        launch_exabeam(self)
        _table_name = get_value("ex_context_table")
        self.driver.find_element_by_xpath("//div[i[text()='search']]").click()
        waitfor(self, 20, By.XPATH, "//input[@placeholder='Search context tables']")
        sleep(2)  # needed
        fprint(self, f"Searching for {_table_name} in table")
        self.driver.find_element_by_xpath("//input[@placeholder='Search context tables']").send_keys(_table_name)
        waitfor(self, 20, By.XPATH, "//span[text()='" + _table_name + "']")
        fprint(self, "Clicking on bin icon")
        self.driver.find_element_by_xpath("//div[span[text()='" + _table_name +
                                          "']]/following-sibling::div/span/i[text()='delete']").click()
        fprint(self, "Clicking on DELETE option from the alert")
        waitfor(self, 20, By.XPATH, "//span[text()='DELETE']")
        self.driver.find_element_by_xpath("//span[text()='DELETE']").click()

    def test_33_configure_splunk_phantom(self):
        """
        Checking if Splunk Phantom account can be added successfully
        """
        fprint(self, "TC_ID: 71033 - verify configure")
        nav_menu_admin(self, "Integration Management")
        waitfor(self, 20, By.XPATH, "//a/span[contains(text(), 'Internal Applications')]")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Internal Applications')]").click()
        fprint(self, "Clicking on SIEM tools")
        waitfor(self, 20, By.XPATH, "//div[p[contains(text(), 'Security Orchestration Automation Response')]]")
        self.driver.find_element_by_xpath(
            "//div[p[contains(text(), 'Security Orchestration Automation Response')]]").click()
        sleep(2)
        fprint(self, "Adding Splunk Phantom Account")
        add_splunk_phantom_account(self)
        manage_actions(self)
        sleep(2)
        process_console_logs(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
