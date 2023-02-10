import requests
from lib.api.common_utilities import *
import lib.ui.integration_management as c
from testdata.feeds import *

mattermost_header = {"Authorization": "Bearer rui9a5bfhi8dfe8xyhwsxsyq5e", "Content-Type": "application/json"}


def get_ref_set_data_qradar(set_name):
    """
        Function to get data in reference set of QRADAR
        params:
            set_name: Name of the reference set whose data is to be fetched
    """
    endpoint = f'api/reference_data/sets/{set_name}'
    url = f"{c.QRADAR_URL}{endpoint}"
    headers = {"MIME_Type": "application/json"}
    print(f'Making the get request for the {c.QRADAR_URL}')
    response = requests.get(url=url, headers=headers, auth=(c.QRADAR_USERNAME, c.QRADAR_PASSWORD), verify=False)
    print("qradar - ", response.text)
    return response


def create_ref_set_qradar(set_name):
    """
        Function to create ref set in QRADAR
        params:
            set_name: Name of the reference set to be created
    """
    endpoint = f"api/reference_data/sets"
    url = f"{c.QRADAR_URL}{endpoint}"
    headers = {"MIME_Type": "application/json"}
    params = {"name": set_name, "element_type": "ALN"}
    print(url)
    response = requests.post(url=url, params=params, headers=headers, auth=(c.QRADAR_USERNAME, c.QRADAR_PASSWORD),
                             verify=False)
    print(response.text)
    return response


def delete_ref_set_qradar(set_name, purge="false"):
    """
        Function to delete reference set in QRADAR
        params:
            set_name: Name of the reference set to be deleted
    """
    endpoint = f"api/reference_data/sets/{set_name}"
    url = f"{c.QRADAR_URL}{endpoint}"
    headers = {"MIME_Type": "application/json"}
    params = {"purge_only": purge}
    response = requests.delete(url=url, headers=headers, params=params, auth=(c.QRADAR_USERNAME, c.QRADAR_PASSWORD),
                             verify=False)
    if response.json()["status"] == "QUEUED":
        print(f"Reference Set {set_name} is now deleted successfully")


def search_data_in_qradar(set_name, intel_list):
    """
        Function to search for required intel in reference set
        params:
            set_name: Name of the reference set in QRadar
            intel: IOC that is to be searched for in the reference set
    """
    count = 0
    response = get_ref_set_data_qradar(set_name)
    _all_data = [i["value"] for i in response.json()["data"]]
    for i in intel_list:
        if i in _all_data:
            count += 1
            print(f"Found {i} in reference set")
    if count == len(intel_list):
        return True
    return False


def get_all_channels():
    """
        Function to get a list of all channels on mattermost
    """
    header = mattermost_header
    response = requests.get(url='https://mattermost.mycyware.com/api/v4/channels', headers=header)
    print(response.json())


def get_all_teams():
    """
        Function to get list of all teams
    """
    header = mattermost_header
    response = requests.get(url='https://mattermost.mycyware.com/api/v4/teams', headers=header)
    print(response.json())


def get_team_id(team_name):
    """
        Function to get the id of team based on team name
        params:
            team_name: name of the team to be searched
        returns:
            team_id: id of the team provided
    """
    header = mattermost_header
    response = requests.get(url=f'https://mattermost.mycyware.com/api/v4/teams/name/{team_name}', headers=header)
    return response.json()["id"]


def get_channel_id(team_id, channel_name):
    """
        Function to get channel id of the provided channel
        params:
            team_id: id of the team to access channel
            channel_name: Name of the channel whose id is to be received
        returns:
            channel_id: Id of the channel queried for
    """
    header = mattermost_header
    response = requests.get(url=f'https://mattermost.mycyware.com/api/v4/teams/{team_id}/channels/name/{channel_name}',
                            headers=header)
    print("Channel id is - " + response.json()["id"])
    return response.json()["id"]


def create_public_channel(team_name, channel_name):
    """
        Function to create a new public channel in mattermost
        params:
            channel_name: Name of the channel to be created
    """
    team_id = get_team_id(team_name)
    body = {
        "team_id": team_id,
        "name": channel_name,
        "display_name": channel_name,
        "type": "O",
        "permanant": "true"
    }
    header = mattermost_header
    response = requests.post(url='https://mattermost.mycyware.com/api/v4/channels', headers=header, json=body)
    print(response.json())
    print(response.status_code)


def delete_public_channel(team_name, channel_name):
    """
        Function to delete a channel from mattermost
        params:
            channel_name: Name of the channel to be deleted
    """
    team_id = get_team_id(team_name=team_name)
    channel_id = get_channel_id(team_id=team_id, channel_name=channel_name)
    header = mattermost_header
    response = requests.delete(url=f'https://mattermost.mycyware.com/api/v4/channels/{channel_id}', headers=header)
    print(response.json())
    print(response.status_code)


def create_outgoing_webhook(team_name, channel_name, webhook_url):
    """
        Function to create a new outgoing webhook in mattermost
        params:
            channel_name: Name of the channel to be linked to webhook
            webhook_url: URL to be linked with the outgoing webhook
        returns:
            token: Token to be used to add a webhook in CTIX
    """
    team_id = get_team_id(team_name)
    channel_id = get_channel_id(team_id=team_id, channel_name=channel_name)
    body = {
        "team_id": team_id,
        "channel_id": channel_id,
        "trigger_words": [],
        "trigger_when": 1,
        "callback_urls": [webhook_url.strip()],
        "display_name": f"hook_{channel_name}",
        "content_type": "application/json"
    }
    header = mattermost_header
    response = requests.post(url="https://mattermost.mycyware.com/api/v4/hooks/outgoing", headers=header, json=body)
    print(response.json())
    print(response.status_code)
    return response.json()["token"], response.json()["id"]


def delete_outgoing_webhook(webhook_name):
    """
        Function to delete a created outgoing webhook
        params:
            webhook_name: Name of the webhook to be deleted
    """
    hook_id = get_webhook_id(webhook_name=webhook_name)
    print(f"Deleting outgoing webhook {webhook_name}")
    header = mattermost_header
    response = requests.delete(url=f"https://mattermost.mycyware.com/api/v4/hooks/outgoing/{hook_id}", headers=header)
    print(response.status_code)


def get_webhook_id(webhook_name):
    """
        Function to get the id of the webhook of the provided name
        params:
            webhook_name: Name of the outgoing webhook
        returns:
            webhook_id: id of the created webhook
    """
    header = mattermost_header
    response = requests.get(url="https://mattermost.mycyware.com/api/v4/hooks/outgoing", headers=header)
    for i in response.json():
        if i["display_name"] == webhook_name:
            return i["id"]
    return None


def create_post_in_channel(team_name, channel_name, post_content):
    """
        Function to send a post to a channel in mattermost
        params:
            team_name: name pf the team of the user
            channel_name: Name of the channel where the post is to be sent
            post_content: content that is to be sent to the channel
    """
    team_id = get_team_id(team_name)
    channel_id = get_channel_id(team_id=team_id, channel_name=channel_name)
    header = mattermost_header
    body = {'channel_id': channel_id, "message": post_content}
    response = requests.post("https://mattermost.mycyware.com/api/v4/posts", headers=header, json=body)
    print(response.json())
