import sys
import time
from config.process_config import *

# Timing is given by considering the time required by API Feeds
if Build_Version.__contains__("3."):
    duration = 2100     # waiting for 35 minutes as default
else:
    duration = 4800     # waiting for 80 minutes as default

if len(sys.argv) == 2 and str(sys.argv[1]).strip() != '':
    duration = int(sys.argv[1])     # overwrite default time with the given time
print("Waiting for the seconds - ", duration)     # Sleep for a given seconds
time.sleep(duration)
