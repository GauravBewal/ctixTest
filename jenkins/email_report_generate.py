from config.process_config import *
import matplotlib.pyplot as plotter
import glob
import xml.etree.ElementTree as et
import datetime
import re
import pandas as pd
from jira import JIRA
import datetime
begin_time = datetime.datetime.now()


def deduce_reason(message):
    print("Message - "+message)
    if str(message).__contains__("Browser Console Debug Logs"):
        return "  Error in the Browser Console"
    elif str(message).__contains__("not found") or str(message).__contains__("Unable to locate element"):
        return "  Expected element is not found"
    elif str(message).__contains__("could not be scrolled into view"):
        return "  Element is not interactable"
    elif str(message).__contains__("obscures it"):
        return "  Element is overlapped by another element"
    elif str(message).__contains__("No Alert Found"):
        return "  No Alert Found"
    elif str(message).__contains__("False is not true"):
        return "  Assertion Failed"
    else:
        return ""


def find_known_issue(testname, xmlpath):
    try:
        file1 = open(xmlpath, "r")
        readfile = file1.read()
        testid = re.findall(testname + '::\d+', readfile)
        if len(testid) > 0:
            testid = int(testid[0].replace(testname + '::', ''))
        else:
            testid = 0
        known_failures = os.path.join(os.environ["PYTHONPATH"], "jenkins", "known_failures.csv")
        df = pd.read_csv(known_failures)  # skiprows = [1
        comment = ""
        for index, row in df.iterrows():
            if row[0] == testid:
                comment = row[1]
                break  # break with the first reason itself.
        return comment
    except Exception as z:
        return ""


def reg_find_id(input):
    testid = re.findall(r'-?\\-?\d+\.?\d*', input)
    if len(testid) > 0:
        testid = testid[0]
    else:
        testid = 0
    return testid


def find_between(start, end, filepath=None, data=None):
    try:
        startindex = -1
        endindex = -1
        readfile = ""
        if filepath is None:
            readfile = data
        else:
            file1 = open(filepath, "r")
            readfile = file1.read()
        startindex = readfile.index(start) + len(start)
        print("startindex:" + str(startindex))
        if startindex != -1:
            endindex = readfile.index(end, startindex)
            print("endindex:" + str(endindex))
        if endindex != -1:
            return readfile[startindex:endindex]
        else:
            return ""
    except Exception as z:
        return ""

# ### Last 10 Critical Bugs ######


def add_last_10_issues():
    try:
        global last10_issues
        last10_issues += "<table style='border:1px solid black;width: 100%;border-collapse: collapse;'><tr style=\"background: #E6E6FA;font-family: sans-serif;\">" \
                        "<th style='border:1px solid #ccc;'>Bug ID</th>" \
                        "<th style='border:1px solid #ccc;'>Summary</th>" \
                        "<th style='border:1px solid #ccc;'>Status</th></tr>"
        all_issues = jira.search_issues(
            "project = 'CTIX V3' AND issuetype = Bug AND status not in (Closed, Fixed) and priority = 'P1 - Critical' ORDER BY created DESC",
            maxResults=10)

        for bugid in all_issues:
            buginfo = jira.issue(bugid)
            summary = buginfo.raw['fields']['summary']
            priority = "P" + buginfo.raw['fields']['priority']['id']
            # print(buginfo.raw['fields']['assignee']['displayName'])
            status = buginfo.raw['fields']['status']['name']
            last10_issues += "<tr><td style='border:1px solid #ccc;'>" + '<a href="https://cyware.atlassian.net/browse/' + str(bugid) + '" target="_blank"' + ">" + str(
                bugid) + "</a>" + "</td><td style='border:1px solid #ccc;'>" + summary + "</td>" \
              "<td style='border:1px solid black;'>" + status + "</td></tr>"
        last10_issues += "</table><Br><Br>"
    except Exception as e:
        print("Error: Some issue occurred while querying Jira last 10 issues:" + str(e))


#################################


