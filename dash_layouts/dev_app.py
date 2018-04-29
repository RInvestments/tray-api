# This will run a separate server for dash. This code
# can hopefully be copied in the main-app


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


dash_app = dash.Dash( __name__ ) #can set a static folder here (separate for it for images etc)

from Layout1 import Layout1


lay = Layout1(dash_app)
dash_app.layout = lay.render()

@dash_app.callback( Output('output', 'children'), [Input( 'my-dropdown', 'value' ) ] )
def update_info( input_value ):
    # return 'you entered : '+ str(input_value)
    return lay.r.geturl_as_raw( '/tickerInfo/%s/description' %(input_value) )



dash_app.run_server(debug=True, host='0.0.0.0', ssl_context='adhoc')
