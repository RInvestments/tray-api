""" Queries related to the Income statement. Will have individual functions
    for common thing like revenues etc.

        Author  : Manohar Kuse <mpkuse@connect.ust.hk>
        Created : 25th Feb, 2018
"""


from pymongo import MongoClient
from TickerQueries import TickerQueries


class IncomeStatementQueries(TickerQueries):
    def __init__(self, mongodb_uri ):
        TickerQueries.__init__(self,mongodb_uri)

    def jdk(self):
        print 'jdk'