def add_jira_stats():
    global emailcontent
    open_issues = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = Open", maxResults=None, fields='key')
    open_issues_c = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = Open AND priority = 'P1 - Critical'", maxResults=None, fields='key')
    open_issues_h = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = Open AND priority = 'P2 - High'", maxResults=None, fields='key')
    open_issues_m = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = Open AND priority = 'P3 - Medium'", maxResults=None, fields='key')

    inprogress_issues = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = 'In Progress'", maxResults=None, fields='key')
    inprogress_issues_c = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = 'In Progress' AND priority = 'P1 - Critical'",
                                           maxResults=None, fields='key')
    inprogress_issues_h = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = 'In Progress' AND priority = 'P2 - High'",
                                           maxResults=None, fields='key')
    inprogress_issues_m = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = 'In Progress' AND priority = 'P3 - Medium'",
                                           maxResults=None, fields='key')
    reopened_issues = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = 'Reopened'",
                                         maxResults=None, fields='key')
    reopened_issues_c = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = 'Reopened' AND priority = 'P1 - Critical'",
                                         maxResults=None, fields='key')
    reopened_issues_h = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = 'Reopened' AND priority = 'P2 - High'",
                                         maxResults=None, fields='key')
    reopened_issues_m = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = 'Reopened' AND priority = 'P3 - Medium'",
                                         maxResults=None, fields='key')
    fixed_issues = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = 'Fixed'", maxResults=None)
    fixed_issues_c = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = 'Fixed' AND priority = 'P1 - Critical'", maxResults=None, fields='key')
    fixed_issues_h = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = 'Fixed' AND priority = 'P2 - High'", maxResults=None, fields='key')
    fixed_issues_m = jira.search_issues("project= 'CTIX V3' AND issuetype = Bug AND status = 'Fixed' AND priority = 'P3 - Medium'", maxResults=None, fields='key')
    resolved7days_issues = jira.search_issues("project = 'CTIX V3' AND type =Bug AND  resolved> startOfDay(-7d)",
                                         maxResults=None, fields='key')
    resolved7days_issues_c = jira.search_issues("project = 'CTIX V3' AND type =Bug AND  resolved> startOfDay(-7d) AND priority = 'P1 - Critical'",
                                              maxResults=None, fields='key')
    resolved7days_issues_h = jira.search_issues("project = 'CTIX V3' AND type =Bug AND  resolved> startOfDay(-7d) AND priority = 'P2 - High'",
                                              maxResults=None, fields='key')
    resolved7days_issues_m = jira.search_issues("project = 'CTIX V3' AND type =Bug AND  resolved> startOfDay(-7d) AND priority = 'P3 - Medium'",
                                              maxResults=None, fields='key')
    created7days_issues = jira.search_issues("project = 'CTIX V3' AND type =Bug AND  created> startOfDay(-7d)",
                                              maxResults=None, fields='key')
    created7days_issues_c = jira.search_issues("project = 'CTIX V3' AND type =Bug AND  created> startOfDay(-7d) AND priority = 'P1 - Critical'",
                                             maxResults=None, fields='key')
    created7days_issues_h = jira.search_issues("project = 'CTIX V3' AND type =Bug AND  created> startOfDay(-7d) AND priority = 'P2 - High'",
                                             maxResults=None, fields='key')
    created7days_issues_m = jira.search_issues("project = 'CTIX V3' AND type =Bug AND  created> startOfDay(-7d) AND priority = 'P3 - Medium'",
                                             maxResults=None, fields='key')

    emailcontent += "" \
    "<span style=\"font-size:22px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;\">Jira Stats </span>" \
    "<div style='height:10px'></div>" \
    "<table width='800' style=\"font-family: sans-serif; font-weight: bold; table-layout: fixed\">" \
    "<tr style=\"font-size:34px;color:#ef867c;text-align: center;background: #F0FFF0;\"><td>" + str(len(open_issues)) + "</td><td>" + str(len(inprogress_issues)) + "</td><td>" + str(len(reopened_issues)) + "</td><td>" + str(len(fixed_issues)) + "</td></tr>" \
    "<tr style=\"font-size:15px;color:#5F9EA0;text-align: center;background: #F0FFF0;\"><td>C:" + str(
        len(open_issues_c)) + ", H:" + str(len(open_issues_h)) + ", M:" + str(len(open_issues_m)) + "</td><td>C:" + str(
        len(inprogress_issues_c)) + ", H:" + str(len(inprogress_issues_h)) + ", M:" + str(len(inprogress_issues_m)) + "</td><td>C:" + str(
        len(reopened_issues_c)) + ", H:" + str(len(reopened_issues_h)) + ", M:" + str(len(reopened_issues_m)) + "</td><td>C:" + str(
        len(fixed_issues_c)) + ", H:" + str(len(fixed_issues_h)) + ", M:" + str(len(fixed_issues_m)) + "</td></tr>" \
    "<tr style=\"font-size:17px;color:#000000;text-align: center;background: #F0FAA0;\"><td >Open</td><td>In Progress</td><td>Reopened</td><td>Fixed</td></tr>" \
    "</table><div style='height:20px'></div>" \
    "<table width='800' style=\"font-family: sans-serif; font-weight: bold; table-layout: fixed\">" \
    "<tr style=\"font-size:34px;;color:#ef867c;text-align: center;background: #F0FFF0;\"><td>" + str(len(resolved7days_issues)) + "</td><td>" + str(len(created7days_issues)) + "</td></tr>" \
    "<tr style=\"font-size:15px;color:#5F9EA0;text-align: center;background: #F0FFF0;\"><td>C:" + str(
        len(resolved7days_issues_c)) + ", H:" + str(len(resolved7days_issues_h)) + ", M:" + str(len(resolved7days_issues_m)) + "</td><td>C:" + str(
        len(created7days_issues_c)) + ", H:" + str(len(created7days_issues_h)) + ", M:" + str(
        len(created7days_issues_m)) + "</td></tr>" \
    "<tr style=\"font-size:17px;color:#000000;text-align: center;background: #F0FAA0;\"><td >Bugs resolved in last 7 days</td><td>New Bugs created in last 7 days</td></tr>" \
    "</table><Br><Br>"


