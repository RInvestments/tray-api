""" Queries related quotes data. For example, functions here can giveout the
latest open price of stock, quote open price at any given date etc.

        Author  : Manohar Kuse <mpkuse@connect.ust.hk>
        Created : 25th Mar, 2017
"""

from pymongo import MongoClient, DESCENDING
from DBBase import DBBase
import code

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
                print r
                to_return[ _t ] = r


        code.interact( local=locals() )
