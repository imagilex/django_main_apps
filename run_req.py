import subprocess
import sys

with open("requirements.txt", "r") as req_file:
    for library in req_file.readlines():
        subprocess.call(['pip', 'install', '-U', library], stdout=sys.stdout)
