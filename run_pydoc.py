import os
import pydoc
import subprocess

from main_app_tool.settings import INSTALLED_APPS

apps = [app for app in INSTALLED_APPS 
    if app.find("django.contrib") == -1 and app.find("crispy_forms") == -1]

base_path = os.getcwd()

for app in apps:
    subprocess.call(['python', '-m', 'pydoc', '-w', ], stdout=sys.stdout)
    