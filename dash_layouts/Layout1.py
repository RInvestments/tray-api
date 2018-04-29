import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from Retriver import Retriver



class Layout1:
    def __init__(self,dash_app):
        self.dash_app = dash_app
        xdash_app = dash_app

    def render(self):
        """ Returns a Dash layout """

        r = Retriver('https://localhost:5000')
        self.r = r 
        url = '/industryInfo/HK/'
        url = '/industryInfo/all/Automotive:Agriculture/all'
        url = '/industryInfo/all/all/all'
        data_dict = r.geturl_as_dict(url)


        options = []
        for industry in data_dict.keys():
            for sector in data_dict[industry].keys():
                for ticker in data_dict[industry][sector].keys():
                    label = '%s %s' %(ticker, data_dict[industry][sector][ticker]['companyName'])
                    options.append( {'label': label, 'value': ticker} )
        dropdown = dcc.Dropdown( options=options, multi=False, id='my-dropdown' )

        return html.Div( [html.H1("Welcome Dash!"),\
                          html.P("This is dash react"),\
                          html.Div( dropdown ),\
                          html.Div( id='output' )
                          ])
