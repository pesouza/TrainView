import flask
import dash
import dash_bootstrap_components as dbc

server = flask.Flask(__name__)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, '/assets/style.css'], server=server)
app.scripts.config.serve_locally = True