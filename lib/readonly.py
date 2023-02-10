from lib.ui.notes import *
from lib.ui.attackNavigator import *
from lib.ui.cyware_products import click_on_product, go_back_to_product_page
from lib.ui.nav_tableview import click_on_actions_item


def snap_nested_modules(self, module):
    """
        Function to dive into modules with Multiple sections
    """
    _section_path = "//main[@id='main-layout']//li[@aria-label]"
    _sub_module_path = "//main[@id='main-layout']//a[@aria-label]"
    if waitfor(self, 2, By.XPATH, _section_path, False):
        sections = self.driver.find_elements_by_xpath(_section_path)
        for i in range(len(sections)):
            _section = self.driver.find_elements_by_xpath(_section_path)[i]
            _section_name = _section.get_attribute('aria-label')
            if "/" in _section_name:
                _section_name = _section_name.replace('/', '|')
            _section.click()
            sleep(2)  # required
            globals()["run_" + get_func_name(module)](self, module, _section_name)
    elif waitfor(self, 2, By.XPATH, _sub_module_path, False):
        sections = self.driver.find_elements_by_xpath(_sub_module_path)
        for i in range(len(sections)):
            _submodule = self.driver.find_elements_by_xpath(_sub_module_path)[i]
            _submodule_name = _submodule.get_attribute('aria-label')
            if "/" in _submodule_name:
                _submodule_name = _submodule_name.replace('/', '|')
            _submodule.click()
            sleep(2)  # required
            globals()["run_" + get_func_name(module)](self, module, _submodule_name)
    else:
        globals()["run_" + get_func_name(module)](self, module)


def run_dashboards(self, module):
    """Function for readonly on Dashboard"""
    save_screenshots(self, module=module, sname="Landing page")
    dashboard_names = [dashboard.text for dashboard in
                       self.driver.find_elements_by_xpath('//div[@role="tablist"]//span[@data-testid]')]
    for dashboard_name in dashboard_names:
        self.driver.find_element_by_xpath(f"//span[@data-testid='{dashboard_name}']").click()
        save_screenshots(self, module=module, sname=dashboard_name, slp_time=3)
        fprint(self, dashboard_name + " Page Load")
    self.driver.find_element_by_xpath("//span[@class = 'cyicon-more-vertical']").click()
    sleep(2)  # required
    self.driver.find_element_by_xpath("//li[@data-testaction = 'export-dashboard']").click()
    waitfor(self, 2, By.XPATH, "//input[@aria-label = 'PDF']")
    self.driver.find_element_by_xpath("//input[@aria-label = 'PDF']").click()
    self.driver.find_element_by_xpath("//button[@data-cy-event = 'Export']").click()
    verify_success(self, "Your dashboard will be available")
    save_screenshots(self, module=module, sname="export dashboard", slp_time=1)
    fprint(self, "Export Dashboard")
    self.driver.find_element_by_xpath("(//div//button[@aria-label = 'View All'])[1]").click()
    waitfor(self, 2, By.XPATH, "//button[contains(text(),' Data Values ')]")
    save_screenshots(self, module=module, sname="Widget View All page load", slp_time=1)
    self.driver.find_element_by_xpath("//i[@class='cyicon-chevron-left']").click()
    waitfor(self, 2, By.XPATH, "//h1[contains(text(),'Dashboard')]")
    self.driver.find_element_by_xpath("//span[contains(text(),'Add Dashboard')]").click()
    waitfor(self, 2, By.XPATH, "//div[contains(text(),' Create New Dashboard ')]")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys("Add dashboard")
    self.driver.find_element_by_xpath("//img[@alt='Basic']").click()
    self.driver.find_element_by_xpath("//input[@name='stationary']").click()
    self.driver.find_element_by_xpath("//button[@data-cy-id = 'create-dashboard']").click()
    waitfor(self, 5, By.XPATH, "//div[contains(text(),'Information Widget Section')]")
    self.driver.find_element_by_xpath(
        "//span[@class='cyicon-add']//ancestor::div[@data-test-id='layout-col-0-0']").click()
    waitfor(self, 2, By.XPATH, "//div[contains(text(),' Add Information Widget ')]")
    save_screenshots(self, module=module, sname="widget slider load", slp_time=1)
    close_slider(self)
    sleep(2)    # required
    self.driver.find_element_by_xpath("//i[contains(@class,'cyicon-chevron-left')]").click()
    sleep(2)    # required


def run_reports(self, module):
    """Function for readonly on Reports"""
    save_screenshots(self, module=module, sname="Landing page")


def run_threatdata(self, module):
    """Function for readonly on Threat Data"""
    _tab_xpath = "//div[normalize-space(text())='{}']"
    save_screenshots(self, module=module, sname="Landing page")
    self.driver.find_element_by_xpath('//tr[td//span[@data-testid="name"]]').click()
    waitfor(self, 2, By.XPATH, "//div[normalize-space(text())='Basic Details']")
    tab_names = [tab.text for tab in self.driver.find_elements_by_xpath('//ul[@role="tablist"]/li[@data-cy-event]')]
    for tab_name in tab_names:
        self.driver.find_element_by_xpath(_tab_xpath.format(tab_name)).click()
        save_screenshots(self, module=module, sname=tab_name, slp_time=1)
    if waitfor(self, 2, By.XPATH, "//button[@data-cy-event='Timeline']", False):
        self.driver.find_element_by_xpath("//button[@data-cy-event='Timeline']").click()
        save_screenshots(self, module=module, sname="Timeline", slp_time=1)
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()


