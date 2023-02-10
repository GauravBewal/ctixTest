# This file contains all the details about API Automation.

* ### Nomenclature:

    * ##### For the module names:
        {test}_{Service}_{SubService} (Title can be decided from the api docs.Services and SubServices should be in upper camel case)
        Example for Module : "test_Service_SubService"

    * ##### For the class names:
        {Service}{SubService} (In Upper camel case)
        Example for class name: "IntegrationServicesAction"

    * ##### For unittest names:
        {test}_{priority}_{validate_status_code/validate_response}_{request name}. (Request name can be decided from the api docs.)
        Example for unittest name validating status code: "test_01_validate_status_code_action_configs"

* ### Authentication:
    * ##### Mandatory parameters in CTIX API calls:
        * For any API URL request made to the CTIX application, you must include three mandatory parameters Access ID, Expires, and Signature.
        * Access ID - Access ID is available to you when you generate API credentials from the CTIX application.
        * Expires - Expires indicates when this request expires. Use the below formula to make expires. You can give a margin of 10-15 sec for expiry.
        * expires = current time + 10 sec

        * Signature - Create a signature from Access ID, Secret Key, and Expired Time using the following formula. You can get the access ID and the secret key when you generate API credentials from the CTIX application.
        * StringToSign = access_id + \n + expires

        * Signature = Base64(HMAC-SHA1(secret_key, UTF-8-Encoding-Of(StringToSign)))

        * Base URL - A base URL (base_url) is the consistent part of your web address for the CTIX application. https://example.com/ctixapi/ is an example of a Base URL.

    * "creds.py" file is used to get the credentials. "generate_credentials_for_api" can be used for generating credentials.

* ### Important directories:

    1. ##### testdata/api_response: 
        This contains the fixed api response so that when a new call is made to an api we can validate the response

    2. ##### testdata/api_response_runtime:  
        This contains latest response of the api call. This helps in getting realtime id and other attributes which changes during deployment.

    3. ##### lib/api/common_utilities.py: 
         This contains functions for most frequently use operations like comparing response, generating signatures etc

    4. ##### PROJECTS/API: 
        This contains all the module which have the test cases.
        This also contains readme.md file

    5. ##### testdata/api_payload: 
        This contains the payload data which is required while making put, post requests.


* ### Email Report :

    * ##### jenkins/email_report_generate_api.py : File that generates the email report for api-cases.

    * ##### Table in email report contains following columns:
        * Module (class name)
        * Unit Test ( test case name, Red color represents that case is failed and green represents that case is passed)
        * Endpoint (endpoint to which request is to be made)
        * Service (backend services which is responsible for particular endpoint)
        * REQ. Type (e-g GET, PUT, POST etc)

    * ##### Attachments:
       * Pie chart ( Passed vs Failed)
       * Bar graph ( Graph:Total vs Failed vs Pass requests)