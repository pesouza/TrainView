import os
import json

# Conectar ao MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['trainview']
videos_collection = db['videos']
scenes.collection = db['scenes']
notes_collection = db['notes']

# =================================
def get_videos(user):
    videos = videos_collection.find({'user': user})
    return videos

def get_scenes(user, video):
    scenes = scenes_collection.find({'user': user; 'video': video})
    return scenes

def get_notes(user, video):
    notes = notes_collection.find({'user': user; 'video': video})
    return notes

# =================================
# My videos

MY_VIDEOS = {
    "Forehand compilation": 'https://www.youtube.com/watch?v=_7xV_CE8y28&list=PLjZrvsjkqCCgVIeTfKa-pipLiqZ-pXWjL',
    #"JOGO vs VITOR - 09/10/2021": "https://www.youtube.com/watch?v=B7M1vhZ2C6c",
    #"TREINO COM ALINE - 12/10/2021": "https://www.youtube.com/watch?v=waD4JJ1_pBQ",
    #"JOGO vs FLÁVIO - 26/09/2021": "https://www.youtube.com/watch?v=6yoK7kCSRb8",
    #"JOGO vs VAL - 22/10/2021": "https://www.youtube.com/watch?v=LuQUnj8nztg",
    #"JOGO vs VAL 2 - 24/10/2021": "https://www.youtube.com/watch?v=MxqECYnJK6I",
    }



if "dict_scenes.json" in os.listdir():
    DICT_SCENES = json.load(open('dict_scenes.json'))
else:
    DICT_SCENES = {j: {} for i, j in MY_VIDEOS.items()}

# for url in MY_VIDEOS.values():
#     if url not in DICT_SCENES.keys():
#         DICT_SCENES[url] = {}
#with open('dict_scenes.json', 'w') as f:
#    json.dump(DICT_SCENES, f)


# =================================
# My videos
DICT_NOTES = json.load(open('dict_notes.json')) if "dict_notes.json" in os.listdir() else {}
#with open('dict_notes.json', 'w') as f:
#    json.dump(DICT_NOTES, f)