def run_threatmailbox(self, module):
    """
        Function for readonly on Threat mailbox
    """
    email_card = "//div[contains(@class, 'cy-email-card')]"
    save_screenshots(self, module=module, sname="Landing page")
    if waitfor(self, 2, By.XPATH, email_card, False):
        self.driver.find_element_by_xpath(email_card).click()
        self.driver.find_element_by_xpath("//button[contains(text(), 'Create Intel')]").click()
        waitfor(self, 2, By.XPATH, "//div[normalize-space(text())='Create Intel']")
        slider_tabs = "//li[@role='tab']/span"
        tabs = [tab.text for tab in self.driver.find_elements_by_xpath(slider_tabs)]
        nav_tabs_readonly(self, module, tabs)


def run_threatbulletin(self, module):
    """Function for capturing the screenshot of the first enteries of the received and created bulletin"""
    save_screenshots(self, module=module, sname="Landing Page")
    if waitfor(self, 10, By.XPATH, "(//tr[contains(@class, 'el-table__row cy-table-row')])[1]", False):
        save_screenshots(self, module=module, sname="Created Page")
    else:
        self.driver.find_element_by_xpath("(//tr[contains(@class, 'el-table__row cy-table-row')])[1]").click()
        waitfor(self, 10, By.XPATH, "//span[@role='button']/span[contains(text(),'Tags')]")
        sleep(5)  # required for the loading of the content of the bulletin
        save_screenshots(self, module=module, sname="Created Detail Page")
    self.driver.find_element_by_xpath("//div[contains(text(),' Received ')]").click()
    if waitfor(self, 10, By.XPATH, "(//tr[contains(@class, 'el-table__row cy-table-row')])[1]", False):
        save_screenshots(self, module=module, sname="Received Page")
    else:
        self.driver.find_element_by_xpath("(//tr[contains(@class, 'el-table__row cy-table-row')])[1]").click()
        waitfor(self, 10, By.XPATH, "//span[@role='button']/span[contains(text(),'Tags')]")
        sleep(5)  # required for the loading of the content of the bulletin
        save_screenshots(self, module=module, sname="Received Detail Page")
    sleep(2)  # required


def run_rssfeeds(self, module):
    """Function for readonly on RSS Feeds"""
    _rss_card = "//div[@class='cy-card__body']"
    save_screenshots(self, module=module, sname="Landing page")
    if waitfor(self, 2, By.XPATH, "//*[normalize-space(text())='RSS Feeds not configured']", False):
        fprint(self, "No Account configured under RSS")
    else:
        self.driver.find_elements_by_xpath("//li[@class='cy-page-menu__item']")[0].click()
        sleep(1)
        self.driver.find_element_by_xpath("//button[normalize-space(text())= 'Create Intel']").click()
        waitfor(self, 2, By.XPATH, "//div[normalize-space(text())='Create Intel']")
        slider_tabs = "//li[@role='tab']/span"
        tabs = [tab.text for tab in self.driver.find_elements_by_xpath(slider_tabs)]
        nav_tabs_readonly(self, module, tabs)
        sleep(.5)  # required
        self.driver.find_element_by_xpath("//span[normalize-space(text())='Bookmarked']").click()
        save_screenshots(self, module=module, sname="Bookmarked")


def run_twitterfeeds(self, module):
    """Function for readonly on Twitter"""
    slider_tabs = "//li[@role='tab']/span"
    save_screenshots(self, module=module, sname="Landing page")
    if waitfor(self, 10, By.XPATH, "//button[contains(text(),'Add Account')]", False):
        pass
    else:
        waitfor(self, 10, By.XPATH, "(//div[contains(@class, 'tweet-deck__body')])[1]")
        self.driver.find_element_by_xpath("(//div[contains(@class, 'tweet-deck__body')])[1]").click()
        waitfor(self, 10, By.XPATH, "//button[contains(text(),'Parse')]")
        save_screenshots(self, module=module, sname="Slider")
        tabs = [tab.text for tab in self.driver.find_elements_by_xpath(slider_tabs)]
        nav_tabs_readonly(self, module, tabs[1:])
    sleep(2)  # required


def run_globalnotes(self, module):
    """Function for readonly on Global notes"""
    save_screenshots(self, module=module, sname="Landing page")
    add_note(self, readOnly=True, sname="Add Note")
    if waitfor(self, 4, By.XPATH, "(//pre[contains(@class, 'cy-notes-card__text')])[1]", False):
        text = self.driver.find_element_by_xpath("(//pre[contains(@class, 'cy-notes-card__text')])[1]").text
        click_on_note(self, text, readOnly=True)
        save_screenshots(self, module=module, sname="Note Details Slider")

    waitfor(self, 4, By.XPATH, "//div[contains(text(), 'My Notes')]")
    self.driver.find_element_by_xpath("//div[contains(text(), 'My Notes')]").click()
    save_screenshots(self, module=module, sname="My Notes")
    add_note(self, readOnly=True, sname="My Notes Add button")
    if waitfor(self, 4, By.XPATH, "(//pre[contains(@class, 'cy-notes-card__text')])[1]", False):
        text = self.driver.find_element_by_xpath("(//pre[contains(@class, 'cy-notes-card__text')])[1]").text
        click_on_note(self, text)
        save_screenshots(self, module=module, sname="My Note Details Slider")
        edit_note(self, text, readOnly=True, module=module)
    sleep(0.5)


