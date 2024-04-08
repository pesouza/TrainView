from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

from app import app
from left_video import *
from notes_form import *
# import callbacks

# Função para obter o nome de usuário do cookie
def get_username_from_cookie():
    return request.cookies.get('username')

# Layout da página principal (tela inicial)
layout = dbc.Container(
        style={"padding": "50px 50px",
               '--light-bg-color': '#ffffff',  # Cor de fundo no modo claro
               '--dark-bg-color': '#212529',    # Cor de fundo no modo escuro
               '--light-text-color': '#000000',  # Cor do texto no modo claro
               '--dark-text-color': '#ffffff'},  # Cor do texto no modo escuro
        children=[
            dbc.Row([
                dbc.Col([
                    html.Div(
                        children=[
                            html.Img(id="logo", src=app.get_asset_url("bg_aeria.png"), height=50, 
                            style={"margin-bottom": "20px"}),
                            html.H2("TrainView", style={"font-weight": "bold", "font-size": "32px", "color": "var(--light-text-color)", "marginLeft": "20px", "display": "inline"}),
                            html.Div(id='username-output')
                        ]
                    ),

                    dcc.Slider(id='slider-playback-rate', min=0.25, max=5, 
                    step=None, marks={i: str(i) + 'x' for i in [0.25, 1, 2, 5]}, value=1),
                    
                    l_controls
                ], md="9"),

                dbc.Col([
                    notes_form
                ], md="3")

            ]),
        ], fluid=True)

@app.callback(Output('video-player', 'playbackRate'),
              [Input('slider-playback-rate', 'value')])
def update_playbackRate(value):
    return value

# Callback para exibir o nome de usuário
@app.callback(Output('username-output', 'children'),
              [Input('page-content', 'children')])
def display_username(children):
    username = get_username_from_cookie()
    if username:
        USERNAME = username
        return f'Bem-vindo, {username}!'
    else:
        raise PreventUpdate

# Callback para exibir o nome 
if __name__ == '__main__':
    app.run_server(debug=True)