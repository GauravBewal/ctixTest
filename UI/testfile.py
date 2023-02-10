from selenium.webdriver import Firefox
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from config.process_config import *
from selenium.webdriver.firefox.options import Options as FOptions


class MyListener(AbstractEventListener):
    def before_navigate_to(self, url, driver):
        print("Before navigate to %s" % url)

    def after_navigate_to(self, url, driver):
        print("After navigate to %s" % url)

    def before_find(self, by, value, driver):
        print("I am being called before finding: " + str(value))

driver_path = os.path.join(os.environ["PYTHONPATH"], "tools", "macos", "geckodriver")
op = FOptions()
op.add_argument("--headless")
driver = Firefox(options=op, executable_path=driver_path)
driver = EventFiringWebDriver(driver, MyListener())

print(str(type(driver)))
driver.get("http://www.google.co.in/")
elm = driver.find_element_by_xpath("//input[@name='q']")
if not isinstance(elm, WebElement):
    #raise AttributeError("not a WebElement")
    print("not a WebElement")
    print(str(type(elm)))
else:
    print("its a webelement")

#action = ActionChains(driver)
#action.move_to_element(elm).perform()
print("finished")
driver.quit()