def run_threatinvestigations(self, module):
    """Function for readonly on investigations"""
    save_screenshots(self, module=module, sname="Landing page")
    waitfor(self, 3, By.XPATH, "//*[contains(text(),'Intel History')]")
    fprint(self, "Clicked on intel history")
    self.driver.find_element_by_xpath("//*[contains(text(),'Intel History')]").click()
    sleep(3)
    save_screenshots(self, module=module, sname="Intel History")
    waitfor(self, 3, By.XPATH, "//span[@data-testaction='slider-close']")
    self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
    if waitfor(self, 3, By.XPATH, "(//tr[contains(@class, 'el-table__row')])[1]", False):
        self.driver.find_element_by_xpath("(//tr[contains(@class, 'el-table__row')])[1]").click()
        sleep(3)
        if waitfor(self, 3, By.XPATH, "//button[contains(text(),'SKIP')]", False):
            fprint(self, "Skipping the walkthrough")
            self.driver.find_element_by_xpath("//button[contains(text(),'SKIP')]").click()
            waitfor(self, 2, By.XPATH, "//button[contains(text(),'OK, GOT IT')]")
            fprint(self, "Clicked on Ok got it")
            self.driver.find_element_by_xpath("//button[contains(text(),'OK, GOT IT')]").click()
        sleep(2)
        save_screenshots(self, module=module, sname="Single Canvas")
        waitfor(self, 3, By.XPATH, "//i[contains(@class, 'cyicon-chevron-left')]")
        self.driver.find_element_by_xpath("//i[contains(@class, 'cyicon-chevron-left')]").click()
    sleep(2)


def run_sandbox(self, module):
    """Function for readonly on Sandbox"""
    save_screenshots(self, module=module, sname="Landing page")
    if waitfor(self, 10, By.XPATH, "(//tr[contains(@class, 'cy-table-row')])[1]", False):
        self.driver.find_element_by_xpath("(//tr[contains(@class, 'cy-table-row')])[1]").click()
        waitfor(self, 10, By.XPATH, "//button[contains(text(),'Create')]")
        save_screenshots(self, module=module, sname="Details Page")
        self.driver.find_element_by_xpath("//span/i[@class='cyicon-chevron-left']").click()
        waitfor(self, 10, By.XPATH, "//button[contains(text(), 'Analyze')]")
        self.driver.find_element_by_xpath("//button[contains(text(), 'Analyze')]").click()
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Analyze Sources')]")
        save_screenshots(self, module=module, sname="Analyze Page")
    else:
        self.driver.find_element_by_xpath("//a[contains(text(),'Get Help')]").click()
        sleep(5)  # Waiting for the 5 seconds to page get load properly
        win_handles = len(self.driver.window_handles)
        var = self.driver.window_handles[0]
        win_instance = self.driver.window_handles[win_handles - 1]
        self.driver.switch_to.window(win_instance)
        if waitfor(self, 1, By.XPATH, "//h1[contains(text(),'How can we help you today?')]"):
            save_screenshots(self, module=module, sname="Help Doc Page")
        self.driver.switch_to.window(var)
        save_screenshots(self, module=module, sname="CTIX_screen")
    sleep(2)  # required


def run_threatdefenderlibrary(self, module):
    """Function for readonly on Defender"""
    save_screenshots(self, module=module, sname="Landing page")
    waitfor(self, 4, By.XPATH, "//div[contains(text(), 'Checked Files')]")
    self.driver.find_element_by_xpath("//div[contains(text(), 'Checked Files')]").click()
    sleep(2)
    save_screenshots(self, module=module, sname="Checked Files")
    sleep(2)


def run_attcknavigator(self, module):
    """Function for readonly on ATT&CK Navigator"""
    save_screenshots(self, module=module, sname="Landing page")
    click_on_technique(self)
    save_screenshots(self, module=module, sname="Technique's slider")
    close_slider(self)
    fprint(self, "Checked Enterprise --> MITRE, now checking Enterprise --> Custom Base Layer")
    click_on_customBase_layer(self)
    sleep(1)  # Waiting for the Techniques to load
    save_screenshots(self, module=module, sname="Enterprise Custom Base Layer")
    click_on_technique(self)
    save_screenshots(self, module=module, sname="Technique's slider")
    close_slider(self)
    self.driver.find_element_by_xpath("//button[@data-testaction='dropdown-button']").click()
    waitfor(self, 5, By.XPATH, "//span[contains(text(),' Mobile ')]/parent::li")
    self.driver.find_element_by_xpath("//span[contains(text(),' Mobile ')]/parent::li").click()
    sleep(1)  # Waiting for the Techniques to load
    save_screenshots(self, module=module, sname="Mobile Landing page")
    click_on_technique(self)
    save_screenshots(self, module=module, sname="Technique's slider")
    close_slider(self)
    fprint(self, "Checked Mobile --> MITRE, now checking Mobile --> Custom Base Layer")
    click_on_customBase_layer(self)
    sleep(1)  # Waiting for the Techniques to load
    save_screenshots(self, module=module, sname="Mobile Custom Base Layer")
    click_on_technique(self)
    save_screenshots(self, module=module, sname="Technique's slider")
    close_slider(self)


