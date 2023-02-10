import configparser
import os
import time
import sys

# To avoid issues of file path which depends from where the execution has been done we will calucate the relative path
os.environ["PYTHONPATH"] = os.path.join(os.getcwd().split("ctix_tests")[0], "ctix_tests")
ini_path = os.path.join(os.environ["PYTHONPATH"], "config", "config.ini")
config = configparser.ConfigParser()
config.read(ini_path)
temp_settings_path = os.path.join(os.environ["PYTHONPATH"], "tempvalues.txt")

# APP SETTINGS
APP_URL = config['APP_SETTINGS']['APP_URL']
Admin_Email = config['APP_SETTINGS']['Admin_Email']
Admin_Password = config['APP_SETTINGS']['Admin_Password']

# BROWSER SETTINGS
RunOnBrowser = config['BROWSER_SETTINGS']['RunOnBrowser']

# TESTPLAN_EXECUTION
testplan = config['TESTPLAN_EXECUTION']['testplan']

# REPORT_SETTINGS
report_format = config['REPORT_SETTINGS']['report_format']

# JENKINS JOB NAME - Used for pointing to Screenshot link in Jenkins
jenkins_job_name = ""

# OVERWRITE SETTINGS FROM ENVIRONMENT IF EXISTS
if "APP_URL" in os.environ:
    APP_URL = os.environ['APP_URL']
    print("Overwriting APP_URL with environment variable")

if "Admin_Email" in os.environ:
    Admin_Email = os.environ['Admin_Email']
    print("Overwriting Admin_Email with environment variable")

if "Admin_Password" in os.environ:
    Admin_Password = os.environ['Admin_Password']
    print("Overwriting Admin_Password with environment variable")

if "RunOnBrowser" in os.environ:
    RunOnBrowser = os.environ['RunOnBrowser']
    print("Overwriting RunOnBrowser with environment variable")

if "testplan" in os.environ:
    testplan = os.environ['testplan']
    print("Overwriting testplan with environment variable")

if "report_format" in os.environ:
    report_format = os.environ['report_format']
    print("Overwriting report_format with environment variable")

if "jenkins_job_name" in os.environ:
    jenkins_job_name = os.environ['jenkins_job_name']
    print("Overwriting jenkins_job_name with environment variable")

if "First_Password" in os.environ:
    First_Password = os.environ['First_Password']
    print("Overwriting First_Password with environment variable")
else:
    First_Password = "System.Default@)9*"

if "Build_Version" in os.environ:
    Build_Version = os.environ['Build_Version']
    print("Overwriting Build_Version with environment variable")
else:
    Build_Version = "3.0"  # Use 2.9.0, 2.9.1, 3.0 |

if "CTIX_LITE" in os.environ:
    CTIX_LITE = os.environ['CTIX_LITE']
    print("Overwriting CTIX_LITE with environment variable")
else:
    CTIX_LITE = False  # Value should be FALSE and TRUE

# Other variables
uniquestr = str(round(time.time() * 1000))
#ctix_version = 2.8  # Todo: Get this value dynamically from the build version

# STATIC CONFIGURATION BELOW
# Reporting
report_location = os.path.join(os.environ["PYTHONPATH"], "reports")

