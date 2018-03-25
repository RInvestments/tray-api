""" Basic queries related to a `ticker`

        Author  : Manohar Kuse <mpkuse@connect.ust.hk>
        Created : 25th Feb, 2018
"""

from pymongo import MongoClient
from DBBase import DBBase
import code

class TickerQueries(DBBase):
    def __init__(self, mongodb_uri ):
        DBBase.__init__(self,mongodb_uri)
        self.db = self.client.universalData.universalData

    def getName(self, ticker ):
        ticker_list = self.to_json_list( colon_separated_list=ticker, key='ticker' )

        pcursor = self.db.find( { "$or": ticker_list , 'type1':'Profile', 'type2':'companyName'}    )

        to_return = {}
        for p in pcursor:
            to_return[ p['ticker'] ] = p['company']
        return to_return


    def getIndustry(self, ticker ):
        # ticker_list = []
        # for tick in ticker.split(':'):
        #     ticker_list.append( {'ticker': tick } )
        ticker_list = self.to_json_list( colon_separated_list=ticker, key='ticker' )


        pcursor = self.db.find( { "$or": ticker_list , 'type1':'Profile', 'type2':'companyName'}    )

        to_return = {}
        for p in pcursor:
            to_return[ p['ticker'] ] = p['industry']
        return to_return


    def getSector( self, ticker ):
        # ticker_list = []
        # for tick in ticker.split(':'):
            # ticker_list.append( {'ticker': tick } )
        ticker_list = self.to_json_list( colon_separated_list=ticker, key='ticker' )

        pcursor = self.db.find( { "$or": ticker_list , 'type1':'Profile', 'type2':'companyName'}    )

        to_return = {}
        for p in pcursor:
            to_return[ p['ticker'] ] = p['sector']
        return to_return

    def getDescription( self, ticker ):
        # ticker_list = []
        # for tick in ticker.split(':'):
            # ticker_list.append( {'ticker': tick } )
        ticker_list = self.to_json_list( colon_separated_list=ticker, key='ticker' )


        pcursor = self.db.find( { "$or": ticker_list ,  'type1':'Profile', 'type2':'Description'}    )

        to_return = {}
        for p in pcursor:
            to_return[ p['ticker'] ] = p['value_string']
        return to_return



    def getEmployeesCount( self, ticker ):
        # ticker_list = []
        # for tick in ticker.split(':'):
            # ticker_list.append( {'ticker': tick } )
        ticker_list = self.to_json_list( colon_separated_list=ticker, key='ticker' )

        pcursor = self.db.find( { "$or": ticker_list ,  'type1':'Profile', 'type2':'Company Info', 'type3':'Employees'}    )

        to_return = {}
        for p in pcursor:
            to_return[ p['ticker'] ] = p['value_string']
        return to_return


    def getStreetAddress( self, ticker ):
        # ticker_list = []
        # for tick in ticker.split(':'):
            # ticker_list.append( {'ticker': tick } )
        ticker_list = self.to_json_list( colon_separated_list=ticker, key='ticker' )

        pcursor = self.db.find( { "$or": ticker_list ,   'type1':'Profile', 'type2':'Contact Address'}    )

        to_return = {}
        for p in pcursor:
            to_return[ p['ticker'] ] = p['value_string']
        return to_return



    def getFiscalNote(self, ticker, year):
        return self.getIncomeStatementDetails( ticker, year, '_FISCAL_NOTE_', return_raw=True)
        # print self.getBalanceSheetAssetsDetails( ticker, year, '_FISCAL_NOTE_', return_raw=True)
        # print self.getBalanceSheetLiabilitiesDetails( ticker, year, '_FISCAL_NOTE_', return_raw=True)
        # print self.getCashFlowOperatingActivityDetails( ticker, year, '_FISCAL_NOTE_', return_raw=True)
        # print self.getCashFlowInvestingActivityDetails( ticker, year, '_FISCAL_NOTE_', return_raw=True)
        # print self.getCashFlowFinancingActivityDetails( ticker, year, '_FISCAL_NOTE_', return_raw=True)



    def getAccountingCurrency(self, ticker, year ):
        xjson = self.getIncomeStatementDetails( ticker, year, '_FISCAL_NOTE_', return_raw=True)

        for _ticker in xjson.keys():
            for _year in xjson[_ticker].keys():
                try:
                    sentence = xjson[_ticker][_year]['_FISCAL_NOTE_']
                except:
                    sentence = None

                if sentence is None:
                    continue

                words = sentence.split( ' ')
                for i, w in enumerate(words):
                    if w.find( 'Thousand' ) >= 0:
                        xjson[_ticker][_year]['Currency'] = words[i-1]
                        xjson[_ticker][_year]['Currency Unit'] = 1000.
                        xjson[_ticker][_year]['Currency Unit Word'] = 'Thousand'

                    if w.find( 'Million' ) >= 0:
                        xjson[_ticker][_year]['Currency'] = words[i-1]
                        xjson[_ticker][_year]['Currency Unit'] = 1000000.
                        xjson[_ticker][_year]['Currency Unit Word'] = 'Million'

                    if w.find( 'Billion' ) >= 0:
                        xjson[_ticker][_year]['Currency'] = words[i-1]
                        xjson[_ticker][_year]['Currency Unit'] = 1000000000.
                        xjson[_ticker][_year]['Currency Unit Word'] = 'Billion'

                    if w.find( 'Trillion' ) >= 0:
                        xjson[_ticker][_year]['Currency'] = words[i-1]
                        xjson[_ticker][_year]['Currency Unit'] = 1000000000000.
                        xjson[_ticker][_year]['Currency Unit Word'] = 'Trillion'

        return xjson



    def getIncomeStatementDetails( self, ticker, year, item_string1, item_string2='None', item_string3='None', return_raw=False ):
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements', 'type2':'income_statement', 'type3':'None', 'type4':2016, 'type5':'Sales/Revenue', 'type6':'None', 'type7':'None' } )

        # Also implement REGEX for ticker, year and item_string1
        query = {}

        query['ticker'] = {}
        query['ticker']['$in'] = self.to_json_list( colon_separated_list=ticker, key=None )

        query['type1'] = 'Financial Statements'
        query['type2'] = 'income_statement'
        # query['period'] = 'a'

        if year is not None:
            query['type4'] = {}
            query['type4']['$in'] = self.to_json_list( colon_separated_list=str(year), key=None, dtype='int32' )
            # query['$or'] = year_list


        # query['type5'] = item_string1#'Sales/Revenue'
        if item_string1 is not None:
            query['type5'] = {}
            query['type5']['$in'] = self.to_json_list( colon_separated_list=str(item_string1), key=None )
        query['type6'] = item_string2#'None'
        query['type7'] = item_string3#'None'


        pcursor = self.db.find( query )


        to_return = {}
        for p in pcursor:
            #print '---'
            #print p['ticker']
            #print p['type4'] # year
            #print item_string1, p['value_string'] # raw value
            #print item_string1, float(p['val']) * float(p['fiscal_mul']) # processed and uniformed value. Will be in Millions, but in local currency

            if p['ticker'] not in to_return.keys():
                to_return[ p['ticker'] ] = {}

            if  p['type4'] not in to_return[ p['ticker'] ].keys():
                to_return[ p['ticker'] ][ p['type4'] ] = {}

            if p['type5'] not in to_return[ p['ticker'] ][ p['type4'] ]:

                # Select betrween raw or processed

                Kx = p['type5']
                if return_raw:
                    to_return[ p['ticker'] ][ p['type4'] ][ Kx ] = p['value_string']
                else:
                    to_return[ p['ticker'] ][ p['type4'] ][ Kx ] = float(p['val']) * float(p['fiscal_mul'])
        return to_return

        # result=self.db.find_one( query )
        #
        # if result is not None:
        #     # return result['val']
        #     if return_raw:
        #         return result['value_string']
        #     return float(result['val']) * float(result['fiscal_mul'])
        # else:
        #     return None

    def getBalanceSheetAssetsDetails( self, ticker, year, item_string='None', item_string2='None', item_string3='None', return_raw=False ):
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements', 'type2':'balance_sheet', 'type3':'assets', 'type4':2016, 'type5':'Total Accounts Receivable', 'type6':'None', 'type7':'None'} )
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements',
        #'type2':'balance_sheet', 'type3':'assets', 'type4':2016,
        #'type5':'Total Accounts Receivable', 'type6':'None', 'type7':'None'} )

        query = {}

        #query['ticker'] = str(ticker)
        query['ticker'] = {}
        query['ticker']['$in'] = self.to_json_list( colon_separated_list=ticker, key=None )
        query['type1'] = 'Financial Statements'
        query['type2'] = 'balance_sheet'
        query['type3'] = 'assets'
        # query['period'] = 'a'

        if year is not None:
            #query['type4'] = year
            query['type4'] = {}
            query['type4']['$in'] = self.to_json_list( colon_separated_list=str(year), key=None, dtype='int32' )

        if item_string is not None:
            query['type5'] = {}
            query['type5']['$in'] = self.to_json_list(colon_separated_list=str(item_string), key=None )#'Total Assets'
        query['type6'] = item_string2#'None'
        query['type7'] = item_string3#'None'



        # return str(query)
        pcursor = self.db.find( query )


        to_return = {}
        for p in pcursor:
            #print '---'
            #print p['ticker']
            #print p['type4'] # year
            #print item_string, p['value_string'] # raw value
            #print item_string, float(p['val']) * float(p['fiscal_mul']) # processed and uniformed value. Will be in Millions, but in local currency

            if p['ticker'] not in to_return.keys():
                to_return[ p['ticker'] ] = {}

            if  p['type4'] not in to_return[ p['ticker'] ].keys():
                to_return[ p['ticker'] ][ p['type4'] ] = {}

            if p['type5'] not in to_return[ p['ticker'] ][ p['type4'] ]:

                # Select betrween raw or processed
                Kx = p['type5']
                if return_raw:
                    to_return[ p['ticker'] ][ p['type4'] ][ Kx ] = p['value_string']
                else:
                    to_return[ p['ticker'] ][ p['type4'] ][ Kx ] = float(p['val']) * float(p['fiscal_mul'])
        return to_return


        # result=self.db.find_one( query  )
        #
        # if result is not None:
        #     if return_raw :
        #         return result['value_string']
        #
        #     return float(result['val']) * float(result['fiscal_mul'])
        # else:
        #     return None


    def getBalanceSheetLiabilitiesDetails( self, ticker, year, item_string='None', item_string2='None', item_string3='None', return_raw=False ):
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements', 'type2':'balance_sheet', 'type3':'assets', 'type4':2016, 'type5':'Total Accounts Receivable', 'type6':'None', 'type7':'None'} )
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements',
        #'type2':'balance_sheet', 'type3':'assets', 'type4':2016,
        #'type5':'Total Accounts Receivable', 'type6':'None', 'type7':'None'} )

        query = {}

        #query['ticker'] = str(ticker)
        query['ticker'] = {}
        query['ticker']['$in'] = self.to_json_list( colon_separated_list=ticker, key=None )
        query['type1'] = 'Financial Statements'
        query['type2'] = 'balance_sheet'
        query['type3'] = 'liabilities'
        # query['period'] = 'a'

        if year is not None:
            #query['type4'] = year
            query['type4'] = {}
            query['type4']['$in'] = self.to_json_list( colon_separated_list=str(year), key=None, dtype='int32' )

        if item_string is not None:
            query['type5'] = {}
            query['type5']['$in'] = self.to_json_list(colon_separated_list=str(item_string), key=None )#'Total Assets'
        query['type6'] = item_string2#'None'
        query['type7'] = item_string3#'None'
        # return str(query)

        pcursor = self.db.find( query )


        to_return = {}
        for p in pcursor:
            #print '---'
            #print p['ticker']
            #print p['type4'] # year
            #print item_string, p['value_string'] # raw value
            #print item_string, float(p['val']) * float(p['fiscal_mul']) # processed and uniformed value. Will be in Millions, but in local currency

            if p['ticker'] not in to_return.keys():
                to_return[ p['ticker'] ] = {}

            if  p['type4'] not in to_return[ p['ticker'] ].keys():
                to_return[ p['ticker'] ][ p['type4'] ] = {}

            if p['type5'] not in to_return[ p['ticker'] ][ p['type4'] ]:

                # Select betrween raw or processed
                Kx = p['type5']
                if return_raw:
                    to_return[ p['ticker'] ][ p['type4'] ][ Kx ] = p['value_string']
                else:
                    to_return[ p['ticker'] ][ p['type4'] ][ Kx ] = float(p['val']) * float(p['fiscal_mul'])
        return to_return


        # result=self.db.find_one( query  )
        #
        # if result is not None:
        #     if return_raw :
        #         return result['value_string']
        #     return float(result['val']) * float(result['fiscal_mul'])
        # else:
        #     return None


    #TODO implement getCashFlowOperatingActivityDetails, getCashFlowInvestingActivityDetails, getCashFlowFinancingActivityDetails
    def getCashFlowOperatingActivityDetails( self, ticker, year, item_string='None', item_string2='None', item_string3='None', return_raw=False ):
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements', 'type2':'cash_flow_statement', 'type3':'operating', 'type4':2016, 'type5':'Other Funds', 'type6':'None', 'type7':'None'})
        #db.getCollection('universalData').find({'ticker':'2333.HK',
        #   'type1':'Financial Statements', 'type2':'cash_flow_statement',
        #   'type3':'operating', 'type4':2016,
        #   'type5':'Other Funds', 'type6':'None', 'type7':'None'})
        query = {}

        #query['ticker'] = str(ticker)
        query['ticker'] = {}
        query['ticker']['$in'] = self.to_json_list( colon_separated_list=ticker, key=None )
        query['type1'] = 'Financial Statements'
        query['type2'] = 'cash_flow_statement'
        query['type3'] = 'operating'
        # query['period'] = 'a'

        if year is not None:
            #query['type4'] = year
            query['type4'] = {}
            query['type4']['$in'] = self.to_json_list( colon_separated_list=str(year), key=None, dtype='int32' )


        if item_string is not None:
            query['type5'] = {}
            query['type5']['$in'] = self.to_json_list(colon_separated_list=str(item_string), key=None )#'Total Assets'
        query['type6'] = item_string2#'None'
        query['type7'] = item_string3#'None'
        # return str(query)

        pcursor = self.db.find( query )


        to_return = {}
        for p in pcursor:
            #print '---'
            #print p['ticker']
            #print p['type4'] # year
            #print item_string, p['value_string'] # raw value
            #print item_string, float(p['val']) * float(p['fiscal_mul']) # processed and uniformed value. Will be in Millions, but in local currency

            if p['ticker'] not in to_return.keys():
                to_return[ p['ticker'] ] = {}

            if  p['type4'] not in to_return[ p['ticker'] ].keys():
                to_return[ p['ticker'] ][ p['type4'] ] = {}

            if p['type5'] not in to_return[ p['ticker'] ][ p['type4'] ]:

                # Select betrween raw or processed
                Kx = p['type5']
                if return_raw:
                    to_return[ p['ticker'] ][ p['type4'] ][ Kx ] = p['value_string']
                else:
                    to_return[ p['ticker'] ][ p['type4'] ][ Kx ] = float(p['val']) * float(p['fiscal_mul'])
        return to_return


        # result=self.db.find_one( query  )
        #
        # if result is not None:
        #     if return_raw :
        #         return result['value_string']
        #     return float(result['val']) * float(result['fiscal_mul'])
        # else:
        #     return None


    def getCashFlowInvestingActivityDetails( self, ticker, year, item_string='None', item_string2='None', item_string3='None', return_raw=False ):
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements', 'type2':'cash_flow_statement', 'type3':'operating', 'type4':2016, 'type5':'Other Funds', 'type6':'None', 'type7':'None'})
        #db.getCollection('universalData').find({'ticker':'2333.HK',
        #   'type1':'Financial Statements', 'type2':'cash_flow_statement',
        #   'type3':'operating', 'type4':2016,
        #   'type5':'Other Funds', 'type6':'None', 'type7':'None'})
        query = {}

        #query['ticker'] = str(ticker)
        query['ticker'] = {}
        query['ticker']['$in'] = self.to_json_list( colon_separated_list=ticker, key=None )
        query['type1'] = 'Financial Statements'
        query['type2'] = 'cash_flow_statement'
        query['type3'] = 'investing'
        # query['period'] = 'a'

        if year is not None:
            #query['type4'] = year
            query['type4'] = {}
            query['type4']['$in'] = self.to_json_list( colon_separated_list=str(year), key=None, dtype='int32' )


        if item_string is not None:
            query['type5'] = {}
            query['type5']['$in'] = self.to_json_list(colon_separated_list=str(item_string), key=None )#'Total Assets'
        query['type6'] = item_string2#'None'
        query['type7'] = item_string3#'None'
        # return str(query)

        pcursor = self.db.find( query )


        to_return = {}
        for p in pcursor:
            #print '---'
            #print p['ticker']
            #print p['type4'] # year
            #print item_string, p['value_string'] # raw value
            #print item_string, float(p['val']) * float(p['fiscal_mul']) # processed and uniformed value. Will be in Millions, but in local currency

            if p['ticker'] not in to_return.keys():
                to_return[ p['ticker'] ] = {}

            if  p['type4'] not in to_return[ p['ticker'] ].keys():
                to_return[ p['ticker'] ][ p['type4'] ] = {}

            if p['type5'] not in to_return[ p['ticker'] ][ p['type4'] ]:

                # Select betrween raw or processed
                Kx = p['type5']
                if return_raw:
                    to_return[ p['ticker'] ][ p['type4'] ][ Kx ] = p['value_string']
                else:
                    to_return[ p['ticker'] ][ p['type4'] ][ Kx ] = float(p['val']) * float(p['fiscal_mul'])
        return to_return


        # result=self.db.find_one( query  )
        #
        # if result is not None:
        #     if return_raw :
        #         return result['value_string']
        #     return float(result['val']) * float(result['fiscal_mul'])
        # else:
        #     return None


    def getCashFlowFinancingActivityDetails( self, ticker, year, item_string='None', item_string2='None', item_string3='None', return_raw=False ):
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements', 'type2':'cash_flow_statement', 'type3':'operating', 'type4':2016, 'type5':'Other Funds', 'type6':'None', 'type7':'None'})
        #db.getCollection('universalData').find({'ticker':'2333.HK',
        #   'type1':'Financial Statements', 'type2':'cash_flow_statement',
        #   'type3':'operating', 'type4':2016,
        #   'type5':'Other Funds', 'type6':'None', 'type7':'None'})
        query = {}

        #query['ticker'] = str(ticker)
        query['ticker'] = {}
        query['ticker']['$in'] = self.to_json_list( colon_separated_list=ticker, key=None )
        query['type1'] = 'Financial Statements'
        query['type2'] = 'cash_flow_statement'
        query['type3'] = 'financing'
        # query['period'] = 'a'

        if year is not None:
            #query['type4'] = year
            query['type4'] = {}
            query['type4']['$in'] = self.to_json_list( colon_separated_list=str(year), key=None, dtype='int32' )


        if item_string is not None:
            query['type5'] = {}
            query['type5']['$in'] = self.to_json_list(colon_separated_list=str(item_string), key=None )#'Total Assets'
        query['type6'] = item_string2#'None'
        query['type7'] = item_string3#'None'
        # return str(query)

        pcursor = self.db.find( query )


        to_return = {}
        for p in pcursor:
            #print '---'
            #print p['ticker']
            #print p['type4'] # year
            #print item_string, p['value_string'] # raw value
            #print item_string, float(p['val']) * float(p['fiscal_mul']) # processed and uniformed value. Will be in Millions, but in local currency

            if p['ticker'] not in to_return.keys():
                to_return[ p['ticker'] ] = {}

            if  p['type4'] not in to_return[ p['ticker'] ].keys():
                to_return[ p['ticker'] ][ p['type4'] ] = {}

            if p['type5'] not in to_return[ p['ticker'] ][ p['type4'] ]:

                # Select betrween raw or processed
                Kx = p['type5']
                if return_raw:
                    to_return[ p['ticker'] ][ p['type4'] ][ Kx ] = p['value_string']
                else:
                    to_return[ p['ticker'] ][ p['type4'] ][ Kx ] = float(p['val']) * float(p['fiscal_mul'])
        return to_return


        # result=self.db.find_one( query  )
        #
        # if result is not None:
        #     if return_raw :
        #         return result['value_string']
        #     return float(result['val']) * float(result['fiscal_mul'])
        # else:
        #     return None