def run_encodedecodebase(self, module):
    """Function for readonly on Encode and Decode"""
    save_screenshots(self, module=module, sname="Landing page")


def run_cvsscalculator(self, module):
    """Function for readonly on CVSS"""
    save_screenshots(self, module=module, sname="Landing page")


def run_fangdefang(self, module):
    """Function for readonly on Fang Defang"""
    save_screenshots(self, module=module, sname="Landing page")


def run_stixconversion(self, module):
    """Function for readonly on STIX Conversion"""
    save_screenshots(self, module=module, sname="Landing page")


def run_networkutilities(self, module):
    """Function for readonly on Network"""
    save_screenshots(self, module=module, sname="Landing page")


def run_rules(self, module):
    """Function for readonly on Rules"""
    save_screenshots(self, module=module, sname="Landing page")
    sleep(1)
    if waitfor(self, 3, By.XPATH, "(//tr[contains(@class, 'el-table__row')])[1]", False):
        self.driver.find_element_by_xpath("(//tr[contains(@class, 'el-table__row')])[1]").click()
        sleep(2)
        save_screenshots(self, module=module, sname="Details")
        waitfor(self, 3, By.XPATH, "//i[contains(@class, 'cyicon-chevron-left')]")
        self.driver.find_element_by_xpath("//i[contains(@class, 'cyicon-chevron-left')]").click()
        sleep(2)
        fprint(self, [i.text for i in self.driver.find_elements_by_xpath("//span[@data-testid='name']")])
        text = ""
        for i in self.driver.find_elements_by_xpath("//span[@data-testid='name']"):
            if i.text != "":
                text = i.text
                break

        print(text + " " + "adfsasdaf")
        waitfor(self, 2, By.XPATH, "//input[@id='main-input']")
        self.driver.find_element_by_xpath("//input[@id='main-input']").click()
        sleep(2)
        self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys(text)
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        sleep(2)
        a = ActionChains(self.driver)
        m = self.driver.find_element_by_xpath("(//tr[contains(@class, 'el-table__row')])[1]")
        a.move_to_element(m).perform()
        waitfor(self, 2, By.XPATH, "//button[@data-testid='action']")
        self.driver.find_element_by_xpath("//button[@data-testid='action']").click()
        save_screenshots(self, module=module, sname="Quick Actions")

        m = self.driver.find_element_by_xpath("(//li[contains(text(), 'View Threat Data')])[2]")
        self.driver.execute_script("arguments[0].click();", m)
        sleep(5)
        p = self.driver.window_handles[0]
        c = self.driver.window_handles[1]
        self.driver.switch_to.window(c)
        save_screenshots(self, module=module, sname="View Threat Data")
        self.driver.close()
        self.driver.switch_to.window(p)
        sleep(2)


def run_globaltasks(self, module):
    """Function for readonly on Global Tasks"""
    save_screenshots(self, module=module, sname="Landing page")


def run_detailedsubmission(self, module):
    """Function for readonly on Detailed Submission"""

    def select_status(state):
        self.driver.find_element_by_xpath("//div[@data-testid='filters']").click()
        sleep(2)
        self.driver.find_element_by_xpath(status_path).click()
        self.driver.find_element_by_xpath(
            f"//li[contains(@id, 'cy-filters')]//span[normalize-space(text())= '{state}']").click()
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()

    status_path = "//span[@class='icon']/following-sibling::span[normalize-space(text())='Status']"
    save_screenshots(self, module=module, sname="Landing page")
    if waitfor(self, 2, By.XPATH, "//span[normalize-space(text())= 'Add Detailed Submission']", False):
        pass
    else:
        for status in ["Processing", "Draft", "Published"]:
            select_status(status)
            sleep(2)
            if status == "Processing" and waitfor(self, 5, By.XPATH, "//tr"):
                save_screenshots(self, module=module, sname="Processing state")
            elif status == "Draft" and waitfor(self, 5, By.XPATH, "//tr"):
                self.driver.find_elements_by_xpath("//tr[contains(@class,'el-table__row')]")[-1].click()
                waitfor(self, 2, By.XPATH, "//div[normalize-space(text())='STIX Components']/following-sibling", False)
                save_screenshots(self, module=module, sname="Draft")
                self.driver.find_element_by_xpath("//div[i[contains(@class, 'cyicon-chevron-left')]]").click()
                sleep(1)  # required
            else:
                self.driver.find_elements_by_xpath("//tr[contains(@class,'el-table__row')]")[-1].click()
                sleep(3)
                p = self.driver.window_handles[0]
                c = self.driver.window_handles[1]
                self.driver.switch_to.window(c)
                if waitfor(self, 10, By.XPATH, "//h1/span/span[normalize-space(text())= 'Threat Data']", False):
                    sleep(2)  # required
                save_screenshots(self, module=module, sname="Published")
                self.driver.close()
                self.driver.switch_to.window(p)
            self.driver.find_element_by_xpath("//div[i[contains(@class, 'cyicon-cross-o-active')]]").click()


