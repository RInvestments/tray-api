from flask import Blueprint

mod = Blueprint( 'site', __name__ )

@mod.route( '/homepage' )
def homepage():
    return "you are on the homepage (site)"
