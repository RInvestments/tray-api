""" Contains all the routes """

from app import app

@app.route( "/")
def index( ):
    return "<h1>This is index page</h1>"