def run_indicatorsallowed(self, module):
    """Function for readonly on Allowed Indicators"""
    save_screenshots(self, module=module, sname="Landing page")


def run_watchlist(self, module):
    """Function for readonly on Watchlist"""
    save_screenshots(self, module=module, sname="Landing page")
    fprint(self, "Clicking on the Refresh Button...")
    waitfor(self, 2, By.XPATH, "//button[@aria-label='Refresh']")
    self.driver.find_element_by_xpath("//button[@aria-label='Refresh']").click()
    save_screenshots(self, module=module, sname="After Refresh")
    if waitfor(self, 10, By.XPATH, "//table//tr", False):
        self.driver.find_element_by_xpath("(//table//tr[1])[2]").click()
        sleep(2)  # Need to wait to the list properly
        save_screenshots(self, module=module, sname="Under a particular watchlist")


def run_tags(self, module):
    """Function for readonly on Tags"""
    save_screenshots(self, module=module, sname="Landing page")
    self.driver.find_element_by_xpath("//button[contains(text(),'Add Tag')]").click()
    save_screenshots(self, module=module, sname="Add Tag")
    sleep(2)  # required


def run_usermanagement(self, module, smodule):
    """Function for readonly on User Management"""
    if smodule == 'User Listing':
        save_screenshots(self, module=module, sname=f"{smodule} Landing page")
        self.driver.find_element_by_xpath("(//span[contains(text(),'User Listing')])[1]").click()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'/ User Listing')]")
        waitfor(self, 10, By.XPATH, "(//button[contains(text(),'Add User')])[1]")
        self.driver.find_element_by_xpath("(//button[contains(text(),'Add User')])[1]").click()
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'New User')]")
        save_screenshots(self, module=module, sname="Add User Page")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
    elif smodule == 'User Groups':
        sleep(.5)  # required
        self.driver.find_element_by_xpath("//span[contains(text(),'User Groups')]").click()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),' / User Groups ')]")
        save_screenshots(self, module=module, sname="User Group Page")
        self.driver.find_element_by_xpath("(//button[contains(text(),'Add User Group')])[1]").click()
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Add User Group')]")
        save_screenshots(self, module=module, sname="Add User group")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        self.driver.find_element_by_xpath("(//div[contains(@class,'cy-card cy-p-3')])[1]").click()
        waitfor(self, 10, By.XPATH, "(//div[contains(text(),'View User Group')])[1]")
        save_screenshots(self, module=module, sname="View User group")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()


def run_customentitiesmanagement(self, module, smodule):
    """Function for readonly on Custom Entities Management"""
    save_screenshots(self, module=module, sname=f"{smodule} Landing page")


def run_integrationmanagement(self, module, smodule):
    """Function for readonly on Integration Management"""
    save_screenshots(self, module=module, sname=f"{smodule} Landing page")

    if smodule == "STIX":
        integration_stix(self, module, smodule)
    if smodule == "RSS":
        integration_rss(self, module, smodule)
    if smodule == "Email":
        integration_email(self, module, smodule)
    if smodule == "Subscribers":
        integration_subscribers(self, module, smodule)
    if smodule == "Internal Applications":
        integration_internalapplications(self, module, smodule)
    if smodule == "Cyware Products":
        integration_cywareproducts(self, module, smodule)
    if smodule == "CTIX Integrators":
        run_ctixintegrator(self, module, smodule)
    if smodule == "Browser Extension":
        run_browserextension(self, module, smodule)


def run_browserextension(self, module, smodule):
    save_screenshots(self, module=module, sname=f"{smodule} Landing page")
    browser_list = [i.text for i in self.driver.find_elements_by_xpath("//div[contains(@class, 'cy-card')]")]
    for browser in browser_list:
        self.driver.find_element_by_xpath(f"//div[contains(text(),'{browser}')]").click()
        save_screenshots(self, module=module, sname=smodule + f" {browser} Landing Page")
        fprint(self, browser + " Page load")


