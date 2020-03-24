import os
import pydoc
import subprocess

def main():
    subprocess.call(
        ['python', '-m', 'pydoc', '-w', '.\\'])
    subprocess.call(
        ['move', '*.html', 'docs\pydoc'])

if __name__ == "__main__":
    main()
