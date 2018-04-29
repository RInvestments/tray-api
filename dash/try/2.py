"""

    Basic drop down with dash (using my data)
    https://35.194.163.228:5000/industryInfo/HK/

"""
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
app = dash.Dash()
# app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


import urllib2
import ssl
import json

class Retriver:
    def __init__(self, server_base_url):
        self.ctx = ssl.create_default_context()
        self.ctx.check_hostname = False
        self.ctx.verify_mode = ssl.CERT_NONE
        self.server_base_url = server_base_url

    def geturl_as_raw( self, url ):
        contents = urllib2.urlopen(self.server_base_url+url, context=self.ctx).read()
        return contents

    def geturl_as_dict( self, url ):
        response = urllib2.urlopen(self.server_base_url+url, context=self.ctx)
        data = json.load( response )
        return data


r = Retriver('https://localhost:5000')
url = '/industryInfo/HK/'
url = '/industryInfo/all/Automotive:Agriculture/all'
url = '/industryInfo/all/all/all'
data_dict = r.geturl_as_dict(url)
# Retrives a nested json object which is set into dcc.Dropdown

options = []
for industry in data_dict.keys():
    for sector in data_dict[industry].keys():
        for ticker in data_dict[industry][sector].keys():
            label = '%s %s' %(ticker, data_dict[industry][sector][ticker]['companyName'])
            options.append( {'label': label, 'value': ticker} )
dropdown = dcc.Dropdown( options=options, multi=False, id='my-dropdown' )



slider = dcc.Slider( min=2011, max=2017, step=1, marks={i: '%d' %(i) for i in range(2011,2017) }, id='my-slider' )


app.layout = html.Div( [html.Div([dropdown, slider]), html.Div( 'output goes here', id='output') ] )


@app.callback(
    Output( component_id='output', component_property='children' ),
    [Input(component_id='my-dropdown', component_property='value') , Input(component_id='my-slider', component_property='value') ]
)
def update_info( input_value, input_value2 ):
    # return 'you have entered: %s' %(input_value) + str(input_value2)
    return r.geturl_as_raw( '/tickerInfo/%s/description' %(input_value) )


if __name__ == '__main__':
    app.run_server(debug=True)
