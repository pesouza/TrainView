import dash_player
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import json
import dash
from app import app
from globals import *

USERNAME = get_current_user()
MY_SPORTS = get_sports()

l_controls = dbc.Col([
    dcc.Dropdown(
        id='rd-sports',
        options=[{"label": sport, "value": sport} for sport in MY_SPORTS],
        value=MY_SPORTS[0] if MY_SPORTS else None,
        style={"margin-top": "10px"},
        placeholder="Selecione seu esporte"
    ),

    dcc.Dropdown(
        id="dd-my-videos",
        options=[{"label": i['video'], "value": i['url']} for i in get_videos(USERNAME, MY_SPORTS[0])],
        value=get_videos(USERNAME, MY_SPORTS[0])[0]['url'] if get_videos(USERNAME, MY_SPORTS[0]) else None,
        style={"margin-top": "10px"},
        placeholder="Selecione seu vídeo"
    ),

    # Formulário "popup" para inserir novo vídeo
    dbc.Modal([
        dbc.ModalHeader("Adicionar Novo Vídeo"),
        dbc.ModalBody([
            dbc.Input(id="input-video-name", placeholder="Nome do vídeo"),
            dbc.Input(id="input-video-url", placeholder="URL do vídeo"),
            dbc.Button("Adicionar", id="btn-add-video", color="primary", className="mr-2")
        ]),
        dbc.ModalFooter(dbc.Button("Fechar", id="close-add-video", color="secondary"))
    ], id="modal-add-video", centered=True),

    dbc.Collapse(
        dbc.Card([   
            dbc.CardBody([
                dbc.Input(
                    id="inpt-cut-name",
                    placeholder="Nome do corte",
                    type="text",
                    style={"margin-bottom": "10px"}
                ),
                dcc.RadioItems(
                    id='rd-cut-kind',
                    labelStyle={'display': 'inline-block', 'margin': '10px'}
                ),
                dbc.Input(
                    id="inpt-mov",
                    placeholder="Novo golpe",
                    type="text",
                    size="lg",
                    style={"margin-top": "10px"}
                ),
                dbc.Button(
                    "Adicionar Golpe",
                    id="btn-add-movie",
                    color="primary",
                    className="mr-2",
                    style={"margin-top": "10px", "margin-bottom": "10px"}
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
            style={"margin-top": "10px", "margin-right": "10px"}
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
    return [{"label": i['video'], "value": i['url']} for i in get_videos(USERNAME, selected_sport)]

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

@app.callback(
    Output('inpt-mov', 'value'),
    [Input('btn-add-movie', 'n_clicks'), Input('rd-sports', 'value')],
    [State('inpt-mov', 'value')]
)
def add_new_movie(n_clicks, selected_sport, new_movie):
    if n_clicks:
        if new_movie:
            add_movie(selected_sport, new_movie)  
            return ''
    return new_movie

# Callback para abrir e fechar o formulário "popup" de adicionar novo vídeo
@app.callback(
    Output("modal-add-video", "is_open"),
    [Input("btn-add-video", "n_clicks"), Input("close-add-video", "n_clicks")],
    [State("modal-add-video", "is_open")],
)
def toggle_modal_add_video(add_clicks, close_clicks, is_open):
    if add_clicks or close_clicks:
        return not is_open
    return is_open

# Callback para adicionar um novo vídeo ao banco de dados e fechar o formulário "popup"
@app.callback(
    [Output("modal-add-video", "is_open"), Output("dd-my-videos", "options")],
    [Input("btn-add-video", "n_clicks")],
    [State("input-video-name", "value"), State("input-video-url", "value"), State("rd-sports", "value")]
)
def add_new_video_and_update_options(n_clicks, video_name, video_url, selected_sport):
    if n_clicks and video_name and video_url:
        add_video(USERNAME, selected_sport, video_name, video_url)
        videos = get_videos(USERNAME, selected_sport)
        options = [{"label": i['video'], "value": i['url']} for i in videos]
        return False, options
    return dash.no_update, dash.no_update

# Restante dos callbacks ...
