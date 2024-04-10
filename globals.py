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
sports_collection = db['sports']
movies_collection = db['movies']

# =================================
# Current user functions

current_user = db['current_user']

def set_current_user(username):
    current_user.delete_many({})
    current_user.insert_one({'username': username})

def get_current_user():
    user = current_user.find_one({})
    return user['username'] if user else None

# =================================
def get_user(username):
    user = usuarios_collection.find_one({'username': username})
    return user

def save_user(user): 
    usuarios_collection.insert_one(user)

# =================================
def add_video(user, sport, video, url):
    videos_collection.insert_one({'username': user, 'sport': sport, 'video': video, 'url': url})

def get_videos(user, sport):
    videos = videos_collection.find({'username': user, 'sport': sport})
    return list(videos)

def get_video(user, sport, video):
    video = videos_collection.find_one({'username': user, 'sport': sport, 'video': video})
    return video if video else None 

def delete_video(user, video):
    videos_collection.delete_one({'username': user, 'video': video})

# =================================
def add_scene(user, video, scene, position):
    scenes_collection.insert_one({'username': user, 'video': video, 'scene': scene,  'position': position})

def delete_scene(user, video, scene):
    scenes_collection.delete_one({'username': user, 'video': video, 'scene': scene})
    
def get_scene(user, video, scene):
    scene = scenes_collection.find_one({'username': user, 'video': video, 'scene': scene})
    return scene if scene else None

def get_scenes(user, video):
    scenes = scenes_collection.find({'username': user, 'video': video})
    return list(scenes)

# =================================
def add_notes(user, video, scene, notes):
    notes_collection.insert_one({ 'username': user, 'video': video, 'scene': scene, 'notes': notes})

def get_note(user, video, scene):
    note = notes_collection.find_one({'username': user, 'video': video, 'scene': scene})
    return note if note else None

def update_note(user, video, scene, notes):
    notes_collection.update_one({'username': user, 'video': video, 'scene': scene}, {'$set': {'notes': notes}})

def delete_note(user, video, scene):
    notes_collection.delete_one({'username': user, 'video': video, 'scene': scene})

def get_notes(user, video):
    notes = notes_collection.find({'username': user, 'video': video})
    return list(notes)

# =================================
def add_sport(sport):
    sports_collection.insert_one({'sport': sport})

def get_sports():
    sports = sports_collection.find()
    return list({sport['sport'] for sport in sports})

def remove_sport(sport): 
    sports_collection.delete_one({'sport': sport})

# =================================
def add_movie(sport,mov):
    mov_value = mov.lower().replace(" ", "_")  # Convertendo o movimento para o formato de valor
    movies_collection.insert_one({'sport': sport, 'mov': mov, 'mov_value': mov_value})

def get_movies(sport):
    movies = movies_collection.find({'sport': sport})
    options = [{'label': movie['mov'], 'value': movie['mov_value']} for movie in movies]
    return options

def remove_movie(mov): 
    movies_collection.delete_one({'sport': sport,'movie': mov})

# =================================

# My videos


#{
#    "Forehand compilation": 'https://www.youtube.com/watch?v=_7xV_CE8y28&list=PLjZrvsjkqCCgVIeTfKa-pipLiqZ-pXWjL',
    #}

#for url in MY_VIDEOS.items():
#    if not get_video("admin", url[0]):
#        add_video("admin",  url[0], url[1])

# =================================
#DICT_SCENES = get_scenes(USERNAME, MY_VIDEOS[0]["video"])

#if "dict_scenes.json" in os.listdir():
#    DICT_SCENES = json.load(open('dict_scenes.json'))
#else:
#    DICT_SCENES = {j: {} for i, j in MY_VIDEOS.items()}


# =================================
#DICT_NOTES = get_notes(USERNAME, MY_VIDEOS[0]["video"])

#DICT_NOTES = json.load(open('dict_notes.json')) if "dict_notes.json" in os.listdir() else {}
#with open('dict_notes.json', 'w') as f:
#    json.dump(DICT_NOTES, f)