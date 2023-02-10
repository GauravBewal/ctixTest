import unittest
from lib.ui.nav_app import *


class BackgroundTasks(unittest.TestCase):

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

    def test_01_background_page_load(self):
        """
        Verify if background tasks page is loading
        """
        nav_menu_main(self, "Background Tasks")
        fprint(self, "--------- TC_ID 1: Verifying if Background Tasks page is loading")
        waitfor(self, 2, By.XPATH, "//h1[contains(text(),'Background Tasks')]")
        fprint(self, "[PASSED] Background tasks page loaded successfully")
        process_console_logs(self)

    def test_02_task_queues_check(self):
        """
        Verify if all the task queues are being shown
        """
        fprint(self, "\n--------- TC_ID 2: Verifying if all task queues are listed ---------")
        nav_menu_main(self, "Background Tasks")
        waitfor(self, 2, By.XPATH, "//button[contains(text(),'Task Queues')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Task Queues')]").click()
        waitfor(self, 2, By.XPATH, "//div[contains(text(),'Task Queues')]")
        waitfor(self, 10, By.XPATH, "//div[@class='cy-right-modal-content']//span[contains(text(),'critical')]")
        fprint(self, "[PASSED] critical queue name is found")
        waitfor(self, 10, By.XPATH, "//div[@class='cy-right-modal-content']//span[contains(text(),'high')]")
        fprint(self, "[PASSED] high queue name is found")
        waitfor(self, 10, By.XPATH, "//div[@class='cy-right-modal-content']//span[contains(text(),'medium')]")
        fprint(self, "[PASSED] medium queue name is found")
        waitfor(self, 10, By.XPATH, "//div[@class='cy-right-modal-content']//span[contains(text(),'low')]")
        fprint(self, "[PASSED] low queue name is found")
        fprint(self, "[PASSED] All queues are listed in the slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        process_console_logs(self)

    def test_03_refresh_tasks(self):
        """
        Verify if refresh tasks is working as expected
        """
        nav_menu_main(self, "Background Tasks")
        fprint(self, "\n--------- TC_ID 3: Verify if refresh tasks is working as expected --------")
        waitfor(self, 2, By.XPATH, "//button/following-sibling::div//button[contains(text(),'Refresh')]")
        self.driver.find_element_by_xpath\
            ("//button/following-sibling::div//button[contains(text(),'Refresh')]").click()
        waitfor(self, 2, By.XPATH, "//span[@data-testid='task_title']")
        fprint(self, "[PASSED] Refresh button is working as expected")
        process_console_logs(self)


if __name__ == '__main__':
    unittest.main()
