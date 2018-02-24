""" Main App File

        Created : 17th Feb, 2018
        Author  : Manohar Kuse
"""

from flask import Flask, redirect, url_for, request


app = Flask( __name__ )
app.config.from_pyfile( 'blue/config_var.py')


db = 0 #init mongodb here


############################################
########## OAuth - flask_dance #############
############################################
from flask_dance.contrib.github import make_github_blueprint, github
github_blueprint = make_github_blueprint( client_id="12ed11d1c1a4aebadeaf", client_secret="8d4cd826b3ad43fa945cdb53f37567ac0035121b" )



#############################################
######### Import Custom Blueprints ##########
#############################################
# Import Blueprints
from blue.site.routes import mod as xsite #site blueprint
from blue.api.routes_ticker import mod as xticker   # other blueprints

# Register Blueprints
app.register_blueprint( xsite, url_prefix='/mysite' ) #try
app.register_blueprint( xticker, url_prefix='/tickerInfo' )

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
    app.run(host='0.0.0.0')
