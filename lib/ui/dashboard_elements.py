from lib.ui.nav_app import *
from lib.common_functions import *
from selenium.webdriver.common.by import By
widget_list = ['Allowed Indicators by Type', 'Confidence Score Vs TLP', 'Deprecated IOCs by Type']


def add_dashboard(self):
    nav_menu_main(self, 'Dashboards')
    waitfor(self, 20, By.XPATH, "//button[@data-testid='add-dashboard']")
    self.driver.find_element_by_xpath("//button[@data-testid='add-dashboard']").click()
    waitfor(self, 20, By.XPATH, "//div[contains(text(),'Create New Dashboard')]")
    waitfor(self, 20, By.XPATH, "//input[@aria-placeholder='Title*']")
    self.driver.find_element_by_xpath("//input[@aria-placeholder='Title*']").send_keys('test')
    waitfor(self, 20, By.XPATH, "//input[@name='basic']")
    self.driver.find_element_by_xpath("//input[@name='basic']").click()
    waitfor(self, 20, By.XPATH, "//p[contains(text(),'Stationary Dashbaord')]")
    self.driver.find_element_by_xpath("//p[contains(text(),'Stationary Dashbaord')]").click()
    waitfor(self, 20, By.XPATH, "//button[@data-testid='save-dashboard']")
    self.driver.find_element_by_xpath("//button[@data-testid='save-dashboard']").click()
    waitfor(self, 20, By.XPATH, "//span[contains(text(),'Hide')]")
    self.driver.find_element_by_xpath("//span[contains(text(),'Hide')]").click()
    for i in widget_list:
        waitfor(self, 20, By.XPATH, "//span[@class='cyicon-add'][1]")
        self.driver.find_element_by_xpath("//span[@class='cyicon-add'][1]").click()
        fprint(self, 'Adding widget  - '+i+'')
        waitfor(self, 20, By.XPATH,
                "(//div[contains(text(),'"+i+"')]/following::button/span[@class='cyicon-add'])[1]")
        self.driver.find_element_by_xpath(
            "(//div[contains(text(),'Allowed Indicators by Type')]/following::button/span[@class='cyicon-add'])[1]").click()
    waitfor(self, 20, By.XPATH, "//button[@data-testid='save']")
    self.driver.find_element_by_xpath("//button[@data-testid='save']").click()
    waitfor(self, 20, By.XPATH, "//*[contains(text(),'Dashboards') and contains(@class,'cy-page__title')]")
    fprint(self, 'Dashboard created successfully!')


def clickOnHorizontalLoadButton(self):
    waitfor(self, 1, By.XPATH, "(//span[@class='cyicon-chevron-right']//parent::button)[1]")
    self.driver.find_element_by_xpath("(//span[@class='cyicon-chevron-right']//parent::button)[1]").click()


def Herocard_Visible(self, element):
    fprint(self, "checking for " + element)
    try:
        f"//*[normalize-space(text())='{element}']"
        waitfor(self, 20, By.XPATH, f"//*[normalize-space(text())='{element}']")
        ele = self.driver.find_element_by_xpath(f"//*[normalize-space(text())='{element}']")
    except:
        clickOnHorizontalLoadButton(self)
        waitfor(self, 20, By.XPATH, f"//*[normalize-space(text())='{element}']")
        ele = self.driver.find_element_by_xpath(f"//*[normalize-space(text())='{element}']")
    self.driver.execute_script("arguments[0].scrollIntoView();", ele)
    fprint(self, "[Passed] " + element + " Visible")
    if (element == "Domain Objects"):
        fprint(self, "Domain Objects : " + self.driver.find_element_by_xpath(
            "//div[starts-with(@id,'sdo')]/div[1]/span/span").text + "\n\n")
    elif (element == "TLP Red" or element == "TLP Amber" or element == "TLP Green"):
        path = "//div[starts-with(@id,'tlp_" + (element[4:]).lower() + "')]/div[1]/span/span"
        fprint(self, "TLP " + element[4:] + " : " + self.driver.find_element_by_xpath(path).text + "\n\n")
    else:
        s = element[0:3]
        s = s.lower()
        path2 = "//div[starts-with(@id,'" + s + "')]/div[1]/span/span"
        fprint(self, element + " : " + self.driver.find_element_by_xpath(path2).text + "\n\n")


def widgets(self, attribute):
    waitfor(self, 20, By.XPATH,f"//*[normalize-space(text())='{attribute}']")
    try:
        waitfor(self, 20, By.XPATH, f"//*[normalize-space(text())='{attribute}']")
        ele = self.driver.find_element_by_xpath(f"//*[normalize-space(text())='{attribute}']")
    except:
        clickOnHorizontalLoadButton(self)
        waitfor(self, 20, By.XPATH, f"//*[normalize-space(text())='{attribute}']")
        ele = self.driver.find_element_by_xpath(f"//*[normalize-space(text())='{attribute}']")
    self.driver.execute_script("arguments[0].scrollIntoView();", ele)
    fprint(self,"[Passed] "+attribute+ " widget Visible\n")


def sources_Vs_Iocs(self,attr):
    waitfor(self, 20,By.XPATH,"//button[normalize-space()='"+attr+"']")
    fprint(self,"[Passed] "+attr+ " Vs IOCs widget Visible\n")


def TLP_Vs_All_IOCs(self,attr):
    waitfor(self, 20, By.XPATH, "//button[normalize-space()='" + attr + "']")
    fprint(self, "[Passed] TLP Vs " + attr + " widget Visible\n")


def Timeline_for_all_countries(self,attr):
    waitfor(self, 5, By.XPATH, "//button[normalize-space()='" + attr + "']")
    fprint(self, "[Passed] Timeline for " + attr + " widget Visible\n")


def Indicator_vs_Timeline(self,attr):
    waitfor(self, 5, By.XPATH, "//button[normalize-space()='" + attr + "']")
    fprint(self, "[Passed] Timeline for " + attr + " widget Visible\n")

