from lib.ui.notes import *

class ThreatDataNotes(unittest.TestCase):

    note = "This is the threat data notes created by UI automation"

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

    def test_01_verify_threat_data_notes_tab(self):
        fprint(self, "TC_ID: 77201 verifying that threat data notes page is loading")
        nav_to_threat_data_notes(self)

    def test_02_verify_add_threat_data_note(self):
        fprint(self, "TC_ID: 77202 verifying that threat data notes can be added")
        nav_to_threat_data_notes(self)
        add_note(self)
        fprint(self, "[PASSED] Notes added successfully")

    def test_03_verify_edit_threat_data_note(self):
        fprint(self, "TC_ID: 77203 verifying that notes can be edited")
        nav_to_threat_data_notes(self)
        click_on_note(self, self.note)
        edit_note(self, " Updated")
        fprint(self, "[PASSED] Notes edited successfully")

    def test_04_verify_search_threat_data_note(self):
        fprint(self, "TC_ID: 77204 verifying that search is working fine")
        nav_to_threat_data_notes(self)
        search_note(self)
        fprint(self, "[PASSED] Search is working fine, notes is visible")

    def test_05_verify_threat_data_note_quick_actions(self):
        fprint(self, "TC_ID: 77205 verifying that quick actions are working fine")
        nav_to_threat_data_notes(self)
        note_quick_action(self)
        fprint(self, "[PASSED] Quick actions verified successfly")

    def test_06_verify_search_threat_data_note_in_global_notes(self):
        fprint(self, "TC_ID: 77206 verifying that notes are present in global notes")
        nav_menu_main(self, "Global Notes")
        search_note(self)
        fprint(self, "[PASSED] Threat data notes is visible")

    def test_07_verify_redirection_to_threat_data_from_global_notes(self):
        fprint(self, "TC_ID: 77207 verifying that redirection to threat data note from global notes is working fine")
        nav_menu_main(self, "Global Notes")
        click_on_note(self, self.note+" Updated")
        click_on_redirection(self)
        fprint(self, "[PASSED] Notes is visible in threat data, redirection is working properly")

    def test_08_verify_delete_threat_data_note(self):
        fprint(self, "TC_ID: 77208 verifying that notes can be deleted in threat data")
        nav_menu_main(self, "Global Notes")
        click_on_note(self, self.note + " Updated")
        click_on_redirection(self)
        click_on_note(self, self.note + " Updated")
        delete_note(self)


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
