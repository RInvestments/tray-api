""" Base class for all the queries. Holds the Mongodb handle

        Author  : Manohar Kuse <mpkuse@connect.ust.hk>
        Created : 25th Feb, 2018
"""

from pymongo import MongoClient

class DBBase:
    def __init__(self, client):
        self.client = client 
        # self.db =



    def to_json_list( self, colon_separated_list, key, dtype=None ):
        """ Given a colon_separated_list string eg. '0175.HK:1211.HK:0875.HK:GOOG.NASDAQ'
        converts to json with the key as `key`. Eg.

        F = example to_json_list( '0175.HK:1211.HK:0875.HK:GOOG.NASDAQ', 'foo' )

        F = [ {'foo':'0175.HK'}, {'foo':'1211.HK'}, {'foo':'0875.HK'}, {'foo':'GOOG.NASDAQ'}  ]

        Valid values for dtype : ['int32', 'float32']
        """

        if dtype is not None:
            if dtype == 'int32':
                dtype_func = int
            else:
                if dtype == 'float32':
                    dtype_func = float
                else:
                    raise NameError( 'dtype should either be None (no conversion) or be either of [\'int32\', \'float32\']')


        F = []
        if dtype is None:
            for element in colon_separated_list.split(':'):
                if key is not None:
                    F.append( {key: element } )
                else:
                    F.append( element )
            return F
        else:
            for element in colon_separated_list.split(':'):
                if key is not None:
                    F.append( {key: dtype_func(element) } )
                else:
                    F.append( dtype_func(element) )
            return F
