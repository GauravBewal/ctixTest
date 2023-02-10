import unittest
from lib.ui.nav_app import *


def add_note(self, save_index=1, readOnly=False, sname=""):
    if waitfor(self, 10, By.XPATH, "//button/span[contains(text(),'Add Note')]", False):
        self.driver.find_element_by_xpath("//button/span[contains(text(),'Add Note')]").click()
    else:
        waitfor(self, 10, By.XPATH, "//button[contains(text(),'Add Note')]", False)
        self.driver.find_element_by_xpath("//button[contains(text(),'Add Note')]").click()

    fprint(self, "Clicked on Add notes button")
    waitfor(self, 10, By.XPATH, "//textarea[@placeholder='Add your note']")
    if not readOnly:
        self.driver.find_element_by_xpath("//textarea[@placeholder='Add your note']").send_keys(self.note)
        fprint(self, "Provided the content of the notes")
        waitfor(self, 10, By.XPATH, f"(//button[contains(text(),'Save')])[{save_index}]")
        self.driver.find_element_by_xpath(f"(//button[contains(text(),'Save')])[{save_index}]").click()
        fprint(self, "Clicked on save")
        verify_success(self, "Note created successfully.")
    else:
        save_screenshots(self, module="Global Notes", sname=sname)
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Cancel')])[2]").click()
        sleep(1)
        fprint(self, "Closed the add notes input box")

def click_on_note(self, text, readOnly=False):
    waitfor(self, 10, By.XPATH, f"//pre[contains(text(),'{text}')]")
    self.driver.find_element_by_xpath(f"//pre[contains(text(),'{text}')]").click()
    fprint(self, "Clicked on notes")
    waitfor(self, 10, By.XPATH, f"//pre[contains(text(),'{text}')]")
    fprint(self, "Notes slider opened")
    if readOnly:
        waitfor(self, 5, By.XPATH, "//span[@data-testaction='slider-close']")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        sleep(1)


def edit_note(self, text, readOnly=False, module=""):
    waitfor(self, 10, By.XPATH, "//button[contains(text(),'Edit')]")
    self.driver.find_element_by_xpath("//button[contains(text(),'Edit')]").click()
    fprint(self, "Clicked on edit")
    if not readOnly:
        waitfor(self, 10, By.XPATH, "//textarea[@placeholder='Add your note']")
        self.driver.find_element_by_xpath("//textarea[@placeholder='Add your note']").send_keys(text)
        fprint(self, "Provided the updated content of the notes")
        waitfor(self, 10, By.XPATH, "//button[contains(text(),'Submit')]")
        self.driver.find_element_by_xpath("//button[contains(text(),'Submit')]").click()
        fprint(self, "Clicked on Submit")
        verify_success(self, "Note updated successfully.")
        fprint(self, "[PASSED] notes updated successfully")
        close_slider(self)
    else:
        save_screenshots(self, module=module, sname="My Notes Edit Slider")
        waitfor(self, 3, By.XPATH, "(//button[contains(text(), 'Cancel')])[1]")
        self.driver.find_element_by_xpath("(//button[contains(text(), 'Cancel')])[1]").click()
        fprint(self, "Clicked on Cancel")
        waitfor(self, 5, By.XPATH, "//span[@data-testaction='slider-close']")
        self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
        sleep(0.5)


def delete_note(self, button_index=1, readOnly=False):
    waitfor(self, 10, By.XPATH, f"(//button[contains(text(),'Delete')])[{button_index}]")
    self.driver.find_element_by_xpath(f"(//button[contains(text(),'Delete')])[{button_index}]").click()
    fprint(self, "Clicked on delete")
    waitfor(self, 10, By.XPATH, "//button[@data-testalert='confirm-delete']")
    self.driver.find_element_by_xpath("//button[@data-testalert='confirm-delete']").click()
    verify_success(self, "Note deleted successfully.")
    fprint(self, "[PASSED] notes deleted successfully")


def search_note(self):
    waitfor(self, 10, By.XPATH, "//input[@name='searchbar']")
    self.driver.find_element_by_xpath("//input[@name='searchbar']").send_keys(self.note + " Updated")
    fprint(self, "Provided the title in the search bar")
    self.driver.find_element_by_xpath("//input[@name='searchbar']").send_keys(Keys.ENTER)
    waitfor(self, 10, By.XPATH, f"//pre[contains(text(),'{self.note + ' Updated'}')]")
    fprint(self, "Notes is visible")


def note_quick_action(self, slider_close=True):
    waitfor(self, 10, By.XPATH, "(//div[contains(@class,'cy-notes-card__head-right')])[1]")
    self.driver.find_element_by_xpath("(//div[contains(@class,'cy-notes-card__head-right')])[1]").click()
    fprint(self, "Clicked on three dots")
    waitfor(self, 10, By.XPATH, "//li/span[contains(text(), 'Edit')]")
    self.driver.find_element_by_xpath("//li/span[contains(text(), 'Edit')]").click()
    fprint(self, "Clicked on edit")
    waitfor(self, 10, By.XPATH, "//span[contains(text(), 'Edit Note')]")
    if slider_close:
        close_slider(self)
    fprint(self, "Closing the slider")
    fprint(self, "Edit action is verified")
    waitfor(self, 10, By.XPATH, "(//div[contains(@class,'cy-notes-card__head-right')])[1]")
    self.driver.find_element_by_xpath("(//div[contains(@class,'cy-notes-card__head-right')])[1]").click()
    waitfor(self, 10, By.XPATH, "//li/span[contains(text(), 'Delete')]")
    self.driver.find_element_by_xpath("//li/span[contains(text(), 'Delete')]").click()
    waitfor(self, 10, By.XPATH, "//button[@data-testalert='cancel-delete']")
    self.driver.find_element_by_xpath("//button[@data-testalert='cancel-delete']").click()
    fprint(self, "Delete action is verified")

