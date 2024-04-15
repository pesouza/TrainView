import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
import dash_bootstrap_components as dbc
from app import app
from copy import deepcopy
from globals import *
import json


notes_form = html.Div([
                    html.H6("Anotações", className="display-4", 
                    style={"margin-left": "10px"}),

                    dbc.Button("Salvar nota", color="info", size="lg", 
                    id="btn-save-note", style={"margin-top": "10px", "margin-bottom": "10px"}),

                    dbc.Textarea(size="lg", id="txt-notes", 
                                placeholder="Notas do vídeo ou corte", 
                                style={'width': '100%', 'height': "90%", 
                                "margin-left": "10px"}),

        ], className="h-100 p-5 text-white rounded-3")


@app.callback(Output("txt-notes", "value"),
              [Input('btn-save-note', 'n_clicks'), State("txt-notes", "value"),
              Input("video-player", "url"), Input("dd-cut-scenes", "value")])
def update_notes(n_clicks, note, url, cut_scene):
    cut_scene = "" if cut_scene is None else cut_scene
    url = "" if url is None else url
    key_name = url + "-" + cut_scene

    trigg = dash.callback_context.triggered[0]["prop_id"]
    if "btn-save-note.n_clicks" == trigg:
        # Salvar nota no MongoDB
        notes_collection.update_one({"_id": key_name}, {"$set": {"note": note}}, upsert=True)
        return note
        
    if ("video-player.url" in trigg or "dd-cut-scenes.value" in trigg) and key_name in DICT_NOTES.keys():
        # Recuperar nota do MongoDB
        saved_note = notes_collection.find_one({"_id": key_name})
        if saved_note:
            return saved_note["note"]
        else:
            return ""