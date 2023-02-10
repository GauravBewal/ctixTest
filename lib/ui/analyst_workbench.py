from lib.common_functions import fprint


def verify_data(self, exp_data):
    elem = self.driver.find_element_by_xpath("(//textarea[@aria-placeholder='Type (or paste) data here'])[2]")
    actual_decode_data = elem.get_attribute("_value")
    fprint(self, "Actual Data - "+actual_decode_data)
    if actual_decode_data == exp_data:
        fprint(self, "[Passed] - Getting Expected Data")
    else:
        fprint(self, "[Failed] - Not Getting Expected Data")
        self.fail("[Failed] - Not Getting Expected Data")


def click_to_process(self, module):
    if module == "Encode - Decode: Base64":
        self.driver.find_element_by_xpath("(//span[contains(@class,'cyicon-angle-double-left')])[1]").click()
    elif module == "Fang - Defang":
        self.driver.find_element_by_xpath("(//button[contains(@class,'cyicon-angle-double-left')])[1]").click()
    elif module == "STIX conversion":
        self.driver.find_element_by_xpath("//button[contains(@class,'cyicon-angle-double-left')]").click()
    fprint(self, "Clicked on the button to Processed it...")
