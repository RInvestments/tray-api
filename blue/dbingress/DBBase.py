""" Base class for all the queries. Holds the Mongodb handle

        Author  : Manohar Kuse <mpkuse@connect.ust.hk>
        Created : 25th Feb, 2018
"""

from pymongo import MongoClient

class DBBase:
    def __init__(self, mongodb_uri):
        #TODO: Have a try-except block and error reporting.
        print 'Connecting to ', mongodb_uri
        self.client = MongoClient( mongodb_uri )
        # self.db =
