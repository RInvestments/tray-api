""" Routes related to getting quotes of tickers """



from flask import Blueprint, request, jsonify
from ..config import login_required
from ..config import q_ticker, q_quotes

import datetime

# Name of the module
mod = Blueprint( __file__, __name__)



@mod.route( '/<ticker>/')
@login_required
def quote( ticker ):
    return jsonify( q_quotes.lastest_quote( ticker ) )



@mod.route( '/<ticker>/<start_date>/<end_date>')
@login_required
def quote_range( ticker, start_date, end_date ):
    # start_date and end_date of the form YYYY-MM-DD. Eg. 2017-02-26
    try:
        a = datetime.datetime.strptime( start_date, '%Y-%m-%d' )
        b = datetime.datetime.strptime( end_date  , '%Y-%m-%d' )
    except:
        return jsonify( {'error':'Invalid date format. Expecting start_date and end_date of the form YYYY-MM-DD. Eg. 2017-02-26' } )


    QE = q_quotes.range_quote(ticker, start_date=start_date, end_date=end_date)
    return jsonify(QE)


@mod.route( '/<ticker>/<on_date>')
@login_required
def quote_ondate( ticker, on_date ):
    # on_date can be a ':' spaced object, each on the format YYYY-MM-DD.
    # Eg: 2017-02-28:2016-02-25:2015-02-25
    try:
        for a in on_date.split(':'):
            a0 = datetime.datetime.strptime( a, '%Y-%m-%d' )
    except:
        return jsonify( {'error':'Invalid date format. Expecting start_date and end_date of the form YYYY-MM-DD. Eg. 2017-02-26' } )


    QE = q_quotes.date_quote( ticker, on_date )
    return jsonify(QE)
