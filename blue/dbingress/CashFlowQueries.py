""" Queries related to the Cashflow Statement. Will have individual functions
    for common thing like total operating cashflow etc.

        Author  : Manohar Kuse <mpkuse@connect.ust.hk>
        Created : 25th Feb, 2018
"""

from pymongo import MongoClient
from TickerQueries import TickerQueries


class CashFlowQueries(TickerQueries):
    def __init__(self, mongodb_uri ):
        TickerQueries.__init__(self,mongodb_uri)

    def tbz(self):
        print 'tbz'
