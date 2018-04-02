""" This file will hold the init info,
    - Mongodb Access handle
    - Authorization decorator

        Author  : Manohar Kuse <mpkuse@connect.ust.hk>
        Created : 24th Feb, 2018
"""

from functools import wraps
from flask import g, request, redirect, url_for, abort, session
from flask_dance.contrib.github import github

import pymongo
import os

from dbingress.TickerQueries import TickerQueries
from dbingress.IndustryQueries import IndustryQueries
from dbingress.IncomeStatementQueries import IncomeStatementQueries
from dbingress.BalanceSheetQueries import BalanceSheetQueries
from dbingress.CashFlowQueries import CashFlowQueries
from dbingress.QuotesQueries import QuotesQueries

###
### Authorization
###
# GITHUB Only
# def login_required(f):
#     @wraps(f)
#     def decorated_function( *args, **kwargs ):
#         if not github.authorized:
#             #return redirect( url_for("github.login", next=request.url) )
#             #abort(401)
#             return "<h2>You are unauthorized for this page</h2> Please go to /authorize_me<p>--manohar"
#             return
#         return f(*args, **kwargs )
#     return decorated_function

from encription.vigenere import decode
def login_required(f):
    @wraps(f)
    def decorated_function( *args, **kwargs ):
        # Github Authorization check
        if not github.authorized:
            # GET access token Authorization check
            try:
                decoded = decode( os.environ['GITHUB_CLIENT_SECRET'], str(request.args.get('authorization_token')) )
                first5 = decoded[:5]
                last5  = decoded[-6:]
            except:
                return "<h2>KAGO cannot authorize with github. Cannot authorize with GET</h2>"

            if first5 == '<msg>' and last5 == '</msg>': #Decoded seem to be unaltered
                raw_msg = decoded[5:-6].split(':')

                if len(raw_msg) == 2:
                    username = raw_msg[0]
                    session['username'] = raw_msg[0]
                    return f(*args, **kwargs )

                    #TODO: Check if the token is expired with raw_msg[1].
                else:
                    return "<h2>cannot authrize with GET. Invalid raw_msg"
            else:
                return "<h2>cannot authorize with github. Cannot authorize with GET</h2>"
            # return 'decoded: '+decoded+'<p>first5:'+first5+'<p>last5:'+last5

            #return redirect( url_for("github.login", next=request.url) )
            #abort(401)
            return "<h2>You not github.authorized for this page</h2> Please go to /authorize_me<p>--manohar"

        return f(*args, **kwargs )


    return decorated_function
#


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
q_quotes = QuotesQueries( client )
