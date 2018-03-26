""" Routes related to ticker accounting statements """


from flask import Blueprint, request, jsonify
from ..config import login_required
from ..config import q_ticker


# Name of the module
mod = Blueprint( __file__, __name__)

### Accounting statements
Q = {}
Q['is'] = q_ticker.getIncomeStatementDetails
Q['assets'] = q_ticker.getBalanceSheetAssetsDetails
Q['liabs'] = q_ticker.getBalanceSheetLiabilitiesDetails
Q['cf_op'] = q_ticker.getCashFlowOperatingActivityDetails
Q['cf_inv'] = q_ticker.getCashFlowInvestingActivityDetails
Q['cf_fin'] = q_ticker.getCashFlowFinancingActivityDetails



@mod.route( '/<ticker>/<statement>/<year>/<items>' )
@login_required
def lookup( ticker, statement, year, items ):
    if year == 'all':
        year = None

    if items == 'all':
        items = None

    if items is not None:
        items = items.replace( '_', '/')

    if statement in Q.keys():
        X = Q[statement]( ticker, year, items, return_raw=False )
        return jsonify(X)
    else:
        return jsonify( {'error':'Invalid account statement type' } )


@mod.route( '/<ticker>/<statement>/<year>/<items>/raw' )
@login_required
def lookup_raw( ticker, statement, year, items ):
    if year == 'all':
        year = None

    if items == 'all':
        items = None

    if items is not None:
        items = items.replace( '_', '/')

    if statement in Q.keys():
        X = Q[statement]( ticker, year, items, return_raw=True )
        return jsonify(X)
    else:
        return jsonify( {'error':'Invalid account statement type' } )
