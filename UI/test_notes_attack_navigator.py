from lib.ui.notes import *

class AttackNavNotes(unittest.TestCase):

    note = "This is the Attack navigator notes created by UI automation"

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

    def test_01_verify_attck_nav_notes_tab(self):
        fprint(self, "TC_ID: 77501 verifying that Attack navigator notes page is loading")
        nav_to_attck_nav_notes(self, True)
        close_slider(self)

    def test_02_verify_add_attck_nav_note(self):
        fprint(self, "TC_ID: 77502 verifying that Attack navigator notes can be added")
        nav_to_attck_nav_notes(self)
        add_note(self, 2)
        close_slider(self)
        fprint(self, "[PASSED] Notes added successfully")

    def test_03_verify_edit_attck_nav_note(self):
        fprint(self, "TC_ID: 77503 verifying that notes can be edited")
        nav_menu_main(self, "Global Notes")
        click_on_note(self, self.note)
        click_on_redirection(self)
        click_on_note(self, self.note)
        edit_note(self, " Updated")
        fprint(self, "[PASSED] Notes edited successfully")

    def test_04_verify_search_attck_nav_note(self):
        fprint(self, "TC_ID: 77504 verifying that search is working fine")
        nav_menu_main(self, "Global Notes")
        click_on_note(self, self.note)
        click_on_redirection(self)
        close_slider(self)
        fprint(self, "[PASSED] Search is working fine, notes is visible")

    # bug is reported once that is fix will implement
    def test_05_verify_attck_nav_note_quick_actions(self):
        fprint(self, "TC_ID: 77505 verifying that quick actions are working fine")
        nav_menu_main(self, "Global Notes")
        click_on_note(self, self.note)
        click_on_redirection(self)
        note_quick_action(self, False)
        fprint(self, "[PASSED] Quick actions verified successfully")

    def test_06_verify_search_attck_nav_note_in_global_notes(self):
        fprint(self, "TC_ID: 77506 verifying that attack navigator notes are present in global notes")
        nav_menu_main(self, "Global Notes")
        search_note(self)
        fprint(self, "[PASSED] Attack navigator notes is visible")

    def test_07_verify_redirection_to_attck_nav_from_global_notes(self):
        fprint(self, "TC_ID: 77507 verifying that redirection to Attack navigator note from global notes is working fine")
        nav_menu_main(self, "Global Notes")
        click_on_note(self, self.note+" Updated")
        click_on_redirection(self, " Updated")
        close_slider(self)
        fprint(self, "[PASSED] Notes is visible in Attack Navigator, redirection is working properly")

    def test_08_verify_delete_attck_nav_note(self):
        fprint(self, "TC_ID: 77508 verifying that notes can be deleted in Attack navigator feed")
        nav_menu_main(self, "Global Notes")
        click_on_note(self, self.note + " Updated")
        click_on_redirection(self)
        click_on_note(self, self.note + " Updated")
        delete_note(self, 2)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
