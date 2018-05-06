import dash

app = dash.Dash()
server = app.server
app.config.supress_callback_exceptions = True #it is required to set this True. Setting it to False won't let the app start
