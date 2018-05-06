""" This app shows a list of all the stocks in a dropdown. You can select a stock
    it will printout the description for the company. And a graph summary of the
    income statement.
"""


import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


from app import app

from Retriver import Retriver

r = Retriver('https://localhost:5000')
url = '/industryInfo/all/all/all'
data_dict = r.geturl_as_dict(url)

options = []
for industry in data_dict.keys():
    for sector in data_dict[industry].keys():
        for ticker in data_dict[industry][sector].keys():
            label = '%s %s' %(ticker, data_dict[industry][sector][ticker]['companyName'] )
            options.append( {'label': label, 'value': ticker} )
dropdown = dcc.Dropdown( options=options, multi=False, id='my-dropdown' )

graph = dcc.Graph( id='basic-interactions',
            figure={
                'data': [
                    {
                        'x': [1, 2, 3, 4],
                        'y': [4, 1, 3, 5],
                        'text': ['a', 'b', 'c', 'd'],
                        'name': 'Trace 1',
                        'mode': 'markers',
                        'marker': {'size': 12}
                    }
                        ]
                    }
                )


layout= html.Div(
        [
            html.H1('My Data App'),
            dropdown,
            html.Div(id='description'),
            html.Div(id='accounting_currency'),
            graph,
            html.Div( id='debug' )
        ] )



@app.callback( Output('description', 'children'), [Input( 'my-dropdown', 'value' ) ] )
def update_info( input_value ):
    # return 'you entered : '+ str(input_value)
    if input_value is not None:
        return r.geturl_as_dict( '/tickerInfo/%s/description' %(input_value) )[input_value]


@app.callback( Output('accounting_currency', 'children'), [Input( 'my-dropdown', 'value' ) ] )
def update_info( input_value ):
    # return 'you entered : '+ str(input_value)
    if input_value is not None:
        d = r.geturl_as_dict( '/tickerInfo/%s/accountingCurrency/2016' %(input_value) )[input_value]['2016']['_FISCAL_NOTE_']
        return str(d)


@app.callback( Output('basic-interactions', 'figure'), [Input( 'my-dropdown', 'value' ) ] )
# # @dash_app.callback( Output('debug', 'children'), [Input( 'my-dropdown', 'value' ) ] )
def update_fig( input_value ):
    if input_value is None :
        return

    # Get Financial statements data
    #https://35.194.163.228:5000
    data_frame = r.geturl_as_dict( '/accountingStatements/%s/is/all/Sales_Revenue:Gross%%20Income:Net%%20Income' %(input_value) )
    # return str( data_frame )

    list_of_tuples = []
    for ticker in data_frame:
        for year in data_frame[ticker]:
            try:
                year_int = int(year)
                if year_int > 2100:
                    continue
            except:
                continue

            _year = year_int
            _revenue = data_frame[ticker][year]['Sales/Revenue']
            _gross_income = data_frame[ticker][year]['Gross Income']
            _net_income = data_frame[ticker][year]['Net Income']
            list_of_tuples.append( (_year, _revenue, _gross_income, _net_income) )


    list_of_tuples.sort( key=lambda tup: tup[0] )
    li = list_of_tuples

    # return '{"data": [{"y": [1, 2, 3], "x": [1, 2, 3]}]}'
    data = []
    data.append( { 'x': [ l[0] for l in li ], 'y': [ l[1] for l in li ], 'name':'revenue' } )
    data.append( { 'x': [ l[0] for l in li ], 'y': [ l[2] for l in li ], 'name':'gross income' } )
    data.append( { 'x': [ l[0] for l in li ], 'y': [ l[3] for l in li ], 'name':'net income' } )

    figure = { 'data': data }

    return figure
