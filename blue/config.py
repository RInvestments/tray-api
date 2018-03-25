""" This file will hold the init info,
    - Mongodb Access handle
    - Authorization decorator

        Author  : Manohar Kuse <mpkuse@connect.ust.hk>
        Created : 24th Feb, 2018
"""

from functools import wraps
from flask import g, request, redirect, url_for, abort
from flask_dance.contrib.github import github

import pymongo
import os

from dbingress.TickerQueries import TickerQueries
from dbingress.IndustryQueries import IndustryQueries
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
### Database connection try-except
###
def connect_mongodb(MONGO_URI, lazy_connection=False):
    """Set up a connection to the MongoDB server.

    Parameters:
        MONGO_URI: MongoDB server address (including username & pass).
        lazy_connection: avoid testing if the connection is working while
            initializing it.
    """
    print 'Attempt Connection to: ', MONGO_URI
    client = pymongo.MongoClient(MONGO_URI )

    if lazy_connection:
        return client

    # Send a query to the server to see if the connection is working.
    try:
        client.server_info()
    except pymongo.errors.PyMongoError as e:
        print e
        client = None

    return client

###
### Query Handles
###
try:
    print 'Looking up environment variable : $MONGO_URI'
    MONGO_URI = os.environ['MONGO_URI']
    print 'Found environment variable : $MONGO_URI'
except:
    print 'Environment variable $MONGO_URI not found. Now using mongodb://localhost:27017/'
    MONGO_URI = 'mongodb://localhost:27017/'
client = connect_mongodb( MONGO_URI )

q_ticker = TickerQueries( client )
q_industry = IndustryQueries( client )
q_income = IncomeStatementQueries( client )
q_balance_sht = BalanceSheetQueries( client )
q_cashflw = CashFlowQueries( client )