# LICENSE
license_string = 'LS0tLS1CRUdJTiBQR1AgU0lHTkVEIE1FU1NBR0UtLS0tLQpIYXNoOiBTSEE1MTIKCi0gLS0tLS1CR ' \
                 'UdJTiBQR1AgTUVTU0FHRS0tLS0tCgpoUUVNQTJYVS9EejlWaUZrQVFnQW1pNzJ5czN0eXlZdnNuc ' \
                 'jFsVGNFTjB1d3NGU3IwZGQvaTFhUHRBdmFkeHhTCi9tOFIvaGk2V0YvYXFyY0dVeDVpYXJRTHdIT ' \
                 'TAzMFRaa25ldmVHQ3h0RkhOM1MvMHBMRy9jVUNZWlVrWnhwVnoKalYzdTJLeHdjWDhCQnVpL1V ' \
                 'rUjVMMHhueFlSN1FqYkVRbkdiMEJvc2M0dWVBZEhqc2RQb3ZCeTFQd3EwNWRseAo2dFVVeVVrS ' \
                 'E9KMjdSYTk1Qmd4TE03U3habnJLc2ZjVHZGVmNBSEx3SzZtbmhPSGpjbzNieDZ0THNjQ2UvSFpW ' \
                 'CnNVVnMzRFlsWUE2R0JnVjhFbzZqeDlBOWZDNDJ5SlF1cmNlejZxNEcvUEp6SUNyd0JSUU1VZ05I ' \
                 'clYzZ1ZhWkcKQ01WclpUVW44NWNpY051SWl1ZUthZGhrQXllWHViNkJDSkI1Zk9OanJkTHFBUUVS ' \
                 'VnEvLzlQV1RNcG9zLzFwdgpveHdBVS9seUtGMEt0OS93SC95b3k1b3gwTFpxd2ppS2FaQzVpY1NL ' \
                 'V3hSbEI1QXhsUDhVYXFTNTN4Q3pjTmR3Ckl0ZnJ2blU3NVFjUTA5NEdEMm5KcVpiRnVKZnJiYjMz ' \
                 'NkttMksrcnQwU3dKZ1BiN2xCREdSQ2c5czlVYmpWbVgKc1dpZWJVcmNoY3Iwa0tUYjFLeEd4UjRjNU ' \
                 'JMckVpQXNnN29CUkJXV3NMOE9yWHg4Yk4wZ09xcTg0c0hNWWc3TwpYaCs2N08xYUJ6VHMrcmk ' \
                 'zaWs0UUFEYTlGUG5TelFVVzVOeFU3WGIwRlptZ0hZcXFEbmtlbFJseXRLQitDYzZvCjVtN0EzMjB5d ' \
                 'kx6OGRqODNyVEV3VVdrNjBua3pCcHp6YVB1ZTdRQ2JtaXB2ZlpNTjZkdm04Zmdva2kweFpzSEMK ' \
                 'OFhIYVZaeGk4UUtpbWxESHo0a0V3VFB3cG1Wb2RjNUF0WmlqZXVJUnd4eWFvWXhEaWpya0o2a ' \
                 'WxzT2lPVytQeQpxWEZ4bDZhOURobnJabzZFRy95eU8yT20zcTJjbEhMNkdpWVU1Z2ZveWt1YlV6O ' \
                 'EdLUGlpYzlTdHUxTUJXemtPCmM3Y0xFVXEvd3A2VWhCUTZIRW53NnlSWjlYTkFBY3ZyWEJpaUor ' \
                 'bktmSlBFZXJkTTFCK2ZsTUZxb3pWZUZTTi8KdHVPSVhKQTU1NnFZNWdKT3dibGd2VEx5V1c5Z3N ' \
                 '0b3lsQ01nSFA5aklIOXhrcXhhZThhUkMrdHFvcGdaZVUvYQpiemx2YWQvSnZXcVpOaHBxcmJHczhV ' \
                 'MWVRTEV4VERsM3h0MkVSdkxobk5xcnFlb2pqeU5KbjkzZUFIUGovUk14CjhNc0xYamlxdWthM3NaM ' \
                 'lZFbk1mMk1Ib2xETzVweXB2eldDeEtRd0tWZ1ErZnF4TmROeVdjMTMrWm1MVDNoRmkKcjNZbVB3 ' \
                 'OWZyaVh3UG9BY253UVBkcit5bHNwT0I2NFN4U1h0UFJLb0phVDlPR2Q5K2tGVUhxSmxYQXdWQU ' \
                 '9xNQppMGV2dG5saTJoSHFKd21HbTYxZ3ZSMnhnWmlCS0M2NFVzZ3Vsd3FoTE02UzNPSTRTOW ' \
                 'ZvdlN5OGZQMUpSL3VuCnlrb2ZUTlpJT3lseXg3cnhieXJ0OFdTdlNvczR0Mng2bG1kazYwQzBuT0NuR ' \
                 'GlENlZZRG9ERVRIQTU4dWxkVWgKb2N2R0cxVGhzWi9ESGw2TENPaHNsNlpSTnU0aUxKb2hXUn ' \
                 'VDSysvMWtnQ1l6L1htRmtjdjcxU2cza000VWVPYwpYT3Zhek56bFJKKzVlOFhUVDFqelhXT0l2OTVUc ' \
                 'jV0Q1JVc1NxelZGcVMwUjNSSzRnK2J5TDAzZnZiaEt3U1FoCmpFdFR4NjRLQW9lSVR2ampoSzc3Y ' \
                 '0Q3aytrZUhLRGpJdzFsRWFlR1pacTBYNGVQVHJuSWdTeVlYMGFPd01vRTIKVVY4UHZHdzJTYVl2 ' \
                 'REl3TDJtM3NpUXpMUjNFZXRhTHdDZjBGT2szL3pUMDJjTEEyTk4vYXlkRmlTY0xtbjExdwpxRXNNan ' \
                 'VOK1l4cklDM3A0Z3l6OGxaTXY5V3BFOUl5Z1VCTXRQQTZLSnlvVXZENXNkQ1NlUDhFU1k3OUN4Z ' \
                 '0piCkhsNlV1bDhnbXlnY1FqMzRKTlRpVFRzK0hGV1IxYzFFdmRSVFlVSlY4dHRoOHJQRGpJVFBmM ' \
                 '3k5Vk42aks0OVUKdUNrdWl5M052eXdFRFN2M3JqelluNkZscDZYdDg1MU80OUdHYkIwNmE5MkpT ' \
                 'ZlNMWkdIYWZqYVhzbzQ4UGxIdQpyY0RGM1NPczRQWjBtanJaU3FuRlAzWUM2VlNJZWViN0dJVUt ' \
                 '1ZHdMMnJMckFkcncyeDZ4M2YxMGQ0a3E5SUdzCjJQVzVsTG5mL1BiRlZETHdRTjlQRHZjRlVJUHB ' \
                 'veS8vb1FBNXBPRmxGZnRUTWpaWW9SR0lUMUtOQ3U1TmJtSGYKSTZpRnZ3elRueDVUTWNqZn ' \
                 'pzRS90T3BXYXJtRVo5Y25ZcGN2RXdpZnljbjBpT1MyQysydXUxdzlOTzRZYzN3MQp4YXdpVnliT3Zv ' \
                 'YlNhOUhGWFJiOEtQaXNJbjBRSkI5dEgxeUdFck1GaTVCZ2RnNlF2bTFndTVKYXRLckdRK2FxClBC ' \
                 'SU5YSktEV1c4QllmaFBpVXJGMzkzTXJKY0haeVhXQklDVG9BT05JTTRkNEcvNUViLzF3Q0VsblZnU ' \
                 'G1WWXIKcUF2VCs2VmRQb25BOCtPMzh4VkxSVXFUaTkxOFBoRmdLbEFqRWRmTU5zcnlVK1JZZ ' \
                 'VFYdU5vMzltaW42MlJXQQpSVTR0OFA0S1gzcE9GVHNaaHc4ckFZK1FIUzdDclo2b1IzdnRaTFAvU1 ' \
                 'N4enZ4S25lOWNmRjU1VmdyNm9pU2ZYClp1S1RsdkNDRUpET3dWMXNLYUV6R2ZmK3VnbHdXT ' \
                 'GdvdzJCQjdoaWZsSU8xbzlWeUpDT2t2ZHdhM3oxN0Z4UDcKcWFWalhJNmF6ZnM9Cj1aaUFBCi0gL ' \
                 'S0tLS1FTkQgUEdQIE1FU1NBR0UtLS0tLQotLS0tLUJFR0lOIFBHUCBTSUdOQVRVUkUtLS0tLQoKa ' \
                 'VFFekJBRUJDZ0FkRmlFRUNtN2ZBaEJnTGduUlBLMHdMeUlrYkt0ajV6Z0ZBbUNYdUNRQUNna1FM ' \
                 'eUlrYkt0ago1emhxTHdmNkFwT09SOWdvUnFjMTNVSzFIU3pEQmJoNy82THA3aTVWYkowanJTRjF1 ' \
                 'Y2d5dGdicHFRdm1kREhECkYxNEV6V0RndGdoMCtINUxoaUNwN3A0UDFjREVLZ1JZMHdGR0RFa ' \
                 'FlCQVgxaDFzM3Bac3N3S01NeVBOY0VydGUKa0NxV2pTd0hOVWVTcmk0RERqcWtFNHRNMWhiM ' \
                 'EVNUzBDWnk4aDJ3akZ0MmVRa3lmUVVKUHJVYUJlMmlSRlVJVwowdkFWamRUK1ZjekZ3VmhQT ' \
                 'GpOV2lBc3lIQ0d2WjkrQ0N5Y1NUTDdSU3BTS0t1b2Z4V2xObnJKVG9NTFJFb2ZYCkd3U2kvL1VvUX ' \
                 'F3Uk1zVWg5S1QxL0hJdS91TTVpSlBIYnlnanRQeUJOSSthRE9ralFsNHJuTU1uS1lCeWJuM1YKcU1 ' \
                 'uZTVqM21hb1dicE9xanFjakloMlRPY2xtK3dBPT0KPUhlOGYKLS0tLS1FTkQgUEdQIFNJR05BVFVSR S0tLS0tCg== '

# DO NOT MODIFY BELOW THIS
# Disable WebDriver-manager logs
os.environ['WDM_LOG_LEVEL'] = '0'

print("Initiated Tests on: " + APP_URL)

# #################### MAIN EXECUTION #########################
# Check if the program is executed from the execute_testplan if yes then read the configured test plan and execute.
calling_script = os.path.basename(sys.argv[0])
print("Calling script : " + str(calling_script))
if calling_script == "process_config.py":
    f = open("temp.txt", "a")
    f.write(testplan)
    f.close()

# calling_script = os.path.basename(sys.argv[0])
# if calling_script == "execute_testplan.py":
#    print("Executing TestPlan: " + testplan)
#    p = Popen([r'../PROJECTS/UI/test_stix_collection.py', "python3"], shell=True, stdin=PIPE, stdout=PIPE)
#    output = p.communicate()
#    print(output[0])
