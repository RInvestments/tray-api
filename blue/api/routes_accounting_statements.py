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


@mod.route( '/<ticker>/<statement>/<year>/all' )
@login_required
def lookup_incomeStatement_full( statement, ticker, year ):
    if statement in Q.keys():
        X = Q[statement]( ticker, year, None )
        return jsonify(X)
    else:
        return jsonify( {'error':'Invalid account statement type'} )

@mod.route( '/<ticker>/<statement>/<year>/all/raw' )
@login_required
def lookup_incomeStatement_fullraw( statement, ticker, year ):
    if statement in Q.keys():
        X = Q[statement]( ticker, year, None, return_raw=True )
        return jsonify(X)
    else:
        return jsonify( {'error':'Invalid account statement type'} )

@mod.route( '/<ticker>/<statement>/<year>/ls' )
@login_required
def lookup_incomeStatement_ls( statement, ticker, year ):
    if statement in Q.keys():
        X = Q[statement]( ticker, year, None )
        # clean the values
        for _ticker in X.keys():
            for _year in X[_ticker].keys():
                for _item in X[_ticker][_year].keys():
                    X[_ticker][_year][_item] = None
        return jsonify(X)
    else:
        return jsonify( {'error':'Invalid account statement type' } )



@mod.route( '/<ticker>/<statement>/<year>/<items>' )
@login_required
def lookup_incomeStatement_select( statement, ticker, year, items ):
    # return items
    if statement in Q.keys():
        X = Q[statement]( ticker, year, items )
        return jsonify(X)
    else:
        return jsonify( {'error':'Invalid account statement type' } )


@mod.route( '/<ticker>/<statement>/<year>/<items>/raw' )
@login_required
def lookup_incomeStatement_select_raw( statement, ticker, year, items ):
    # return items + 'raw'
    if statement in Q.keys():
        X = Q[statement]( ticker, year, items, return_raw=True )
        return jsonify(X)
    else:
        return jsonify( {'error':'Invalid account statement type' } )