def run_ctixintegrator(self, module, smodule):
    save_screenshots(self, module=module, sname=f"{smodule} Landing page")
    if waitfor(self, 3, By.XPATH, "(//tr[contains(@class, 'el-table__row')])[1]", False):
        text = ""
        for i in self.driver.find_elements_by_xpath("//span[@data-testid='name']"):
            if i.text != "":
                text = i.text
                break

        waitfor(self, 2, By.XPATH, "//input[@id='main-input']")
        self.driver.find_element_by_xpath("//input[@id='main-input']").click()
        sleep(2)
        self.driver.find_element_by_xpath("//input[@id='main-input']").send_keys(text)
        self.driver.find_element_by_xpath("//div[i[@data-testid='filter-search-icon']]").click()
        sleep(2)

        a = ActionChains(self.driver)
        m = self.driver.find_element_by_xpath("(//tr[contains(@class, 'el-table__row')])[1]")
        a.move_to_element(m).perform()
        waitfor(self, 2, By.XPATH, "//button[@data-testid='action']")
        self.driver.find_element_by_xpath("//button[@data-testid='action']").click()
        save_screenshots(self, module=module, sname=f"{smodule} Quick Actions")

        waitfor(self, 3, By.XPATH, "(//li[contains(text(), 'Edit')])[2]")
        self.driver.find_element_by_xpath("(//li[contains(text(), 'Edit')])[2]").click()
        sleep(1)
        save_screenshots(self, module=module, sname=f"{smodule} Edit Slider")
        waitfor(self, 10, By.XPATH, "//span[@data-testaction='slider-close']", False)
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        fprint(self, "Closing the slider")
        sleep(1)

        m = self.driver.find_element_by_xpath("(//tr[contains(@class, 'el-table__row')])[1]")
        a.move_to_element(m).perform()
        waitfor(self, 2, By.XPATH, "//button[@data-testid='action']")
        self.driver.find_element_by_xpath("//button[@data-testid='action']").click()
        waitfor(self, 3, By.XPATH, "(//li[contains(text(), 'Edit')])[2]")
        self.driver.find_element_by_xpath("(//li[contains(text(), 'Logs')])[2]").click()
        sleep(1)
        save_screenshots(self, module=module, sname=f"{smodule} Logs")
        waitfor(self, 10, By.XPATH, "//span[@data-testaction='slider-close']", False)
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        sleep(2)


def run_enrichmentmanagement(self, module, smodule):
    """Function for readonly on Enrichment management"""
    save_screenshots(self, module=module, sname=f"{smodule} Landing page")
    if smodule == "Enrichment Tools":
        waitfor(self, 2, By.XPATH, "//div[@data-testaction='dropdown-link']//"
                                   "span[contains(text(),'Status - All')]/parent::button")
        self.driver.find_element_by_xpath("//div[@data-testaction='dropdown-link']//"
                                          "span[contains(text(),'Status - All')]/parent::button").click()
        waitfor(self, 2, By.XPATH, "//li[contains(text(),'Active')]")
        self.driver.find_element_by_xpath("//li[contains(text(),'Active')]").click()
        if waitfor(self, 5, By.XPATH, "//input[@value='true']//"
                                      "ancestor::div[contains(@class,'cy-integrations__card')]", False):
            self.driver.find_element_by_xpath("//input[@value='true']//"
                                              "ancestor::div[contains(@class,'cy-integrations__card')]").click()
            save_screenshots(self, module=module, sname=smodule + " Inside Tool")
            self.driver.find_element_by_xpath("//div[contains(@class,'cy-page__back-button')]").click()

    if smodule == "Enrichment Policy":
        self.driver.find_element_by_xpath("//a[@aria-label='Enrichment Policy']").click()
        if waitfor(self, 5, By.XPATH, "(//table//tr)[2]", False):
            self.driver.find_element_by_xpath("(//table//tr)[2]").click()
            sleep(1)  # Opening of popup is slower
            save_screenshots(self, module=module, sname=smodule + " Inside Policy")
            self.driver.find_element_by_xpath("//i[contains(@class,'cyicon-cross')]/parent::span").click()
            sleep(1)  # Waiting to close the popup
        else:
            save_screenshots(self, module=module, sname=smodule + " Inside Enrichment Policy")


def helper_audit_log_management(self, module, smodule, default=""):
    waitfor(self, 3, By.XPATH, "(//tr[contains(@class, 'el-table__row')])[1]")
    self.driver.find_element_by_xpath("(//tr[contains(@class, 'el-table__row')])[1]").click()
    sleep(1)
    save_screenshots(self, module=module, sname=f"{smodule} Landing page {default}")
    waitfor(self, 3, By.XPATH, "//i[contains(@class, 'cyicon-chevron-left')]")
    self.driver.find_element_by_xpath("//i[contains(@class, 'cyicon-chevron-left')]").click()
    sleep(2)


def run_auditlogmanagement(self, module, smodule):
    """Function for readonly on Audit logs"""
    save_screenshots(self, module=module, sname=f"{smodule} Landing page")
    if smodule == "User (API) Activity Logs":
        helper_audit_log_management(self, module, smodule, default="one row details")

    if smodule == "Subscriber Logs":
        helper_audit_log_management(self, module, smodule, default="one row details")

    if smodule == "Configuration Change Logs":
        sleep(1)
        save_screenshots(self, module=module, sname=f"{smodule} Landing page")


def run_organizationtype(self, module):
    """Function for readonly on Organisation Type"""
    save_screenshots(self, module=module, sname="Landing page")


def run_licensemanagement(self, module):
    """Function for readonly on License"""
    save_screenshots(self, module=module, sname="Landing page")


def run_certificates(self, module):
    """Function for readonly on Certificates"""
    save_screenshots(self, module=module, sname="Landing page")


def run_configuration(self, module, smodule):
    """Function for readonly on Configuration"""
    save_screenshots(self, module=module, sname=f"{smodule} Landing page")


