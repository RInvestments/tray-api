""" Queries related to the Balance Sheet. Will have individual functions
    for common thing like total assets etc, current liabilities.

        Author  : Manohar Kuse <mpkuse@connect.ust.hk>
        Created : 25th Feb, 2018
"""

from pymongo import MongoClient
from TickerQueries import TickerQueries


class BalanceSheetQueries(TickerQueries):
    def __init__(self, mongodb_uri ):
        TickerQueries.__init__(self,mongodb_uri)

    def y2k(self):
        print 'y2k'
