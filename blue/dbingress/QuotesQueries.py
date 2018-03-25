""" Queries related quotes data. For example, functions here can giveout the
latest open price of stock, quote open price at any given date etc.

        Author  : Manohar Kuse <mpkuse@connect.ust.hk>
        Created : 25th Mar, 2017
"""

from pymongo import MongoClient, DESCENDING, ASCENDING
from DBBase import DBBase
import code
import datetime

class QuotesQueries(DBBase):
    def __init__(self, args ):
        DBBase.__init__(self,args)
        self.quote_db = self.client.sun_dance.stock_quotes

    def lastest_quote( self, ticker ):
        """ input tickers eg,
            ticker="2333.HK" or
            ticker="2333.HK,1211.HK,AMZN.NASDAQ"
        """
        #pass
        i_ticker = self.to_json_list( colon_separated_list=ticker, key=None )

        to_return = {}
        for _t in i_ticker:
            query = {}
            query['ticker'] = _t

            result = self.quote_db.find( query ).sort( [('datetime',DESCENDING), ('inserted_on',DESCENDING)] ).limit(1)

            to_return[ _t ] = {}
            for r in result:
                del r['_id']
                del r['id']
                # print r
                to_return[ _t ] = r
        return to_return

    def range_quote( self, ticker, start_date, end_date ):
        """ input ticker and date range. WIll giveout quote data in daterange for all the tickers

        ticker="2333.HK" or
        ticker="2333.HK,1211.HK,AMZN.NASDAQ"

        start_date, end_date= "2017-03-26"

        """

        query = {}
        query['ticker'] = {}
        query['ticker']['$in'] = self.to_json_list( colon_separated_list=ticker, key=None )


        # query['datetime'] = { "$gt": _start_date, "$lt": _end_date }
        query['datetime'] = {}
        if start_date is not None:
            query['datetime']["$gt"] = datetime.datetime.strptime( start_date, '%Y-%m-%d' )
        if end_date is not None:
            query['datetime']["$lt"] = datetime.datetime.strptime( end_date, '%Y-%m-%d' )

        result = self.quote_db.find( query ).sort( [ ('ticker', ASCENDING), ('datetime', ASCENDING) ] )
        to_return = {}
        for r in result:
            del r['_id']
            del r['id']
            if r['ticker'] not in to_return.keys():
                to_return[ r['ticker'] ] = []


            to_return[ r['ticker']].append( r )
            # print r
        return to_return
