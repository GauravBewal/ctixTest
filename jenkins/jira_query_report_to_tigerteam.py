from config.process_config import *
from jira import JIRA

jira = JIRA(basic_auth=('jeet.raikar@cyware.com', 'M9ZmznhAxIZRA17mtrSU5CE0'),
            options={"server": 'https://cyware.atlassian.net/'})
person = "anyone@cyware.com"
emailcontent = ""


def fetch_bugs_for_qa():
    sq_to_be_verified = "labels = POC_Bug and status in (Fixed, 'QA in Progress') ORDER BY priority"
    all_issues = jira.search_issues(sq_to_be_verified, maxResults=None)
    return all_issues

def fetch_bugs_for_dev():
    sq_to_be_verified = "labels = POC_Bug and status not in (Closed,Fixed, 'QA in Progress', 'QA Cleared in QA') ORDER BY priority"
    all_issues = jira.search_issues(sq_to_be_verified, maxResults=None)
    return all_issues


def add_heading(heading):
    global emailcontent
    emailcontent += "<b>" + heading + "</b><Br>"


def start_detail_table():
    global emailcontent
    emailcontent += "<table style='border:1px solid black;width: 100%;border-collapse: collapse;'><tr>" \
                    "<th style='border:1px solid black;'>Bug ID</th>" \
                    "<th style='border:1px solid black;'>Summary</th>" \
                    "<th style='border:1px solid black;'>Priority</th>" \
                    "<th style='border:1px solid black;'>Assignee</th>" \
                    "<th style='border:1px solid black;'>QA</th>" \
                    "<th style='border:1px solid black;'>Status</th></tr>"

def start_count_table():
    global emailcontent
    emailcontent += "<table style='border:1px solid black;width: 100%;border-collapse: collapse;'><tr>" \
                    "<th style='border:1px solid black;'>Name</th>" \
                    "<th style='border:1px solid black;'>Count</th></tr>"

def end_table():
    global emailcontent
    emailcontent += "</table><Br><Br>"



def add_detail_content(all_issues):
    for bugid in all_issues:
        buginfo = jira.issue(bugid)
        #print(str(buginfo.raw))
        summary = buginfo.raw['fields']['summary']
        priority = "P" + buginfo.raw['fields']['priority']['id']
        assignee = str(buginfo.raw['fields']['assignee']['displayName'])
        if buginfo.raw['fields']['customfield_10172'] is not None:
            qa = str("" + buginfo.raw['fields']['customfield_10172']['displayName'])
        else:
            qa = "-"
        # print(buginfo.raw['fields']['assignee']['displayName'])
        status = buginfo.raw['fields']['status']['name']
        global emailcontent
        emailcontent += "<tr><td style='border:1px solid black;'><a href='https://cyware.atlassian.net/browse/" + str(
            bugid) + "'>" + str(bugid) + "</a></td><td style='border:1px solid black;'>" + summary + "</td>" \
            "<td style='border:1px solid black;'>" + priority + "</td>" \
            "<td style='border:1px solid black;'>" + assignee + "</td>" \
            "<td style='border:1px solid black;'>" + qa + "</td>" \
            "<td style='border:1px solid black;'>" + status + "</td></tr>"

def add_count_content(name, count):
    global emailcontent
    emailcontent += "<tr><td style='border:1px solid black;'>" + str(
        name) + "</td><td style='border:1px solid black;'>" + str(count) + "</td></tr>"



def write_to_file(filename, emailcontent):
    with open(os.path.join(report_location, filename), "wb+") as writer:
        writer.write(str(emailcontent).encode())


add_heading("Pending with Dev/PM")
start_detail_table()
add_detail_content(fetch_bugs_for_dev())
end_table()
add_heading("Pending with QA")
start_detail_table()
add_detail_content(fetch_bugs_for_qa())
end_table()


write_to_file("jira_query_report_to_tigerteam.html", emailcontent)