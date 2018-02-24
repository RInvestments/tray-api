""" This file will hold the init info,
    - Mongodb Access handle
    - Authorization decorator

        Author  : Manohar Kuse <mpkuse@connect.ust.hk>
        Created : 24th Feb, 2018
"""

from functools import wraps
from flask import g, request, redirect, url_for, abort
from flask_dance.contrib.github import github

from dbingress.TickerQueries import TickerQueries
from dbingress.IncomeStatementQueries import IncomeStatementQueries
from dbingress.BalanceSheetQueries import BalanceSheetQueries
from dbingress.CashFlowQueries import CashFlowQueries

###
### Authorization
###
def login_required(f):
    @wraps(f)
    def decorated_function( *args, **kwargs ):
        if not github.authorized:
            #return redirect( url_for("github.login", next=request.url) )
            #abort(401)
            return "<h2>You are unauthorized for this page</h2> Please go to /authorize_me<p>--manohar"
            return
        return f(*args, **kwargs )
    return decorated_function


###
### DataBase
###
MONGO_URI = 'mongodb://localhost:27017/'
q_ticker = TickerQueries( MONGO_URI )
q_income = IncomeStatementQueries( MONGO_URI )
q_balance_sht = BalanceSheetQueries( MONGO_URI )
q_cashflw = CashFlowQueries( MONGO_URI )
