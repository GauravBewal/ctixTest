from config.process_config import *
from lib.ui.nav_app import *
import subprocess


def processfile(filepath):
    #a = os.popen("git log --pretty=format:'%an' " + filepath + " | head -n 1").read()
    #a = str(a).replace("0", "").replace("\n", "")
    #set_value(filepath, a)

    data = ""
    #for line in os.popen("git log --pretty=format:'%an' " + filepath + " | head -n 1"):
    #    data = data + str(line.rstrip().encode('UTF-8'))
    #data = str(data).replace("0", "").replace("\n", "")
    #set_value(filepath, data)

    #output = subprocess.run(["git", "log", "--pretty=format:'%an'", filepath, "|", "head", "-n", "1"], encoding='utf-8', capture_output=True)
    #print(output)
    # We are checking the original author and not the last checkin person
    pip = os.popen("git log --reverse --pretty=format:'%an' " + filepath + " | head -n 1")
    data = pip.buffer.read().decode(encoding='utf8').strip()
    data = ''.join([i if ord(i) < 128 else ' ' for i in data])
    #data = str(data).replace("0", "").replace("\n", "").encode('utf-8').strip()
    print(data)
    set_value(filepath, data)


for dirpath, dirnames, files in os.walk(os.environ["PYTHONPATH"]):
    for f in files:
        if f.endswith('.py') and f.startswith('test_'):
            print(os.path.join(dirpath, f))
            processfile(os.path.join(dirpath, f))

