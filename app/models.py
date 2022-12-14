from secrets import token_hex
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash


db = SQLAlchemy()


match_odds = db.Table("match_odds",
                      db.Column('follow_id', db.Integer,
                                db.ForeignKey('user.id')),
                      db.Column('game_data_id', db.Integer,
                                db.ForeignKey('game_data.id'))
                      )


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    username = db.Column(db.String(75), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    apitoken = db.Column(db.String, default=None, nullable=True)
    # games = db.relationship("GameData", back_populates='User')
    followed_games = db.relationship("GameData",
                                     secondary=match_odds,
                                     backref='following',
                                     lazy='dynamic'
                                     )

    def __init__(self, first_name, last_name, email, username, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)
        self.apitoken = token_hex(16)

    def follow(self, user):
        self.followed_games.append(user)
        db.session.commit()


class GameData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.String(150), nullable=False)
    sport = db.Column(db.String(300), nullable=False)
    match_up = db.Column(db.String(300), nullable=False)
    time = db.Column(db.DateTime)
    favorite = db.Column(db.String(150), nullable=False)
    odds = db.Column(db.Float, nullable=False)
    # uid = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship('User', back_populates="Gamedata")

    def __init__(self, game_id, sport, match_up, time, favorite, odds):
        self.game_id = game_id
        self.sport = sport
        self.match_up = match_up
        self.time = time
        self.favorite = favorite
        self.odds = odds

    def save_game(self):
        db.session.add(self)
        db.session.commit()
