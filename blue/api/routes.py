from flask import Blueprint

# Name of the module
mod = Blueprint( 'api', __name__)

@mod.route( '/getStuff' )
def homepage():
    return '{"result": "you are on the homepage (api)" }'
