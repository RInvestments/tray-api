""" Routes related to industry lists """



from flask import Blueprint, request, jsonify
from ..config import login_required
from ..config import q_ticker, q_industry


# Name of the module
mod = Blueprint( __file__, __name__)


@mod.route( '/ls/<bourse>' )
@mod.route( '/ls' )
@login_required
def lookup_industry_list( bourse=None  ):
    return jsonify( q_industry.getIndustryList( bourse ) )
    return 'ls'+str(bourse)

# @mod.route( '/<industry>/<bourse>' )
@mod.route( '/<industry>/' )
@login_required
def lookup_sector_list( industry, bourse=None ):
    if industry == 'all':
        return jsonify(  q_industry.getSectorsOf( None, bourse=bourse )  )
    return jsonify(  q_industry.getSectorsOf( industry, bourse=bourse )  )

@mod.route( '/<industry>/<sector>/<bourse>' )
@mod.route( '/<industry>/<sector>/' )
@login_required
def lookup_ticker_list( industry, sector, bourse=None ):
    if industry == 'all':
        industry = None
    if sector == 'all':
        sector = None
    return jsonify(  q_industry.getTickersOf( industry, sector, bourse=bourse )  )
