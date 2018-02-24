from blue.config import q_ticker
from blue.config import q_income
from blue.config import q_balance_sht
from blue.config import q_cashflw

ticker = 'GOOG.NASDAQ'
# ticker = '1301.TYO'
ticker = '0857.HK'
# ticker = '000001.SZ'
# ticker = '600000.SH'
# ticker = '20MICRONS.NSE'
# ticker = '500002.BSE'
print q_ticker.getName( ticker )
# print q_ticker.getIndustry( ticker )
# print q_ticker.getSector( ticker )
# print q_ticker.getDescription( ticker )
print q_ticker.getEmployeesCount( ticker )
# print q_ticker.getStreetAddress( ticker )

q_income.jdk()
q_balance_sht.y2k()
q_cashflw.tbz()

print q_ticker.getIncomeStatementDetails( ticker, 2015, 'Sales/Revenue')
print q_ticker.getIncomeStatementDetails( ticker, 2015, 'Sales/Revenue', return_raw=True)
print q_ticker.getIncomeStatementDetails( ticker, 2015, '_FISCAL_NOTE_', return_raw=True)
print q_ticker.getBalanceSheetAssetsDetails( ticker, 2015, '_FISCAL_NOTE_', return_raw=True)
print q_ticker.getBalanceSheetLiabilitiesDetails( ticker, 2015, '_FISCAL_NOTE_', return_raw=True)
print q_ticker.getCashFlowOperatingActivityDetails( ticker, 2015, '_FISCAL_NOTE_', return_raw=True)
print q_ticker.getCashFlowInvestingActivityDetails( ticker, 2015, '_FISCAL_NOTE_', return_raw=True)
print q_ticker.getCashFlowFinancingActivityDetails( ticker, 2015, '_FISCAL_NOTE_', return_raw=True)

print 'currency:', q_ticker.getAccountingCurrency(ticker, 2015)
print 'unit    :', q_ticker.getAccountingCurrencyUnit(ticker,2015)
