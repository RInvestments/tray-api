import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2, app3


# Master layout. The real contents will go in div page-content
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    layouts_table = {}
    layouts_table['/apps/app1'] = app1.layout
    layouts_table['/apps/app2'] = app2.layout
    layouts_table['/apps/app3'] = app3.layout


    if pathname in layouts_table.keys():
        return layouts_table[pathname]
    else:
        return '404'




if __name__ == '__main__':
    # app.run_server(debug=True)
    app.run_server(debug=True, host='0.0.0.0', ssl_context='adhoc')
