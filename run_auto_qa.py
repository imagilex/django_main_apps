import os
import subprocess
import sys

print("\n")
print("Fixing imports (fiximports)")
for root, dirs, files in os.walk(os.getcwd()):
    if root != os.getcwd():
        for f in files:
            if len(f.split('.')) > 1 and 'py' == f.split('.')[1]:
                arch = "{}".format(os.path.join(root, f))
                if "migrations" not in arch:
                    subprocess.call(['fiximports', arch], stdout=sys.stdout)

print("\n")
print("Codestyle Checking (pycodestyle)")
for root, dirs, files in os.walk(os.getcwd()):
    if root != os.getcwd():
        for f in files:
            if len(f.split('.')) > 1 and 'py' == f.split('.')[1]:
                arch = "{}".format(os.path.join(root, f))
                if "migrations" not in arch:
                    subprocess.call(['pycodestyle', arch], stdout=sys.stdout)

print("\n")
print("Import checking (importchecker)")
subprocess.call(['importchecker', "."], stdout=sys.stdout)

print("\n")
print("""Imports order:

1) Std Clases
2) Implemented Clases
3) Std Functions
4) Implemented Functions
5) Std Models
6) Implemented Models
7) Std Forms
8) Implemented Forms

""")