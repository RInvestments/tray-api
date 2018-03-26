""" Main App File

        Created : 17th Feb, 2018
        Author  : Manohar Kuse
"""

from flask import Flask, redirect, url_for, request
import os

app = Flask( __name__ )
app.config.from_pyfile( 'blue/config_var.py')



############################################
########## OAuth - flask_dance #############
############################################
from flask_dance.contrib.github import make_github_blueprint, github

try:
    github_blueprint = make_github_blueprint( client_id=os.environ['GITHUB_CLIENT_ID'], client_secret=os.environ['GITHUB_CLIENT_SECRET'] )
    print 'Using shell evirons $GITHUB_CLIENT_ID and $GITHUB_CLIENT_SECRET'
except:
    print 'ERROR. Cannot set oauth with github. Make sure $GITHUB_CLIENT_ID and $GITHUB_CLIENT_SECRET are available'
    quit()



#############################################
######### Import Custom Blueprints ##########
#############################################
# Import Blueprints
from blue.site.routes import mod as xsite #site blueprint
from blue.api.routes_ticker import mod as xticker   # other blueprints
from blue.api.routes_accounting_statements import mod as xstatements   # other blueprints
from blue.api.routes_industry import mod as xindustry   # other blueprints

# Register Blueprints
app.register_blueprint( xsite, url_prefix='/mysite' ) #try
app.register_blueprint( xticker, url_prefix='/tickerInfo' )
app.register_blueprint( xstatements, url_prefix='/accountingStatements' )
app.register_blueprint( xindustry, url_prefix='/industryInfo' )

app.register_blueprint( github_blueprint, url_prefix="/login") #Github Authorization



############################################
############## Authorize_me ################
############################################
@app.route( "/authorize_me")
def authorize_me():
    if not github.authorized:
        return redirect( url_for("github.login",  next=request.url) )
    resp = github.get( "/user")

    to_return = "<h1>You are Authorized</h1>Authorized github user: " + resp.json()['login']
    to_return += '<p>' + str( resp.json() )
    return to_return



@app.route( "/")
def index():
    return "<h1>Welcome to tray-api!</h1>"


if __name__ == "__main__":
    app.run(host='0.0.0.0', ssl_context='adhoc')
