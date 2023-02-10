import unittest
from lib.ui.nav_app import *
from lib.ui.nav_tableview import click_on_actions_item,visible_column
from lib.ui.quick_add import quick_create_ip
from lib.ui.subscribers import create_subs
from lib.ui.sources import create_creds,create_source
class ThreatBulletin(unittest.TestCase):

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

    Bulletin = "First"
    Tag = "Bulletin_tag"
    val = "7.5.6.7"
    new_name = "NewName"
    col ='Sau_inb_col'
    sourcename = "source_bull_inb"
    desc = "TEST"

    def parse_froala_actions(self):
        nav_menu_main(self, "Threat Bulletin")
        self.driver.find_element_by_xpath("//div[normalize-space()='Created']").click()
        fprint(self, "[Passed]-clicked on the created button")
        search(self, self.Bulletin)
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'First')]")
        self.driver.find_element_by_xpath(
            "(//span[contains(@data-testid,'title')][normalize-space()='First'])[2]").click()
        fprint(self, "[Passed]-clicked on the Bulletin")
        waitfor(self, 10, By.XPATH, "//button[span[contains(text(),'Bold')]]")
        self.driver.find_element_by_xpath("//button[span[contains(text(),'Select All')]]").click()
        fprint(self, "[Passed]-clicked on select all text")

    def click_bulletin(self):
        nav_menu_main(self, "Threat Bulletin")
        self.driver.find_element_by_xpath("//div[normalize-space()='Created']").click()
        fprint(self, "[Passed]-clicked on the created button")
        waitfor(self, 10, By.XPATH, "//td/div//span[@data-testid='title']")
        search(self, self.Bulletin)
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'First')]")
        self.driver.find_element_by_xpath(
            "(//span[contains(@data-testid,'title')][normalize-space()='First'])[2]").click()
        fprint(self, "[Passed]-clicked on the Bulletin")


    def test_01_verify_threat_bulletin_page_load(self):
        fprint(self, "TC_ID: 7861 - To verify that threat bulletin page load successfully.")
        nav_menu_main(self, "Threat Bulletin")
        fprint(self, "[Passed]-Clicked on the threat Bulletin")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Threat Bulletin')]")
        fprint(self, "[Passed]-Page loaded successfully")

    def test_02_verify_add_threat_bulletin(self):
        fprint(self, "TC_ID: 7862 - to verify that threat Bulletin can be added successfully")
        nav_menu_main(self, "Threat Bulletin")
        fprint(self, "[Passed]-Clicked on the threat Bulletin")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Threat Bulletin')]")
        fprint(self, "[Passed]-Page loaded successfully")
        self.driver.find_element_by_xpath("//div[normalize-space()='Created']").click()
        fprint(self, "[Passed]-clicked on the created button")
        if waitfor(self, 5, By.XPATH, "//button[contains(text(),'Threat Bulletin')]", False):
            self.driver.find_element_by_xpath("//button[contains(text(),'Threat Bulletin')]").click()
            fprint(self, "[Passed]- Clicked on the add threat bulletin button")
        waitfor(self, 10, By.XPATH, "//input[@name='title']")
        self.driver.find_element_by_xpath("//input[@name='title']").send_keys(self.Bulletin)
        fprint(self, "[Passed]-entered the title of bulletin")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        fprint(self, "[Passed]-clicked on the add button")
        waitfor(self, 10, By.XPATH, "//span[normalize-space()='Type something']")
        self.driver.find_element_by_xpath("//div[@contenteditable='true']").send_keys("Testing")
        sleep(5) # the sleep here is mandatory
        self.driver.find_element_by_xpath("//button[normalize-space()='Save as Draft']").click()
        fprint(self, "[Passed]-clicked on save as draft")
        verify_success(self, "Threat Bulletin created successfully")
        if waitfor(self, 5, By.XPATH, "//i[@class='cyicon-chevron-left cy-text-f10 cy-color-gray-110']", False):
            self.driver.find_element_by_xpath("//i[@class='cyicon-chevron-left cy-text-f10 cy-color-gray-110']").click()
        fprint(self, "[Passed]-Back on the created page")
        fprint(self, "[Passed]-Threat Bulletin created successfully")

    def test_03_verify_search_threat_bulletin(self):
        fprint(self, "TC_ID: 7863 - To verify that created bulletin is present in the Module")
        nav_menu_main(self, "Threat Bulletin")
        fprint(self, "[Passed]-Clicked on the threat Bulletin")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'Threat Bulletin')]")
        fprint(self, "[Passed]-Page loaded successfully")
        self.driver.find_element_by_xpath("//div[normalize-space()='Created']").click()
        fprint(self, "[Passed]-clicked on the created button")
        search(self, self.Bulletin)
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+self.Bulletin+"')]")
        fprint(self, "[Passed]-Bulletin present in the created tab")

    def test_04_verify_clone_threat_bulletin(self):
        fprint(self, "TC_ID: 7864 - To verify that we are able to clone the threat bulletin")
        nav_menu_main(self, "Threat Bulletin")
        self.driver.find_element_by_xpath("//div[normalize-space()='Created']").click()
        fprint(self, "[Passed]-clicked on the created button")
        search(self, self.Bulletin)
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+self.Bulletin+"')]")
        click_on_actions_item(self, 'First', 'Clone', 'threatbulletin')
        waitfor(self, 10, By.XPATH, "//button[normalize-space()='Save as Draft']")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save as Draft']").click()
        fprint(self, "[Passed]-clicked on save as draft")
        verify_success(self, "Threat Bulletin created successfully")
        if waitfor(self, 5, By.XPATH, "//i[@class='cyicon-chevron-left cy-text-f10 cy-color-gray-110']", False):
            self.driver.find_element_by_xpath("//i[@class='cyicon-chevron-left cy-text-f10 cy-color-gray-110']").click()
        fprint(self, "[Passed]-Back on the created page")
        search(self, "First (cloned)")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+self.Bulletin+" (cloned)')]")
        fprint(self, "[Passed]-element cloned successfully!!")

    def test_05_verify_bold_is_working(self):
        fprint(self, "TC_ID: 7865 - To verify that the bold functionality of threat bulletin is working")
        self.parse_froala_actions()
        self.driver.find_element_by_xpath("//button[span[contains(text(),'Bold')]]").click()
        fprint(self, "[Passed]-Clicked on the bold text")
        waitfor(self, 10, By.XPATH, "//strong[normalize-space()='Testing']")
        fprint(self, "[Passed]- The text is converted into bold")

    def test_06_verify_italic_is_working(self):
        fprint(self, "TC_ID: 7866- To verify that the italic functionality of threat bulletin is working")
        self.parse_froala_actions()
        self.driver.find_element_by_xpath("//button[span[contains(text(),'Italic')]]").click()
        waitfor(self, 10, By.XPATH, "//em[normalize-space()='Testing']")
        fprint(self, "[Passed]- The text is converted into italic")

    def test_07_verify_underline_is_working(self):
        fprint(self, "TC_ID: 7867- To verify that the italic functionality of threat bulletin is working")
        self.parse_froala_actions()
        self.driver.find_element_by_xpath("//button[span[contains(text(),'Underline')]]").click()
        waitfor(self, 10, By.XPATH, "//u[normalize-space()='Testing']")
        fprint(self, "[Passed]- The text is converted into italic")

    def test_08_verify_align_center(self):
        fprint(self, "TC_ID:7868- to verify that text aling center is working fine")
        self.parse_froala_actions()
        self.driver.find_element_by_xpath("//button[span[contains(text(),'Align Center')]]").click()
        waitfor(self, 10, By.XPATH, "//p[@style='text-align: center;' and contains(text(),'Testing')]")
        fprint(self, "[Passed]-Text align centre functionality is working fine")

    def test_09_verify_align_left(self):
        fprint(self, "TC_ID: 7869- to verify that text aling left is working fine")
        self.parse_froala_actions()
        self.driver.find_element_by_xpath("//button[span[contains(text(),'Align Left')]]").click()
        waitfor(self, 10, By.XPATH, "//p[@style='text-align: left;' and contains(text(),'Testing')]")
        fprint(self, "[Passed]-Text align left functionality is working fine")

    def test_10_verify_ordered_list(self):
        fprint(self, "TC_ID: 78610- to verify that the ordered list functionality is working fine")
        self.parse_froala_actions()
        self.driver.find_element_by_xpath("(//button[span[contains(text(),'Ordered List')]])[1]").click()
        waitfor(self, 10, By.XPATH, " //li[normalize-space()='Testing']/ancestor::ol")
        fprint(self, "[Passed]-the ordered list functionality is working fine")

    def test_11_verify_add_tag(self):
        fprint(self, "TC_ID: 78611- to verify that add tag functionality is working fine")
        self.click_bulletin()
        waitfor(self, 10, By.XPATH, "//span[normalize-space()='Add Tag']")
        self.driver.find_element_by_xpath("//span[normalize-space()='Add Tag']").click()
        fprint(self, "[Passed]-Clicked on the add tag")
        self.driver.find_element_by_xpath("//input[@placeholder='Search Tags']").send_keys(self.Tag)
        fprint(self, "[Passed]-Entered the value for the tag")
        waitfor(self, 10, By.XPATH, "//button[normalize-space()='+ Add Tag']")
        self.driver.find_element_by_xpath("//button[normalize-space()='+ Add Tag']").click()
        fprint(self, "[Passed]-clicked on add tag functionality")
        sleep(5)# mandatory
        self.driver.find_element_by_xpath("//button[normalize-space()='Save as Draft']").click()
        fprint(self, "[Passed]-clicked on save as draft")
        verify_success(self, "Threat Bulletin updated successfully")
        self.driver.refresh()
        sleep(5)# mandatory
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+self.Tag+"')]")
        fprint(self, "[Passed]-Tag is visible")

    def test_12_verify_update_tlp(self):
        fprint(self, "TC_ID: 78612- to verify that the tlp can be updated successfully")
        self.click_bulletin()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Add TLP')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Red')]").click()
        fprint(self, "[Passed]-clicked on TLP red")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save as Draft']").click()
        fprint(self, "[Passed]-clicked on save as draft")
        verify_success(self, "Threat Bulletin updated successfully")
        self.driver.refresh()
        sleep(5)# mandatory
        if waitfor(self, 5, By.XPATH, "//i[@class='cyicon-chevron-left cy-text-f10 cy-color-gray-110']", False):
            self.driver.find_element_by_xpath("//i[@class='cyicon-chevron-left cy-text-f10 cy-color-gray-110']").click()
        fprint(self, "[Passed]-Back on the created page")
        search(self, self.Bulletin)
        waitfor(self, 10, By.XPATH, "//td[contains(@class ,'cy-tlp--red')]")
        fprint(self, "[Passed]-updated the tlp of the bulletin")

    def test_13_verify_title_as_mandatory(self):
        fprint(self, "TC_ID: 78613- to verify that the title is mandatory field to create bulletin")
        nav_menu_main(self, "Threat Bulletin")
        fprint(self, "[Passed]-clicked on the Threat Bulletin")
        self.driver.find_element_by_xpath("//div[normalize-space()='Created']").click()
        fprint(self, "[Passed]-clicked on the created button")
        self.driver.find_element_by_xpath("//button[contains(text(),'Threat Bulletin')]").click()
        fprint(self, "[Passed]- Clicked on the add threat bulletin button")
        self.driver.find_element_by_xpath("//button[normalize-space()='Add']").click()
        fprint(self, "[Passed]-clicked on the add button")
        waitfor(self, 10, By.XPATH, "//div[normalize-space()='Title is required']")
        fprint(self, "[Passed]-Verified that the Threat Bulletin cannot be created without title")

    def test_14_verify_add_investigation(self):
        fprint(self, "TC_ID: 78614- to verify that the threat Investigation can be added successfully")
        self.click_bulletin()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Add Investigation')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Add Investigation')]").click()
        fprint(self, "[Passed]-clicked on the Add Threat Investigation")
        waitfor(self, 10, By.XPATH, "//span[normalize-space()='Select Investigation']")
        self.driver.find_element_by_xpath("//div[contains(@data-testaction,'close')]//span").click()
        fprint(self, "[Passed]-Clicked on select Investigtion")
        waitfor(self, 10, By.XPATH, "//div[@id='create-bulletin']//input[@name='search-input']")
        self.driver.find_element_by_xpath("//div[@id='create-bulletin']//input[@name='search-input']").send_keys("IPv4_canvas")
        waitfor(self, 10, By.XPATH, "//div[contains(text(),'IPv4_canvas')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'IPv4_canvas')]").click()
        sleep(5)#mandatory
        self.driver.find_element_by_xpath("//button[normalize-space()='Continue']").click()
        fprint(self, "[Passed]-clicked on continue button")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save as Draft']").click()
        fprint(self, "[Passed]-clicked on save as draft")
        verify_success(self, "Threat Bulletin updated successfully")
        self.driver.refresh()
        sleep(5)  # mandatory
        if not waitfor(self, 10, By.XPATH, "//img[contains(@class,'fr-draggable')]/ancestor::p", False):
            self.click_bulletin()
            waitfor(self, 10, By.XPATH, "//img[contains(@class,'fr-draggable')]/ancestor::p")
        fprint(self, "[Passed]-Threat Investigation added successfully")

    def test_15_verify_add_object(self):
        fprint(self, "TC_ID: 78615- to verify that we can add object successfully")
        quick_create_ip(self, self.val, self.val)
        self.click_bulletin()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Add Object')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Add Object')]").click()
        fprint(self, "[Passed]-clicked on Add Objects")
        waitfor(self, 10, By.XPATH, "//textarea[@placeholder='Search Query']")
        self.driver.find_element_by_xpath("//textarea[@placeholder='Search Query']").click()
        fprint(self, "[Passed]-clicked on search query")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Object Type')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]").click()
        fprint(self, "[Passed]-Clicked on object Type")
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'=')])[1]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'=')])[1]").click()
        fprint(self, "[Passed]-clicked on =")
        waitfor(self, 10, By.XPATH, "//li[@name='select-option']//span//span[contains(text(),'Indicator')]")
        self.driver.find_element_by_xpath("//li[@name='select-option']//span//span[contains(text(),'Indicator')]").click()
        fprint(self, "[Passed]-clicked 0n indicators")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'AND')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'AND')]").click()
        fprint(self, "[Passed]-clicked on and")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'IOC Type')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'IOC Type')]").click()
        fprint(self, "[Passed]-clicked on the IOC type")
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'=')])[1]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'=')])[1]").click()
        fprint(self, "[Passed]-clicked on =")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Ipv4 addr')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Ipv4 addr')]").click()
        fprint(self, "[Passed]-clicked on IpV4")
        self.driver.find_element_by_xpath("//textarea[@placeholder='Search Query']").click()
        sleep(4)#mandatory
        self.driver.find_element_by_xpath("//button[@data-testaction='search']//span").click()
        fprint(self, "[Passed]-Clicked on the search icon")
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'"+self.val+"')]/ancestor::tr//span)[1]")
        elem = self.driver.find_element_by_xpath("(//span[contains(text(),'"+self.val+"')]/ancestor::tr//span)[1]")
        action = ActionChains(self.driver).move_to_element(elem)
        action.click()
        action.perform()
        fprint(self, "[Passed]-clicked on the checkbox")
        sleep(5)  # mandatory
        self.driver.find_element_by_xpath("//button[normalize-space()='Continue']").click()
        fprint(self, "[Passed]-clicked on continue button")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save as Draft']").click()
        fprint(self, "[Passed]-clicked on save as draft")
        verify_success(self, "Threat Bulletin updated successfully")
        self.driver.refresh()
        sleep(5)# mandatory
        if waitfor(self, 10, By.XPATH, "//td[normalize-space()='"+self.val+"']", False):
            self.click_bulletin()
            waitfor(self, 10, By.XPATH, "//td[normalize-space()='" + self.val + "']")
        fprint(self, "[Passed]-Verified that the objects are added successfully")

    def test_16_verify_attachment(self):
        fprint(self, "TC_ID: 78616- to verify that the attachments aree added")
        self.click_bulletin()
        waitfor(self, 10, By.XPATH, "//span[normalize-space()='Attachments']")
        file_name = os.path.join(os.environ["PYTHONPATH"], "testdata", "test_attachments.csv")
        self.driver.find_element_by_xpath("//input[@type='file']").send_keys(file_name)
        fprint(self, "[Passed]-Attached the file in attachment")
        sleep(5)  # mandatory
        self.driver.find_element_by_xpath("//button[normalize-space()='Save as Draft']").click()
        fprint(self, "[Passed]-clicked on save as draft")
        verify_success(self,"Threat Bulletin updated successfully")
        self.driver.refresh()
        sleep(5)  # mandatory
        if not waitfor(self, 10, By.XPATH, "//span[normalize-space()='test_attachments.csv']", False):
            self.click_bulletin()
            waitfor(self, 10, By.XPATH, "//span[normalize-space()='test_attachments.csv']")
        fprint(self, "[Passed]-the attachements are added successfully")

    def test_17_verify_name_change(self):
        fprint(self, "TC_ID: 78617- To verify that name is changed")
        self.click_bulletin()
        waitfor(self, 10, By.XPATH, "//input[@placeholder='Enter value']")
        clear_field(self.driver.find_element_by_xpath("//input[@placeholder='Enter value']"))
        fprint(self, "[Passed]-Cleared the value of the name")
        self.driver.find_element_by_xpath("//input[@placeholder='Enter value']").send_keys(self.new_name)
        fprint(self, "[Passed]-Entered the new name")
        sleep(5)
        self.driver.find_element_by_xpath("//button[normalize-space()='Save as Draft']").click()
        fprint(self, "[Passed]-clicked on save as draft")
        verify_success(self,"Threat Bulletin updated successfully")
        if waitfor(self, 5, By.XPATH, "//i[@class='cyicon-chevron-left cy-text-f10 cy-color-gray-110']", False):
            self.driver.find_element_by_xpath("//i[@class='cyicon-chevron-left cy-text-f10 cy-color-gray-110']").click()
        fprint(self, "[Passed]-Back on the created page")
        search(self, self.new_name)
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'NewName')])[1]")
        fprint(self, "[Passed]-Updated the name of the bulletin")

    def test_18_verify_add_mitre(self):
        """
        Test case to verify that the mitre can be added successfully
        """
        fprint(self, "TC_ID: 78618- Test case to verify that the mitre can be added successfully")
        nav_menu_main(self, "Threat Bulletin")
        self.driver.find_element_by_xpath("//div[normalize-space()='Created']").click()
        fprint(self, "[Passed]-clicked on the created button")
        search(self, self.new_name)
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'"+self.new_name+"')])[2]")
        fprint(self, "[Passed]-searched the new bulletin")
        self.driver.find_element_by_xpath("(//span[contains(text(),'"+self.new_name+"')])[2]").click()
        fprint(self, "[Passed]-clicked on the bulletin")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Add MITRE')]")
        fprint(self, "[Passed]-Page loaded successfully")
        self.driver.find_element_by_xpath("//span[contains(text(),'Add MITRE')]").click()
        fprint(self, "[Passed]-clicked on the Add mitre button successfully")
        waitfor(self, 10, By.XPATH, "//button[contains(text(),'Continue')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Continue')]").click()
        waitfor(self, 10, By.XPATH, "//p/img[contains(@class, 'fr-fic fr-dii fr-draggable')]")
        fprint(self, "[Passed]-Mitre Added Successfully")

    def test_19_verify_publish_flow(self):
        repeat = 1
        fprint(self, "TC_ID: 78619- To verify that the processing state is updated successfully")
        nav_menu_main(self, "Threat Bulletin")
        self.driver.find_element_by_xpath("//div[normalize-space()='Created']").click()
        fprint(self, "[Passed]-clicked on the created button")
        search(self, self.new_name)
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'" + self.new_name + "')]")
        click_on_actions_item(self, self.new_name, 'Publish', 'threatbulletin')
        fprint(self, "[Passed]-clicked on publish")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'col_2.1')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'col_2.1')]").click()
        fprint(self, "[Passed]-Clicked on the colletion")
        sleep(2)
        self.driver.find_element_by_xpath("//button[normalize-space()='Publish']").click()
        fprint(self, "[Passed]-Clicked on the publish")
        verify_success(self, "Threat Bulletin publishing is in progress")
        while repeat <= 6:
            if not waitfor(self, 10, By.XPATH, "//span[contains(text(),'" + self.new_name + "')]/ancestor::tr//span[@data-testid='status' and contains(text(),'Published')]", False):
                fprint(self, "clicking on refresh button")
                self.driver.find_element_by_xpath("//button[normalize-space()='Refresh']").click()
            else:
                break
            repeat = repeat + 1
        #self.driver.find_element_by_xpath("//button[normalize-space()='Refresh']").click()
        search(self, self.new_name)
        # waitfor(self, 20, By.XPATH, "//span[contains(text(),'" + self.new_name + "')]")
        sleep(5)
        visible_column(self, "Status")
        waitfor(self, 10, By.XPATH,
                "//span[contains(text(),'" + self.new_name + "')]/ancestor::tr//span[@data-testid='status' and contains(text(),'Published')]")
        fprint(self, "[Passed]-Processing flow is working fine")

    def test_20_verify_published_under_threat_data(self):
        fprint(self, "TC_ID: 78620- To verify that the publish cases are working fine")
        nav_menu_main(self, "Threat Data")
        waitfor(self, 60, By.XPATH, threat_data_main_search_field)
        self.driver.find_element_by_xpath(threat_data_main_search_field).click()
        fprint(self, "Clicked on the search field")
        clear_field(self.driver.find_element_by_xpath(threat_data_main_search_field))
        self.driver.find_element_by_xpath(threat_data_main_search_field).send_keys(self.new_name)
        fprint(self, "Searching - " + self.new_name)
        waitfor(self, 10, By.XPATH,
                "(//span[@data-testid='name'][normalize-space()='"+self.new_name+"'])[2]")
        fprint(self, "Feed Visible - " + self.new_name)
        self.driver.find_element_by_xpath("(//span[@data-testid='name'][normalize-space()='"+self.new_name+"'])[2]").click()
        waitfor(self, 20, By.XPATH, "//div[normalize-space()='Overview']")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'col_2.1')]")
        fprint(self, "Collection visible - col_2.1")
        fprint(self, "[Passed]-Publish flow is working fine")

    def test_21_verify_send_to_inbox(self):
        """
        Test case to verify send to inbox flow
        """
        fprint(self, "TC_ID: 78621- Test case to verify send to inbox flow")
        nav_menu_main(self, "Threat Bulletin")
        self.driver.find_element_by_xpath("//div[normalize-space()='Created']").click()
        fprint(self, "[Passed]-clicked on the created button")
        search(self, self.Bulletin)
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),' First (cloned) ')])[1]")
        self.driver.find_element_by_xpath("(//span[contains(text(),' First (cloned) ')])[2]").click()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Add Object')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Add Object')]").click()
        fprint(self, "[Passed]-clicked on Add Objects")
        waitfor(self, 10, By.XPATH, "//textarea[@placeholder='Search Query']")
        self.driver.find_element_by_xpath("//textarea[@placeholder='Search Query']").click()
        fprint(self, "[Passed]-clicked on search query")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Object Type')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Object Type')]").click()
        fprint(self, "[Passed]-Clicked on object Type")
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'=')])[1]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'=')])[1]").click()
        fprint(self, "[Passed]-clicked on =")
        waitfor(self, 10, By.XPATH, "//li[@name='select-option']//span//span[contains(text(),'Indicator')]")
        self.driver.find_element_by_xpath(
            "//li[@name='select-option']//span//span[contains(text(),'Indicator')]").click()
        fprint(self, "[Passed]-clicked 0n indicators")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'AND')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'AND')]").click()
        fprint(self, "[Passed]-clicked on and")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'IOC Type')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'IOC Type')]").click()
        fprint(self, "[Passed]-clicked on the IOC type")
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'=')])[1]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'=')])[1]").click()
        fprint(self, "[Passed]-clicked on =")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'Ipv4 addr')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Ipv4 addr')]").click()
        fprint(self, "[Passed]-clicked on IpV4")
        self.driver.find_element_by_xpath("//textarea[@placeholder='Search Query']").click()
        sleep(4)  # mandatory
        self.driver.find_element_by_xpath("//button[@data-testaction='search']//span").click()
        fprint(self, "[Passed]-Clicked on the search icon")
        waitfor(self, 10, By.XPATH, "(//span[contains(text(),'" + self.val + "')]/ancestor::tr//span)[1]")
        elem = self.driver.find_element_by_xpath("(//span[contains(text(),'" + self.val + "')]/ancestor::tr//span)[1]")
        action = ActionChains(self.driver).move_to_element(elem)
        action.click()
        action.perform()
        fprint(self, "[Passed]-clicked on the checkbox")
        sleep(5)  # mandatory
        self.driver.find_element_by_xpath("//button[normalize-space()='Continue']").click()
        fprint(self, "[Passed]-clicked on continue button")
        self.driver.find_element_by_xpath("//button[normalize-space()='Save as Draft']").click()
        fprint(self, "[Passed]-clicked on save as draft")
        verify_success(self, "Threat Bulletin updated successfully")
        create_subs(self, self.col, self.desc)
        create_source(self, self.sourcename, self.col)
        nav_menu_main(self, "Threat Bulletin")
        click_on_actions_item(self, "First (cloned)", 'Publish', 'threatbulletin')
        fprint(self, "[Passed]-clicked on publish")
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'To Inbox')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'To Inbox')]").click()
        waitfor(self, 10, By.XPATH, "//span[contains(text(),'"+self.col+"')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'"+self.col+"')]").click()
        self.driver.find_element_by_xpath("//button[contains(text(),'Publish')]").click()
        verify_success(self, "Threat Bulletin published successfully")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
