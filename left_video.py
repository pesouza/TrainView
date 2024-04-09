import dash_player
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import json
import dash
from app import app
from globals import *

USERNAME = get_current_user()
MY_VIDEOS = get_videos(USERNAME)
MY_SPORTS = get_sports()

l_controls = dbc.Col([
    dcc.Dropdown(
        id="dd-my-videos",
        options=[{"label": i['video'], "value": i['url']} for i in MY_VIDEOS],
        value=MY_VIDEOS[0]['url'] if MY_VIDEOS else None,
        style={"margin-top": "10px"},
        placeholder="Selecione seu vídeo"
    ),

    dcc.RadioItems(
        id='rd-sports',
        options=[{"label": sport, "value": sport} for sport in MY_SPORTS],
        value=MY_SPORTS[0] if MY_SPORTS else None,
        labelStyle={'display': 'inline-block', 'margin': '10px'}
    ),

    dbc.Collapse(
        dbc.Card([   
            dbc.CardBody([
                dbc.Input(
                    id="inpt-cut-name",
                    placeholder="Nome do corte",
                    type="text"
                ),
                dbc.Button(
                    "Adicionar Golpe",
                    id="btn-add-movie",
                    color="primary"
                ),
                dbc.Row([
                    dbc.Button(
                        "Início: 0",
                        color="secondary",
                        id="btn-set-start",
                        size="lg",
                        style={"width": "150px"}
                    ),

                    dbc.Button(
                        "Fim: 10",
                        color="secondary",
                        id="btn-set-end",
                        size="lg",
                        style={"width": "150px"}
                    ),

                    dbc.Button(
                        "Criar corte",
                        color="info",
                        id="btn-create-cut",
                        size="lg",
                        style={"width": "150px"}
                    )
                ]),
            ])
        ],
        color="dark",
        outline=True),
        id="collapse",
        is_open=False,
        style={"margin-top": "25px", "margin-bottom": "25px"}
    ),

    dbc.Row([
        dbc.Col(
            dbc.Button(
                "Cortes",
                color="info",
                id="btn-collapse",
                size="lg"
            ),
            md="1",
            style={"margin-top": "10px"}
        ),

        dbc.Col(
            dbc.Button(
                "Deletar",
                color="danger",
                id="btn-delete-cut",
                size="lg"
            ),
            md="1",
            style={"margin-top": "10px"}
        ),

        dbc.Col(
            dcc.Dropdown(
                id="dd-cut-scenes",
                style={"margin-top": "10px"},
                placeholder="Selecione seu corte"
            ),
            md="10"
        )
    ]),
    
    dash_player.DashPlayer(
        id='video-player',
        controls=True,
        width='100%',
        height="600px",
        intervalSecondsLoaded=200,
        style={"margin-top": "20px"}
    )
])

@app.callback(
    Output("collapse", "is_open"),
    [Input("btn-collapse", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

@app.callback(
    Output('video-player', 'url'),
    [Input('dd-my-videos', 'value')]
)
def select_video_1(value):
    return value

@app.callback(
    Output('btn-set-start', 'children'),
    [Input('btn-set-start', 'n_clicks'), State('video-player', 'currentTime')]
)
def update_btn_start1(n_clicks, value):
    value = 0 if value is None else value
    return "INÍCIO: {:.1f}".format(value)

@app.callback(
    Output('btn-set-end', 'children'),
    [Input('btn-set-end', 'n_clicks'), State('video-player', 'currentTime')]
)
def update_btn_end1(n_clicks, value):
    value = 10 if value is None else value
    return "FIM: {:.1f}".format(value)

@app.callback(
    Output('dd-my-videos', 'options'),
    [Input('rd-sports', 'value')]
)
def update_video_options(selected_sport):
    return [{"label": i['video'], "value": i['url']} for i in MY_VIDEOS if i['sport'] == selected_sport]

@app.callback(
    Output('rd-cut-kind', 'options'),
    [Input('rd-sports', 'value')]
)
def update_movie_options(selected_sport):
    return get_movies(selected_sport)

@app.callback(
    Output('rd-cut-kind', 'value'),
    [Input('rd-sports', 'value')]
)
def update_default_movie(selected_sport):
    movies = get_movies(selected_sport)
    return movies[0]['value'] if movies else None

@app.callback(
    Output('dd-cut-scenes', 'options'),
    [Input('btn-create-cut', 'n_clicks'), Input('btn-delete-cut', 'n_clicks'), Input('video-player', 'url')],
    [State('btn-set-start', 'children'), State('btn-set-end', 'children'), State('inpt-cut-name', 'value'),
     State('rd-cut-kind', 'value'), State('dd-cut-scenes', 'value')]
)
def create_cut_1(create_cut, delete_cut, url, start, end, cut_name, cut_kind, selected_scene):
    if create_cut:
        start = float(start.split(":")[1])
        end = float(end.split(":")[1])
        add_scene(USERNAME, url, cut_kind.upper() + " : " + cut_name, [start, end])
    elif delete_cut:
        if selected_scene:
            delete_scene(USERNAME, url, selected_scene)

    options = [{"label": scene['scene'], "value": scene['scene']} for scene in get_scenes(USERNAME, url)]
    return options

@app.callback(
    Output('video-player', 'seekTo'),
    [Input('dd-cut-scenes', 'value'), State('video-player', 'url'), Input('video-player', 'currentTime')]
)
def control_scene_time1(cut_scene, url, current_time):
    if cut_scene:
        scene = get_scene(USERNAME, url, cut_scene)
        if scene:
            start_time = scene['position'][0]
            if current_time < start_time:
                return start_time
            elif current_time > scene['position'][1]:
                return start_time
