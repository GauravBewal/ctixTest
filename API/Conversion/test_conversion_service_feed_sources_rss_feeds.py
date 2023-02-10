import unittest
import requests

from lib.api.common_utilities import *

'''
This module contains all the testcases of the Feed Source --> RSS feed
'''

service = "conversion"

class RSSFeeds(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        pass

    def test_01_create_rss_feed(self):
        log("----- Test Case: test_01_create_rss_feed -----")
        payload = getJsonFileData('api_payload/test_01_create_rss_feed.json')

        endpoint = "/feed-sources/rss_feed"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the POST request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.post(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_01_create_rss_feed_runtime', response)

        if response.status_code == 201 and validate_schema(response, 'conversion/Feed_Sources/RSS_Feed/test_01_create_rss_feed_schema'):
            log("[PASSED] POST request is successful")
        else:
            log("[FAILED] POST request is not successful")
            self.fail()

    def test_02_list_rss_source(self):
        log("----- Test Case: test_02_list_rss_source   -----")
        endpoint = "/feed-sources/rss_feed"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_02_list_rss_source_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/RSS_Feed/test_02_list_rss_source_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_03_update_rss_feed(self):
        log("----- Test Case: test_03_update_rss_feed -----")
        payload = getJsonFileData('api_payload/test_03_update_rss_feed.json')
        result = getJsonFileData('api_response_runtime/test_01_create_rss_feed_runtime.json')
        rss_source_id = result["id"]

        endpoint = f"/feed-sources/rss_feed/{rss_source_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_03_update_rss_feed_runtime', response)

        if response.status_code == 200 and validate_schema(response,  'conversion/Feed_Sources/RSS_Feed/test_03_update_rss_feed_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

    def test_04_rss_feed_source_detail(self):
        log("----- Test Case: test_04_rss_feed_source_detail   -----")
        result = getJsonFileData('api_response_runtime/test_01_create_rss_feed_runtime.json')
        rss_source_id = result["id"]
        endpoint = f"/feed-sources/rss_feed/{rss_source_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_04_rss_feed_source_detail_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/RSS_Feed/test_04_rss_feed_source_detail_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_05_list_rss_feed_article(self):
        log("----- Test Case: test_05_list_rss_feed_article   -----")
        endpoint = f"/feed-sources/rss/articles"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_05_list_rss_feed_article_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/RSS_Feed/test_05_list_rss_feed_article_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_06_view_rss_feed_article(self):
        log("----- Test Case: test_06_view_rss_feed_article   -----")
        result = getJsonFileData('api_response_runtime/test_02_list_rss_source_runtime.json')
        feed_id = result["results"][0]["id"]
        param = {
            "feed_id": feed_id
        }
        log(f"feed id is {feed_id}")
        endpoint = f"/feed-sources/rss/articles"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_06_view_rss_feed_article_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/RSS_Feed/test_06_view_rss_feed_article_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_07_update_rss_feed_article(self):
        log("----- Test Case: test_07_update_rss_feed_article -----")
        payload = {
            "bookmark": True,
            "id": "bb042a32-6eb5-4cec-8886-c3921a9860c0"
            }

        result = getJsonFileData('api_response_runtime/test_05_list_rss_feed_article_runtime.json')
        payload["id"] = result["results"][0]["id"]

        endpoint = f"/feed-sources/rss/articles"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_07_update_rss_feed_article_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/RSS_Feed/test_07_update_rss_feed_article_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

    def test_08_ioc_listing_api(self):
        log("----- Test Case: test_08_ioc_listing_api   -----")
        result = getJsonFileData('api_response_runtime/test_06_view_rss_feed_article_runtime.json')
        feed_id = result["results"][0]["id"]
        param = {
            "type": "rss_feed"
        }

        endpoint = f"/feed-sources/{feed_id}/iocs"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the GET request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.get(f"{url}/{authentication()}", params=param)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_08_ioc_listing_api_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/RSS_Feed/test_08_ioc_listing_api_schema'):
            log("[PASSED] GET request is successful")
        else:
            log("[FAILED] GET request is not successful")
            self.fail()

    def test_09_create_intel_feeds(self):
        log("----- Test Case: test_09_create_intel_feeds   -----")
        payload = getJsonFileData('api_payload/test_09_create_intel_feeds.json')
        feed_id = getJsonFileData('api_response_runtime/test_05_list_rss_feed_article_runtime.json')["results"][0]["id"]
        result = getJsonFileData('api_response_runtime/test_08_ioc_listing_api_runtime.json')
        for val in result["results"]:
            if len(result["results"][val]) != 0:
                values = []
                for item in result["results"][val]:
                    values.append(item["value"])

                dict = {
                    "all": True,
                    "negation": True,
                    "values": values
                }
                payload["content"][val] = dict

        log(payload)

        endpoint = f"/feed-sources/{feed_id}/stix"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the PUT request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.put(f"{url}/{authentication()}", json=payload)
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_09_create_intel_feeds_runtime', response)

        if (response.status_code in [200, 400]) and validate_schema(response, 'conversion/Feed_Sources/RSS_Feed/test_09_create_intel_feeds_schema'):
            log("[PASSED] PUT request is successful")
        else:
            log("[FAILED] PUT request is not successful")
            self.fail()

    def test_10_delete_rss_source(self):
        log("----- Test Case: test_10_delete_rss_source -----")
        result = getJsonFileData('api_response_runtime/test_01_create_rss_feed_runtime.json')
        source_id = result["id"]
        endpoint = f"/feed-sources/rss_feeds/{source_id}"
        url = f"{base_url}{service}{endpoint}"
        log(f'Making the DELETE request for the {url}')
        log("Calling authentication function for getting the unique authenticator")
        response = requests.delete(f"{url}/{authentication()}")
        log(f"response code is : {response.status_code}")
        log(f"Received response is: {json.dumps(json.loads(response.text), indent=4)}")

        save_runtime_response('testdata/api_response_runtime', 'test_10_delete_rss_source_runtime', response)

        if response.status_code == 200 and validate_schema(response, 'conversion/Feed_Sources/RSS_Feed/test_10_delete_rss_source_schema'):
            log("[PASSED] DELETE request is successful")
        else:
            log("[FAILED] DELETE request is not successful")
            self.fail()


if __name__ == '__main__':
    unittest.main(testRunner=reporting())