def add_sanity_report():
    global emailcontent
    emailcontent += '<b>Download SANITY REPORT : </b> ' +f"https://jenkins.cyware.com/view/CTIX_TESTS/job/{jenkins_job_name}/lastSuccessfulBuild/artifact/reports/sanity.docx" + '<br><br>'


print("Generating Results from XML reports")
jira = JIRA(basic_auth=('jeet.raikar@cyware.com', 'M9ZmznhAxIZRA17mtrSU5CE0'),
            options={"server": 'https://cyware.atlassian.net/'})
person = "anyone@cyware.com"
emailcontent = ""
last10_issues = ''

add_last_10_issues()

passed_table = "<b><u>Passed</u></b><table style='border:1px solid black;width: 100%;border-collapse: collapse;'><tr>" \
               "<th style='border:1px solid black;'>Module</th><th style='border:1px solid black;'>Unit Test</th>" \
               "<th style='border:1px solid black;'>Status</th></tr>"

failed_table = "<b><u>Failed</u></b><table style='border:1px solid black;width: 100%;border-collapse: collapse;'><tr>" \
               "<th style='border:1px solid black;'>Module</th><th style='border:1px solid black;'>Failed Unit Test</th>" \
               "<th style='border:1px solid black;'>Status</th><th style='border:1px solid black;'>Comments</th><th style='border:1px solid black;'>Author</th></tr>"

#single_table = "<table style='border:1px solid black;width: 100%;border-collapse: collapse;'><tr>" \
#               "<th style='border:1px solid black;'>Module</th><th style='border:1px solid black;'>Unit Test</th>" \
#               "<th style='border:1px solid black;'>Status</th><th style='border:1px solid black;'>Comments</th><th style='border:1px solid black;'>Author</th></tr>"


single_table = "<span style=\"font-size:22px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;\">Automation Execution</span>" \
"<div style='height:10px'></div>" \
"<table style=\"border:5px solid #F0FAA0;font-family: sans-serif; font-weight: bold\">" \
"<tr>" \
"<td style='width:25%; border:5px solid #F0FAA0;'><img style='width:100%; height: 100%' src='cid:results.png' /></td>" \
"<td style='width:75%; vertical-align: top;'><div style='text-align: center;'>Last 10 Critical issues</div>" + str(last10_issues) + "</td>" \
"</tr>" \
"</table><Br>" \
"<table style='width: 100%;border-collapse: collapse;'>" \
"<tr style='background: #E6E6FA;font-family: sans-serif;'><th style='border:1px solid #ccc;'>Module</th><th style='border:1px solid #ccc;'>Unit Test</th><th style='border:1px solid #ccc;'>Status</th><th style='border:1px solid #ccc;'>Comments</th><th style='border:1px solid #ccc;'>POC</th></tr>" \

