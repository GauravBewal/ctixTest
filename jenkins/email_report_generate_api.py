import json
import re
import matplotlib.patches as mpatches
from config.process_config import *
import matplotlib.pyplot as plotter
import glob
import xml.etree.ElementTree as et
import datetime
import re
import pandas as pd
import numpy as np
from jira import JIRA
import datetime
begin_time = datetime.datetime.now()


def deduce_reason(message):
    if str(message).__contains__("Browser Console Debug Logs"):
        return ",Error in Browser Console"
    elif str(message).__contains__("Element name with value"):
        return ",Element not found"
    else:
        return ""

def get_color(method_type):
    if method_type == "GET":
        return "#5bb1fc"
    if method_type == "PUT":
        return "#f59753"
    if method_type == "POST":
        return "#b3b31d"
    if method_type == 'DELETE':
        return "#be6cf5"

def update_count(method_type, total, pass_or_fail):
    if method_type == "GET":
        total[0] = total[0] + 1
        pass_or_fail[0] = pass_or_fail[0] + 1
    if method_type == "POST":
        total[1] = total[1] + 1
        pass_or_fail[1] = pass_or_fail[1] + 1
    if method_type == "PUT":
        total[2] = total[2] + 1
        pass_or_fail[2] = pass_or_fail[2] + 1
    if method_type == 'DELETE':
        total[3] = total[3] + 1
        pass_or_fail[3] = pass_or_fail[3] + 1

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

# commenting this one, have some gmail restriction
# single_table = "<style>.tooltiptext {visibility: hidden;background-color: black;color: #fff;text-align: center;border-radius: 6px;padding: 5px 0;position: absolute;z-index: 1;}.tooltip:hover .tooltiptext {visibility: visible;}</style>"
single_table = "<span style=\"font-size:22px;font-family: 'Montserrat', 'Trebuchet MS', 'Lucida Grande', 'Lucida Sans Unicode', 'Lucida Sans', Tahoma, sans-serif;\">Automation Execution</span>" \
"<div style='height:10px'></div>" \
"<table style=\"border:5px solid #F0FAA0;font-family: sans-serif; font-weight: bold\">" \
"<tr>" \
"<td style='width:25%; border:5px solid #F0FAA0;'><img style='width:100%; height: 100%' src='cid:results.png' /></td>" \
"<td style='width:75%; vertical-align: top;'><div style='text-align: center;'>Last 10 Critical issues</div>" + str(last10_issues) + "</td>" \
"</tr>" \
"</table><Br>" \
"<table style='width: 100%;border-collapse: collapse;'>" \
"<tr style='background: #000000;font-family: sans-serif; color:#ffffff'><th style='border:1px solid #cff800;'>Module</th><th style='border:1px solid #cff800;'>Unit Test</th><th style='border:1px solid #cff800;'>Endpoint</th><th style='border:1px solid #cff800;'>Service</th><th style='border:1px solid #cff800;'>REQ. Type</th><th style='border:1px solid #cff800;'>Status Code</th></tr>" \

