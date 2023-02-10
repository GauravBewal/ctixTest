import json
import unittest
import requests
from lib.api.common_utilities import *
service = 'conversion'
'''
This module contains test cases to verify the Webscrapper from the automation side 
'''

class Webscrapper(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pass

    def test_01_Get_Webscrapper_List(self):
        """
        test case to verify the status code and response of the get webscrapper API
        """
        print("----- Test Case: Test case to verify the status code and response of the get webscrapper API -----")
        endpoint = "/feed-sources/web-scrapper/collection/"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the GET request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_01_Get_Webscrapper_List_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'conversion/Feed_Sources/Webscrapper/test_01_Get_Webscrapper_List_schema'):
            print("[PASSED] GET request is successful")
        else:
            print("[FAILED] GET request is not successful")
            self.fail()

    def test_02_Fetch_IOC_From_Webscrapper_URL(self):
        """
        test case to verify the status code and response of the Fetch Ioc From Webscrapper URL API
        """
        print("----- Test Case: Test case to verify the status code and response of the Fetch Ioc From Webscrapper URL API-----")
        payload = getJsonFileData('api_payload/test_02_Fetch_IOC_From_Webscrapper_URL.json')
        endpoint = "/feed-sources/web-scrapper/analyse/url"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_02_Fetch_IOC_From_Webscrapper_URL_runtime', response)
        value = getJsonFileData('api_response_runtime/test_02_Fetch_IOC_From_Webscrapper_URL_runtime.json')
        val = value["mapping"][0]["headers"] # getting the value to change in the schema
        print(val) # printing the value to be changed
        read_schema = getJsonFileData('api_schema/conversion/Feed_Sources/Webscrapper/test_02_Fetch_IOC_From_Webscrapper_URL_schema.json') # loading the schema
        read_schema["properties"]["suggestions"]["properties"][str(val)] = {"type": "array", "items": {"type": "string"}}
        read_schema["properties"]["suggestions"]["required"].clear()
        read_schema["properties"]["suggestions"]["required"].append(str(val))
        test = json.dumps(read_schema)
        dict = test.replace("runtime_ip", val)
        temp = json.loads(dict)
        print(temp)
        filepath = os.path.join(os.environ["PYTHONPATH"], f"testdata/api_schema/conversion/Feed_Sources/Webscrapper",
                                f'test_02_Fetch_IOC_From_Webscrapper_URL_schema.json')
        with open(filepath, "w") as outfile:
            json.dump(temp, outfile)
        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Webscrapper/test_02_Fetch_IOC_From_Webscrapper_URL_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_03_Add_new_Webscrapper(self):
        """
        test case to verify the status code and response of the add new webscrapper API
        """
        print("----- Test Case: Test case to verify the status code and response of the add new webscrapper API-----")
        value = getJsonFileData('api_response_runtime/test_02_Fetch_IOC_From_Webscrapper_URL_runtime.json')
        val = value["mapping"][0]["headers"]  # getting the value to change in the schema
        print(val)  # printing the value to be changed
        payload = getJsonFileData('api_payload/test_03_Add_new_Webscrapper.json')
        payload["mapping"][0]["headers"] = val
        print(payload)
        endpoint = "/feed-sources/web-scrapper/collection"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_03_Add_new_Webscrapper_runtime', response)
        if response.status_code == 200 and validate_schema(response,
                                                           'conversion/Feed_Sources/Webscrapper/test_03_Add_new_Webscrapper_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_04_Poll_Now_Manually(self):
        """
        test case to verify the response and the status code of the Poll Now Manually API
        """
        print("----- Test Case: Test case to verify the response and the status code of the Poll Now Manually API-----")
        source_id = getJsonFileData("api_response_runtime/test_03_Add_new_Webscrapper_runtime.json")["id"]
        endpoint = f"/feed-sources/web-scrapper/collection/{source_id}/publish"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the POST request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json="")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_04_Poll_Now_Manually_runtime',
                              response)
        if response.status_code == 200 and validate_schema(response,'conversion/Feed_Sources/Webscrapper/test_04_Poll_Now_Manually_schema'):
            print("[PASSED] POST request is successful")
        else:
            print("[FAILED] POST request is not successful")
            self.fail()

    def test_05_Update_Webscrapper_Collection(self):
        """
        Test case to verify the status code and response of the Update Webscrapper collection API
        """
        print("----- Test Case:Test case to verify the status code and response of the Update Webscrapper collection API-----")
        source_id = getJsonFileData("api_response_runtime/test_03_Add_new_Webscrapper_runtime.json")["id"]
        endpoint = f"/feed-sources/web-scrapper/collection/{source_id}/"
        url = f"{base_url}{service}{endpoint}"
        print(f'Making the Put request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json="")
        print(f"response code is : {response.status_code}")
        print(f"Received response is: {response.text}")
        save_runtime_response('testdata/api_response_runtime', 'test_05_Update_Webscrapper_Collection_runtime',
                              response)
        if response.status_code == 202 and validate_schema(response,
                                                           'conversion/Feed_Sources/Webscrapper/test_05_Update_Webscrapper_Collection_schema'):
            print("[PASSED] PUT request is successful")
        else:
            print("[FAILED] PUT request is not successful")
            self.fail()

    def test_06_Delete_Collection(self):
        """
        test case to verify the status code and response of the delete collection
        """
        print("----- Test Case: Test case to verify the status code and response of the delete source category-----")
        source_id = getJsonFileData("api_response_runtime/test_03_Add_new_Webscrapper_runtime.json")["id"]
        endpoint = f"/feed-sources/web-scrapper/collection/{source_id}"
        url = f"{base_url}{service}{endpoint}"
        print("Validating response got from the endpoint")
        print(f'Making the DELETE request for the {url}')
        print("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        print(f"response code is : {response.status_code}")
        print(response.text)
        save_runtime_response('testdata/api_response_runtime', 'test_06_Delete_Collection_runtime',
                              response)
        if response.status_code == 202 and validate_schema(response,
                                                           "conversion/Feed_Sources/Webscrapper/test_06_Delete_Collection_schema"):
            print("[PASSED] DELETE request is successful")
        else:
            print("[FAILED] DELETE request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
