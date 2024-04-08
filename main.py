import dash
from dash import html, dcc

from app import app


# Definir as páginas
from landpage import layout as landpage_layout
from index import layout as dashboard_layout

app.layout = html.Div([
    dcc.Store(id='stored-params', data={}),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname'), dash.dependencies.Input('stored-params', 'data')])
def display_page(pathname, stored_params):
    if pathname == '/':
        return landpage_layout
    elif pathname == '/index':
        if stored_params and 'username' in stored_params:
            username = stored_params['username']
            return dashboard_layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)