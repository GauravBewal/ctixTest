import unittest
import requests
from lib.api.common_utilities import *

'''
This module contains all the testcases of the Twitter feeds
'''

service = 'conversion'

class Twitter(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_create_twitter_account(self):
        log("----- Test Case: test_01_create_twitter_account -----")
        # This variable is used in case the account is already created so we delete that.
        already_created_id = ""

        for val in json.loads(requests.get(f"{base_url}{service}/feed-sources/twitter_feeds/{authentication()}").text)["results"]:
            if val["account_handle"] == "kumaryogesh2501":
                already_created_id = val["id"]
                break

        if already_created_id != "":
            requests.delete(f"{base_url}{service}/feed-sources/twitter_feeds/{already_created_id}/{authentication()}")

        payload = getJsonFileData('api_payload/test_01_create_twitter_account.json')
        endpoint = "/feed-sources/twitter_feeds"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_create_twitter_account_runtime', response)

        if response.status_code == 201 and validate_schema(response, 'conversion/Feed_Sources/Twitter/test_01_create_twitter_account_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_02_twitter_feed_list(self):
        log("----- Test Case: test_02_twitter_feed_list -----")
        endpoint = "/feed-sources/twitter_feeds/"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_twitter_feed_list_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Twitter/test_02_twitter_feed_list_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_03_All_tweets(self):
        log("----- Test Case: test_03_All_tweets -----")
        id = list_of_values(getJsonFileData('api_response_runtime/test_02_twitter_feed_list_runtime.json'), 'id')[0]
        endpoint = "/feed-sources/twitter/tweets"
        param = {
                "account_id": id
        }
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_03_All_tweets_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Twitter/test_03_All_tweets_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_04_save_search(self):
        log("----- Test Case: test_04_save_search -----")
        payload = getJsonFileData('api_payload/test_04_save_search.json')
        account_id = list_of_values(getJsonFileData('api_response_runtime/test_02_twitter_feed_list_runtime.json'), 'id')[0]
        payload['account_id'] = account_id
        endpoint = "/feed-sources/twitter/save-searches"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_04_save_search_runtime', response)

        if response.status_code == 201 and validate_schema(response, 'conversion/Feed_Sources/Twitter/test_04_save_search_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_05_get_saved_searches(self):
        log("----- Test Case: test_05_get_saved_searches -----")
        endpoint = "/feed-sources/twitter/save-searches"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_05_get_saved_searches_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Twitter/test_05_get_saved_searches_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_06_test_twitter_connectivity(self):
        log("----- Test Case: test_06_test_twitter_connectivity -----")
        account_id = list_of_values(getJsonFileData('api_response_runtime/test_02_twitter_feed_list_runtime.json'),'id')[0]
        endpoint = f"/feed-sources/twitter/connectivity/{account_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_06_test_twitter_connectivity_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Twitter/test_06_test_twitter_connectivity_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_07_twitter_account_details(self):
        log("----- Test Case: test_07_twitter_account_details -----")
        account_id = list_of_values(getJsonFileData('api_response_runtime/test_02_twitter_feed_list_runtime.json'),'id')[0]
        endpoint = f"/feed-sources/twitter_feeds/{account_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the get request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_07_twitter_account_details_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Twitter/test_07_twitter_account_details_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_08_get_saved_search_details(self):
        log("----- Test Case: test_08_get_saved_search_details -----")
        account_id =list_of_values(getJsonFileData('api_response_runtime/test_02_twitter_feed_list_runtime.json'), 'id')[0]
        save_search_id = list_of_values(getJsonFileData("api_response_runtime/test_05_get_saved_searches_runtime.json"), 'id')[0]
        endpoint = f"/feed-sources/twitter/save-searches/{save_search_id}"
        param = {
                "account_id" :account_id
                }
        url = f"{base_url}{service}{endpoint}"
        log("Validating response got from the endpoint")
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_08_get_saved_search_details_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Twitter/test_08_get_saved_search_details_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_09_update_twitter_account(self):
        log("----- Test Case: test_09_update_twitter_account -----")
        account_id = list_of_values(getJsonFileData('api_response_runtime/test_01_create_twitter_account_runtime.json'), 'id')[0]
        payload = getJsonFileData('api_payload/test_09_update_twitter_account.json')
        endpoint = f'/feed-sources/twitter_feeds/{account_id}'
        url = f"{base_url}{service}{endpoint}"

        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_09_update_twitter_account_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Twitter/test_09_update_twitter_account_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

    def test_10_parse_tweet(self):
        log("----- Test Case: test_10_parse_tweet -----")
        payload = getJsonFileData('api_payload/test_10_parse_tweet.json')
        result = getJsonFileData('api_response_runtime/test_03_All_tweets_runtime.json')

        payload['tweet_id'] = result["results"][0]["tweet_id"]
        payload["text"] = result["results"][0]["text"]
        payload["linked_urls"] = result["results"][0]["linked_urls"]
        payload["user_id"] = result["results"][0]["user_id"]
        payload["user_handle"] = result["results"][0]["user_handle"]
        log(payload)
        endpoint = f"/feed-sources/{payload['tweet_id']}/iocs"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_10_parse_tweet_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Twitter/test_10_parse_tweet_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_11_delete_twitter_account(self):
        log("----- Test Case: test_11_delete_twitter_account -----")
        result = getJsonFileData('api_response_runtime/test_01_create_twitter_account_runtime.json')
        source_id = result["id"]
        endpoint = f"/feed-sources/twitter_feeds/{source_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the DELETE request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_11_delete_twitter_account_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/Twitter/test_11_delete_twitter_account_schema'):
            log("[PASSED] DELETE request is successful")
        else:
            log("[FAILED] DELETE request is not successful")
            self.fail()

if __name__ == '__main__':
    unittest.main(testRunner=reporting())