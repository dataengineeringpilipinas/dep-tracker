# Barangay DEP Tanod Tracker App
[https://deptracker.pythonanywhere.com/](https://deptracker.pythonanywhere.com/)

#### A [Puso Project](https://www.thepusoproject.ph/) by [Data Engineering Pilipinas](https://dataengineering.ph/)

[Barangay DEP Tanod Tracker Codebase](https://github.com/dataengineeringpilipinas/dep-tracker)


## Pre-requisites
To join, you just need the enough basic knowledge of Python, Flask and GitHub PR Merge process.
##### [Step 1 | Python for Everybody](https://citizendev.code.sydney/)
##### [Step 2 | Intro to Flask](https://www.youtube.com/playlist?list=PLXmMXHVSvS-AjwTOtiW1DXFYTgUlrUmHV)
##### [Step 3 | Basic GitHub PR Merge Knowledge](https://github.com/dataengineeringpilipinas/thepusoproject/wiki/CitizenDev-%7C-TPP-GitHub-PR-Merge-Flow)
##### [Step 4 | Join DEP Discord to collaborate](https://discord.com/invite/buDgydz7J9)

###How to copy and deploy the app to your Barangay

1. Clone [https://github.com/dataengineeringpilipinas/dep-tracker.git](https://github.com/dataengineeringpilipinas/dep-tracker.git)
2. Install dependencies.
3. Run the app locally and adjust the code to your liking including the look-and-feel of your Barangay. 
4. Deploy the app in [PythonAnywhere](https://www.pythonanywhere.com/). It has a free tier. Please see some steps below on how to deploy a Flask app in PythonAnywhere.

###How to deploy your Flask app in PythonAnywhere.
1. Add a new app and choose deploy app manually.
2. Enter bash and clone your Github repo.
3. Go to Files and correct the location of your appointments.db.
4. Edit your WSGI similar to the below: 
```bash
import sys
#
path = '/home/deptracker/dep-tracker'
if path not in sys.path:
    sys.path.append(path)
#
from app import app as application  # noqa
```
5. Reload app.
6. If no errors, you should have the app running in production.

