from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
from typing import List
from sqlalchemy.orm import Session

load_dotenv()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)

    print(result.status_code)
    print(result.text)

    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artists(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"
    
    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artists with this name exists")
        return None
    
    return json_result[0]

def get_songs_by_artist(token, aristis_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

token = get_token()
result = search_for_artists(token, {name_artist})
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx + 1}. {song['name']}")

@router.get("/name_artists", response_model=List[artistDTO], name="name_artist")
async def request_name_artist(artist: artistDTO, db: Session=depends(earch_for_artists)):
    return request_name_artist