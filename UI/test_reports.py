import unittest
from lib.ui.nav_reports import *
from lib.ui.nav_threat_data import select_threatData_filter

global_reportName = "Global_Report"
private_reportName = "Private_Report"
flag = "OLD"


class Reports(unittest.TestCase):

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

    def add_report(self, report_name, report_type, flag):
        fprint(self, "[PASSED] - Validating if Report/Title Name field is present...")
        if waitfor(self, 5, By.XPATH, "//input [@placeholder = 'Report Name*']", False) and flag == "OLD":
            self.driver.find_element_by_xpath("//input [@placeholder = 'Report Name*']").send_keys(report_name)
            fprint(self, "Found the field, entered Report Name")
        elif waitfor(self, 1, By.XPATH, "//input[@name='title']", False):
            self.driver.find_element_by_xpath("//input [@name='title']").send_keys(report_name)
            fprint(self, "Found the field, entered Report Name")
            self.driver.find_element_by_xpath("//button[contains(text(),' Add ')]").click()
            fprint(self, "Clicked on the Add Button")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[@role='tab']/following-sibling::div//span[contains(text(),'Indicator')]").click()
        fprint(self, "[Passed] - Selected Indicator as Object type")
        waitfor(self, 20, By.XPATH, "//span[@data-key='name']")
        sleep(2)
        self.driver.find_element_by_xpath("//span[contains(text(), 'Save')]/ancestor::button").click()
        fprint(self, "[Passed] - Clicked on Save button")
        if report_type == "Global":
            waitfor(self, 5, By.XPATH, "//li[contains(text(), 'Global Report')]")
            self.driver.find_element_by_xpath("//li[contains(text(), 'Global Report')]").click()
        elif report_type == "Private":
            waitfor(self, 5, By.XPATH, "//li[contains(text(), 'Private Report')]")
            self.driver.find_element_by_xpath("//li[contains(text(), 'Private Report')]").click()

    def schedule_report(self):
        self.driver.find_element_by_xpath("//span[contains(text(), 'Schedule')]").click()
        waitfor(self, 5, By.XPATH, "//div[contains(text(), 'Schedule Report')]")
        self.driver.find_element_by_xpath(
            "//span[contains(text(), 'Start Date & Time*')]/ancestor::div[1]/preceding-sibling::div//input").click()
        fprint(self, "[Passed] - Clicked on Scheduled Report")
        waitfor(self, 5, By.XPATH, "//input[@placeholder = 'Select date']")
        self.driver.find_element_by_xpath("//td[@class = 'available today']").click()
        fprint(self, "[Passed] - Today's date is selected for schedule")
        self.driver.find_element_by_xpath("//div[contains(text(), 'Schedule Report')]").click()
        self.driver.find_element_by_xpath(
            "//div[contains(text(), 'Repeat Interval After')]/following-sibling::div/input").send_keys("1")
        fprint(self, "[Passed] - Entered Value for Repeat Interval")
        self.driver.find_element_by_xpath(
            "//div[contains(text(), 'Duration of Data')]/following-sibling::div/input").send_keys("1")
        fprint(self, "[Passed] - Entered Value for Duration of data")
        element = self.driver.find_element_by_xpath("//span[contains(text(),'File Format')]")
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        sleep(2)
        waitfor(self, 5, By.XPATH, "//div[@name = 'internal_recipients']")
        self.driver.find_element_by_xpath("//div[@name = 'internal_recipients']").click()
        fprint(self, "[Passed] - Clicked on internal recipients")
        waitfor(self, 5, By.XPATH, "//li[contains(@id,'list-item-0')]")
        self.driver.find_element_by_xpath("//input[@name = 'search-input']").send_keys("System")
        fprint(self, "[Passed] - Entered System in internal recipients")
        waitfor(self, 5, By.XPATH, "//div[contains(text(), 'System')]")
        self.driver.find_element_by_xpath("//div[contains(text(), 'System')]").click()
        self.driver.find_element_by_xpath("//div[(contains(text(), 'Both'))]").click()
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Schedule')])[1]").click()

    def navigate_back(self):
        self.driver.find_element_by_xpath("(//i[contains(@class, 'cyicon-chevron-left')])[1]").click()
        fprint(self, "[Passed] - Navigated back to report listing page")

    def close_calender(self):
        try:
            self.driver.find_element_by_xpath("//header[contains(text(),'Run Now')]").click()
            fprint(self, "Clicked on the Run Now title")
        except:
            self.driver.find_element_by_xpath("//div[contains(text(),'Email Recipients')]").click()
            fprint(self, "Clicked on the Email Recipients title")

    def test_01_reports_add(self):
        fprint(self, "TC_ID: 1 - Add Reports")
        nav_menu_main(self, "Reports")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add Report')]").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(),'New')]")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title *']").send_keys("automation_report"+uniquestr)
        sleep(1)
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description']").send_keys("Report_description")
        sleep(1)
        report = self.driver.find_element_by_xpath("//div[contains(text(), 'Report Interval')]")
        self.driver.execute_script("arguments[0].scrollIntoView();", report)
        sleep(2)
        self.driver.find_element_by_xpath("(//span[contains(text(),'Repeat')]/ancestor::div[contains(@class,'cy-select__menu')])[2]").click()
        self.driver.find_element_by_xpath("//li[@id='list-item-0']").click()
        sleep(1)
        self.driver.find_element_by_xpath("(//span[contains(text(),' Select Widget*')]/ancestor::div[contains(@class,'cy-select__menu')])[2]").click()
        self.driver.find_element_by_xpath("//div[contains(text(), 'Detailed IOC report')]").click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[contains(text(), ' Add More Widgets')]").click()
        widget2 = self.driver.find_element_by_xpath("//div[contains(text(), 'Widget 2')]")
        self.driver.execute_script("arguments[0].scrollIntoView();", widget2)
        sleep(2)
        self.driver.find_element_by_xpath("(//span[contains(text(),' Select Widget*')]/ancestor::div[contains(@class,'cy-select__menu')])[4]").click()
        self.driver.find_element_by_xpath("//div[contains(text(), 'No. of IOCs disseminated per Collection')]").click()
        sleep(1)
        recipients = self.driver.find_element_by_xpath("//div[contains(text(), 'Recipients')]")
        self.driver.execute_script("arguments[0].scrollIntoView();", recipients)
        sleep(1)
        self.driver.find_element_by_xpath("(//span[contains(text(), 'Internal')]/ancestor::div[contains(@class,'cy-select__menu--label')])[2]").click()
        self.driver.find_element_by_xpath("(//div[@class='cy-select-search multiple']/input[@type = 'text'])[2]").click()
        self.driver.find_element_by_xpath("//li[@id='list-item-0']").click()
        sleep(2)
        self.driver.find_element_by_xpath("//button[text()='Add' and contains(@class,'primary')]").click()
        verify_success(self, "Report created successfully")
        process_console_logs(self)

    def test_02_reports_check_widgets(self):
        fprint(self, "TC_ID: 2 - Check all the widgets")
        self.driver.find_element_by_xpath("(//button[@data-testid='action'])[1]").click()
        waitfor(self, 2, By.XPATH, "(//li[contains(text(),'Edit Report')])[last()]")
        self.driver.find_element_by_xpath("(//li[contains(text(),'Edit Report')])[last()]").click()
        waitfor(self, 2, By.XPATH, "(//div[contains(text(),'Edit')])[2]")
        widget = self.driver.find_element_by_xpath("//div[contains(text(), 'Widget(s)*')]")
        self.driver.execute_script("arguments[0].scrollIntoView;", widget)
        waitfor(self, 2, By.XPATH, "//div[contains(text(), 'Widget(s)*')]")
        sleep(2)
        self.driver.find_element_by_xpath(
            "(//span[contains(text(),' Select Widget*')]/ancestor::div[contains(@class,'cy-select__menu')])[2]").click()
        widgets = self.driver.find_elements_by_xpath("//ul[@id='dropdown-list']/li")
        list_of_widgets = ['No. of IOCs ingested per Source', 'No. of IOCs disseminated per IOC Type', 'No. of IOCs per IOC Type per Source', 'Daily Domain and URL Report (.ae extension)', 'No. of feeds published to each subscriber', 'Confidence Score distribution on Indicators','No. of IOCs Blocked per IOC Type per Source','Indicator Relations Data','Published IOC Report','User Information','No. of STIX Objects ingested per Object Type','No. of IOCs received per Collection','No. of IOCs ingested from System Feeds','Subscriber Report - Inbox','Daily IP Report (UAE Country)','Daily CSV Report - All IOCs received by Source','IP Distribution over top 5 countries','Daily CSV Report - New IOCs received by Source','No. of IOCs per Source per Confidence','No. of IOCs disseminated per IOC Type per Collection','Top 5 Malware','Top 5 Campaigns','No. of IOCs ingested per RSS Feed Source','No. of IOCs processed per ATT&CK Tactic','No. of Vulnerabilities ingested per Source','Top 5 TTPs','IOC list data','Detailed IOC report','No. of IOCs ingested per Geographical Location','No. of IOCs disseminated per Collection','Top 5 Threat Actors','No. of IOCs ingested per IOC Type','No. of IOCs processed from rules','No. of IOCs ingested from open source feeds.','Subscriber Report - Polling']
        flag = 0
        not_present = ''
        for i in range(1, len(widgets)):
            all_widget = self.driver.find_element_by_xpath(
                "(//ul[@id='dropdown-list']/li)[" + str(i) + "]").text
            if all_widget in list_of_widgets:
                pass
            else:
                not_present += all_widget + ','
                flag = 1
        if flag == 1:
            print(not_present + ' not available in the drop down')
        else:
            print("all widgets are present")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        process_console_logs(self)

    def test_03_reports_edit(self):
        fprint(self, "TC_ID: 3 - Edit Reports")
        self.driver.find_element_by_xpath("(//button[@data-testid='action'])[1]").click()
        sleep(2)
        self.driver.find_element_by_xpath("(//li[contains(text(),'Edit Report')])[last()]").click()
        waitfor(self, 2, By.XPATH, "(//div[contains(text(),'Edit')])[2]")
        sleep(2)
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title *']").send_keys("test")
        self.driver.find_element_by_xpath("//button[text()='Update']").click()
        verify_success(self, "updated successfully")
        #verify_success(self, "updated successfully")
        process_console_logs(self)

    def test_04_reports_runnow(self):
        fprint(self, "TC_ID: 4 - Run Now")
        self.driver.find_element_by_xpath("(//button[@data-testid='action'])[1]").click()
        sleep(2)
        self.driver.find_element_by_xpath("(//li[contains(text(),'Run Now')])[last()]").click()
        waitfor(self, 2, By.XPATH, "(//div[contains(text(),'Run')])[2]")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        process_console_logs(self)

    def test_05_reports_view_run_logs(self):
        fprint(self, "TC_ID: 5 - View Run Logs")
        self.driver.find_element_by_xpath("(//button[@data-testid='action'])[1]").click()
        sleep(2)
        self.driver.find_element_by_xpath("(//li[contains(text(),'View Run Logs')])[last()]").click()
        waitfor(self, 2, By.XPATH, "//span[contains(text(),'Logs')]")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        process_console_logs(self)

    def test_06_reports_view_reports(self):
        fprint(self, "TC_ID: 6 - View Reports")
        self.driver.find_element_by_xpath("(//button[@data-testid='action'])[1]").click()
        sleep(2)
        self.driver.find_element_by_xpath("(//li[contains(text(),'View Report')])[last()]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        process_console_logs(self)

    def test_07_reports_delete_reports(self):
        fprint(self, "TC_ID: 7 - Delete Reports")
        self.driver.find_element_by_xpath("(//button[@data-testid='action'])[1]").click()
        sleep(2)
        self.driver.find_element_by_xpath("(//li[text()='Delete'])[last()]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//button[@name='Delete']").click()
        verify_success(self, "Report deleted successfully")
        #verify_success(self, "Report deleted successfully")
        process_console_logs(self)

    def test_08_v3_report_add_global_report(self):
        global flag
        fprint(self, "TC_ID: 98500 - Reports - add global report")
        nav_menu_main(self, "Reports")
        if waitfor(self, 2, By.XPATH, "//input[@name='title']", False):
            self.driver.find_element_by_xpath("//input[@name='title']").send_keys(global_reportName)
            flag = "NEW"
        self.driver.find_element_by_xpath("//button[contains(text(),'Add')]").click()
        fprint(self, "[Passed] - Clicked on Add Report Button")
        self.add_report(global_reportName, "Global", flag)
        verify_success(self, "Report created successfully")
        fprint(self, "[Passed] - Global Report created")
        self.navigate_back()
        waitfor(self, 5, By.XPATH, "(//span[@data-testid = 'name'])[1]")
        report_name = self.driver.find_element_by_xpath("(//span[@data-testid = 'name'])[1]").text
        search(self, report_name)
        waitfor(self, 5, By.XPATH, "(//span[@data-testid = 'name'])[1]")
        get_report_name = self.driver.find_element_by_xpath("(//span[@data-testid = 'name'])[1]").text
        if report_name.upper() == get_report_name.upper():
            fprint(self, "[Passed] - Report is listed on the page")
        else:
            fprint(self, "[Failed] - Report is not listed on the page")
            self.fail("[Failed] - Report is not listed on the page")

    def test_09_v3_report_edit_global_report(self):
        fprint(self, "TC_ID: 98501 - Reports - edit report")
        nav_menu_main(self, "Reports")
        search(self, global_reportName)
        waitfor(self, 5, By.XPATH, "//span[@data-testid = 'shared_type']")
        report_type = self.driver.find_element_by_xpath("//span[@data-testid = 'shared_type']").text
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element_by_xpath("//span[@data-testid = 'shared_type']")).perform()
        sleep(2)
        waitfor(self, 5, By.XPATH, "//button[@data-testid = 'action']")
        self.driver.find_element_by_xpath("//button[@data-testid = 'action']").click()
        fprint(self, "[Passed] - clicked on action 3 dots")
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Edit')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Edit')]").click()
        fprint(self, "[Passed] - clicked on edit option]")
        waitfor(self, 5, By.XPATH, "//input [@placeholder = 'Report Name*']")
        self.driver.find_element_by_xpath("//input [@placeholder = 'Report Name*']").send_keys("_edit")
        fprint(self, "[Passed] - Edited the report name")
        self.driver.find_element_by_xpath("//span[contains(text(), 'Malware')]").click()
        fprint(self, "[Passed] - Selected Malware as Object type")
        sleep(2)
        waitfor(self, 20, By.XPATH, "//span[@data-key='name']")
        self.driver.find_element_by_xpath("//span[contains(text(), 'Save')]/ancestor::button").click()
        fprint(self, "[Passed] - Clicked on Save button")
        waitfor(self, 5, By.XPATH, "//li[contains(text(), 'Private Report')]")
        if report_type.upper() == "PRIVATE":
            self.driver.find_element_by_xpath("//li[contains(text(), 'Global Report')]").click()
        elif report_type.upper() == "GLOBAL":
            self.driver.find_element_by_xpath("//li[contains(text(), 'Private Report')]").click()
        verify_success(self, "updated successfully")
        self.schedule_report()
        verify_success(self, "Report scheduled successfully")

    def test_10_v3_report_add_private_report(self):
        global flag
        fprint(self, "TC_ID: 98502 - Reports - add private report")
        nav_menu_main(self, "Reports")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(),'Reports')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Add')]").click()
        fprint(self, "[Passed] - Clicked on Add Report Button")
        if waitfor(self, 2, By.XPATH, "//input[@name='title']", False):
            self.driver.find_element_by_xpath("//input[@name='title']").send_keys(private_reportName)
            self.driver.find_element_by_xpath("(//button[contains(text(),'Add')])[2]").click()
            flag="NEW"
        self.add_report(private_reportName, "Private", flag)
        verify_success(self, "Report created successfully")
        fprint(self, "[Passed] - Private Report created")
        self.navigate_back()
        waitfor(self, 5, By.XPATH, "(//span[@data-testid = 'name'])[1]")
        report_name = self.driver.find_element_by_xpath("(//span[@data-testid = 'name'])[1]").text
        search(self, report_name)
        waitfor(self, 5, By.XPATH, "(//span[@data-testid = 'name'])[1]")
        get_report_name = self.driver.find_element_by_xpath("(//span[@data-testid = 'name'])[1]").text
        if report_name.upper() == get_report_name.upper():
            fprint(self, "[Passed] - Report is listed on the page")
        else:
            fprint(self, "[Failed] - Report is not listed on the page")
            self.fail("[Failed] - Report is not listed on the page")

    def test_11_v3_report_edit_private_report(self):
        fprint(self, "TC_ID: 98503 - Reports - edit report")
        nav_menu_main(self, "Reports")
        search(self, private_reportName)
        waitfor(self, 5, By.XPATH, "//span[@data-testid = 'shared_type']")
        report_type = self.driver.find_element_by_xpath("//span[@data-testid = 'shared_type']").text
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element_by_xpath("//span[@data-testid = 'shared_type']")).perform()
        sleep(2)
        waitfor(self, 5, By.XPATH, "//button[@data-testid = 'action']")
        self.driver.find_element_by_xpath("//button[@data-testid = 'action']").click()
        fprint(self, "[Passed] - clicked on action 3 dots")
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Edit')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Edit')]").click()
        fprint(self, "[Passed] - clicked on edit option")
        waitfor(self, 5, By.XPATH, "//input [@placeholder = 'Report Name*']")
        self.driver.find_element_by_xpath("//input [@placeholder = 'Report Name*']").send_keys("_edit")
        fprint(self, "[Passed] - Edited the report name")
        self.driver.find_element_by_xpath("//span[contains(text(), 'Malware')]").click()
        fprint(self, "[Passed] - Selected Malware as Object type")
        sleep(2)
        waitfor(self, 20, By.XPATH, "//span[@data-key='name']")
        self.driver.find_element_by_xpath("//span[contains(text(), 'Save')]/ancestor::button").click()
        fprint(self, "[Passed] - Clicked on Save button")
        waitfor(self, 5, By.XPATH, "//li[contains(text(), 'Private Report')]")
        if report_type.upper() == "PRIVATE":
            self.driver.find_element_by_xpath("//li[contains(text(), 'Global Report')]").click()
        elif report_type.upper() == "GLOBAL":
            self.driver.find_element_by_xpath("//li[contains(text(), 'Private Report')]").click()
        verify_success(self, "updated successfully")
        self.schedule_report()
        verify_success(self, "Report scheduled successfully")

    def test_12_v3_report_run_report(self):
        fprint(self, "TC_ID: 98504 - Reports - Run report")
        nav_menu_main(self, "Reports")
        search(self, private_reportName)
        waitfor(self, 5, By.XPATH, "//span[@data-testid = 'shared_type']")
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element_by_xpath("//span[@data-testid = 'shared_type']")).perform()
        sleep(2)
        waitfor(self, 5, By.XPATH, "//button[@data-testid = 'action']")
        self.driver.find_element_by_xpath("//button[@data-testid = 'action']").click()
        fprint(self, "[Passed] - clicked on action 3 dots")
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Run Now')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Run Now')]").click()
        fprint(self, "[Passed] - clicked on run now option]")
        waitfor(self, 5, By.XPATH, "(//span[@class = 'el-input__prefix'])[1]")
        self.driver.find_element_by_xpath("(//span[@class = 'el-input__prefix'])[1]").click()
        fprint(self, "[Passed - Clicked on the start date field]")
        waitfor(self, 5, By.XPATH, "(//td[@class = 'available today'])[1]")
        self.driver.find_element_by_xpath("(//td[@class = 'available today'])[1]").click()
        fprint(self, "[Passed] - Today's date is selected as start date")
        self.close_calender()
        waitfor(self, 5, By.XPATH, "(//span[@class = 'el-input__prefix'])[2]")
        self.driver.find_element_by_xpath("(//span[@class = 'el-input__prefix'])[2]").click()
        fprint(self, "[Passed - Clicked on end date field]")
        waitfor(self, 5, By.XPATH, "(//td[@class = 'available today'])[1]")
        self.driver.find_element_by_xpath("(//td[@class = 'available today'])[1]").click()
        fprint(self, "[Passed] - Today's date is selected as end date")
        self.close_calender()
        sleep(1)
        self.driver.find_element_by_xpath("//div[(contains(text(), 'Both'))]").click()
        fprint(self, "[Passed] - Clicked on both as File format")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Proceed')]").click()
        fprint(self, "[Passed] - Clicked on proceed")
        verify_success(self, "We will notify you through email once the report has been generated, and it will be available under History")
        # process_console_logs(self)

    def test_13_v3_report_History_report(self):
        fprint(self, "TC_ID: 98505 - Reports - report history")
        nav_menu_main(self, "Reports")
        search(self, global_reportName)
        waitfor(self, 5, By.XPATH, "//span[@data-testid = 'shared_type']")
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element_by_xpath("//span[@data-testid = 'shared_type']")).perform()
        sleep(2)
        waitfor(self, 5, By.XPATH, "//button[@data-testid = 'action']")
        self.driver.find_element_by_xpath("//button[@data-testid = 'action']").click()
        fprint(self, "[Passed] - clicked on action 3 dots")
        waitfor(self, 5, By.XPATH, "//div[@id='action-popper']//div[contains(text(),'History')]")
        self.driver.find_element_by_xpath("//div[@id='action-popper']//div[contains(text(),'History')]").click()
        fprint(self, "[Passed] - clicked on history option]")
        fprint(self, "[Passed] - verify if all the run history is coming or not")
        if waitfor(self, 5, By.XPATH, "//span[contains(text(), 'No Data found!')]", False):
            fprint(self, "[Failed] No History found")
            self.fail("[Failed] No History found")
        else:
            fprint(self, "Found History")

    def test_14_v3_report_Delete_report(self):
        fprint(self, "TC_ID: 98506 - Reports - delete report")
        nav_menu_main(self, "Reports")
        search(self, global_reportName)
        waitfor(self, 5, By.XPATH, "//span[@data-testid = 'shared_type']")
        actions = ActionChains(self.driver)
        actions.move_to_element(self.driver.find_element_by_xpath("//span[@data-testid = 'shared_type']")).perform()
        sleep(2)
        waitfor(self, 5, By.XPATH, "//button[@data-testid = 'action']")
        self.driver.find_element_by_xpath("//button[@data-testid = 'action']").click()
        fprint(self, "[Passed] - clicked on action 3 dots")
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Delete')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Delete')]").click()
        fprint(self, "[Passed] - clicked on Delete option]")
        waitfor(self, 5, By.XPATH, "//button[contains(text(), 'Delete')]")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Delete')]").click()
        fprint(self, "Confirm Deleted")
        verify_success(self, "Report deleted successfully")

    # Right now of no use, should include some valuable assertions in it.
    # def test_15_v3_report_view_report(self):
    #     fprint(self, "TC_ID: 98507 - Reports - view report")
    #     nav_menu_main(self, "Reports")
    #     search(self, private_reportName)
    #     waitfor(self, 5, By.XPATH, "//span[@data-testid = 'shared_type']")
    #     actions = ActionChains(self.driver)
    #     actions.move_to_element(self.driver.find_element_by_xpath("//span[@data-testid = 'shared_type']")).perform()
    #     waitfor(self, 5, By.XPATH, "//i[@class = 'cy-color-base-primary cyicon-eye']")
    #     self.driver.find_element_by_xpath("//i[@class = 'cy-color-base-primary cyicon-eye']").click()
    #     fprint(self, "[Passed] - Clicked on view icon")
    #     waitfor(self, 5, By.XPATH, "//span[contains(text(), 'Schedule') and contains(@class,'medium')]")
    #     fprint(self, "[Passed] - View checkbox opened")
    #     process_console_logs(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
