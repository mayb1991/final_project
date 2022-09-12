from app import app
from flask import render_template, request, url_for, redirect
import requests
from flask_moment import Moment
from datetime import datetime
from .models import GameData, User
from flask_login import login_required, current_user


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
            "Match":[d['home_team'], d['away_team']],
            "Game_Time": d['commence_time'],
            "Odds": d['bookmakers'][5]['markets'][0]['outcomes'][0]['point'],
            "Favorite": d['bookmakers'][5]['markets'][0]['outcomes'][0]['name']
        }
            for d in data]
        # check = GameData.query.filter_by(sport=nfl[0]['id']).all()
        # if not check:
        for x in range(len(nfl)):

            game = GameData(nfl[x]['id'], nfl[x]['Sport'], nfl[x]["Match"],
                            nfl[x]["Game_Time"], nfl[x]["Favorite"], nfl[x]["Odds"])
            game.save_game()

        return render_template('index.html', nfl=nfl)
    return render_template('index.html', nfl=nfl)


@app.route('/follow/<int:user_id>')
@login_required
def follow_odds(user_id):
    user = User.query.get(user_id)
    current_user.follow(user)
    return redirect(url_for('home_page'))


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
            # "Scores": d['scores'][0]['score'],
            "Updated": d['last_update']
        }
            for d in data]
        return render_template('scores.html', game_data=game_data)
    return render_template('scores.html')


@app.route("/ncaaf/odds", methods=["GET", "POST"])
def ncaaf_odds():

    url = "https://odds.p.rapidapi.com/v4/sports/americanfootball_ncaaf/odds"

    querystring = {"regions": "us", "oddsFormat": "decimal",
                   "markets": "spreads", "dateFormat": "iso"}

    headers = {
        "X-RapidAPI-Key": "4afe651181msh7783e50a831acc1p11a544jsnd7f3fdcc2478",
        "X-RapidAPI-Host": "odds.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    # print(response.text)

    if response.ok:
        data = response.json()

        ncaaf = [{

            # "id": data["id"],
            # "Sport": data["sport_key"],
            "Match": [d['home_team'], d['away_team']],
            "Game_Time": d['commence_time'],
            "Odds": d['bookmakers'][5]['markets'][0]['outcomes'][0]['point'],
            "Favorite": d['bookmakers'][5]['markets'][0]['outcomes'][0]['name']
        }
        for d in data]
        return render_template("ncaaf.html", ncaaf=ncaaf)


@app.route("/mlb/odds", methods=["GET", "POST"])
def mlb_odds():

    url = "https://odds.p.rapidapi.com/v4/sports/baseball_mlb/odds"

    querystring = {"regions": "us", "oddsFormat": "decimal",
                   "markets": "spreads", "dateFormat": "iso"}

    headers = {
        "X-RapidAPI-Key": "4afe651181msh7783e50a831acc1p11a544jsnd7f3fdcc2478",
        "X-RapidAPI-Host": "odds.p.rapidapi.com"
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)

    # print(response.text)

    if response.ok:
        data = response.json()

        mlb = [{

            # "id": data["id"],
            # "Sport": data["sport_key"],
            "Match": [d['home_team'], d['away_team']],
            "Game_Time": d['commence_time'],
            "Odds": d['bookmakers'][5]['markets'][0]['outcomes'][0]['point'],
            "Favorite": d['bookmakers'][5]['markets'][0]['outcomes'][0]['name']
        }
        for d in data]
        return render_template("mlb_odds.html", mlb=mlb)
