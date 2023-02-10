import unittest
from lib.ui.nav_threat_data import *

domain = "caentivage.com"    # value taken from the quick add intel domain
analyst_description = "test_analyst_description"
edit_analyst_description = "33.44.55.66"


class ThreatDataDetailsPage(unittest.TestCase):

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

    def test_01_threatdata_SDO_listing(self):
        fprint(self, "TC_ID: 4011500 - Threat data SDO list" +uniquestr)
        nav_menu_main(self, "Threat Data")
        sdo_list= ["Vulnerability", "TTP", 'Malware', 'Campaign', 'Threat Actor', 'Intrusion Set', 'Attack Pattern', 'Incident', 'Course of Action', 'Identity', 'Kill Chain', 'Kill Chain Phases', 'Tool', 'Note', 'Report', 'Infrastructure', 'Location', 'Malware Analysis', "Indicator"]
        for sdo in sdo_list:
            self.driver.find_element_by_xpath("//span[contains(text(),'"+sdo+"')]/ancestor::a[@class='cy-page-menu__link']").click()
            waitfor(self, 15, By.XPATH, "(//div[contains(text(),'"+sdo+"')])[1]")
            fprint(self, "[Passed] - Clicked on '"+sdo+"' object")
            process_console_logs(self)
            clear_console_logs(self)
        fprint(self, "Threat data listing")

    def test_02_indicator_detail(self):
        fprint(self, "TC_ID: 4011501 - Threat data - indicator - details" +uniquestr)
        nav_menu_main(self, "Threat Data")
        # Check if Indicator is already selected, if not then click on the indicator
        if not waitfor(self, 3, By.XPATH, "//span[contains(text(),'Indicator')]/ancestor::a[@class='cy-page-menu__link active']", False):
            self.driver.find_element_by_xpath(
            "//span[contains(text(),'Indicator')]/ancestor::a[@class='cy-page-menu__link']").click()
        # Todo: Search and look for a proper entry which was created earlier
        waitfor(self, 15, By.XPATH, "(//span[@data-testid='name2'])[1]")
        self.driver.find_element_by_xpath("(//span[@data-testid='name2'])[1]").click()
        sleep(2)
        indicator_detail=["Basic Details","Sources","Relations","Investigations","Notes","Tasks","Activity Timeline"]
        for option in indicator_detail:
            self.driver.find_element_by_xpath("//span[contains(text(),'"+option+"')]/ancestor::a[@class-active='active']").click()
            waitfor(self, 15, By.XPATH, "//span[contains(text(),'"+option+"')]/ancestor::span[@role='link']")
            fprint(self, "[Passed] - Clicked on '"+option+"' option of indicator ")
            process_console_logs(self)
            clear_console_logs(self)
        fprint(self, "Threat data listing")

    def test_03_threatvisualizer_redirection(self):
        fprint(self, "TC_ID: 4011502 - Threat data - Threatvisualizer - redirection" + uniquestr)
        nav_menu_main(self, "Threat Data")
        waitfor(self, 15, By.XPATH, "(//span[@class='cy-checkbox__style'])[1]")
        self.driver.find_element_by_xpath("(//span[@class='cy-checkbox__style'])[1]").click()
        sleep(1)
        # Todo: BuildPath This change happened after 2.8.2 builds. present in 2.9 dev builds
        if waitfor(self, 2, By.XPATH, "//button[contains(text(),'Open in Threat Investigations')]", False):
            self.driver.find_element_by_xpath("//button[contains(text(),'Open in Threat Investigations')]").click()
            fprint(self, "[Passed] - Clicked on Open in Threat Investigations button")
            waitfor(self, 15, By.XPATH, "//span[contains(text(),'Threat Investigation')]/ancestor::span[@role='link']")
            fprint(self, "[Passed] - Threat Investigation page opened")
        elif waitfor(self, 2, By.XPATH, "//button[contains(text(),'View in Threat Visualizer')]", False):
            self.driver.find_element_by_xpath("//button[contains(text(),'View in Threat Visualizer')]").click()
            fprint(self, "[Passed] - Clicked on View in Threat Visualizer button")
            waitfor(self, 15, By.XPATH, "//span[contains(text(),'Threat Visualizer')]/ancestor::span[@role='link']")
            fprint(self, "[Passed] - Threat Visualizer page opened")
        else:
            fprint(self, "[Failed] Neither Threat Investigations not Threat Visualizer button was visible")

        #waitfor(self, 15, By.XPATH, "//button[contains(text(),'View in Threat Visualizer')]")
        #self.driver.find_element_by_xpath("//button[contains(text(),'View in Threat Visualizer')]").click()
        #fprint(self, "[Passed] - Clicked on View in Threat Visualizer button")
        #waitfor(self, 15, By.XPATH, "//span[contains(text(),'Threat Visualizer')]/ancestor::span[@role='link']")
        #fprint(self, "[Passed] - Threat Visualizer page opened")

        # self.driver.find_element_by_xpath("//span[contains(text(),'Threat Data')]/ancestor::span[@role='link']").click()
        # waitfor(self, 15, By.XPATH, "/button[contains(text(),'Proceed')]")
        # self.driver.find_element_by_xpath("//button[contains(text(),'Proceed')]").click()
        # fprint(self, "[Passed] - Threat data page opened")
        # process_console_logs(self)

    def test_04_add_detailsPage_analystScore_and_Description(self):
        fprint(self, "TC_ID: 4011504 - test_04_add_detailsPage_analystScore_and_Description")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "IOC Type", "Domain")
        verify_data_in_threatdata(self, domain, "Import")
        sleep(2)    # Sleep is required here
        click_on_intel(self, "Import", domain)
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Basic Details')]")
        fprint(self, "Inside the Intel, Basic Details tab is visible")
        self.driver.find_element_by_xpath("//div[contains(text(),'Basic Details')]").click()
        fprint(self, "Clicked on the Basic Details Page")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Add Analyst Description')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Add Analyst Description')]").click()
        fprint(self, "Clicked on the Add Analyst Description Button")
        waitfor(self, 20, By.XPATH, "//div[contains(@class,'fr-view')]")
        self.driver.find_element_by_xpath("//div[contains(@class,'fr-view')]").click()
        self.driver.find_element_by_xpath("//div[contains(@class,'fr-view')]").send_keys(analyst_description)
        fprint(self, "Added Analyst Description - "+analyst_description)
        self.driver.find_element_by_xpath("//button[@data-testaction='save-description']").click()
        fprint(self, "Clicked on the Save Button")
        waitfor(self, 20, By.XPATH, "//div[contains(@class,'cy-analyst-score__input')]/input")
        fprint(self, "Adding Analyst Score - 44")
        self.driver.find_element_by_xpath("//div[contains(@class,'cy-analyst-score__input')]/input").send_keys("44")
        self.driver.find_element_by_xpath("//*[normalize-space(text())='Correlated View of Sources']").click()
        waitfor(self, 20, By.XPATH, "//span[contains(@class,'cy-analyst-score__score') and normalize-space()='44']")
        fprint(self, "Added Analyst Score - 44")

    def test_05_verify_detailsPage_analystScore_and_Description(self):
        fprint(self, "TC_ID: 4011505 - test_05_verify_detailsPage_analystScore_and_Description")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "IOC Type", "Domain")
        verify_data_in_threatdata(self, domain, "Import")
        sleep(2)    # Sleep is required here
        click_on_intel(self, "Import", domain)
        waitfor(self, 20, By.XPATH, "//div[@data-testid='analyst_description']//p[contains(text(),'"+analyst_description+"')]")
        fprint(self, "Added Analyst description is visible on the Overview Page - "+analyst_description)
        waitfor(self, 20, By.XPATH, "//span[contains(@class,'cy-analyst-score__score') and contains(text(),'44')]")
        fprint(self, "Added Analyst Score is visible on the Overview Page - 44")
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Basic Details')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Basic Details')]").click()
        waitfor(self, 20, By.XPATH, "//p[contains(text(),'"+analyst_description+"')]")
        fprint(self, "Added Analyst Description is visible on the Basic Details Page - "+analyst_description)
        waitfor(self, 20, By.XPATH, "//span[contains(@class,'cy-analyst-score__score') and contains(text(),'44')]")
        fprint(self, "Added Analyst Score is visible on the Basic Details Page - 44")

    def test_06_edit_detailsPage_analystScore_and_Description(self):
        fprint(self, "TC_ID: 4011506 - test_06_edit_detailsPage_analystScore_and_Description")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "IOC Type", "Domain")
        verify_data_in_threatdata(self, domain, "Import")
        sleep(2)  # Sleep is required here
        click_on_intel(self, "Import", domain)
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Basic Details')]")
        fprint(self, "Inside the Intel, Basic Details tab is visible")
        self.driver.find_element_by_xpath("//div[contains(text(),'Basic Details')]").click()
        fprint(self, "Clicked on the Basic Details Page")
        waitfor(self, 20, By.XPATH, "//button[@data-testaction='edit-description']")
        self.driver.find_element_by_xpath("//button[@data-testaction='edit-description']").click()
        fprint(self, "Clicked on the Edit Button")
        waitfor(self, 20, By.XPATH, "//div[contains(@class,'fr-view')]/p")
        self.driver.find_element_by_xpath("//div[contains(@class,'fr-view')]/p").click()
        self.driver.find_element_by_xpath("//div[contains(@class,'fr-view')]/p").clear()
        # clear_field(self.driver.find_element_by_xpath("//div[contains(@class,'fr-view')]/p"))
        self.driver.find_element_by_xpath("//div[contains(@class,'fr-view')]").send_keys(edit_analyst_description)
        fprint(self, "Added Analyst Description - "+edit_analyst_description)
        self.driver.find_element_by_xpath("//button[@data-testaction='save-description']").click()
        waitfor(self, 20, By.XPATH, "//div[contains(@class,'cy-analyst-score__input')]/input")
        fprint(self, "Adding Analyst Score - 50")
        clear_field(self.driver.find_element_by_xpath("//div[contains(@class,'cy-analyst-score__input')]/input"))
        self.driver.find_element_by_xpath("//div[contains(@class,'cy-analyst-score__input')]/input").send_keys("50")
        self.driver.find_element_by_xpath("//*[normalize-space(text())='Correlated View of Sources']").click()
        waitfor(self, 20, By.XPATH, "//span[contains(@class,'cy-analyst-score__score') and contains(text(),'50')]")
        fprint(self, "Added Analyst Score - 50")

    def test_07_verify_edit_detailsPage_analystScore_and_Description(self):
        fprint(self, "TC_ID: 4011507 - test_07_verify_edit_detailsPage_analystScore_and_Description")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "IOC Type", "Domain")
        verify_data_in_threatdata(self, domain, "Import")
        sleep(2)  # Sleep is required here
        click_on_intel(self, "Import", domain)
        waitfor(self, 20, By.XPATH, "//div[@data-testid='analyst_description']//p[contains(text(),'"+edit_analyst_description+"')]")
        fprint(self, "Added Analyst description is visible on the Overview Page - "+edit_analyst_description)
        waitfor(self, 20, By.XPATH, "//span[contains(@class,'cy-analyst-score__score') and contains(text(),'50')]")
        fprint(self, "Added Analyst Score is visible on the Overview Page - 50")
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Basic Details')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Basic Details')]").click()
        waitfor(self, 20, By.XPATH, "//p[contains(text(),'"+edit_analyst_description+"')]")
        fprint(self, "Added Analyst Description is visible on the Basic Details Page - "+edit_analyst_description)
        waitfor(self, 20, By.XPATH, "//span[contains(@class,'cy-analyst-score__score') and contains(text(),'50')]")
        fprint(self, "Added Analyst Score is visible on the Basic Details Page - 50")

    def test_08_verify_detailsPage_fang_defang(self):
        fprint(self, "TC_ID: 4011508 - test_08_verify_detailsPage_fang_defang")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "IOC Type", "Domain")
        verify_data_in_threatdata(self, domain, "Import")
        sleep(2)  # Sleep is required here
        click_on_intel(self, "Import", domain)
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Basic Details')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Basic Details')]").click()
        fprint(self, "Moved to Basic Details page")
        if waitfor(self, 10, By.XPATH, "//div[@data-testid='fang-defang']/button", False):
            self.driver.find_element_by_xpath("//div[@data-testid='fang-defang']/button").click()
        else:
            self.driver.find_element_by_xpath("//div[@data-testid='fang-defang']/span").click()
        waitfor(self, 20, By.XPATH, "//div[@data-testid='description']/p[contains(text(),'33[.]44[.]55[.]66')]")
        fprint(self, "After Fang-Defang enabled - 33[.]44[.]55[.]66")
        try:
            self.driver.find_element_by_xpath("//div[@data-testid='fang-defang']/button").click()
        except:
            self.driver.find_element_by_xpath("//div[@data-testid='fang-defang']/span").click()
        waitfor(self, 20, By.XPATH, "//div[@data-testid='description']/p[contains(text(),'"+edit_analyst_description+"')]")
        fprint(self, "After Fang-Defang disabled - "+edit_analyst_description)
        fprint(self, "Test Case Passed")

    def test_09_verify_detailsPage_quick_actions(self):
        fprint(self, "TC_ID: 4011509 - test_09_verify_detailsPage_quick_actions")
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, domain, "Import")
        sleep(2)  # Sleep is required here
        click_on_intel(self, "Import", domain)
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Manual Review')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Manual Review')]").click()
        verify_success(self, "Selected objects are added for manual review successfully")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Under Manual Review')]")
        fprint(self, "Under Manual Review, option is visible")
        self.driver.find_element_by_xpath("//span[contains(text(),'Under Manual Review')]").click()
        fprint(self, "Clicked on the option - Under Manual Review")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Mark as Reviewed')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Mark as Reviewed')]").click()
        fprint(self, "Mark as Reviewed, option is visible, clicked on it")
        verify_success(self, "Selected objects are marked as reviewed successfully")
        if waitfor(self, 5, By.XPATH, "//span[contains(text(),'Manual Reviewed')]", False) or \
                waitfor(self, 1, By.XPATH, "//span[contains(text(),'Manually Reviewed')]"):
            fprint(self, "Manual Reviewed, option is visible")
        fprint(self, "[Passed] - Quick Action - Manual Review")

        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Deprecate')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Deprecate')]").click()
        fprint(self, "Deprecate, option is visible and clicked on it")
        waitfor(self, 20, By.XPATH, "(//span[contains(text(),'Deprecate')])[2]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'Deprecate')])[2]").click()
        verify_success(self, "Selected indicators are deprecated successfully")
        sleep(1)
        self.driver.find_element_by_xpath("//span[contains(text(),'Deprecated')]").click()
        sleep(2)    # Sleep is needed here
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Undeprecate')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Undeprecate')]").click()
        fprint(self, "Undeprecate, option is visible, clicked on it")
        waitfor(self, 20, By.XPATH, "//td[@class='available today']")
        self.driver.find_element_by_xpath("//td[@class='available today']").click()
        fprint(self, "Calender is visible, selected today's date")
        self.driver.find_element_by_xpath("//span[contains(text(),'Save')]/parent::button").click()
        fprint(self, "Clicked on the Save Button")
        verify_success(self, "Selected indicators are undeprecated successfully")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Deprecate')]")
        fprint(self, "Deprecate, option is visible")
        fprint(self, "[Passed] - Quick Action - Deprecate")

        waitfor(self, 20, By.XPATH, "//span[contains(text(),'False Positive')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'False Positive')]").click()
        fprint(self, "False Positive, option is visible and clicked on it")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Mark False Positive')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Mark False Positive')]").click()
        fprint(self, "Mark False Positive, option is visible and clicked on it")
        verify_success(self, "Selected indicators are marked as false positive successfully")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Marked False Positive')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Marked False Positive')]").click()
        fprint(self, "Marked False Positive, option is visible and clicked on it")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Unmark False Positive')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Unmark False Positive')]").click()
        fprint(self, "Unmark False Positive, option is visible and clicked on it")
        verify_success(self, "Selected indicators are unmarked as false positive successfully")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'False Positive')]")
        fprint(self, "False Positive, option is visible")
        fprint(self, "[Passed] - Quick Action - False Positive")

        waitfor(self, 20, By.XPATH, "//span[contains(text(),'New Task')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'New Task')]").click()
        fprint(self, "New Task, option is visible and clicked on it")
        waitfor(self, 20, By.XPATH, "//textarea[@aria-placeholder='Description']")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description']").send_keys("automation_task")
        fprint(self, "Task Name - automation_task")
        self.driver.find_element_by_xpath("//i[@class='cyicon-user cy-color-B30 cy-text-f16']").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Assign to Self')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Assign to Self')]").click()
        fprint(self, "Selected Assignee - Assign to Self")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        verify_success(self, "Tasks are created for the selected objects successfully")
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Tasks')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Tasks')]").click()
        waitfor(self, 20, By.XPATH, "//pre[contains(text(),'automation_task')]")
        fprint(self, "Created Task is visible under Task Tab")
        fprint(self, "[Passed] - Quick Action - New Task")

    def test_10_verify_detailsPage_tasks(self):
        fprint(self, "TC_ID: 4011510 - test_08_verify_detailsPage_fang_defang")
        nav_menu_main(self, "Threat Data")
        select_threatData_filter(self, "IOC Type", "Domain")
        verify_data_in_threatdata(self, domain, "Import")
        sleep(2)  # Sleep is required here
        click_on_intel(self, "Import", domain)
        waitfor(self, 20, By.XPATH, "//li[@data-cy-event='Tasks' and @role='tab']")
        self.driver.find_element_by_xpath("//li[@data-cy-event='Tasks' and @role='tab']").click()
        waitfor(self, 20, By.XPATH, "//pre[contains(text(),'automation_task')]")
        fprint(self, "Task is visible - automation_task")
        source = self.driver.find_element_by_xpath("(//div[contains(@class,'cy-task-card')])[1]")
        destination = self.driver.find_element_by_xpath("//*[@data-id='in_progress']")
        ActionChains(self.driver).drag_and_drop(source, destination).perform()
        try:
            waitfor(self, 20, By.XPATH, "//span[contains(text(),'Not Started')]/ancestor::header/following-sibling::section//span[contains(text(),'Add Task')]")
        except:
            waitfor(self, 2, By.XPATH, "//div[@data-id='not_started']/parent::main//span[contains(text(),'Add Task')]")
        fprint(self, "Task moved to InProgress")
        source = self.driver.find_element_by_xpath("(//div[contains(@class,'cy-task-card')])[1]")
        destination = self.driver.find_element_by_xpath("//div[@data-id='completed']")
        ActionChains(self.driver).drag_and_drop(source, destination).perform()
        waitfor(self, 20, By.XPATH, "//textarea[@aria-placeholder='Description']")
        fprint(self, "Task moved to Completed, closure comment box appears")
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description']").click()
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description']").send_keys("Closed")
        self.driver.find_element_by_xpath("//span[contains(text(),'Done')]").click()
        waitfor(self, 20, By.XPATH, "//i[contains(@class,'cyicon-comment')]")
        fprint(self, "Task completed with a comment")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
