import os
import json
from pymongo import MongoClient


 # Conectar ao MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['trainview']
usuarios_collection = db['users']
videos_collection = db['videos']
scenes_collection = db['scenes']
notes_collection = db['notes']
current_user = db['current_user']

# =================================
def set_current_user(username):
    current_user.delete_many({})
    current_user.insert_one({'username': username})

def get_current_user():
    user = current_user.find_one({})
    return user['username'] if user else None

def get_user(username):
    user = usuarios_collection.find_one({'username': username})
    return user

def save_user(user): 
    usuarios_collection.insert_one(user)

def add_video(user, video, url):
    videos_collection.insert_one({'username': user, 'video': video, 'url': url})

def get_videos(user):
    videos = videos_collection.find({'username': user})
    return videos

def get_video(user, video):
    video = videos_collection.find_one({'username': user, 'video': video})
    return video

def get_scenes(user, video):
    scenes = scenes_collection.find({'username': user, 'video': video})
    return scenes

def get_notes(user, video):
    notes = notes_collection.find({'username': user, 'video': video})
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

for url in MY_VIDEOS.items():
    if not get_video("admin", url[0]):
        add_video("admin",  url[0], url[1])

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