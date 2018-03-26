""" Routes related to industry lists """



from flask import Blueprint, request, jsonify
from ..config import login_required
from ..config import q_ticker, q_industry


# Name of the module
mod = Blueprint( __file__, __name__)



@mod.route( '/<bourse>/')
@login_required
def j_industry_list( bourse ):
    if bourse == 'all':
        bourse = None
    return jsonify( q_industry.getIndustryList( bourse ) )



@mod.route( '/<bourse>/<industry>')
@login_required
def j_sector_list( bourse, industry ):
    if bourse == 'all':
        bourse = None

    if industry == 'all':
        industry = None

    if industry is not None:
        industry = industry.replace( '_', '/')

    return jsonify( q_industry.getSectorsOf( industry, bourse=bourse ) )

@mod.route( '/<bourse>/<industry>/<sector>')
@login_required
def j_ticker_list( bourse, industry, sector ):
    if bourse == 'all':
        bourse = None

    if industry == 'all':
        industry = None

    if industry is not None:
        industry = industry.replace( '_', '/')

    if sector == 'all':
        sector = None

    if sector is not None:
        sector = sector.replace( '_', '/')

    return jsonify( q_industry.getTickersOf( industry, sector, bourse=bourse ) )
