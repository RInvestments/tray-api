""" Routes related to ticker queries """


from flask import Blueprint, request, jsonify
from ..config import login_required
from ..config import q_ticker


# Name of the module
mod = Blueprint( 'api', __name__)

# Sample Open Route
@mod.route( '/public_page' )
def homepage():
    return '{"result": "you are on the homepage (api)" }'

# Sample Secret Route
@mod.route( '/secret_page')
@login_required
def secret_page():
    return 'This is a secret_page in mysite'


@mod.route( '/<ticker>/name' )
@login_required
def lookup_ticker( ticker ):
    X = {}
    X[str(ticker)] =  q_ticker.getCompanyName( ticker )
    X[str(ticker)+'1'] =  q_ticker.getCompanyName( ticker )
    X[str(ticker)+'2'] =  q_ticker.getCompanyName( ticker )
    return jsonify( X )
    return jsonify( q_ticker.getName( ticker ) )
