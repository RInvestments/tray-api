""" Main App File

        Created : 17th Feb, 2018
        Author  : Manohar Kuse
"""

from flask import Flask, redirect, url_for
import code

app = Flask( __name__ )
app.config.from_pyfile( 'config.py')




db = 0 #init mongodb here

#from views import * #direct routes
#from blue.site.routes import mod as xsite #site blueprint
#from blue.api.routes import mod as xapi   # other blueprints

from flask_dance.contrib.github import make_github_blueprint, github
github_blueprint = make_github_blueprint( client_id="12ed11d1c1a4aebadeaf", client_secret="8d4cd826b3ad43fa945cdb53f37567ac0035121b" )


# code.interact( local=locals() )
#app.register_blueprint( xsite )
#app.register_blueprint( xapi, url_prefix='/api' )
app.register_blueprint( github_blueprint, url_prefix="/login")


@app.route( "/")
def index():
    if not github.authorized:
        return redirect( url_for("github.login") )
    resp = github.get( "/user")
    return "github username: " + resp.json()['login']
    return "resp: " + str( resp.json() )

if __name__ == "__main__":
    app.run()
