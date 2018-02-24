""" All sector related queries. In the future also have cummulation queries here.
    For example, total Automotive revenue, total Automotive growth etc.

        Author  : Manohar Kuse <mpkuse@connect.ust.hk>
        Created : 25th Feb, 2018
"""

from pymongo import MongoClient
from DBBase import DBBase


class SectorQueries(DBBase):
    def __init__(self, mongodb_uri ):
        DBBase.__init__(self,mongodb_uri)

    def getTickersIn( self, sector ):
        pass
