import dash
from dash import html, dcc

from app import app


USERNAME - ''

# Definir as páginas
from landpage import layout as landpage_layout
from index import layout as dashboard_layout

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return landpage_layout
    elif pathname == '/index':
        return dashboard_layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)