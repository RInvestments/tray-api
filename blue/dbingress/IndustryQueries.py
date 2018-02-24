""" All industry related queries. In the future also have cummulation queries here.
    For example, total industry revenue, total industry grown etc.

        Author  : Manohar Kuse <mpkuse@connect.ust.hk>
        Created : 25th Feb, 2018
"""

from pymongo import MongoClient
from DBBase import DBBase


class IndustryQueries(DBBase):
    def __init__(self, mongodb_uri ):
        DBBase.__init__(self,mongodb_uri)

    def getIndustryList(self, ticker ):
        pass

    def getSectorsOf(self, industry ):
        pass
