import unittest
from lib.ui.nav_threat_data import *

condition_cvss2 = ["Local (AV:L)", "Medium (AC:M)", "Multiple (Au:M)", "Partial (C:P)", "None (I:N)", "Partial (A:P)"]
condition_cvss3 = ["Adjacent Network (AV:A)", "High (AC:H)", "Low (PR:L)", "Required (UI:R)", "Changed (S:C)", "Low (C:L)", "Low (I:L)", "Low (A:L)"]
object_scores_cvss2 = {
    "CVSS Base Score": 2.7,
    "Impact Subscore": 4.9,
    "Exploitability Subscore": 2.2,
    "CVSS Temporal Score": 0,
    "CVSS Environmental Score": 0,
    "Modified Impact Subscore": 0,
    "Overall CVSS Score": 2.7
}
object_scores_cvss3 = {
    "Base Score": 5.1,
    "Temporal Score": 5.1,
    "Environmental Score": 5.1
}


class CVSSCalculator(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.driver = initialize_browser(self)
        login(self, Admin_Email, Admin_Password)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def select_object_in_baseScore_metrics(self, object):
        waitfor(self, 1, By.XPATH, "//div[contains(text(),'"+object+"')]")
        self.driver.find_element_by_xpath("//div[contains(text(),'"+object+"')]").click()

    def verify_score(self, object, score):
        wait = WebDriverWait(self.driver, 5)
        wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(),'"+object+"')]/following-sibling::span[contains(text(),'"+str(score)+"')]")))
        fprint(self, "object - " + object + ", score - " + str(score))

    def verify_element(self, selector):
        try:
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.visibility_of_element_located((By.XPATH, selector)))
        except:
            fprint(self, "[Failed] - Not getting expected data/element")

    def click_on_resetButton(self):
        self.driver.find_element_by_xpath("//button[contains(text(),'Reset Scores')]").click()
        fprint(self, "Clicked on the Reset Button")

    def test_01_verify_cvss2_calculator(self):
        fprint(self, "TC_ID: 4110551 - test_01_cvss2_calculator")
        nav_menu_main(self, "CVSS Calculator")
        for obj in condition_cvss2:
            self.select_object_in_baseScore_metrics(obj)

        self.driver.find_element_by_xpath("//button[contains(text(),'Show Scores')]").click()
        self.verify_element("//div[contains(text(),'OVERALL')]/following-sibling::div[contains(text(),'2.7')]")
        self.verify_element("//div[contains(text(),'SCORE')]/following-sibling::div[contains(text(),'2.7')]")
        self.verify_element("//div[@id='scoresGraph']/p[contains(text(),'AV:L/AC:M/Au:M/C:P/I:N/A:P')]")
        for key in object_scores_cvss2.keys():
            self.verify_score(key, object_scores_cvss2.get(key))

        # Checking Reset Button functionality
        self.click_on_resetButton()
        self.verify_element("//div[contains(text(),'OVERALL')]/following-sibling::div[contains(text(),'2.7')]")
        fprint(self, "[Passed] - test_01_verify_cvss2_calculator")

    def test_02_verify_cvss3_calculator(self):
        fprint(self, "TC_ID: 4110552 - test_02_verify_cvss3_calculator")
        nav_menu_main(self, "CVSS Calculator")
        self.driver.find_element_by_xpath("//div[contains(text(),'CVSS 3')]").click()
        for obj in condition_cvss3:
            self.select_object_in_baseScore_metrics(obj)

        self.driver.find_element_by_xpath("//button[contains(text(),'Show Scores')]").click()
        self.verify_element("//div[contains(text(),'SCORE')]/following-sibling::div[contains(text(),'5.1')]")
        self.verify_element("//div[@id='scoresGraph']/p[contains(text(),'AV:A/AC:H/PR:L/UI:R/S:C/C:L/I:L/A:L')]")
        for key in object_scores_cvss3.keys():
            self.verify_score(key, object_scores_cvss3.get(key))

        # Checking Reset Button functionality
        self.click_on_resetButton()
        self.verify_element("//div[contains(text(),'OVERALL')]/following-sibling::div[contains(text(),'2.7')]")
        fprint(self, "[Passed] - test_02_verify_cvss3_calculator")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
