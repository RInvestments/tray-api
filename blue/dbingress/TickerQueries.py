""" Basic queries related to a `ticker`

        Author  : Manohar Kuse <mpkuse@connect.ust.hk>
        Created : 25th Feb, 2018
"""

from pymongo import MongoClient
from DBBase import DBBase

class TickerQueries(DBBase):
    def __init__(self, mongodb_uri ):
        DBBase.__init__(self,mongodb_uri)
        self.db = self.client.universalData.universalData

    def getName(self, ticker ):
        p = self.db.find_one( {'ticker':'%s' %(ticker), 'type1':'Profile', 'type2':'companyName'} )
        try:
            return p['value_string']
        except:
            return None

    def getIndustry(self, ticker ):
        p = self.db.find_one( {'ticker':'%s' %(ticker), 'type1':'Profile', 'type2':'companyName'} )
        try:
            return p['industry']
        except:
            return None

    def getSector( self, ticker ):
        p = self.db.find_one( {'ticker':'%s' %(ticker), 'type1':'Profile', 'type2':'companyName'} )
        try:
            return p['sector']
        except:
            return None

    def getDescription( self, ticker ):
        p = self.db.find_one( {'ticker':'%s' %(ticker), 'type1':'Profile', 'type2':'Description'} )
        try:
            return p['value_string']
        except:
            return None

    def getEmployeesCount( self, ticker ):
        p = self.db.find_one( {'ticker':'%s' %(ticker), 'type1':'Profile', 'type2':'Company Info', 'type3':'Employees'} )
        try:
            return p['val']
        except:
            return None

    def getStreetAddress( self, ticker ):
        p = self.db.find_one( {'ticker':'%s' %(ticker), 'type1':'Profile', 'type2':'Contact Address'} )
        try:
            return p['value_string']
        except:
            return None


    def getFiscalNote(self, ticker, year):
        return self.getIncomeStatementDetails( ticker, year, '_FISCAL_NOTE_', return_raw=True)
        # print self.getBalanceSheetAssetsDetails( ticker, year, '_FISCAL_NOTE_', return_raw=True)
        # print self.getBalanceSheetLiabilitiesDetails( ticker, year, '_FISCAL_NOTE_', return_raw=True)
        # print self.getCashFlowOperatingActivityDetails( ticker, year, '_FISCAL_NOTE_', return_raw=True)
        # print self.getCashFlowInvestingActivityDetails( ticker, year, '_FISCAL_NOTE_', return_raw=True)
        # print self.getCashFlowFinancingActivityDetails( ticker, year, '_FISCAL_NOTE_', return_raw=True)



    def getAccountingCurrency(self, ticker, year ):
        sentence = self.getIncomeStatementDetails( ticker, year, '_FISCAL_NOTE_', return_raw=True)
        if sentence is None:
            return None
        words = sentence.split( ' ')
        for i, w in enumerate(words):
            if w.find( 'Thousand' ) >= 0:
                return words[i-1]
            if w.find( 'Million' ) >= 0:
                return words[i-1]
            if w.find( 'Billion' ) >= 0:
                return words[i-1]
            if w.find( 'Trillion' ) >= 0:
                return words[i-1]
        return None

    def getAccountingCurrencyUnit(self, ticker, year ):
        sentence = self.getIncomeStatementDetails( ticker, year, '_FISCAL_NOTE_', return_raw=True)
        if sentence is None:
            return None
        words = sentence.split( ' ')
        for i, w in enumerate(words):
            if w.find( 'Thousand' ) >= 0:
                return 1000.
            if w.find( 'Million' ) >= 0:
                return 1000000.
            if w.find( 'Billion' ) >= 0:
                return 1000000000.
            if w.find( 'Trillion' ) >= 0:
                return 1000000000000.
        return None


    def getIncomeStatementDetails( self, ticker, year, item_string1, item_string2='None', item_string3='None', return_raw=False ):
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements', 'type2':'income_statement', 'type3':'None', 'type4':2016, 'type5':'Sales/Revenue', 'type6':'None', 'type7':'None' } )
        query = {}

        query['ticker'] = ticker
        query['type1'] = 'Financial Statements'
        query['type2'] = 'income_statement'
        # query['period'] = 'a'

        if year is not None:
            query['type4'] = year

        query['type5'] = item_string1#'Sales/Revenue'
        query['type6'] = item_string2#'None'
        query['type7'] = item_string3#'None'

        result=self.db.find_one( query )

        if result is not None:
            # return result['val']
            if return_raw:
                return result['value_string']
            return float(result['val']) * float(result['fiscal_mul'])
        else:
            return None

    def getBalanceSheetAssetsDetails( self, ticker, year, item_string='None', item_string2='None', item_string3='None', return_raw=False ):
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements', 'type2':'balance_sheet', 'type3':'assets', 'type4':2016, 'type5':'Total Accounts Receivable', 'type6':'None', 'type7':'None'} )
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements',
        #'type2':'balance_sheet', 'type3':'assets', 'type4':2016,
        #'type5':'Total Accounts Receivable', 'type6':'None', 'type7':'None'} )

        query = {}

        query['ticker'] = str(ticker)
        query['type1'] = 'Financial Statements'
        query['type2'] = 'balance_sheet'
        query['type3'] = 'assets'
        # query['period'] = 'a'

        if year is not None:
            query['type4'] = year

        query['type5'] = item_string#'Total Assets'
        query['type6'] = item_string2#'None'
        query['type7'] = item_string3#'None'

        # return str(query)
        result=self.db.find_one( query  )


        if result is not None:
            if return_raw :
                return result['value_string']

            return float(result['val']) * float(result['fiscal_mul'])
        else:
            return None


    def getBalanceSheetLiabilitiesDetails( self, ticker, year, item_string='None', item_string2='None', item_string3='None', return_raw=False ):
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements', 'type2':'balance_sheet', 'type3':'assets', 'type4':2016, 'type5':'Total Accounts Receivable', 'type6':'None', 'type7':'None'} )
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements',
        #'type2':'balance_sheet', 'type3':'assets', 'type4':2016,
        #'type5':'Total Accounts Receivable', 'type6':'None', 'type7':'None'} )

        query = {}

        query['ticker'] = str(ticker)
        query['type1'] = 'Financial Statements'
        query['type2'] = 'balance_sheet'
        query['type3'] = 'liabilities'
        # query['period'] = 'a'

        if year is not None:
            query['type4'] = year

        query['type5'] = item_string#'Total Assets'
        query['type6'] = item_string2#'None'
        query['type7'] = item_string3#'None'
        # return str(query)

        result=self.db.find_one( query  )

        if result is not None:
            if return_raw :
                return result['value_string']
            return float(result['val']) * float(result['fiscal_mul'])
        else:
            return None


    #TODO implement getCashFlowOperatingActivityDetails, getCashFlowInvestingActivityDetails, getCashFlowFinancingActivityDetails
    def getCashFlowOperatingActivityDetails( self, ticker, year, item_string='None', item_string2='None', item_string3='None', return_raw=False ):
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements', 'type2':'cash_flow_statement', 'type3':'operating', 'type4':2016, 'type5':'Other Funds', 'type6':'None', 'type7':'None'})
        #db.getCollection('universalData').find({'ticker':'2333.HK',
        #   'type1':'Financial Statements', 'type2':'cash_flow_statement',
        #   'type3':'operating', 'type4':2016,
        #   'type5':'Other Funds', 'type6':'None', 'type7':'None'})
        query = {}

        query['ticker'] = str(ticker)
        query['type1'] = 'Financial Statements'
        query['type2'] = 'cash_flow_statement'
        query['type3'] = 'operating'
        # query['period'] = 'a'

        if year is not None:
            query['type4'] = year


        query['type5'] = item_string#'Total Assets'
        query['type6'] = item_string2#'None'
        query['type7'] = item_string3#'None'
        # return str(query)

        result=self.db.find_one( query  )

        if result is not None:
            if return_raw :
                return result['value_string']
            return float(result['val']) * float(result['fiscal_mul'])
        else:
            return None


    def getCashFlowInvestingActivityDetails( self, ticker, year, item_string='None', item_string2='None', item_string3='None', return_raw=False ):
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements', 'type2':'cash_flow_statement', 'type3':'operating', 'type4':2016, 'type5':'Other Funds', 'type6':'None', 'type7':'None'})
        #db.getCollection('universalData').find({'ticker':'2333.HK',
        #   'type1':'Financial Statements', 'type2':'cash_flow_statement',
        #   'type3':'operating', 'type4':2016,
        #   'type5':'Other Funds', 'type6':'None', 'type7':'None'})
        query = {}

        query['ticker'] = str(ticker)
        query['type1'] = 'Financial Statements'
        query['type2'] = 'cash_flow_statement'
        query['type3'] = 'investing'
        # query['period'] = 'a'

        if year is not None:
            query['type4'] = year


        query['type5'] = item_string#'Total Assets'
        query['type6'] = item_string2#'None'
        query['type7'] = item_string3#'None'
        # return str(query)

        result=self.db.find_one( query  )

        if result is not None:
            if return_raw :
                return result['value_string']
            return float(result['val']) * float(result['fiscal_mul'])
        else:
            return None


    def getCashFlowFinancingActivityDetails( self, ticker, year, item_string='None', item_string2='None', item_string3='None', return_raw=False ):
        #db.getCollection('universalData').find({'ticker':'2333.HK', 'type1':'Financial Statements', 'type2':'cash_flow_statement', 'type3':'operating', 'type4':2016, 'type5':'Other Funds', 'type6':'None', 'type7':'None'})
        #db.getCollection('universalData').find({'ticker':'2333.HK',
        #   'type1':'Financial Statements', 'type2':'cash_flow_statement',
        #   'type3':'operating', 'type4':2016,
        #   'type5':'Other Funds', 'type6':'None', 'type7':'None'})
        query = {}

        query['ticker'] = str(ticker)
        query['type1'] = 'Financial Statements'
        query['type2'] = 'cash_flow_statement'
        query['type3'] = 'financing'
        # query['period'] = 'a'

        if year is not None:
            query['type4'] = year


        query['type5'] = item_string#'Total Assets'
        query['type6'] = item_string2#'None'
        query['type7'] = item_string3#'None'
        # return str(query)

        result=self.db.find_one( query  )

        if result is not None:
            if return_raw :
                return result['value_string']
            return float(result['val']) * float(result['fiscal_mul'])
        else:
            return None
