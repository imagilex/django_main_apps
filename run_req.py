import subprocess
import sys

def main():
    with open("requirements.txt", "r") as req_file:
        for library in req_file.readlines():
            subprocess.call(['pip', 'install', '-U', library], stdout=sys.stdout)

if __name__ == "__main__":
    main()
