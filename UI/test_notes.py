from lib.ui.notes import *

class GlobalNotes(unittest.TestCase):

    note = "This is the notes created by UI automation"

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

    def test_01_verify_global_notes_page_loading(self):
        fprint(self, "TC_ID: 77101 verifying that global notes page is loading")
        nav_menu_main(self, "Global Notes")
        fprint(self, "Verifying that page is loaded")
        waitfor(self, 5, By.XPATH, "//h1[contains(text(),'Global Notes')]")
        fprint(self, "[PASSED] Global Notes page has loaded properly")

    def test_02_verify_add_global_note(self):
        fprint(self, "TC_ID: 77102 verifying that notes can be added")
        nav_menu_main(self, "Global Notes")
        add_note(self)
        fprint(self, "[PASSED] Notes added successfully")

    def test_03_verify_edit_global_note(self):
        fprint(self, "TC_ID: 77103 verifying that notes can be edited")
        nav_menu_main(self, "Global Notes")
        click_on_note(self, self.note)
        edit_note(self, " Updated")
        fprint(self, "[PASSED] Notes edited successfully")

    def test_04_verify_search_global_note(self):
        fprint(self, "TC_ID: 77104 verifying that search is working fine")
        nav_menu_main(self, "Global Notes")
        search_note(self)
        fprint(self, "[PASSED] Search is working fine, notes is visible")

    def test_05_verify_global_note_quick_actions(self):
        fprint(self, "TC_ID: 77105 verifying that quick actions are working fine")
        nav_menu_main(self, "Global Notes")
        note_quick_action(self)
        fprint(self, "[PASSED] Quick actions verified successfully")

    def test_06_verify_delete_global_note(self):
        fprint(self, "TC_ID: 77106 verifying that notes can be deleted")
        nav_menu_main(self, "Global Notes")
        click_on_note(self, self.note + " Updated")
        delete_note(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
