""" Main App File

        Created : 17th Feb, 2018
        Author  : Manohar Kuse
"""

from flask import Flask, redirect, url_for, request, session
import os
#from flask_cors import CORS #Cross Origin Request

app = Flask( __name__ , static_url_path='/static')
#CORS(app)
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
from blue.api.routes_quotes import mod as xquote   # other blueprints

# Register Blueprints
app.register_blueprint( xsite, url_prefix='/mysite' ) #try
app.register_blueprint( xticker, url_prefix='/tickerInfo' )
app.register_blueprint( xstatements, url_prefix='/accountingStatements' )
app.register_blueprint( xindustry, url_prefix='/industryInfo' )
app.register_blueprint( xquote, url_prefix='/tickerQuotesInfo' )

app.register_blueprint( github_blueprint, url_prefix="/login") #Github Authorization



############################################
############## Authorize_me ################
############################################
from blue.encription.vigenere import decode, encode
import datetime
@app.route( "/authorize_me")
def authorize_me():
    if not github.authorized:
        return redirect( url_for("github.login",  next=request.url) )
    resp = github.get( "/user")
    git_user_name = resp.json()['login']

    to_return = "<h1>You are Authorized</h1>"
    to_return += "<p>Authorized github user: " + git_user_name + "</p>"
    to_return += '<p id="github_raw_data">' + str( resp.json() ) + "</p>"

    # Set session
    session['username'] = git_user_name
    to_return += '<p id="session">session|username : '+ session['username'] + '</p>'

    # Generate GET access token
    generated_time = datetime.datetime.now().strftime( "%Y-%m-%d-%H-%M-%s" )
    encoded_string = encode( os.environ['GITHUB_CLIENT_SECRET'], '<msg>%s:%s</msg>' %(git_user_name, generated_time) )
    to_return += '<p id="GET access coupon">\
        You can also authorize yourself by passing the GET parameter `authorization_token` as: '\
        + encoded_string + '</p>'
    return to_return

@app.route( "/whoami")
def whoami():
    if not github.authorized:
        to_return = "<h1>unauthorized</h1><p>I do not recognize you! You may authorize yourself from /authorize_me</p>"
        to_return += '<p>You IP-addr:'+ request.remote_addr +'</p>'
        return to_return

    to_return = "<h1>authorized</h1>"

    # Session
    to_return += "<p id='user'>I recognize you as: "+ session['username'] + "</p>"

    # Generate GET access token
    git_user_name = session['username']
    generated_time = datetime.datetime.now().strftime( "%Y-%m-%d-%H-%M-%s" )
    encoded_string = encode( os.environ['GITHUB_CLIENT_SECRET'], '<msg>%s:%s</msg>' %(git_user_name, generated_time) )
    to_return += '<p id="GET access coupon">\
        You can also authorize yourself by passing the GET parameter `?authorization_token=%s`</p>' %(encoded_string)

    to_return += '<p>You IP-addr:'+ request.remote_addr +'</p>'

    return to_return

@app.route( "/")
def index():
    return "<h1>Welcome to tray-api!</h1>"



######################################
############## DASH ##################
######################################
# import dash
# import dash_core_components as dcc
# import dash_html_components as html
#
# import uuid
#
# from blue.config import login_required
# from dash_layouts.Layout1 import Layout1
#
# This can server dash with flask server (works!)
# TODO: figure out a way to not be forced to set the layouts and callbacks here.
# May be get it under a blueprint. Figureout a good way to use all this here.
# dash_app_url = '/'+str( uuid.uuid4().get_hex() )
# print 'Start Dash app: ', dash_app_url
# dash_app = dash.Dash( __name__, server=app, url_base_pathname=dash_app_url ) #can set a static folder here (separate for it for images etc)
# # dash_app.layout = html.Div( 'Hello Dash Apl')
#
# l = Layout1()
# dash_app.layout = l.render()
#
# @login_required #this doesnt seem to work as expected
# @app.route( '/dash/app1' )
# def dash_app():
#     return redirect( dash_app_url )


if __name__ == "__main__":
    app.run(host='0.0.0.0', ssl_context='adhoc')
