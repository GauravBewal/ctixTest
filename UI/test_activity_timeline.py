import unittest
from lib.ui.quick_add import quick_create_ip
from lib.ui.nav_threat_data import *
from lib.ui.rules import *

timeline_indicator = "111.111.11.19"


class Timeline(unittest.TestCase):
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

    def moveto_indicator_overview(self, indicator):
        """
        Search and click on indicator which will navigate to indicator's overview page.
        """
        nav_menu_main(self, "Threat Data")
        verify_data_in_threatdata(self, indicator, "Import")
        fprint(self, "clicking on the timeline_indicator ioc.")
        waitfor(self, 20, By.XPATH, "(//span[contains(text(),'" + indicator + "')])[1]")
        _ele = self.driver.find_elements_by_xpath("//span[contains(text(),'" + indicator + "')][1]")[0]
        ActionChains(self.driver).click(_ele).perform()

    def open_timeline(self):
        """
        Function to click on timeline button and landing to timeline window, provided overview page of the indicator is open.
        """
        waitfor(self, 20, By.XPATH, "//button[@datatest-id = 'life-cycle']")
        fprint(self, "clicking on Timeline button.")
        self.driver.find_element_by_xpath("//button[@datatest-id = 'life-cycle']").click()
        fprint(self, "checking if Timeline side panel has opened.")
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Timeline')]")

    def test_01_timeline_loading(self):
        """
        Whether timeline is loading or not for intel added.
        """
        fprint(self, "TC_ID: 45001 - Timeline loading.")
        fprint(self, "Adding intel via quick add.")
        quick_create_ip(self, timeline_indicator, "timeline_indicator")
        fprint(self, "checking for timeline_indicator in threat data.")
        self.moveto_indicator_overview(timeline_indicator)
        self.open_timeline()
        fprint(self, "[PASSED] Timeline Loading successful!")

    def test_02_verify_TLP_from_source_event_in_timeline(self):
        """
        Testcase to validate tlp from source
        """
        fprint(self, "TC_ID: 45002 - Verify event type - 'TLP from source'")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "checking in timeline for event - TLP from source")
        self.open_timeline()
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'TLP From Source')]/span[contains(text(),'RED')]")))
            fprint(self, "[Passed] event type - 'TLP from Source' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'TLP From Source' is not reflected in timeline.")
            self.fail()

    def test_03_verify_received_from_source_event_in_timeline(self):
        """
        Testcase to validate event type : received from source in timeline, here feed is received from import so in time it will be reflected as
        'Feed received from import'
        """
        fprint(self, "TC_ID: 45003 - Verify event type - 'Received from source' in timeline.")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "checking in timeline for event - Received from source")
        self.open_timeline()
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(),'Feed received from')]/span[contains(text(),'Import')]")))
            fprint(self, "[Passed] event type - 'Received from Source' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Received From Source' is not reflected in timeline.")
            self.fail()

    def test_04_verify_manual_mark_false_positive_event_in_timeline(self):
        """
        Mark indicator as false positive from quick actions in threat data and
        check whether 'Marked false positive' event got reflected in timeline.
        """
        fprint(self, "TC_ID: 45004 - Verify event type - 'Marked fp' by adding flag manually via quick actions.")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "Marking indicator as false positive from quick actions.")
        waitfor(self, 20, By.XPATH, "//div[@role = 'button']//span[contains(text(),'False Positive')]")
        self.driver.find_element_by_xpath("//div[@role = 'button']//span[contains(text(),'False Positive')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(), 'Mark False Positive')]")
        self.driver.find_element_by_xpath("//span[contains(text(), 'Mark False Positive')]").click()
        fprint(self, "Verify if able to see 'Marked False Positive' flag.")
        waitfor(self, 20, By.XPATH, "//span[contains(text(), 'Marked False Positive')]")
        self.open_timeline()
        fprint(self, "Checking event - 'Marked as False Positive' in timeline.")
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(), 'Marked as False Positive')])[1]")))
            fprint(self, "[Passed] event type - 'Marked fp' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Marked fp' is not reflected in timeline.")
            self.fail()

    def test_05_verify_confidence_score_0_false_positive_event_in_timeline(self):
        """
        Confidence score should get 0 after marking object as false positive and confidence score should get updated in timeline.
        """
        fprint(self, "TC_ID: 45005 - Verify event type - 'confidence score' by marking indicator as false positive.")
        self.moveto_indicator_overview(timeline_indicator)
        self.open_timeline()
        fprint(self, "Checking event - 'Confidence score' in timeline.")
        waitfor(self, 20, By.XPATH, "(//p[contains(text(), 'Marked as False Positive')])[1]")
        waitfor(self, 20, By.XPATH, "(//p[contains(text(),'Confidence Score Calculated')])[1]")
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='el-progress__text'][contains(text(),'0')])[1]")))
            fprint(self, "[Passed] event type - 'confidence score' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'confidence score' is not reflected in timeline.")
            self.fail()

    def test_06_verify_quick_add_unmark_false_positive_event_in_timeline(self):
        """
        Testcase : Indicator is already marked as false positive from the above case, ingest the same indicator via
        quick add and check if it's Unmarked false positive and 'unmark false positive' event should reflect
        in timeline.
        """
        fprint(self, "TC_ID: 45006 - Verify event type - 'Unmark fp' by adding indicator again via quick add.")
        fprint(self, "Adding existing timeline_indicator again via quick add.")
        quick_create_ip(self, timeline_indicator, "timeline_indicator")
        fprint(self, "checking for timeline_indicator in threat data.")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "Checking if indicator is unmarked as false positive.")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'False Positive')]")
        fprint(self, "Checking event - 'Unmarked as False Positive' in timeline.")
        self.open_timeline()
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(), 'Unmarked as False Positive')])[1]")))
            fprint(self, "[Passed] event type - 'Unmarked fp' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Unmarked fp' is not reflected in timeline.")
            self.fail()

    def test_07_verify_manual_unmark_false_positive_event_in_timeline(self):
        """
        Testcase : indicator is marked as false positive and then umarked as false positive via
        quick acions, unmark fp should reflect in timeline.
        """
        fprint(self, "TC_ID: 45007 - Verify event type - 'Unmark fp' by manually unmarking it false positive.")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "Marking indicator as false positive from quick actions.")
        waitfor(self, 20, By.XPATH, "//div[@role = 'button']//span[contains(text(),'False Positive')]")
        self.driver.find_element_by_xpath("//div[@role = 'button']//span[contains(text(),'False Positive')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(), 'Mark False Positive')]")
        self.driver.find_element_by_xpath("//span[contains(text(), 'Mark False Positive')]").click()
        fprint(self, "Verify if able to see 'Marked False Positive' flag.")
        waitfor(self, 20, By.XPATH, "//span[contains(text(), 'Marked False Positive')]")
        fprint(self, "Unmarking False Positive manually.")
        self.driver.find_element_by_xpath("//span[contains(text(), 'Marked False Positive')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(), 'Unmark False Positive')]")
        self.driver.find_element_by_xpath("//span[contains(text(), 'Unmark False Positive')]").click()
        waitfor(self, 20, By.XPATH, "//div[@role = 'button']//span[contains(text(),'False Positive')]")
        self.open_timeline()
        fprint(self, "Checking event - 'Unmark as False Positive' in timeline.")
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(), 'Unmarked as False Positive')])[1]")))
            fprint(self, "[Passed] event type - 'Unmarked fp' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Unmarked fp' is not reflected in timeline.")
            self.fail()

    def test_08_verify_manual_add_to_watchlist_event_in_timeline(self):
        """
        Testcase : indicator is added to watchlist via quick actions and this event should be reflected in timeline.
        """
        fprint(self, "TC_ID: 45008 - Verify event type - 'Add to Watchlist' by manually marking it watchlisted.")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "Marking indicator as watchlisted from quick actions.")
        waitfor(self, 20, By.XPATH, "(//span[contains(text(),'Add to Watchlist')])[1]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'Add to Watchlist')])[1]").click()
        verify_success(self, "Indicators added to watchlist successfully", 20)
        self.open_timeline()
        fprint(self, "Checking event - 'Added to Watchlist' in timeline.")
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(), 'Added to Watchlist')])[1]")))
            fprint(self, "[Passed] event type - 'Added to Watchlist' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Added to Watchlist' is not reflected in timeline.")
            self.fail()

    def test_09_verify_manual_remove_from_watchlist_event_in_timeline(self):
        """
        Testcase: indicator is removed from watchlist via quick actions and this event should bee reflected in timeline.
        """
        fprint(self, "TC_ID: 45009 - Verify event type - 'Removed from Watchlist' by manually removing watchlist.")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "Removing from watchlist from quick actions.")
        waitfor(self, 20, By.XPATH, "(//span[contains(text(), 'Added to Watchlist')])[1]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'Added to Watchlist')])[1]").click()
        waitfor(self, 20, By.XPATH, "(//span[contains(text(), 'Remove from Watchlist')])[1]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'Remove from Watchlist')])[1]").click()
        verify_success(self, "Selected indicators are removed from watchlist successfully", 20)
        fprint(self, "Checking event - 'Removed from Watchlist' in timeline.")
        self.open_timeline()
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(), 'Removed from Watchlist')])[1]")))
            fprint(self, "[Passed] event type - 'Removed from Watchlist' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Removed from Watchlist' is not reflected in timeline.")
            self.fail()

    def test_10_verify_mark_manual_review_event_in_timeline(self):
        """
        Testcase: indicator is marked under manual review from quick actions.
        """
        fprint(self, "TC_ID: 45010 - Verify event type - 'Mark manual review' via quick actions")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "Marking manual review from quick actions.")
        waitfor(self, 20, By.XPATH, "(//span[contains(text(),'Manual Review')])[1]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'Manual Review')])[1]").click()
        verify_success(self, "Selected objects are added for manual review successfully", 20)
        fprint(self, "Checking event - 'Mark manual review' in timeline.")
        self.open_timeline()
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(), 'Manual Review')])[1]")))
            fprint(self, "[Passed] event type - 'Manual Review' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Manual Review' is not reflected in timeline.")
            self.fail()

    def test_11_verify_manually_mark_reviewed_event_in_timeline(self):
        """
        Testcase: indicator is marked as reviewed from quick actions.
        """
        fprint(self, "TC_ID: 45011 - Verify event type - 'Mark manual review' via quick actions")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "Mark as manual reviewed from quick actions.")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Under Manual Review')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Under Manual Review')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Mark as Reviewed')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Mark as Reviewed')]").click()
        verify_success(self, "Selected objects are marked as reviewed successfully")
        fprint(self, "Checking event - 'Mark Reviewed' in timeline.")
        self.open_timeline()
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(), 'Marked as Manually Reviewed')])[1]")))
            fprint(self, "[Passed] event type - 'Marked as Manual Reviewed' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Marked as Manual Reviewed' is not reflected in timeline.")
            self.fail()

    def test_12_verify_manually_deprecate_event_in_timeline(self):
        """
        Testcase: indicator is deprecated manually from quick actions.
        """
        fprint(self, "TC_ID: 45012 - Verify event type - 'Deprecated' via quick actions")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "Mark as deprecated from quick actions.")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Deprecate')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Deprecate')]").click()
        waitfor(self, 20, By.XPATH, "(//span[contains(text(),'Deprecate')])[2]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'Deprecate')])[2]").click()
        fprint(self, "Checking event - 'Deprecate' in timeline.")
        self.open_timeline()
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(), 'Deprecated')])[1]")))
            fprint(self, "[Passed] event type - 'Deprecate' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Deprecate' is not reflected in timeline.")
            self.fail()

    def test_13_verify_confidence_score_0_deprecate_event_in_timeline(self):
        """
        Confidence score should get 0 after marking object as deprecate and confidence score should get updated in timeline.
        """
        fprint(self, "TC_ID: 45013 - Verify event type - 'confidence score' by marking indicator as deprecate.")
        self.moveto_indicator_overview(timeline_indicator)
        self.open_timeline()
        fprint(self, "Checking event - 'Confidence score' in timeline.")
        waitfor(self, 20, By.XPATH, "(//span[contains(text(),'Deprecate')])[2]")
        waitfor(self, 20, By.XPATH, "(//p[contains(text(),'Confidence Score Calculated')])[1]")
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//div[@class='el-progress__text'][contains(text(),'0')])[1]")))
            fprint(self, "[Passed] event type - 'confidence score' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'confidence score' is not reflected in timeline.")
            self.fail()

    def test_14_verify_manually_undeprecate_event_in_timeline(self):
        """
        Testcase: indicator is undeprecated manually from quick actions.
        """
        fprint(self, "TC_ID: 45014 - Verify event type - 'Deprecated' via quick actions")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "Mark as undeprecated from quick actions.")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Deprecated')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Deprecated')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Undeprecate')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Undeprecate')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Save')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Save')]").click()
        verify_success(self, "Selected indicators are undeprecated successfully", 20)
        fprint(self, "Checking event - 'Undeprecate' in timeline.")
        self.open_timeline()
        try:
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(), 'Deprecated')])[1]")))
            fprint(self, "[PASSED] event type - 'Deprecate' is reflected in timeline successfully.")
        except:
            fprint(self, "[Failed] event type - 'Deprecate'")
            self.fail()

    def test_15_verify_quick_add_undeprecate_event_in_timeline(self):
        """
        Testcase: indicator is undeprecated by ingesting it again via quick add.
        """
        fprint(self, "TC_ID: 45015 - Verify event type - 'Undeprecated' via quick actions")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "Mark as deprecated from quick actions.")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Deprecate')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Deprecate')]").click()
        waitfor(self, 20, By.XPATH, "(//span[contains(text(),'Deprecate')])[2]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'Deprecate')])[2]").click()
        verify_success(self, "Selected indicators are deprecated successfully", 20)
        fprint(self, "Undeprecating indicator from quick actions.")
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Deprecated')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Deprecated')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Undeprecate')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Undeprecate')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Save')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Save')]").click()
        verify_success(self, "Selected indicators are undeprecated successfully", 20)
        fprint(self, "Checking event - 'Undeprecate' in timeline.")
        self.open_timeline()
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(), 'Deprecated')])[1]")))
            fprint(self, "[Passed] event type - 'Deprecate' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Deprecate' is not reflected in timeline.")
            self.fail()

    def test_16_verify_indicator_allowed_event_in_timeline(self):
        """
        Testcase: indicator is marked as indicator allowed manually via quick actions.
        """
        fprint(self, "TC_ID: 45016 - Verify event type - 'Indicator Allowed' via quick actions")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "Marking object as indicator allowed from quick actions.")
        waitfor(self, 20, By.XPATH, "(//span[contains(text(),'Indicator Allowed')])[1]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'Indicator Allowed')])[1]").click()
        waitfor(self, 20, By.XPATH, "(//span[contains(text(),'Add to Indicator Allowed')])[1]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'Add to Indicator Allowed')])[1]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Save')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Save')]").click()
        verify_success(self, "Objects added to Indicators Allowed successfully.", 20)
        fprint(self, "Checking event - 'Added to Allowed Indicators' in timeline.")
        self.open_timeline()
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(), 'Added to Allowed Indicators')])[1]")))
            fprint(self, "[Passed] event type - 'Added to Allowed Indicators' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Added to Allowed Indicators' is not reflected in timeline.")
            self.fail()

    def test_17_verify_remove_indicator_allowed_event_in_timeline(self):
        """
        Testcase: indicator is removed from indicator allowed manually via quick actions.
        """
        fprint(self, "TC_ID: 45017 - Verify event type - 'Removed from Allowed Indicator' via quick actions")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "Removing object from indicator allowed from quick actions.")
        waitfor(self, 20, By.XPATH, "(//span[contains(text(),'Indicator Allowed')])[1]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'Indicator Allowed')])[1]").click()
        waitfor(self, 20, By.XPATH,
                "(//span[contains(text(),'Remove from Indicator Allowed')])[1]")
        self.driver.find_element_by_xpath("(//span[contains(text(),'Remove from Indicator Allowed')])[1]").click()
        verify_success(self, "Selected indicators are removed from indicators allowed successfully", 20)
        fprint(self, "Checking event - 'Removed from Allowed Indicators' in timeline.")
        self.open_timeline()
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(), 'Removed From Allowed Indicators')])[1]")))
            fprint(self, "[Passed] event type - 'Removed From Allowed Indicators' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Removed From Allowed Indicators' is not reflected in timeline.")
            self.fail()

    def test_18_verify_updated_TLP_event_in_timeline(self):
        """
        Testcase: udpdate TLP of indicator from overview page and this event should be reflected in timeline.
        """
        fprint(self, "TC_ID: 45018 - Verify event type - 'Updated TLP' via overview page.")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "Updating TLP to Amber")
        waitfor(self, 20, By.XPATH, "//div[@data-testaction='dropdown-link']//button/div[contains(text(),'RED')]")
        self.driver.find_element_by_xpath("//div[@data-testaction='dropdown-link']//button/div[contains(text(),'RED')]").click()
        waitfor(self, 20, By.XPATH, "//li//div[contains(text(),'Amber')]")
        self.driver.find_element_by_xpath("//li//div[contains(text(),'Amber')]").click()
        fprint(self, "Checking event - 'Updated TLP' in timeline.")
        self.open_timeline()
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(), 'TLP Updated ')]//span[contains(text(),'AMBER')])[1]")))
            fprint(self, "[Passed] event type - 'Updated TLP' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Updated TLP' is not reflected in timeline.")
            self.fail()

    def test_19_verify_updated_description_event_in_timeline(self):
        """
        Testcase: udpdate description of indicator from overview page and this event should be reflected in timeline
        """
        fprint(self, "TC_ID: 45019 - Verify event type - 'Updated description' via overview page.")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "Updating description")
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Basic Details')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Basic Details')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Edit')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Edit')]").click()
        waitfor(self, 20, By.XPATH, "//span[contains(text(),'Save')]")
        self.driver.find_element_by_xpath("//span[contains(text(),'Save')]").click()
        fprint(self, "Checking event - 'Updated description' in timeline.")
        self.open_timeline()
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(), 'Indicator Description Updated')])[1]")))
            fprint(self, "[Passed] event type - 'Updated Description' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Updated Description' is not reflected in timeline.")
            self.fail()

    def test_20_verify_updated_analyst_score_event_in_timeline(self):
        """
        Testcase: update analyst score of indicator from overview page and this event should be reflected in timeline
        """
        fprint(self, "TC_ID: 45020 - Verify event type - 'Updated description' via overview page.")
        self.moveto_indicator_overview(timeline_indicator)
        fprint(self, "Updating analyst score")
        waitfor(self, 20, By.XPATH, "//form")
        self.driver.find_element_by_xpath("//form//input[@type='text']").click()
        self.driver.find_element_by_xpath("//form//input[@type='text']").send_keys("40")
        fprint(self, "Checking event - 'Updated analyst score' in timeline.")
        waitfor(self, 20, By.XPATH, "//div[contains(text(),'Overview')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'Overview')]").click()
        self.open_timeline()
        try:
            wait = WebDriverWait(self.driver, 20)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(), 'Analyst Score Updated to')])[1]")))
            fprint(self, "[Passed] event type - 'Analyst score updated' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Analyst score updated' is not reflected in timeline.")
            self.fail()

    def test_21_verify_passed_by_rule_event_in_timeline(self):
        fprint(self, "TC_ID: 45021 - Verify event type - 'Passed by rule'")
        self.moveto_indicator_overview(update_fp_new_ip)
        self.open_timeline()
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, "(//p[contains(text(),'Passed By Rule')])[1]")))
            fprint(self, "[Passed] event type - 'Passed by rule' is reflected in timeline successfully. ")
        except:
            fprint(self, "[Failed] - event type 'Passed by rule' is not reflected in timeline.")
            self.fail()

    def test_22_verify_maximize_minimize_button_functionality(self):
        fprint(self, "TC_ID: 45022 - Verify maximize/minimize button functionality.")
        self.moveto_indicator_overview(timeline_indicator)
        self.open_timeline()
        fprint(self, "click on maximize button")
        waitfor(self, 10, By.XPATH, "//span[@data-testaction='slider-expand']")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-expand']").click()
        waitfor(self, 10, By.XPATH, "//span[@data-testaction='slider-collapse']")
        fprint(self, "[Passed] - Maximize/Minimize button functionality working properly.")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())