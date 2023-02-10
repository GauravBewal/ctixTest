from lib.readonly import *


class ReadOnly(unittest.TestCase):
    """
    Class representing testcases to be run for readonly sanity
    """

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

    def handle_exceptions(self, module):
        """
            Handle exceptions if any in the executions
        """
        fprint(self, f"Failure in sanity run for {module}")
        if waitfor(self, 1, By.XPATH, "//*[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//*[@data-testaction='slider-close']").click()
            sleep(1)  # required
        if waitfor(self, 1, By.XPATH, "//i[@class='cyicon-chevron-left']", False):
            self.driver.find_element_by_xpath("//i[@class='cyicon-chevron-left']").click()
            sleep(1)  # required


    def test_01_load_main_menu_pages(self):
        """
            Testcase to validate if all pages for modules are being loaded without any error
        """
        fprint(self, testplan)
        fprint(self, "Clicking on main menu")
        fprint(self, "List of all modules listed under main menu are")
        main_modules = get_main_modules(self)
        fprint(self, "\n".join(main_modules))
        fprint(self, "Loading pages for all modules listed under main menu")
        for module in main_modules:
            fprint(self, f"Module --- {module}")
            nav_menu_main(self, module)
            try:
                globals()["run_"+get_func_name(module)](self, module)
            except:
                self.handle_exceptions(module)


    def test_02_load_admin_menu_pages(self):
        """
            Testcase to validate if all admin menu pages are loading
        """
        fprint(self, "Clicking on admin menu")
        fprint(self, "List of all modules listed under admin menu are")
        admin_modules = get_admin_modules(self)
        fprint(self, "\n".join(admin_modules))
        fprint(self, "Loading pages for all modules listed under main menu")
        for module in admin_modules:
            fprint(self, f"Module --- {module}")
            nav_menu_admin(self, module)
            try:
                snap_nested_modules(self, module)
            except:
                self.handle_exceptions(module)

    def test_03_create_sanity_report(self):
        """
            Function to create report of sanity performed
        """
        document = Document()
        document.add_heading("Sanity Report", 0)
        document.add_heading("MAIN MENU", 1)
        populate_sanity_report(document, get_main_modules(self))
        document.add_heading("ADMIN MENU", 1)
        populate_sanity_report(document, get_admin_modules(self))
        document.add_heading("QUICK ADD", 1)
        populate_sanity_report(document, ["Quick Add"])
        document.save(os.path.join(os.environ["PYTHONPATH"], "reports", "sanity.docx"))

    def test_04_quick_actions_page_load(self):
        """
            Functions to validate if quick actions pages are loading as expected
        """
        quick_access_path = "//ul[contains(@class,'cy-topbar__menu')]//button[normalize-space(text())='New']"
        quick_access_dropdown = "//ul[contains(@class,'cy-topbar__quick-menu__container')]//li"
        modules = self.driver.find_elements_by_xpath(quick_access_dropdown)
        for i in range(len(modules)):
            try:
                self.driver.find_element_by_xpath(quick_access_path).click()
                sleep(1)    # required
                _module_name = modules[i].text
                self.driver.find_elements_by_xpath(quick_access_dropdown)[i].click()
                if waitfor(self, 4, By.XPATH, "//button[normalize-space(text())='Skip']", False):
                    self.driver.find_element_by_xpath("//button[normalize-space(text())='Skip']").click()
                sleep(1)    # required
                save_screenshots(self, module="Quick Add", sname=_module_name)
                self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
                sleep(1)    # required
            except:
                self.handle_exceptions("Quick Add")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
