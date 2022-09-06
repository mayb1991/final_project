from urllib import response
from app import app
from flask import render_template, request, url_for, redirect
import requests
from flask_moment import Moment
from datetime import datetime
from .models import GameData


@app.route('/', methods=['GET', 'POST'])
def home_page():

    url = "https://odds.p.rapidapi.com/v4/sports/americanfootball_nfl/odds"

    querystring = {"regions": "us", "oddsFormat": "decimal",
                   "markets": "spreads", "dateFormat": "iso"}

    headers = {
        "X-RapidAPI-Key": "4afe651181msh7783e50a831acc1p11a544jsnd7f3fdcc2478",
        "X-RapidAPI-Host": "odds.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    # print(response.text)

    nfl = {}
    # game_set = set()
    if response.ok:
        data = response.json()
        # print(data)
        nfl = [{
            "id": d["id"],
            "Sport":d["sport_key"],
            "Match":[d['home_team'],d['away_team']],
            "Game_Time": d['commence_time'],
            "Odds": d['bookmakers'][5]['markets'][0]['outcomes'][0]['point'],
            "Favorite": d['bookmakers'][5]['markets'][0]['outcomes'][0]['name']
        }
            for d in data]
        check = GameData.query.filter_by(sport=nfl[0]['Sport']).first()
        if not check:
            game = GameData(nfl[0]['id'],nfl[0]['Sport'], nfl[0]["Match"], nfl[0]["Game_Time"], nfl[0]["Favorite"],
            nfl[0]["Odds"])
            game.save_game()

        return render_template('index.html', nfl=nfl)
    return render_template('index.html', nfl=nfl)


@app.route('/game/<match_up>')
def match_up(match):
    game = GameData.query.filter_by(match_up=match).first()


@app.route('/scores', methods=['GET', 'POST'])
def scores():
    url = "https://odds.p.rapidapi.com/v4/sports/americanfootball_nfl/scores"

    querystring = {"daysFrom": "3"}

    headers = {
        "X-RapidAPI-Key": "4afe651181msh7783e50a831acc1p11a544jsnd7f3fdcc2478",
        "X-RapidAPI-Host": "odds.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    # print(response.text)

    if response.ok:
        data = response.json()
        # print(data)

        game_data = [{
            "Home_Team": d['home_team'],
            "Away_Team": d['away_team'],
            "Scores": d['scores'],
            "Updated": d['last_update']
        }
        for d in data]
        return render_template('scores.html')
    return render_template('scores.html')