if report_format == "xml":

    try:
        add_jira_stats()
    except Exception as e:
        print("Error: Some issue occurred while querying Jira:" + str(e))

    try:
        # this list contain the total request of get, post, put, delete respectively
        total = [0, 0, 0, 0]
        # this list contain the total pass of get, post, put, delete respectively
        success = [0, 0, 0, 0]
        # this list contain the total fail request of get, post, put, delete respectively
        fail = [0, 0, 0, 0]

        total_cases = 0
        failed = 0
        executiontime = 0
        xmlpaths = glob.glob(os.path.join(report_location, "*.xml"))
        xmlpaths.sort()
        file_name = os.path.join(os.environ["PYTHONPATH"], "jenkins", "test_case_vs_endpoint_mapping.json")
        f = open(file_name)
        # This will load json file as a dict object
        data = json.load(f)
        f.close()
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
                endpoint = ""
                service = ""
                color = "white"
                req_type = ""
                try:
                    endpoint = str(data[str(y.attrib['classname'])][str(y.attrib['name'])]['endpoint'])
                    service = str(data[str(y.attrib['classname'])][str(y.attrib['name'])]['service'])
                    req_type = str(data[str(y.attrib['classname'])][str(y.attrib['name'])]['request_type'])
                    color = get_color(str(data[str(y.attrib['classname'])][str(y.attrib['name'])]['request_type']))
                except Exception as e:
                    endpoint = ""
                    service = ""

                status_code = ""
                if endpoint != "":
                    try:
                        regex = re.compile(r'((response code is : )|(Response code is )|(response code is )|(response code is))\d\d\d')
                        # print(str(tree.find('system-out').text))
                        mo = regex.search(str(tree.find('system-out').text))
                        print("MO :", mo.group())
                        status_code = (mo.group().split(" "))[4]
                    except:
                        status_code = "Some error occurred"

                for z in y.findall('error'):
                    testfailed = True
                    info_line = find_between("*** " + str(y.attrib['name']), "***", filepath=xmlpath)
                    #print("info line: " + info_line)
                    #print(find_between("::author::", "::", data=info_line))
                    if req_type in ('GET', 'PUT', 'DELETE', 'POST'):
                        update_count(req_type, total, fail)
                    single_table = single_table + \
                    "<tr>" \
                    "<td style='border:1px solid #ccc;'>" + str(y.attrib['classname']) + "</td>" \
                    "<td style='border:1px solid #ccc; background-color: #f74f4f'>" + str(y.attrib['name']) + "</td>" \
                    "<td style='border:1px solid #ccc;'>" +"<span style= 'color: #1d00ff'>" + endpoint +"</span>" + "</td>" \
                    "<td style='border:1px solid #ccc; text-align:center'>" +" <span style= 'color: #1d00ff'>"+ service +"</span>"+"</td>" \
                    f"<td style='border:1px solid #ccc; background-color: {color}' align='center'>" +" <span style= 'color: #ffffff'>"+ req_type +"</span>"+"</td>" \
                    "<td style='border:1px solid #ccc; text-align:center'>" +"<span style= 'color: #f74f4f; font-weight:bold'>" + status_code +"</span>" + "</td>" \
                    "</tr>"
                    print("Test Suite:" + str(y.attrib['classname']) + " - Failed Test: " + str(y.attrib['name']))
                    # print(str(z.attrib['type']))
                if not testfailed:
                    if req_type in ('GET', 'PUT', 'DELETE', 'POST'):
                        update_count(req_type, total, success)
                    single_table = single_table + \
                    "<tr>" \
                    "<td style='border:1px solid #ccc;'>" + str(y.attrib['classname']) + "</td>" \
                    "<td style='border:1px solid #ccc; background-color:#48f064'>" + str(y.attrib['name']) + "</td>" \
                    "<td style='border:1px solid #ccc;'>" +"<span style= 'color: #1d00ff'>" + endpoint +"</span>" + "</td>" \
                    "<td style='border:1px solid #ccc; text-align:center'>" +" <span style= 'color: #1d00ff'>"+ service +"</span>"+"</td>" \
                    f"<td style='border:1px solid #ccc; background-color: {color}' align='center'>" +" <span style= 'color: #ffffff'>"+ req_type +"</span>"+"</td>" \
                    "<td style='border:1px solid #ccc; text-align:center'>" +"<span style= 'color: #07a336; font-weight:bold'>" + status_code +"</span>" + "</td>" \
                    "</tr>"
                    print("Test Suite:" + str(y.attrib['classname']) + " - Passed Test: " + str(y.attrib['name']))
        #ofailed_table = failed_table + "</table>"
        #opassed_table = passed_table + "</table><br>"
        single_table = single_table + "</table><br>"
        # print(failed)
        # print(total_cases)
        # print(executiontime)

        # code for generating a graph
        w = 0.2
        reqtype = ['GET', 'POST', 'PUT', 'DELETE']
        # colors = ['#5bb1fc', '#3fd168', '#f59753', '#ff523b']

        bar1 = np.arange(len(reqtype))
        bar2 = [i + w for i in bar1]
        bar3 = [i + w for i in bar2]

        fig, ax = plotter.subplots()

        one = plotter.bar(bar1, total, w, label="total", color=['#5bb1fc', '#b3b31d', '#f59753', '#be6cf5'])
        two = plotter.bar(bar2, success, w, label="passed", color='#65eb67')
        three = plotter.bar(bar3, fail, w, label="failed", color='#eb6565')


        def autolabel(rects):
            """
            Attaching a text label above each bar displaying its value
            """
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                        '%d' % int(height),
                        ha='center', va='bottom', fontsize=14)


        autolabel(one)
        autolabel(two)
        autolabel(three)

        plotter.xlabel("Request Type", fontsize=16, labelpad=7)
        plotter.ylabel("Number of request", fontsize=16, labelpad=7)
        plotter.title('Graph:Total vs Failed vs Pass requests', fontsize='x-large', fontweight='bold', color='blue',
                      pad=12)
        plotter.xticks(bar1 + w, reqtype, fontsize=12)

        psd = mpatches.Patch(color='#65eb67', label='Passed')
        fld = mpatches.Patch(color='#eb6565', label='Failed')

        plotter.legend(handles=[psd, fld], fontsize=16)

        y = np.random.randint(low=0, high=total_cases, size=100)
        plotter.yticks(np.arange(0, max(y), 15))

        fig.set_size_inches(10.5, 7.5)
        plotter.savefig(os.path.join(report_location, "graph.png"), dpi=100)
        # graph code ends

        pieLabels = 'Pass', 'Fail'
        populationShare = [total_cases - failed, failed]
        figureObject, axesObject = plotter.subplots()
        axesObject.pie(populationShare, labels=pieLabels, autopct='%1.2f', startangle=90, textprops={'fontsize': 16, 'color': 'black'}, colors=['#65eb67', '#eb6565'])
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