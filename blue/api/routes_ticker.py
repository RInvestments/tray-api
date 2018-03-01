""" Routes related to ticker queries """


from flask import Blueprint, request, jsonify
from ..config import login_required
from ..config import q_ticker


# Name of the module
mod = Blueprint( __file__, __name__)

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
def lookup_name( ticker ):
    X =  q_ticker.getName( ticker )
    return jsonify( X )


@mod.route( '/<ticker>/industry' )
@login_required
def lookup_industry( ticker ):
    X =  q_ticker.getIndustry( ticker )
    return jsonify( X )

@mod.route( '/<ticker>/sector' )
@login_required
def lookup_sector( ticker ):
    X =  q_ticker.getSector( ticker )
    return jsonify( X )


@mod.route( '/<ticker>/description' )
@login_required
def lookup_description( ticker ):
    X =  q_ticker.getDescription( ticker )
    return jsonify( X )

@mod.route( '/<ticker>/employeeCount' )
@login_required
def lookup_employeeCount( ticker ):
    X =  q_ticker.getEmployeesCount( ticker )
    return jsonify( X )

@mod.route( '/<ticker>/streetAddress' )
@login_required
def lookup_streetAddress( ticker ):
    X =  q_ticker.getStreetAddress( ticker )
    return jsonify( X )

@mod.route( '/<ticker>/accountingCurrency/<year>' )
@login_required
def lookup_accountingCurrency( ticker, year=2015 ):
    X =  q_ticker.getAccountingCurrency( ticker, year )
    return jsonify( X )
