# Multiple Page Dash App

This is based on (https://dash.plot.ly/urls)[https://dash.plot.ly/urls].

All the various apps will go in the sub-package apps (see for example app1.py and app2.py).
These files will contain a layout and the callbacks.

The corresponding urls for each of the app can be found in index.py. You are
suppose to exec this file to start the app.


### Howto create new app?
- Make a copy of app2.py. See app1.py and app2.py for example bare bore app.
- Set the url for your new app in index.py::display_page()
