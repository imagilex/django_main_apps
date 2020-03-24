import os
import subprocess
import sys

def main():
    print("\n")
    print("Fixing imports (fiximports)")
    for root, dirs, files in os.walk(os.getcwd()):
        if root != os.getcwd():
            for f in files:
                if len(f.split('.')) > 1 and 'py' == f.split('.')[1]:
                    arch = "{}".format(os.path.join(root, f))
                    if "migrations" not in arch:
                        subprocess.call(
                            ['fiximports', arch], stdout=sys.stdout)
    print("\n")
    print("Codestyle Checking (pycodestyle)")
    for root, dirs, files in os.walk(os.getcwd()):
        if root != os.getcwd():
            for f in files:
                if len(f.split('.')) > 1 and 'py' == f.split('.')[1]:
                    arch = "{}".format(os.path.join(root, f))
                    if "migrations" not in arch:
                        subprocess.call(
                            ['pycodestyle', arch], stdout=sys.stdout)
    print("\n")
    print("Import checking (importchecker)")
    subprocess.call(['importchecker', "."], stdout=sys.stdout)
    
if __name__ == "__main__":
    main()