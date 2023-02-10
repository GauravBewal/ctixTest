from config.process_config import *
from jira import JIRA

jira = JIRA(basic_auth=('jeet.raikar@cyware.com', 'M9ZmznhAxIZRA17mtrSU5CE0'),
            options={"server": 'https://cyware.atlassian.net/'})
person = "anyone@cyware.com"
emailcontent = ""


def fetch_bugs_in_fixed(person):
    sq_to_be_verified = "project = 'CTIX V3' and status in (Fixed,'QA in Progress') and 'QA Owner[User Picker (single user)]' in ('"+person+"') ORDER BY priority"
    #sq_to_be_verified = "project = 'CTIX V3' AND issuetype = Bug and status = Fixed and 'QA Owner[User Picker (single user)]' in ('"+person+"') ORDER BY priority"
    if person == "depinder.bharti@cyware.com":
        sq_to_be_verified = "project = 'CTIX V3' AND issuetype = Bug and status = Fixed and 'QA Owner[User Picker (single user)]' in (EMPTY, '" + person + "') ORDER BY priority"
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
        summary = buginfo.raw['fields']['summary']
        priority = "P" + buginfo.raw['fields']['priority']['id']
        # print(buginfo.raw['fields']['assignee']['displayName'])
        status = buginfo.raw['fields']['status']['name']
        global emailcontent
        emailcontent += "<tr><td style='border:1px solid black;'><a href='https://cyware.atlassian.net/browse/" + str(
            bugid) + "'>" + str(bugid) + "</a></td><td style='border:1px solid black;'>" + summary + "</td>" \
            "<td style='border:1px solid black;'>" + priority + "</td>" \
            "<td style='border:1px solid black;'>" + status + "</td></tr>"

def add_count_content(name, count):
    global emailcontent
    emailcontent += "<tr><td style='border:1px solid black;'>" + str(
        name) + "</td><td style='border:1px solid black;'>" + str(count) + "</td></tr>"



def write_to_file(filename, emailcontent):
    with open(os.path.join(report_location, filename), "wb+") as writer:
        writer.write(str(emailcontent).encode())


add_heading("Issues in Fixed , Waiting for QA verification")
add_heading("Jeet Raikar")
start_detail_table()
add_detail_content(fetch_bugs_in_fixed("jeet.raikar@cyware.com"))
end_table()

add_heading("Divya Jadhav")
start_detail_table()
add_detail_content(fetch_bugs_in_fixed("divya.jadhav@cyware.com"))
end_table()

add_heading("Gaurav Bewal")
start_detail_table()
add_detail_content(fetch_bugs_in_fixed("gaurav.bewal@cyware.com"))
end_table()

add_heading("Kamakshya Kar")
start_detail_table()
add_detail_content(fetch_bugs_in_fixed("kamakshya@cyware.com"))
end_table()

add_heading("Harsh Shukla")
start_detail_table()
add_detail_content(fetch_bugs_in_fixed("harsh.shukla@cyware.com"))
end_table()

add_heading("Saubhagya Marwaha")
start_detail_table()
add_detail_content(fetch_bugs_in_fixed("saubhagya.marwaha@cyware.com"))
end_table()

add_heading("Ipsita Majhi")
start_detail_table()
add_detail_content(fetch_bugs_in_fixed("ipsita.majhi@cyware.com"))
end_table()

add_heading("Issues missing QA Owner/Re-assingnment - Sudhakar/Divya/Kamakshya")
start_detail_table()
add_detail_content(fetch_bugs_in_fixed("sudhakar.reddy@cyware.com"))
end_table()

write_to_file("jira_query_report_to_qa.html", emailcontent)