def nav_to_threat_data_notes(self):
    nav_menu_main(self, "Threat Data")
    waitfor(self, 10, By.XPATH, "(//span[@data-testid='type'])[1]")
    self.driver.find_element_by_xpath("(//span[@data-testid='type'])[1]").click()
    fprint(self, "Clicked on the intel")
    waitfor(self, 10, By.XPATH, "//div[contains(text(), 'Notes')]")
    self.driver.find_element_by_xpath("//div[contains(text(), 'Notes')]").click()
    fprint(self, "Clicked Notes tab in threat data details page")
    waitfor(self, 10, By.XPATH, "//span[contains(text(), 'Add Note')]")
    fprint(self, "[PASSED] Notes tab has loaded properly")


def click_on_redirection(self, text=""):
    waitfor(self, 10, By.XPATH, "//p/i[contains(@class, 'cyicon-external-link')]")
    self.driver.find_element_by_xpath("//p/i[contains(@class, 'cyicon-external-link')]").click()
    fprint(self, "Clicked on the redirection")
    waitfor(self, 10, By.XPATH, f"//pre[contains(text(),'{self.note + text}')]")

def nav_to_rss_notes(self, slider_close=False):
    nav_menu_main(self, "RSS Feeds")
    waitfor(self, 10, By.XPATH, "//button[contains(text(), 'Create Intel')]")
    self.driver.find_element_by_xpath("//button[contains(text(), 'Create Intel')]").click()
    fprint(self, "Clicked on the create intel of the feed")
    waitfor(self, 10, By.XPATH, "//li/span[contains(text(), 'Notes')]")
    self.driver.find_element_by_xpath("//li/span[contains(text(), 'Notes')]").click()
    fprint(self, "Clicked Notes tab in rss feed slider page")
    waitfor(self, 10, By.XPATH, "//button[contains(text(), 'Add Note')]")
    fprint(self, "[PASSED] Notes tab has loaded properly")


def nav_to_twitter_notes(self, slider_close=False):
    nav_menu_main(self, "Twitter Feeds")
    waitfor(self, 10, By.XPATH, "(//div[contains(@class, 'tweet-deck__body--content')])[1]")
    self.driver.find_element_by_xpath("(//div[contains(@class, 'tweet-deck__body--content')])[1]").click()
    fprint(self, "Clicked on the create intel of the feed")
    waitfor(self, 10, By.XPATH, "//li/span[contains(text(), 'Notes')]")
    self.driver.find_element_by_xpath("//li/span[contains(text(), 'Notes')]").click()
    fprint(self, "Clicked Notes tab in rss feed slider page")
    waitfor(self, 10, By.XPATH, "//button[contains(text(), 'Add Note')]")
    fprint(self, "[PASSED] Notes tab has loaded properly")

def nav_to_attck_nav_notes(self, slider_close=False):
    nav_menu_main(self, "ATT&CK Navigator")
    waitfor(self, 10, By.XPATH, "//span[contains(text(), ' Gather Victim Host Information ')]")
    self.driver.find_element_by_xpath("//span[contains(text(), ' Gather Victim Host Information ')]").click()
    fprint(self, "Clicked on the one of the technique")
    waitfor(self, 10, By.XPATH, "//li/span[contains(text(), 'Notes')]")
    self.driver.find_element_by_xpath("//li/span[contains(text(), 'Notes')]").click()
    fprint(self, "Clicked Notes tab in Attack Navigator slider page")
    waitfor(self, 10, By.XPATH, "//button[contains(text(), 'Add Note')]")
    fprint(self, "[PASSED] Notes tab has loaded properly")

def close_slider(self):
    waitfor(self, 10, By.XPATH, "//span[@data-testaction='slider-close']", False)
    self.driver.find_element_by_xpath("//span[@data-testaction='slider-close']").click()
    fprint(self, "Closing the slider")

def nav_to_threat_mail_notes(self):
    nav_menu_main(self, "Threat Mailbox")
    waitfor(self, 10, By.XPATH, "//button[contains(text(), 'Create Intel')]")
    self.driver.find_element_by_xpath("//button[contains(text(), 'Create Intel')]").click()
    fprint(self, "Clicked on the create intel of the feed")
    waitfor(self, 10, By.XPATH, "//li/span[contains(text(), 'Notes')]")
    self.driver.find_element_by_xpath("//li/span[contains(text(), 'Notes')]").click()
    fprint(self, "Clicked Notes tab in rss feed slider page")
    waitfor(self, 10, By.XPATH, "//button[contains(text(), 'Add Note')]")
    fprint(self, "[PASSED] Notes tab has loaded properly")