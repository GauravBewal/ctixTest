import unittest
from lib.ui.nav_app import *
from lib.api.external_apis import *
from lib.ui.nav_threat_data import *
from lib.ui.nav_tableview import *


class IntegrationWebhooks(unittest.TestCase):

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

    def addWebhook(self):
        if Build_Version.__contains__("3."):
            waitfor(self, 10, By.XPATH, "//button[contains(text(),'Webhook')]")
            fprint(self, "Clicking on the 'Add Webhook' button")
            self.driver.find_element_by_xpath("//button[contains(text(),'Webhook')]").click()
        else:
            waitfor(self, 10, By.XPATH, "//button[contains(text(),'Add Webhook')]")
            fprint(self, "Clicking on the 'Add Webhook' button")
            self.driver.find_element_by_xpath("//button[contains(text(),'Add Webhook')]").click()
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Title*']")
        fprint(self, "Adding new webhook")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys("test_automation")
        fprint(self, "Title - test_automation")
        self.driver.find_element_by_xpath("//span[contains(text(),'Select an Application*')]//ancestor::div[6]").click()
        waitfor(self, 5, By.XPATH, "//div[contains(text(),'Mattermost')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Mattermost')]").click()
        fprint(self, "Application - Mattermost")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Expires After (in days)*']").send_keys("30")
        fprint(self, "Expires After - 30 days")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Confidence*']").send_keys("70")
        self.driver.find_element_by_xpath("//*[@class='cy-modal-footer']//button[contains(text(),'Add')]").click()
        fprint(self, "Clicked on the Add button")
        verify_success(self, "Webhook created successfully")
        fprint(self, "Waiting for the Application Token input box")
        waitfor(self, 10, By.XPATH, "//input[@aria-placeholder='Application Token']")
        _mattermost_url = self.driver.find_element_by_xpath("//p[contains(text(), 'webhook')]").text
        _mat_chan = "mat_chan" + uniquestr[-4:]
        print(_mat_chan)
        set_value("mattermost_cnl", _mat_chan)
        create_public_channel(team_name='conversion', channel_name=_mat_chan)
        token, webhook_id = create_outgoing_webhook(team_name='conversion', channel_name=_mat_chan, webhook_url=_mattermost_url)
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Application Token']").send_keys(token)
        fprint(self, "Visible, value set - {token}")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        fprint(self, "Clicked on the Save button")
        verify_success(self, "updated successfully")

        # Verifying it is added or not
        fprint(self, "Searching for the newly added Webhook")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("test_automation")
        self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'test_automation')]")
        fprint(self, "Newly added Webhook is visible")
        sleep(30)   # needed
        filename = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds/webhook_data.csv")
        with open(filename, "r") as file:
            message = file.readlines()
        create_post_in_channel(team_name='conversion', channel_name=get_value("mattermost_cnl"), post_content="".join(message))
        process_console_logs(self)

    def test_01_verify_add_webhooks(self):
        fprint(self, "TC_ID: 98430 - test_01_verify_add_webhooks")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to Webhooks Feed Source")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Webhooks')]").click()
        self.addWebhook()

    # Only for CTIX Version 3.0
    def test_01_v3_verify_add_webhooks(self):
        fprint(self, "TC_ID: 98431 - test_01_v3_verify_add_webhooks")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to Webhooks Feed Source")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Webhooks')]").click()
        self.addWebhook()

    def test_02_verify_edit_webhooks(self):
        fprint(self, "TC_ID: 98432 - test_02_verify_edit_webhooks")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to Webhooks Feed Source")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Webhooks')]").click()
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        fprint(self, "Searching for the Webhook - test_automation")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("test_automation")
        self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
        waitfor(self, 6, By.XPATH, "//span[contains(text(),'test_automation')]")
        fprint(self, "Webhook is visible, clicking on the action menu")
        self.driver.find_element_by_xpath("//button[@data-testid='action']").click()
        waitfor(self, 5, By.XPATH, "//li[contains(text(),'Edit')]")
        fprint(self, "Clicking on the edit option")
        self.driver.find_element_by_xpath("//li[contains(text(),'Edit')]").click()
        waitfor(self, 5, By.XPATH, "//input[@aria-placeholder='Title*']")
        self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys("_edit")
        fprint(self, "Added '_edit' in the Title of the webhook")
        self.driver.find_element_by_xpath("//button[contains(text(),'Save')]").click()
        verify_success(self, "updated successfully")
        waitfor(self, 5, By.XPATH, "//span[contains(text(),'test_automation_edit')]")
        fprint(self, "Edited Webhook is visible")
        process_console_logs(self)

    def test_03_verify_delete_webhooks(self):
        fprint(self, "TC_ID: 98433 - test_03_verify_delete_webhooks")
        fprint(self, "\n--------- Redirecting to the Integration Management page ---------")
        nav_menu_admin(self, "Integration Management")
        fprint(self, "[PASSED] Redirected successfully, switching to Webhooks Feed Source")
        self.driver.find_element_by_xpath("//a/span[contains(text(), 'Webhooks')]").click()
        waitfor(self, 5, By.XPATH, "//input[@placeholder='Search or filter results']")
        fprint(self, "Searching for the Webhook - test_automation")
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").click()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").clear()
        self.driver.find_element_by_xpath("//input[@placeholder='Search or filter results']").send_keys("test_automation")
        self.driver.find_element_by_xpath("//span[text()='Press enter or click to search']").click()
        waitfor(self, 6, By.XPATH, "//span[contains(text(),'test_automation')]")
        fprint(self, "Webhook is visible, clicking on the action menu")
        click_on_actions_item(self, "test_automation", "Delete")
        # self.driver.find_element_by_xpath("//button[@data-testid='action']").click()
        # waitfor(self, 5, By.XPATH, "//li[contains(text(),'Delete')]")
        # fprint(self, "Clicking on the delete option")
        # self.driver.find_element_by_xpath("//li[contains(text(),'Delete')]").click()
        # waitfor(self, 5, By.XPATH, "//button[contains(text(),'Delete')]")
        fprint(self, "Clicking on the Delete option of confirmation popup")
        self.driver.find_element_by_xpath("//button[contains(text(),'Delete')]").click()
        verify_success(self, "deleted successfully")
        # waitfor(self, 5, By.XPATH, "//h1[contains(text(),'No Webhooks found!')]")
        fprint(self, "Webhook is not visible now, it is deleted successfully")

    def test_04_verify_webhook_intel(self):
        """
            Testcase to validate if intel is received from webhook
        """
        fprint(self, "TC_ID: 98434 - test_03_verify_delete_webhooks")
        try:
            nav_menu_main(self, 'Threat Data')
            filename = os.path.join(os.environ["PYTHONPATH"], "testdata/feeds/webhook_data.csv")
            with open(filename, "r") as file:
                message = file.readlines()
            for i in message:
                verify_data_in_threatdata(self, value=i.strip('\n'), source="Mattermost")
        finally:
            delete_outgoing_webhook(webhook_name="hook_" + get_value("mattermost_cnl"))
            delete_public_channel(team_name='conversion', channel_name=get_value("mattermost_cnl"))

if __name__ == '__main__':
    unittest.main(testRunner=reporting())