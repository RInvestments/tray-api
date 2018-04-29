# This will run a separate server for dash. This code
# can hopefully be copied in the main-app


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import json

dash_app = dash.Dash( __name__ ) #can set a static folder here (separate for it for images etc)

from Layout1 import Layout1


lay = Layout1(dash_app)
dash_app.layout = lay.render()

@dash_app.callback( Output('description', 'children'), [Input( 'my-dropdown', 'value' ) ] )
def update_info( input_value ):
    # return 'you entered : '+ str(input_value)
    if input_value is not None:
        return lay.r.geturl_as_dict( '/tickerInfo/%s/description' %(input_value) )[input_value]


@dash_app.callback( Output('accounting_currency', 'children'), [Input( 'my-dropdown', 'value' ) ] )
def update_info( input_value ):
    # return 'you entered : '+ str(input_value)
    if input_value is not None:
        d = lay.r.geturl_as_dict( '/tickerInfo/%s/accountingCurrency/2016' %(input_value) )[input_value]['2016']['_FISCAL_NOTE_']
        return str(d)


@dash_app.callback( Output('basic-interactions', 'figure'), [Input( 'my-dropdown', 'value' ) ] )
# @dash_app.callback( Output('debug', 'children'), [Input( 'my-dropdown', 'value' ) ] )
def update_fig( input_value ):
    if input_value is None :
        return

    # Get Financial statements data
    #https://35.194.163.228:5000
    data_frame = lay.r.geturl_as_dict( '/accountingStatements/%s/is/all/Sales_Revenue:Gross%%20Income:Net%%20Income' %(input_value) )
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



dash_app.run_server(debug=True, host='0.0.0.0', ssl_context='adhoc')
