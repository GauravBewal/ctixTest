import unittest

from lib.ui.analyst_workbench import click_to_process, verify_data
from lib.ui.nav_threat_data import *

encode_data = "Automation@123"
expected_decode_data_manual = "QXV0b21hdGlvbkAxMjM="
expected_decode_data_importFile = "SVBWNCAtIDIzLjE1NC4xNzcuNjIKSVBWNiAtIDgwN2I6OTMzNDo2NGY3OmYyM2I6Y2I5YTo3ODc3OjIxMTM6NzI4MgpEb21haW4gLSBodHRwczovL3N3aXNzY3Bwcml2YXRlMi5jb20vClVSTCAtIGh0dHBzOi8vY3J5cHRvYmVhcndhdGNoY2x1Ym5mdDIuY29tLwpNRDUgLSBjOTVmZGI3ZThlYzE4NTM0YjU0OWRiYTMzOTY4ODM1MgpTSEExIC0gOWYwMWQ0NDQyYzQ5NWM3MTI4NjQ5Yjk4MjAxMTg3YmMwYzU4ZGVkMgpTSEEyMjQgLSBiYjcyNjI5NjM4ZjkzNDMzZDA1YWFlZDBiODlmZDA3Y2UyNmYxMDRmZGExNDM1NTRlZDcwNzVlMgpTSEEyNTYgLSBjZjhiNjhiNzc5YzRlNzE2ZWNlZWQ1ZGFkNzAwM2QyODBlYmE5NmMxMWYzZDc4NjhkNTlmMmRjYWU1NTAwMDYyClNIQTM4NCAtIDFlM2IzNzA1YWYzMjBhYzFjOTlkMjFkNzk4ZmYzNjNhNmMwNjc0YmJlZjQzZTc3ZTNhODczODhmNzlhMjhjNTZmZjFlNjhiNWM1ZWI2N2YzYWE3MzJmNjFhZWE1NDMzMgpTSEE1MTIgLSA5ZWQyMmUzZGEwZDZkNTgxOTM0ODljZGJkM2UwZDE4MWNmYzYzMTU5OGRlMjZiYjBlMTdiYjg4NzRlNmNmMjYyYzRlYjkzNmY0MzY4YTMyNDk5NDk5NmQwYjNiN2MxMDRhNGZkYzU2MTU4MDg1MWI0YmZkYjdjYTQwMjMyMDg4MgpTU0RFRVAgLSAxNTM2OloxUWJGSkw1SmNINXRTSFdEVUlUc2hxZDRYUU5YMjdIMXo6UUZKbDlPVTMyCkVtYWlsIC0gbWFpbGNpdXNAZGl6enlkb20yLmNvbQpNdXRleCAtIHNvbWVtdXRleDIKUmVnaXN0cnkgS2V5IC0gSEtFWV9MT0NBTF9NQUNISU5FXFNPRlRXQVJFXE1pY3Jvc29mdFxlcnJvbmVvdXMyCkxvY2F0aW9uIC0gQzovVXNlci9Gb2xkZXIxL2FwcGxpY2F0aW9uMi50eHQKQVNOIC0gQVMyMTIKQ0lEUiAtIDk4LjIuMTIxLjEyLzMwCkNWRSAtIENWRS0yMDIyLTIzMTcy"
filename = "all_iocs_txt.txt"


class EncodeDecode(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.driver = initialize_browser(self)
        login(self, Admin_Email, Admin_Password)

    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def test_01_verify_encode_decode(self):
        fprint(self, "TC_ID: 4011551 - test_01_verify_encode_decode")
        nav_menu_main(self, "Encode - Decode: Base64")
        self.driver.find_element_by_xpath("(//textarea[@aria-placeholder='Type (or paste) data here'])[1]").click()
        self.driver.find_element_by_xpath("(//textarea[@aria-placeholder='Type (or paste) data here'])[1]").send_keys(encode_data)
        fprint(self, "Entered the Encode data - "+encode_data)
        click_to_process(self, "Encode - Decode: Base64")
        if not waitfor(self, 5, By.XPATH, "//div[@empty='true']", False):
            fprint(self, "Data is Decoded, verifying with the expected one...")
            verify_data(self, expected_decode_data_manual)
        else:
            fprint(self, "[Failed] - Decoded data is not visible.")

    def test_02_verify_encode_decode_by_importFile(self):
        fprint(self, "TC_ID: 4011552 - test_02_verify_encode_decode_by_importFile")
        nav_menu_main(self, "Encode - Decode: Base64")
        self.driver.find_element_by_xpath("(//span[@class='cyicon-more-vertical'])[1]").click()
        try:
            waitfor(self, 10, By.XPATH, "(//span[contains(text(),'Upload a File')])[2]")
            self.driver.find_element_by_xpath("(//span[contains(text(),'Upload a File')])[2]").click()
        except:
            self.driver.find_element_by_xpath("(//div[contains(text(),'Upload a File')])[2]").click()
        waitfor(self, 5, By.XPATH, "//input[@type = 'file']")
        upload = self.driver.find_element_by_xpath("(//input[@type = 'file'])[1]")
        file_path = os.path.join(os.environ["PYTHONPATH"], "testdata", "encode_decode/"+filename)
        fprint(self, "Uploading file... - "+filename)
        upload.send_keys(file_path)
        # Intentionally used sleep waiting for file to be completely uploaded
        sleep(10)
        click_to_process(self, "Encode - Decode: Base64")
        if not waitfor(self, 5, By.XPATH, "//div[@empty='true']", False):
            fprint(self, "Data is Decoded, verifying with the expected one...")
            verify_data(self, expected_decode_data_importFile)
        else:
            fprint(self, "[Failed] - Decoded data is not visible.")


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