def run_stixcollections(self, module):
    """Function for readonly on STIX Collections"""
    save_screenshots(self, module=module, sname="Landing page")
    waitfor(self, 2, By.XPATH, "//h1[contains(text(),' STIX Collections ')]")
    self.driver.find_element_by_xpath("//button[contains(text(),'Add STIX Collection')]").click()
    waitfor(self, 2, By.XPATH, "//div[contains(text(),'New STIX Collection')]")
    save_screenshots(self, module=module, sname="Add STIX collection", slp_time=1)
    close_slider(self)
    search(self, "default")
    waitfor(self, 2, By.XPATH, "(//span[contains(text(), 'default')])[1]")
    actions = ActionChains(self.driver)
    actions.move_to_element(self.driver.find_element_by_xpath("(//span[@data-testid = 'polling'])[1]")).perform()
    sleep(2)
    waitfor(self, 2, By.XPATH, "//button[@data-testid = 'action']")
    self.driver.find_element_by_xpath("//button[@data-testid = 'action']").click()
    waitfor(self, 2, By.XPATH, ("(//li[contains(text(),'View Subscribers')])[2]"))
    self.driver.find_element_by_xpath("(//li[contains(text(),'View Subscribers')])[2]").click()
    waitfor(self, 2, By.XPATH, "//h1[contains(text(),' Subscribers ')]")
    save_screenshots(self, module=module, sname="subsriber logs", slp_time=1)


def run_confidencescore(self, module):
    """Function for readonly on Confidence Score"""
    save_screenshots(self, module=module, sname="Landing page")
    self.driver.find_element_by_xpath("//button[contains(text(),'Configure Source Scoring')]").click()
    waitfor(self, 10, By.XPATH, "//div[contains(text(),'Configure Source Scoring')]")
    save_screenshots(self, module=module, sname="Configure Source Scoring Page")
    self.driver.find_element_by_xpath("//button/span[contains(text(),'Category')]").click()
    save_screenshots(self, module=module, sname="Category Listing")
    self.driver.find_element_by_xpath("//span/span[@class='cyicon-cross']").click()
    waitfor(self, 10, By.XPATH, "//button[@id='enrichment-policy']")
    self.driver.find_element_by_xpath("//button[@id='enrichment-policy']").click()
    sleep(5)  # Waiting for the 5 seconds to page get load properly
    win_handles = len(self.driver.window_handles)
    win_instance = self.driver.window_handles[win_handles - 1]
    self.driver.switch_to.window(win_instance)
    if waitfor(self, 10, By.XPATH, "(//span[contains(text(),'Enrichment Policy')])[1]"):
        save_screenshots(self, module=module, sname="Enrichment Page")


def run_quickaddintel(self, module):
    """Function for readonly on Quick Add Intel"""
    save_screenshots(self, module=module, sname="Landing page")


def run_quickrule(self, module):
    """Function for readonly on Quick add Rule"""
    save_screenshots(self, module=module, sname="Landing page")


def run_quickstix(self, module):
    """Function for readonly on Quick add STIX source"""
    save_screenshots(self, module=module, sname="Landing page")


def run_quickuser(self, module):
    """Function for readonly on Quiok add User"""
    save_screenshots(self, module=module, sname="Landing page")


def run_importintel(self, module):
    """Function for readonly on Import Intel"""
    save_screenshots(self, module=module, sname="Landing page")


def integration_stix(self, module, smodule):
    """Function for readonly on Integration STIX """
    if waitfor(self, 2, By.XPATH, "//span[contains(text(),'STIX')]/"
                                  "ancestor::div[contains(@class,'cy-source-item__footer')]", False):
        self.driver.find_element_by_xpath("//span[contains(text(),'STIX')]/"
                                          "ancestor::div[contains(@class,'cy-source-item__footer')]").click()
        sleep(1)  # Waiting for the Collections to load
        save_screenshots(self, module=module, sname=smodule + " Inside Source")
        self.driver.find_element_by_xpath("//div[contains(@class,'cy-page__back-button')]").click()
        sleep(1)  # Required to reach to the Integration page
    else:
        self.driver.find_element_by_xpath("//button[contains(text(),'Add STIX Source')]").click()
        save_screenshots(self, module=module, sname=smodule + " Add Stix Source Slider")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        sleep(1)  # Required to close the slider properly


def integration_rss(self, module, smodule):
    """
        Function for readonly on integration RSS
    """
    if not waitfor(self, 2, By.XPATH, "//span[@class='cyicon-more-vertical']", False):
        pass
    else:
        self.driver.find_element_by_xpath("//span[@class='cyicon-more-vertical']").click()
        sleep(2)  # required
        self.driver.find_elements_by_xpath("//li[contains(text(), 'Edit')]")[-1].click()
        sleep(2)  # required
        save_screenshots(self, module=module, sname=f"{smodule} Edit page")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        sleep(2)  # required
        self.driver.find_elements_by_xpath("//div/div/p")[0].click()
        if waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'Collections of')]", False):
            save_screenshots(self, module=module, sname=f"{smodule} Collections Page")
            self.driver.find_element_by_xpath("//div[i[contains(@class,'cyicon-chevron-left')]]").click()
        sleep(2)


