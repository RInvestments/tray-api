from blue.config import q_ticker
from blue.config import q_income
from blue.config import q_balance_sht
from blue.config import q_cashflw
from blue.config import q_industry
from blue.config import q_quotes



from pprint import pprint


q_quotes.lastest_quote( '2333.HK:1211.HK:AMZN.NASDAQ')
quit()

industry_list =  q_industry.getIndustryList( 'BSE:HK' )
print industry_list
# pprint( q_industry.getSectorsOf( 'Transportation/Logistics', bourse='NASDAQ' ), indent=2 )

# Y = q_industry.getTickersOf( 'Automotive', 'Automobiles:Tires', "HK" )
# quit()

##################################
ticker = 'GOOG.NASDAQ'
# ticker = '1301.TYO'
ticker = '0857.HK:0005.HK'
# ticker = '000001.SZ'
# ticker = '600000.SH'
# ticker = '20MICRONS.NSE'
# ticker = '500002.BSE'

ticker = '0175.HK:1211.HK:0857.HK:GOOG.NASDAQ:20MICRONS.NSE'
pprint( q_ticker.getName( ticker ) )
pprint( q_ticker.getIndustry( ticker ) )
# quit()
# print q_ticker.getSector( ticker )
# pprint( q_ticker.getDescription( ticker ) )
# pprint(  q_ticker.getEmployeesCount( ticker ) )
# pprint( q_ticker.getStreetAddress( ticker ) )
# quit()

# q_income.jdk()
# q_balance_sht.y2k()
# q_cashflw.tbz()
# X = q_ticker.getIncomeStatementDetails( ticker, '2015:2016', '_FISCAL_NOTE_', return_raw=True)
# print q_ticker.getIncomeStatementDetails( ticker, 2015, 'Sales/Revenue', return_raw=True)
# print q_ticker.getIncomeStatementDetails( ticker, 2015, '_FISCAL_NOTE_', return_raw=True)

# X = q_ticker.getIncomeStatementDetails( ticker, '2015:2016', 'Sales/Revenue:Cost of Goods Sold (COGS) incl. D&A')
# quit()
# X = q_ticker.getIncomeStatementDetails( ticker, None, None )
# X = q_ticker.getBalanceSheetAssetsDetails( ticker, 2015, 'Total Investments and Advances:Net Property, Plant & Equipment:Total Accounts Receivable', return_raw=True)
# X =  q_ticker.getBalanceSheetLiabilitiesDetails( ticker, 2015, 'Provision for Risks & Charges:Deferred Taxes:Other Current Liabilities', return_raw=True)
# X =  q_ticker.getCashFlowOperatingActivityDetails( ticker, 2015, 'Funds from Operations:Net Operating Cash Flow', return_raw=True)
# X =  q_ticker.getCashFlowInvestingActivityDetails( ticker, 2015, 'Net Investing Cash Flow:Purchase/Sale of Investments', return_raw=True)
# X =  q_ticker.getCashFlowFinancingActivityDetails( ticker, 2015, None, return_raw=True)

X = q_ticker.getAccountingCurrency(ticker,2015)
pprint( X )
quit()
