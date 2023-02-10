import unittest
from lib.ui.nav_app import *
from lib.ui.nav_threat_data import verify_data_in_threatdata


class AssigningTLPThreatData(unittest.TestCase):

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

    def test_01_assign_tlp(self):
        """
         Assigning TLP's to top 5 intels in threat data
        """
        fprint(self, "\n----------- TC_ID: 77000 Testing if TLP is assigned correctly")
        nav_menu_main(self, "Threat Data")
        if Build_Version.__contains__("2."):
            waitfor(self, 5, By.XPATH, "(//span[contains(text(),'Indicator')])[4]")
            fprint(self, "Clicked on indicator field")
            self.driver.find_element_by_xpath("(//span[contains(text(),'Indicator')])[4]").click()
            waitfor(self, 3, By.XPATH, "//tbody/tr[1]/td[1]")

            fprint(self, "Selected the top 5 intel")
            values = []
            for i in range(1, 6):
                waitfor(self, 2, By.XPATH, f"(//span[@data-testid='tlp_data'])[{i}]")
                ele = self.driver.find_element_by_xpath(f"(//span[@data-testid='tlp_data'])[{i}]")
                values.append(self.driver.find_element_by_xpath(f"(//span[@data-testid='name2'])[{i}]").text)
                ele.click()
                sleep(2)

            fprint(self, "Clicked on Bulk Actions button")
            waitfor(self, 5, By.XPATH, "//button[normalize-space()='Bulk Actions']")
            self.driver.find_element_by_xpath("//button[normalize-space()='Bulk Actions']").click()

            fprint(self, "Scrolled down for the tag Add TLP and clicked on it")
            while True:
                try:
                    waitfor(self, 5, By.XPATH, "//li[normalize-space()='Add TLP']")
                    self.driver.find_element_by_xpath("//li[normalize-space()='Add TLP']").click()
                    break
                except:
                    waitfor(self, 3, By.XPATH, "//button[normalize-space()='Bulk Actions']")
                    self.driver.find_element_by_xpath("//button[normalize-space()='Bulk Actions']").send_keys(Keys.ARROW_DOWN)
                    continue

            fprint(self, "Clicked on button for Green")
            waitfor(self, 5, By.XPATH, "//div[normalize-space()='Green']//div//input[contains(@type,'radio')]")
            self.driver.find_element_by_xpath("//div[normalize-space()='Green']//div//input[contains(@type,'radio')]").click()

            fprint(self, "Clicked on save")
            waitfor(self, 5, By.XPATH, "(//button[@type='button'][normalize-space()='Save'])[1]")
            self.driver.find_element_by_xpath("(//button[@type='button'][normalize-space()='Save'])[1]").click()

            verify_success(self, "TLP value is assigned to the selected objects successfully")

            fprint(self, "Printing the selected intels")
            for val in values:
                fprint(self, val)

            fprint(self, "Verified whether TLP was assigned or not")
            for val in values:
                waitfor(self, 2, By.XPATH, "//input[@id='main-input']")
                self.driver.find_element_by_xpath("//input[@id='main-input']").click()

                self.driver.find_element_by_xpath("//input[@id='main-input']").clear()
                self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys(val)
                sleep(3)
                self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys(Keys.ENTER)
                if waitfor(self, 5, By.XPATH, "(//span[@data-testid='first_seen'])[1]", False):
                    self.driver.find_element_by_xpath("(//span[@data-testid='first_seen'])[1]").click()
                    if waitfor(self, 5, By.XPATH, "//button/div[contains(text(), 'GREEN')]", False):
                        fprint(self, f"[PASSED] Correct for intel {val}")
                    else:
                        fprint(self, f"[FAILED] Incorrect for intel {val}")
                    waitfor(self, 3, By.XPATH, "//i[@class='cyicon-chevron-left']")
                    self.driver.find_element_by_xpath("//i[@class='cyicon-chevron-left']").click()
                else:
                    fprint(self, f"[FAILED] There is some bug in search algorithm, not able to search {val}")
            process_console_logs(self)
        else:
            if waitfor(self, 5, By.XPATH, "//span[contains(text(),'Object Type')]/ancestor::div[3]/following-sibling::div//span[contains(text(),'Select All')]/parent::div//input[@value='true']", False):
                fprint(self, "Deselecting select ALL")
                self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]/ancestor::div[3]/following-sibling::div//span[contains(text(),'Select All')]/parent::div/div").click()
            waitfor(self, 5, By.XPATH, "(//li[@name='select-option']/div/span/span[contains(text(),'Indicator')])[1]")
            fprint(self, "Clicked on indicator field")
            self.driver.find_element_by_xpath("(//li[@name='select-option']/div/span/span[contains(text(),'Indicator')])[1]").click()
            waitfor(self, 3, By.XPATH, "//tbody/tr[1]/td[1]")
            fprint(self, "Selecting the top 5 intel")
            values = []

            for i in range(1, 6):
                waitfor(self, 2, By.XPATH, f"(//span[@data-testid='name'])[{i}]")
                ele = self.driver.find_element_by_xpath(f"(//span[@data-testid='name'])[{i}]")
                text = ele.get_attribute('innerHTML').strip()
                values.append(text)
                waitfor(self, 5, By.XPATH, f"(//span[contains(text(),'{text}' )]/ancestor::tr//span/input/ancestor::span)[2]")
                fprint(self, "Selected the checkbox")
                self.driver.find_element_by_xpath(f"(//span[contains(text(),'{text}' )]/ancestor::tr//span/input/ancestor::span)[2]").click()
                sleep(2)

            fprint(self, "Clicked on Bulk Actions button")
            waitfor(self, 5, By.XPATH, "//button[normalize-space()='Bulk Actions']")
            self.driver.find_element_by_xpath("//button[normalize-space()='Bulk Actions']").click()

            fprint(self, "Clicked on Add TLP")
            waitfor(self, 5, By.XPATH, "//div[normalize-space()='Add TLP']")
            self.driver.find_element_by_xpath("//div[normalize-space()='Add TLP']").click()

            fprint(self, "Clicked on button for Green")
            waitfor(self, 5, By.XPATH, "//div[normalize-space()='Green']//div//input[contains(@type,'radio')]")
            self.driver.find_element_by_xpath("//div[normalize-space()='Green']//div//input[contains(@type,'radio')]").click()

            fprint(self, "Clicked on save")
            waitfor(self, 5, By.XPATH, "(//button[@type='button'][normalize-space()='Save'])[1]")
            self.driver.find_element_by_xpath("(//button[@type='button'][normalize-space()='Save'])[1]").click()

            verify_success(self, "TLP value is assigned to the selected objects successfully")

            fprint(self, "Printing the selected intels")
            for val in values:
                fprint(self, val)

            fprint(self, "Verified whether TLP was assigned or not")
            i = 0

            for val in values:
                # waitfor(self, 4, By.XPATH, "(//input[contains(@placeholder,'Search')])[4]")
                # self.driver.find_element_by_xpath("(//input[contains(@placeholder,'Search')])[4]").click()
                # filled_val = values[i - 1]
                # i = i + 1
                # j = 0
                # while j <= len(filled_val):
                #     self.driver.find_element_by_xpath("(//input[contains(@placeholder,'Search')])[4]").send_keys(
                #         Keys.BACK_SPACE)
                #     j = j + 1
                # sleep(3)
                # self.driver.find_element_by_xpath("(//input[contains(@placeholder,'Search')])[4]").send_keys(val)
                # sleep(3)
                # self.driver.find_element_by_xpath("(//input[contains(@placeholder,'Search')])[4]").send_keys(Keys.ENTER)
                verify_data_in_threatdata(self, val, "")
                if waitfor(self, 5, By.XPATH, "(//span[@data-testid='type'])[1]", False):
                    self.driver.find_element_by_xpath("(//span[@data-testid='type'])[1]").click()
                    if waitfor(self, 5, By.XPATH, "//button/div[contains(text(), 'GREEN')]", False):
                        fprint(self, f"[PASSED] Correct for intel {val}")
                    else:
                        fprint(self, f"[FAILED] Incorrect for intel {val}")

                    waitfor(self, 3, By.XPATH, "//span[@class='cy-page__back-button']")
                    self.driver.find_element_by_xpath("//span[@class='cy-page__back-button']").click()
                else:
                    fprint(self, f"[FAILED] There is some bug in search algorithm, not able to search {val}")
            process_console_logs(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())