if report_format == "xml":

    try:
        if testplan == 'prodsanity.txt':
            add_sanity_report()
        else:
            add_jira_stats()
    except Exception as e:
        print("Error: Some issue occurred while querying Jira:" + str(e))

    try:
        total_cases = 0
        failed = 0
        executiontime = 0
        xmlpaths = glob.glob(os.path.join(report_location, "*.xml"))
        for xmlpath in xmlpaths:
            tree = et.parse(xmlpath)
            for x in tree.getroot().attrib:
                if x == "errors" or x == "failures":
                    failed = int(failed) + int(tree.getroot().attrib[x])
                elif x == "tests":
                    total_cases = int(total_cases) + int(tree.getroot().attrib[x])
                elif x == "time":
                    executiontime = float(executiontime) + float(tree.getroot().attrib[x])

            for y in tree.findall('testcase'):
                testfailed = False
                for z in y.findall('error'):
                    testfailed = True
                    info_line = find_between("*** " + str(y.attrib['name']), "***", filepath=xmlpath)
                    #print("info line: " + info_line)
                    #print(find_between("::author::", "::", data=info_line))
                    single_table = single_table + \
                    "<tr>" \
                    "<td style='border:1px solid #ccc;'>" + str(y.attrib['classname']) + "</td>" \
                    "<td style='border:1px solid #ccc;'>" + str(y.attrib['name']) + "</td>" \
                    "<td style='border:1px solid #ccc; color:#ff0000;'> Failed </td>" \
                    "<td style='border:1px solid #ccc;'>"
                    temp = find_known_issue(str(y.attrib['name']), xmlpath)
                    strtemp = ""
                    if len(temp) > 0:
                        if temp.__contains__("CTX") or temp.__contains__("CV") or temp.__contains__("DEVOP"):
                            temp = temp.replace(",", "")
                            bugs = temp.split()
                            strtemp = strtemp + bugs[0] + " " + bugs[1]
                            for i in range(2, len(bugs)):
                                strtemp = strtemp + " " + '<a href="https://cyware.atlassian.net/browse/' + bugs[i] + '" target="_blank">' + bugs[i] + "</a>"
                        else :
                            strtemp = strtemp + temp

                    single_table = single_table + \
                    strtemp + deduce_reason(str(z.attrib['message'])) + "</td>" \
                    "<td style='border:1px solid #ccc;'>" + find_between("::author::", "::", data=info_line) + "</td>" \
                    "</tr>"
                    print("Test Suite:" + str(y.attrib['classname']) + " - Failed Test: " + str(y.attrib['name']))
                    # print(str(z.attrib['type']))
                if not testfailed:
                    single_table = single_table + \
                    "<tr>" \
                    "<td style='border:1px solid #ccc;'>" + str(y.attrib['classname']) + "</td>" \
                    "<td style='border:1px solid #ccc;'>" + str(y.attrib['name']) + "</td>" \
                    "<td style='border:1px solid #ccc; color:#008000;'> Passed </td>" \
                    "<td style='border:1px solid #ccc;'></td>" \
                    "<td style='border:1px solid #ccc;'></td>" \
                    "</tr>"
                    print("Test Suite:" + str(y.attrib['classname']) + " - Passed Test: " + str(y.attrib['name']))
        #ofailed_table = failed_table + "</table>"
        #opassed_table = passed_table + "</table><br>"
        single_table = single_table + "</table><br>"
        # print(failed)
        # print(total_cases)
        # print(executiontime)
        pieLabels = 'Pass', 'Fail'
        populationShare = [total_cases - failed, failed]
        figureObject, axesObject = plotter.subplots()
        axesObject.pie(populationShare, labels=pieLabels, autopct='%1.2f', startangle=90,textprops={'fontsize': 16, 'color': 'black'}, colors=['#65eb67', '#eb6565'])
        plotter.title("Failed vs Passed", fontsize='16', fontweight='bold', pad=14)
        axesObject.axis('equal')
        plotter.savefig(os.path.join(report_location, "results.png"))
        # Write html report file
        with open(os.path.join(report_location, "email_report.html"), "wb+") as writer:
            # writer.write(('<h3 style="padding:0 0 6px 0;margin:0;font-family:Arial,
            # Sans-serif;font-size:16px;font-weight:bold;color:#222"><span>Quality Management Report -
            # CTIX:</span></h3>').encode())
            writer.write(
                ('<b>Date: </b> ' + str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) + "<br>").encode())
            writer.write(('<b>TestPlan: </b> ' + str(testplan) + "<br>").encode())
            writer.write(('<b>Build ID: </b><br>').encode())
            writer.write(('<b>URL:</b> ' + str(APP_URL) + "<br><br>").encode())
            writer.write(('<b>Execution Time:</b> ' + str(int(executiontime)) + " sec <br>").encode())
            writer.write(('<b>Total Cases:</b> ' + str(total_cases) + "<br>").encode())
            writer.write(('<b>Passed:</b> ' + str(total_cases - failed) + "<br>").encode())
            writer.write(('<b>Failed:</b> ' + str(failed) + "<br><br>").encode())
            writer.write(emailcontent.encode())
            writer.write(single_table.encode())
            #writer.write(passed_table.encode())
            #if failed > 0:
            #    writer.write(failed_table.encode())
    except Exception as e:
        print("Error: Some issue occurred while preparing email report, details:" + str(e))

print(datetime.datetime.now() - begin_time)