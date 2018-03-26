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
        self.db = self.client.universalData.universalData

    def getIndustryList(self, bourse=None ):
        query = {}
        query['type1'] = 'Profile'
        query['type2'] = 'companyName'

        if bourse is not None:
            query['bourse'] = {}
            query['bourse']['$in'] = self.to_json_list( colon_separated_list=bourse, key=None )

        result=self.db.aggregate( pipeline=[{'$match': query},{'$group': {'_id':'$industry'}} ]  )
        to_return = {}
        for p in result:
            _industry = p['_id']
            to_return[ _industry ] = {}
            # to_return.append( p['_id'] )

        return to_return


    def getSectorsOf(self, industry, bourse=None ):
        query = {}
        query['type1'] = 'Profile'
        query['type2'] = 'companyName'

        if bourse is not None:
            query['bourse'] = {}
            query['bourse']['$in'] = self.to_json_list( colon_separated_list=bourse, key=None )

        if industry is not None:
            query['industry'] = {}
            query['industry']['$in'] = self.to_json_list( colon_separated_list=industry, key=None )

        result=self.db.aggregate( pipeline=[
                                {'$match': query},
                                {'$group':
                                        {'_id':{'sector' : '$sector', 'industry': '$industry' } }
                                } ] )
        to_return = {}
        for p in result:
            _industry = p['_id']['industry']
            _sector = p['_id']['sector']

            if _industry not in to_return.keys():
                to_return[_industry] = {}

            if _sector not in to_return[_industry].keys():
                to_return[_industry][_sector] = {}
            # to_return.append( p['_id'] )

        return to_return

    def getTickersOf( self, industry, sector, bourse=None ):
        query = {}
        query['type1'] = 'Profile'
        query['type2'] = 'companyName'

        if bourse is not None:
            query['bourse'] = {}
            query['bourse']['$in'] = self.to_json_list( colon_separated_list=bourse, key=None )

        if industry is not None:
            query['industry'] = {}
            query['industry']['$in'] = self.to_json_list( colon_separated_list=industry, key=None )

        if sector is not None:
            query['sector'] = {}
            query['sector']['$in'] = self.to_json_list( colon_separated_list=sector, key=None )

        pcursor = self.db.find( query )

        to_return = {}
        for p in pcursor:
            # print p['ticker'], p['industry'], p['sector']
            _ticker = p['ticker']
            _industry = p['industry']
            _sector = p['sector']

            if _industry not in to_return.keys():
                to_return[ _industry ] = {}

            if _sector not in to_return[_industry].keys():
                to_return[ _industry ][ _sector ] = {}

            if _ticker not in to_return[_industry][_sector].keys():
                to_return[_industry][_sector][_ticker] = {'companyName': p['value_string']}

        return to_return
