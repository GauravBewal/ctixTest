import unittest
from lib.ui.nav_app import *
from lib.ui.nav_tableview import click_on_actions_item
from lib.ui.quick_add import quick_create_ip
from lib.ui.nav_threat_data import verify_data_in_threatdata


class Tasks(unittest.TestCase):

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

    def test_01_upcoming_tasks(self):
        """
        Validating if upcoming tasks are loading
        """
        fprint(self, "TC_ID 67891: Testing if upcoming tasks page is loading")
        nav_menu_main(self, "Tasks")
        waitfor(self, 2, By.XPATH, "//a//span[contains(text(), 'Upcoming Tasks')]")
        self.driver.find_element_by_xpath("//a//span[contains(text(), 'Upcoming Tasks')]").click()
        if waitfor(self, 2, By.XPATH, "//h1[contains(text(), 'Upcoming Tasks')]", False):
            fprint(self, "[PASSED] Upcoming tasks loading with tasks")
        elif waitfor(self, 2, By.XPATH, "//h1[contains(text(), 'No Tasks in your queue!')]"):
            fprint(self, "[PASSED] Upcoming tasks loading but no tasks found")
        fprint(self, "Upcoming Tasks page loaded successfully")
        process_console_logs(self)

    def test_02_in_progress_tasks(self):
        """
        Verify if in progress tasks page is loading
        """
        fprint(self, "TC_ID 67892: Testing if In Progress tasks page is loading")
        nav_menu_main(self, "Tasks")
        waitfor(self, 2, By.XPATH, "//a//span[contains(text(), 'In Progress Tasks')]")
        self.driver.find_element_by_xpath("//a//span[contains(text(), 'In Progress Tasks')]").click()
        if waitfor(self, 2, By.XPATH, "//h1[contains(text(), 'In Progress Tasks')]", False):
            fprint(self, "[PASSED] In Progress tasks loading with tasks")
        elif waitfor(self, 2, By.XPATH, "//h1[contains(text(), 'No Tasks in your queue!')]"):
            fprint(self, "[PASSED] In Progress tasks loading but no tasks found")
        fprint(self, "In Progress Tasks page loaded successfully")
        process_console_logs(self)

    def test_03_completed_tasks(self):
        """
        Verify if completed tasks page is loading
        """
        fprint(self, "TC_ID 67893: Testing if Completed tasks page is loading")
        nav_menu_main(self, "Tasks")
        waitfor(self, 2, By.XPATH, "//a//span[contains(text(), 'Completed Tasks')]")
        self.driver.find_element_by_xpath("//a//span[contains(text(), 'Completed Tasks')]").click()
        if waitfor(self, 2, By.XPATH, "//h1[contains(text(), 'Completed Tasks')]", False):
            fprint(self, "[PASSED] Completed tasks loading with tasks")
        elif waitfor(self, 2, By.XPATH, "//h1[contains(text(), 'No Tasks in your queue!')]"):
            fprint(self, "[PASSED] Completed tasks loading but no tasks found")
        fprint(self, "Completed Tasks page loaded successfully")
        process_console_logs(self)

    def test_04_created_by_me(self):
        """
        Validating if created by me tasks page is loading
        """
        fprint(self, "TC_ID 67894: Testing if Completed tasks page is loading")
        nav_menu_main(self, "Tasks")
        waitfor(self, 5, By.XPATH, "//span[contains(text(), 'Created by Me')]")
        self.driver.find_element_by_xpath("//span[contains(text(), 'Created by Me')]").click()
        if waitfor(self, 3, By.XPATH, "//div/h1[contains(text(), 'Tasks')][following-sibling::div]", False):
            fprint(self, "[PASSED] Created by Me tasks page is loaded with tasks")
        elif waitfor(self, 3, By.XPATH, "//h1[contains(text(), 'No Tasks Found!')]"):
            fprint(self, "[PASSED] Created by me tasks page loading but no tasks found")
        fprint(self, "Created by Me tasks page is loaded successfully")
        process_console_logs(self)

    def test_05_all_tasks(self):
        """
        Validating if created by me tasks page is loading
        """
        fprint(self, "TC_ID 67895: Testing if All tasks page is loading")
        nav_menu_main(self, "Tasks")
        waitfor(self, 5, By.XPATH, "//span[contains(text(), 'All Tasks')]")
        self.driver.find_element_by_xpath("//span[contains(text(), 'All Tasks')]").click()
        if waitfor(self, 3, By.XPATH, "//div/h1[contains(text(), 'Tasks')][following-sibling::div]", False):
            fprint(self, "[PASSED] All tasks page is loaded with tasks")
        elif waitfor(self, 3, By.XPATH, "//h1[contains(text(), 'No Tasks Found!')]"):
            fprint(self, "[PASSED] All tasks page loading but no tasks found")
        fprint(self, "All tasks page is loaded successfully")
        process_console_logs(self)

    def test_06_high_priority_tasks(self):
        """
        Validating if high priority tasks page is loading
        """
        fprint(self, "TC_ID 67896: Testing if High Priority tasks page is loading")
        nav_menu_main(self, "Tasks")
        waitfor(self, 5, By.XPATH, "//span[contains(text(), 'All Tasks')]")
        self.driver.find_element_by_xpath("//span[contains(text(), 'All Tasks')]").click()
        waitfor(self, 2, By.XPATH, "//li[contains(text(), 'High Priority')]")
        self. driver.find_element_by_xpath("//li[contains(text(), 'High Priority')]").click()
        if waitfor(self, 3, By.XPATH, "//div/h1[contains(text(), 'Tasks')][following-sibling::div]", False):
            fprint(self, "[PASSED] High Priority tasks page is loaded with tasks")
        elif waitfor(self, 3, By.XPATH, "//h1[contains(text(), 'No Tasks Found!')]"):
            fprint(self, "[PASSED] High Priority tasks page loading but no tasks found")
        fprint(self, "High Priority tasks page loaded successfully")
        process_console_logs(self)

    def test_07_medium_priority_tasks(self):
        """
        Validating if medium priority tasks page is loading
        """
        fprint(self, "TC_ID 67897: Testing if Medium Priority tasks page is loading")
        nav_menu_main(self, "Tasks")
        waitfor(self, 5, By.XPATH, "//span[contains(text(), 'All Tasks')]")
        self.driver.find_element_by_xpath("//span[contains(text(), 'All Tasks')]").click()
        waitfor(self, 2, By.XPATH, "//li[contains(text(), 'Medium Priority')]")
        self. driver.find_element_by_xpath("//li[contains(text(), 'Medium Priority')]").click()
        if waitfor(self, 3, By.XPATH, "//div/h1[contains(text(), 'Tasks')][following-sibling::div]", False):
            fprint(self, "[PASSED] Medium Priority tasks page is loaded with tasks")
        elif waitfor(self, 3, By.XPATH, "//h1[contains(text(), 'No Tasks Found!')]"):
            fprint(self, "[PASSED] Medium Priority tasks page loading but no tasks found")
        fprint(self, "Medium Priority tasks page loaded successfully")
        process_console_logs(self)

    def test_08_low_priority_tasks(self):
        """
        Validating if low priority tasks page is loading
        """
        fprint(self, "TC_ID 67898: Testing if Low Priority tasks page is loading")
        nav_menu_main(self, "Tasks")
        waitfor(self, 5, By.XPATH, "//span[contains(text(), 'All Tasks')]")
        self.driver.find_element_by_xpath("//span[contains(text(), 'All Tasks')]").click()
        waitfor(self, 2, By.XPATH, "//li[contains(text(), 'Low Priority')]")
        self. driver.find_element_by_xpath("//li[contains(text(), 'Low Priority')]").click()
        if waitfor(self, 3, By.XPATH, "//div/h1[contains(text(), 'Tasks')][following-sibling::div]", False):
            fprint(self, "[PASSED] Low Priority tasks page is loaded with tasks")
        elif waitfor(self, 3, By.XPATH, "//h1[contains(text(), 'No Tasks Found!')]"):
            fprint(self, "[PASSED] Low Priority tasks page loading but no tasks found")
        fprint(self, "Low Priority tasks page loaded successfully")
        process_console_logs(self)

    def test_09_show_all_priority_tasks(self):
        """
        Validating if all priority tasks page is loading
        """
        fprint(self, "TC_ID 67899: Testing if Show All Priority tasks page is loading")
        nav_menu_main(self, "Tasks")
        waitfor(self, 5, By.XPATH, "//span[contains(text(), 'All Tasks')]")
        self.driver.find_element_by_xpath("//span[contains(text(), 'All Tasks')]").click()
        waitfor(self, 2, By.XPATH, "//li[contains(text(), 'Show All')]")
        self. driver.find_element_by_xpath("//li[contains(text(), 'Show All')]").click()
        if waitfor(self, 3, By.XPATH, "//div/h1[contains(text(), 'Tasks')][following-sibling::div]", False):
            fprint(self, "[PASSED] Show All Priority tasks page is loaded with tasks")
        elif waitfor(self, 3, By.XPATH, "//h1[contains(text(), 'No Tasks Found!')]"):
            fprint(self, "[PASSED] Show All Priority tasks page loading but no tasks found")
        fprint(self, "Show All Priority tasks page loaded successfully")
        process_console_logs(self)

    def test_10_Verify_Module_load_successfully(self):
        fprint(self, "TC_ID 678910: Testing the Task Module loaded successfully")
        nav_menu_main(self, "Tasks")
        fprint(self, "[Passed]-Clicked on the task Module")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(),'Tasks')]")
        fprint(self, "[Passed]-The heading Loaded Successfully")
        waitfor(self, 5, By.XPATH, "//div/span[contains(text(),'Assignee')]")
        fprint(self, "[Passed]-The Assignee is Loaded Successfully.")
        waitfor(self, 5, By.XPATH, "(//div/span[contains(text(),'Priority')])[1]")
        fprint(self, "[Passed]-Priority  is Loaded Successfully.")
        waitfor(self, 5, By.XPATH, "//div/span[contains(text(),'Created by')]")
        fprint(self, "[Passed]-Created By  is Loaded Successfully.")
        waitfor(self, 5, By.XPATH, "//div/span[contains(text(),'Deadline')]")
        fprint(self, "[Passed]-Deadline is Loaded Successfully.")
        waitfor(self, 5, By.XPATH, "(//div/span[contains(text(),'Not Started')])[1]")
        fprint(self, "[Passed]-Not started is Loaded Successfully.")
        waitfor(self, 5, By.XPATH, "(//div/span[contains(text(),'Assigned to me')])")
        fprint(self, "[Passed]-Assigned to me is Loaded Successfully.")
        waitfor(self, 5, By.XPATH, "(//div/span[contains(text(),'High Priority')])")
        fprint(self, "[Passed]-High Priority is Loaded Successfully.")
        waitfor(self, 5, By.XPATH, "(//span[contains(text(),'In Progress')])[1]")
        fprint(self, "[Passed]-In Progress is Loaded Successfully.")
        waitfor(self, 5, By.XPATH, "(//span[contains(text(),'Completed')])[1]")
        fprint(self, "[Passed]-Completed is Loaded Successfully.")

    def test_11_Verify_Show_all_Selected(self):
        fprint(self, "TC_ID 678911: Testing if Show All is selected By default")
        nav_menu_main(self, "Tasks")
        fprint(self, "[Passed]-Clicked on the task Module")
        waitfor(self, 10, By.XPATH, "//h1[contains(text(),'Tasks')]")
        fprint(self, "[Passed]-Clicked on the Priority Button")
        self.driver.find_element_by_xpath("(//div/span[contains(text(),'Priority')])[1]").click()
        waitfor(self, 10, By.XPATH, "//span[@class='cy-flex-center cy-text-f12-medium']/span[contains(text(),'Show All')]")
        fprint(self, "[Passed]-Show All is selected By Default")

    def test_12_Verify_Task_created(self):
        fprint(self, "TC_ID 678912: Testing that the task which is created in threat data ")
        quick_create_ip(self, '12.12.12.44', 'task_report')
        nav_menu_main(self, 'Threat Data')
        fprint(self, "[Passed]-Clicked on the threat data")
        verify_data_in_threatdata(self, '12.12.12.44', "Import")
        fprint(self, "clicking on the search button")
        sleep(5)
        ele = self.driver.find_element_by_xpath("(//span[contains(text(),'12.12.12.44')]/ancestor::tr//span/input/ancestor::span)[1]")
        action = ActionChains(self.driver).move_to_element(ele)
        action.click()
        action.perform()
        waitfor(self, 10, By.XPATH, "//button[normalize-space()='Bulk Actions']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Bulk Actions']").click()
        sleep(5)
        self.driver.find_element_by_xpath("//div[normalize-space()='New Task']").click()
        waitfor(self, 10, By.XPATH, "//header[contains(text(),'New Task')]")
        self.driver.find_element_by_xpath("//textarea[@placeholder='Enter a task']").send_keys('Task_1')
        fprint(self, "[Passed]- Entered the name of the task")
        self.driver.find_element_by_xpath("//i[@class='cyicon-user cy-color-B30 cy-text-f16']").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Assign to Self')]").click()
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        verify_success(self, "Tasks are created for the selected objects successfully")

    def test_13_Verify_task_visible(self):
        fprint(self, "TC_ID 678913: Testing that the task is visible in Task Module ")
        nav_menu_main(self, "Tasks")
        fprint(self, "[Passed]-Clicked on the task Module")
        self.driver.find_element_by_xpath("(//span[contains(@data-testaction,'search-icon')])[1]").click()
        fprint(self, "[Passed]-Click on search Icon")
        waitfor(self, 10, By.XPATH, "(//input[contains(@placeholder,'Search')])[2]")
        fprint(self, "[Passed] -Waited for the search option")
        self.driver.find_element_by_xpath("(//input[contains(@placeholder,'Search')])[2]").send_keys('Task_1')
        fprint(self, "[Passed]-Send the value for the searching - Task_1")
        waitfor(self, 10, By.XPATH, "(//pre[contains(text(),'Task_1')])[1]")
        fprint(self, "[Passed]-Present in the task Module")

    def test_14_Verify_Not_Started_To_In_Progress(self):
        fprint(self, "TC_ID 678914: verifying that we are able to move the task from not started to In progress state")
        nav_menu_main(self, "Tasks")
        fprint(self, "[Passed]-Navigated to the task module")
        self.driver.find_element_by_xpath("(//span[contains(@data-testaction,'search-icon')])[1]").click()
        fprint(self, "[Passed]-Click on search Icon")
        waitfor(self, 10, By.XPATH, "(//input[contains(@placeholder,'Search')])[2]")
        fprint(self, "[Passed] -Waited for the search option")
        self.driver.find_element_by_xpath("(//input[contains(@placeholder,'Search')])[2]").send_keys('Task_1')
        fprint(self, "[Passed]-Send the value for the searching - Task_1")
        waitfor(self, 10, By.XPATH, "(//pre[contains(text(),'Task_1')])[1]")
        elem1 = self.driver.find_element_by_xpath("//pre[contains(text(),'Task_1')]")
        ActionChains(self.driver).drag_and_drop_by_offset(elem1, 415, 281).perform()
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'1')])[1]")
        fprint(self, "[Passed]-Changed the state from Not started to In Progress State")

    def test_15_verify_In_Progress_To_Completed(self):
        fprint(self, "TC_ID 678915: verifying that we are able to move the task from In Progress  to In Completed State")
        nav_menu_main(self, "Tasks")
        fprint(self, "[Passed]-Navigated to the task module")
        self.driver.find_element_by_xpath("(//span[contains(@data-testaction,'search-icon')])[2]").click()
        fprint(self, "[Passed]-Click on search Icon")
        waitfor(self, 10, By.XPATH, "(//input[contains(@placeholder,'Search')])[2]")
        fprint(self, "[Passed] -Waited for the search option")
        self.driver.find_element_by_xpath("(//input[contains(@placeholder,'Search')])[3]").send_keys('Task_1')
        fprint(self, "[Passed]-Send the value for the searching - Task_1")
        waitfor(self, 10, By.XPATH, "(//pre[contains(text(),'Task_1')])[1]")
        elem1 = self.driver.find_element_by_xpath("//pre[contains(text(),'Task_1')]")
        elem2 = self.driver.find_element_by_xpath("//ul[@data-id='completed']/parent::section")
        ActionChains(self.driver).drag_and_drop(elem1, elem2).perform()
        sleep(10)   # mandatory
        # self.driver.find_element_by_xpath("//i[contains(@class,'cyicon-check-circle-outline')]").click()
        self.driver.find_element_by_xpath("//textarea[@aria-placeholder='Description']").send_keys("Completed")
        fprint(self, "Entered the text for Description")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Done')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Done')]").click()
        fprint(self, "[Passed]-Clicked on the Done Button")

        self.driver.find_element_by_xpath("(//span[@data-testaction='search-icon'])[3]").click()
        fprint(self, "Clicked on the cross button of InProgress")
        self.driver.find_element_by_xpath("//button[@data-testaction='clear']").click()
        fprint(self, "Clicked on the search button of Completed, searching now...")
        waitfor(self, 5, By.XPATH, "(//input[@name='searchbar'])[3]")
        self.driver.find_element_by_xpath("(//input[@name='searchbar'])[3]").send_keys("Task_1")
        waitfor(self, 20, By.XPATH, "//ul[@data-id='completed']//pre[contains(text(),'Task_1')]")
        fprint(self, "[Passed]-Moved to completed State")

    def test_16_Verify_Edit_task(self):
        fprint(self, "TC_ID 678916: Testing that the task is editable ")
        quick_create_ip(self, '12.12.12.43', 'task_report_edited')
        nav_menu_main(self, 'Threat Data')
        fprint(self, "[Passed]-Clicked on the threat data")
        verify_data_in_threatdata(self, '12.12.12.43', "Import")
        fprint(self, "clicking on the search button")
        sleep(5)#mandatory
        ele = self.driver.find_element_by_xpath(
            "(//span[contains(text(),'12.12.12.43')]/ancestor::tr//span/input/ancestor::span)[1]")
        action = ActionChains(self.driver).move_to_element(ele)
        action.click()
        action.perform()
        waitfor(self, 10, By.XPATH, "//button[normalize-space()='Bulk Actions']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Bulk Actions']").click()
        waitfor(self, 10, By.XPATH, "//div[normalize-space()='New Task']")
        self.driver.find_element_by_xpath("//div[normalize-space()='New Task']").click()
        waitfor(self, 10, By.XPATH, "//header[contains(text(),'New Task')]")
        self.driver.find_element_by_xpath("//textarea[@placeholder='Enter a task']").send_keys('Task_2')
        fprint(self, "[Passed]- Entered the name of the task")
        self.driver.find_element_by_xpath("//i[@class='cyicon-user cy-color-B30 cy-text-f16']").click()
        self.driver.find_element_by_xpath("//span[contains(text(),'Assign to Self')]").click()
        self.driver.find_element_by_xpath("//button[normalize-space()='Save']").click()
        verify_success(self, "Tasks are created for the selected objects successfully")
        nav_menu_main(self, "Tasks")
        fprint(self, "[Passed]-Clicked on the task Module")
        self.driver.find_element_by_xpath("(//span[contains(@data-testaction,'search-icon')])[1]").click()
        fprint(self, "[Passed]-Click on search Icon")
        waitfor(self, 10, By.XPATH, "(//input[contains(@placeholder,'Search')])[2]")
        fprint(self, "[Passed] -Waited for the search option")
        self.driver.find_element_by_xpath("(//input[contains(@placeholder,'Search')])[2]").send_keys('Task_2')
        fprint(self, "[Passed]-Send the value for the searching - Task_2")
        waitfor(self, 10, By.XPATH, "(//pre[contains(text(),'Task_2')])[1]")
        self.driver.find_element_by_xpath("(//i[@class= 'cy-color-base-primary cyicon-more'])[1]").click()
        waitfor(self, 10, By.XPATH, "//li[normalize-space()='Edit']")
        self.driver.find_element_by_xpath("//li[normalize-space()='Edit']").click()
        self.driver.find_element_by_xpath("//textarea[@placeholder='Enter a task']").send_keys("Task_2")
        self.driver.find_element_by_xpath("//span[contains(text() ,'Save')]").click()
        self.driver.find_element_by_xpath("(//span[contains(@data-testaction,'search-icon')])[1]").click()
        fprint(self, "[Passed]-Click on search Icon")
        waitfor(self, 10, By.XPATH, "(//input[contains(@placeholder,'Search')])[2]")
        fprint(self, "[Passed] -Waited for the search option")
        self.driver.find_element_by_xpath("(//input[contains(@placeholder,'Search')])[2]").send_keys('Task_2')
        fprint(self, "[Passed]-Send the value Task2 for the searching")
        waitfor(self, 10, By.XPATH, "(//pre[contains(text(),'Task_2Task_2')])[1]")
        fprint(self, "[Passed]- the Task is modified succesfully.")

    def test_17_Verify_Delete_task(self):
        fprint(self, "TC_ID 678917: Verify that Delete is working fine ")
        nav_menu_main(self, "Tasks")
        fprint(self, "[Passed]-Clicked on the task Module")
        self.driver.find_element_by_xpath("(//span[contains(@data-testaction,'search-icon')])[1]").click()
        fprint(self, "[Passed]-Click on search Icon")
        waitfor(self, 10, By.XPATH, "(//input[contains(@placeholder,'Search')])[2]")
        fprint(self, "[Passed] -Waited for the search option")
        self.driver.find_element_by_xpath("(//input[contains(@placeholder,'Search')])[2]").send_keys('Task_2')
        fprint(self, "[Passed]-Send the value Task2 for the searching")
        waitfor(self, 10, By.XPATH, "(//pre[contains(text(),'Task_2Task_2')])[1]")
        self.driver.find_element_by_xpath("(//i[@class= 'cy-color-base-primary cyicon-more'])[1]").click()
        waitfor(self, 10, By.XPATH, "//li[normalize-space()='Delete']")
        self.driver.find_element_by_xpath("//li[normalize-space()='Delete']").click()
        fprint(self, "[Passed]-Task Deleted Succesfully")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
