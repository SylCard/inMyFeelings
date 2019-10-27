from flask import Flask, render_template, redirect, url_for, flash, session, request
from joblib import load
import pandas as pd
import numpy as np
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from config import Config
import os, json, requests, spotipy, time, pprint
from spotipy import oauth2
scope = 'user-library-read user-read-currently-playing user-top-read playlist-modify-public user-follow-read'


sp_oauth = oauth2.SpotifyOAuth('1f6e7665f5c74cf8bc7d1c880321b6f3', 'lool','https://inmyfeelings.me/logged',
scope=scope,cache_path='.spocache')


spot = None


app = Flask(__name__)
app.config.from_object(Config)

import logging
handler = logging.FileHandler('imferror.log')  # errors logged to this file
handler.setLevel(logging.ERROR)  # only log errors and above
app.logger.addHandler(handler)  # attach the handler to the app's logger



model = load('forest.joblib')

@app.route("/")
def hello():
    return render_template("home.html")


@app.route("/logged")
def logged():
    global spot
    # get the auth portion of url

    code = request.args['code']
    if code:
        token_info = sp_oauth.get_access_token(code)
        access_token = token_info['access_token']
    if access_token:
        spot = spotipy.Spotify(auth=access_token)
        session['token']=access_token
        user = spot.me()

    current = spot.current_user_playing_track()['item']
    name = current['name']
    artist= current['artists'][0]['name']
    id = current['id']

    features = get_features(id,spot)

    playing = name + " by " + artist

    definitions = ['Chill','Energetic','Cheerful','Romantic']

    song = pd.DataFrame.from_dict(features)

    # normalise loudness range is  -60 to 0 db
    norm_loudness = song['loudness'] / 60
    song['loudness'] = norm_loudness

    mood = model.predict(song)[0]

    prob = model.predict_proba(song)[0][mood]

    return render_template("logged.html",playing=playing,mood=definitions[mood],prob=prob)


def get_features(track_id,sp):
    f = sp.audio_features([track_id])[0]
    track_features = dict(danceability=[f['danceability']],
                               loudness=[f['loudness']],
                               speechiness=[f['speechiness']],
                               acousticness=[f['acousticness']],
                               liveness=[f['liveness']],
                                    )
    return track_features



def get_spotify_token(code, redirect_url):
    url = "https://accounts.spotify.com/api/token"
    payload = {"grant_type": "authorization_code", "code": code, "redirect_uri":redirect_url,
        "client_id":'1f6e7665f5c74cf8bc7d1c880321b6f3',
        "client_secret": '37769094da86417080b8553e0d821edf' }
    res = requests.post(url, data=payload)
    resjson = res.json()
    return resjson

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
