from config.process_config import *
from jira import JIRA

jira = JIRA(basic_auth=('jeet.raikar@cyware.com', 'M9ZmznhAxIZRA17mtrSU5CE0'),
            options={"server": 'https://cyware.atlassian.net/'})
person = "anyone@cyware.com"
emailcontent = ""




sq_1day_issues_worked_upon = "project= 'CTIX V3' AND issuekey IN updatedBy('" + person + "','-1d') ORDER BY priority DESC"




#Count Bugs Created in last 7 days
#Name , BugsCount


# Bug id - Priority - Summary - Assignee - Status


def fetch_count_sq_1day_new_bugs_created(person):
    sq_1day_new_bugs_created = "project = CTX AND created > startOfDay(-1d) and (reporter = '" + person + "') ORDER BY priority DESC"
    all_issues = jira.search_issues(sq_1day_new_bugs_created, maxResults=None)
    return len(all_issues)


def fetch_count_sq_7days_issues_worked_upon(person):
    sq_7days_issues_worked_upon = "project= 'CTIX V3' AND issuekey IN updatedBy('" + person + "','-7d') ORDER BY priority DESC"
    all_issues = jira.search_issues(sq_7days_issues_worked_upon, maxResults=None)
    return len(all_issues)


def fetch_bugs_1day(person):
    #sq_1day = "project = CTX AND updated > startOfDay(-1d) and (reporter = '" + person + "' OR assignee = '" + person + "') ORDER BY priority DESC"
    sq_1day_issues_worked_upon = "project= 'CTIX V3' AND issuekey IN updatedBy('" + person + "','-1d') ORDER BY priority DESC"
    all_issues = jira.search_issues(sq_1day_issues_worked_upon, maxResults=None)
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



add_heading("New Issues [Created] by QA in last 1 day")
start_count_table()
add_count_content("Jeet Raikar", fetch_count_sq_1day_new_bugs_created("jeet.raikar@cyware.com"))
add_count_content("Divya Jadhav", fetch_count_sq_1day_new_bugs_created("divya.jadhav@cyware.com"))
add_count_content("Gaurav Bewal", fetch_count_sq_1day_new_bugs_created("gaurav.bewal@cyware.com"))
add_count_content("Kamakshya", fetch_count_sq_1day_new_bugs_created("kamakshya@cyware.com"))
add_count_content("Harsh Shukla", fetch_count_sq_1day_new_bugs_created("harsh.shukla@cyware.com"))
add_count_content("Saubhagya Marwaha", fetch_count_sq_1day_new_bugs_created("saubhagya.marwaha@cyware.com"))
add_count_content("Ipsita Majhi", fetch_count_sq_1day_new_bugs_created("ipsita.majhi@cyware.com"))
end_table()

add_heading("Issues [Worked Upon] by QA in Last 7 days")
start_count_table()
add_count_content("Jeet Raikar", fetch_count_sq_7days_issues_worked_upon("jeet.raikar@cyware.com"))
add_count_content("Divya Jadhav", fetch_count_sq_7days_issues_worked_upon("divya.jadhav@cyware.com"))
add_count_content("Gaurav Bewal", fetch_count_sq_7days_issues_worked_upon("gaurav.bewal@cyware.com"))
add_count_content("Kamakshya", fetch_count_sq_7days_issues_worked_upon("kamakshya@cyware.com"))
add_count_content("Harsh Shukla", fetch_count_sq_7days_issues_worked_upon("harsh.shukla@cyware.com"))
add_count_content("Saubhagya Marwaha", fetch_count_sq_7days_issues_worked_upon("saubhagya.marwaha@cyware.com"))
add_count_content("Ipsita Majhi", fetch_count_sq_7days_issues_worked_upon("ipsita.majhi@cyware.com"))
end_table()



add_heading("Detailed:- Issues Worked Upon by QA in Last 1 day")
add_heading("Jeet Raikar")
start_detail_table()
add_detail_content(fetch_bugs_1day("jeet.raikar@cyware.com"))
end_table()

add_heading("Divya Jadhav")
start_detail_table()
add_detail_content(fetch_bugs_1day("divya.jadhav@cyware.com"))
end_table()

add_heading("Gaurav Bewal")
start_detail_table()
add_detail_content(fetch_bugs_1day("gaurav.bewal@cyware.com"))
end_table()

add_heading("Kamakshya Kar")
start_detail_table()
add_detail_content(fetch_bugs_1day("kamakshya@cyware.com"))
end_table()

add_heading("Harsh Shukla")
start_detail_table()
add_detail_content(fetch_bugs_1day("harsh.shukla@cyware.com"))
end_table()

add_heading("Saubhagya Marwaha")
start_detail_table()
add_detail_content(fetch_bugs_1day("saubhagya.marwaha@cyware.com"))
end_table()

add_heading("Ipsita Majhi")
start_detail_table()
add_detail_content(fetch_bugs_1day("ipsita.majhi@cyware.com"))
end_table()











write_to_file("email_jira.html", emailcontent)



#sq_1day_new_bugs_created = "project = CTX AND created > startOfDay(-1d) and (reporter = '" + person + "' OR assignee = '" + person + "') ORDER BY priority DESC"

#search_query = "project = 'CTIX V3' AND issuetype = Bug AND status not in (Resolved, Closed, 'Fixed in QA', 'Fixed in Dev', 'Fixed in Prod', 'Fixed in Demo', 'Not a Bug') AND resolution = Unresolved AND priority = 'P1 - Critical' ORDER BY assignee ASC"


#sq_1day = "project = CTX AND updated > startOfDay(-1d) and (reporter = '" + person + "' OR assignee = '" + person + "') ORDER BY priority DESC"
#sq_7days = "project = CTX AND updated > startOfDay(-7d) and (reporter = '" + person + "' OR assignee = '" + person + "') ORDER BY priority DESC"


# print(str(issue['fields']['description']))
# if str(issue.fields.status) == 'Done' or str(issue.fields.status) == 'Closed':
#        print(issue)

# for x in issues:
#    print(str(x['fields']['description']))

# project = jira.projects()

# for project in projects:
#    issues = jira.search_issues('project=JA')



# issue = jira.issue("CTX-1111")
# print(str(issue.raw['fields']['description'] ))