def integration_email(self, module, sname):
    """
        Function to readonly on Integration Email
    """
    if not waitfor(self, 2, By.XPATH, "//span[@class='cyicon-more-vertical']", False):
        pass
    else:
        self.driver.find_element_by_xpath("//span[@class='cyicon-more-vertical']").click()
        sleep(2)  # required
        self.driver.find_elements_by_xpath("//li[contains(text(), 'Edit')]")[-1].click()
        sleep(2)  # required
        save_screenshots(self, module=module, sname=f"{sname} Edit page")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        sleep(2)  # required
        self.driver.find_elements_by_xpath("//div[contains(@class, 'card__body')]/div/p")[0].click()
        if waitfor(self, 5, By.XPATH, "//h1[contains(text(), 'Collections of')]", False):
            save_screenshots(self, module=module, sname=f"{sname} Collections Page")
            self.driver.find_element_by_xpath("//div[i[contains(@class,'cyicon-chevron-left')]]").click()
        sleep(2)


def integration_internalapplications(self, module, smodule):
    """
        Function to run readonly on Internal Applications
    """
    section_path = "//div/div[contains(@class, 'cy-card__body')]/p"
    _section_names = [i.text for i in self.driver.find_elements_by_xpath(section_path)]
    fprint(self, ' '.join(_section_names))
    for section in _section_names:
        self.driver.find_element_by_xpath(f"//div[p[text()='{section}']]").click()
        sleep(2)  # required
        save_screenshots(self, module=module, sname=smodule + f" {section} Landing Page")
        self.driver.find_elements_by_xpath("//div[img]")[0].click()
        if waitfor(self, 10, By.XPATH,
                   "//img/following-sibling::span[normalize-space(text())='Internal Application']", False):
            sleep(2)  # required
            save_screenshots(self, module=module, sname=smodule + f" {section} Details Page")
        if waitfor(self, 1, By.XPATH, "//span[@data-testaction='slider-close']", False):
            self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
            sleep(2)
        if waitfor(self, 1, By.XPATH, "//div[i[contains(@class,'cyicon-chevron-left')]]", False):
            self.driver.find_element_by_xpath("//div[i[contains(@class,'cyicon-chevron-left')]]").click()
            sleep(1)


def integration_cywareproducts(self, module, smodule):
    """Function for readonly on Cyware Products"""
    click_on_product(self, "CFTR")
    save_screenshots(self, module=module, sname=smodule + " CFTR page")
    if not go_back_to_product_page(self):
        self.driver.find_element_by_xpath("//div[contains(@class,'cy-page__back-button')]").click()
        waitfor(self, 5, By.XPATH, "//span[contains(text(),' / Cyware Products ')]")
    click_on_product(self, "CSAP")
    save_screenshots(self, module=module, sname=smodule + " CSAP page")
    if not go_back_to_product_page(self):
        self.driver.find_element_by_xpath("//div[contains(@class,'cy-page__back-button')]").click()
        waitfor(self, 5, By.XPATH, "//span[contains(text(),' / Cyware Products ')]")
    click_on_product(self, "CO")
    save_screenshots(self, module=module, sname=smodule + " CO page")
    if not go_back_to_product_page(self):
        self.driver.find_element_by_xpath("//div[contains(@class,'cy-page__back-button')]").click()
        waitfor(self, 5, By.XPATH, "//span[contains(text(),' / Cyware Products ')]")
    click_on_product(self, "CTIX")
    save_screenshots(self, module=module, sname=smodule + " CTIX page")
    if not go_back_to_product_page(self):
        self.driver.find_element_by_xpath("//div[contains(@class,'cy-page__back-button')]").click()
        waitfor(self, 5, By.XPATH, "//span[contains(text(),' / Cyware Products ')]")


def integration_subscribers(self, module, smodule):
    """
        Function for readonly cases of subscribers
    """
    save_screenshots(self, module, smodule + "Landing Page")
    if waitfor(self, 5, By.XPATH, "//tr[contains(@class, 'el-table__row')]", False):
        _ele = self.driver.find_elements_by_xpath("//tr[contains(@class, 'el-table__row')]")[-1]
        click_on_actions_item(self, _ele.text, "Edit")
        save_screenshots(self, module=module, sname=smodule + " Edit Details")
        if waitfor(self, 2, By.XPATH, "//div[span[@data-testaction='slider-close']]", False):
            hover = ActionChains(self.driver).move_to_element(_ele)
            hover.perform()
            self.driver.find_element_by_xpath("//div[span[@data-testaction='slider-close']]").click()
        sleep(1)  # required
        hover = ActionChains(self.driver).move_to_element(_ele)
        hover.perform()
        click_on_actions_item(self, _ele.text, "View Logs")
        save_screenshots(self, module=module, sname=smodule + " Logs")
        if waitfor(self, 2, By.XPATH, "//i[contains(@class,'cyicon-chevron-left')]", False):
            self.driver.find_element_by_xpath("//i[contains(@class,'cyicon-chevron-left')]").click()
        sleep(2)  # required
        self.driver.find_elements_by_xpath("//tr[contains(@class, 'el-table__row')]")[-1].click()
        if waitfor(self, 2, By.XPATH, "//h1[contains(text(), 'Collection')]", False):
            save_screenshots(self, module=module, sname=smodule + " Collections")
            self.driver.find_element_by_xpath("//i[contains(@class,'cyicon-chevron-left')]").click()
        sleep(2)  # required
