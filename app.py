from flask import Flask, render_template, redirect, url_for
from flask.globals import request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from utils import getPlayerNames, getRosterPlayers, getPlayerStats, getPlayerScores, getUserWeekByWeekScore
from random import randrange
from functools import reduce

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secrettunnel'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./database.db'
Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(15), unique=True)
  email = db.Column(db.String(50), unique=True)
  password = db.Column(db.String(80))
  RosterID = db.Column(db.Integer)

class Roster(UserMixin, db.Model):
  RosterID = db.Column(db.Integer, primary_key=True)
  QB = db.Column(db.Integer)
  WR1 = db.Column(db.Integer)
  WR2 = db.Column(db.Integer)
  RB1 = db.Column(db.Integer)
  RB2 = db.Column(db.Integer)
  TE = db.Column(db.Integer)

class Team(UserMixin, db.Model):
  TeamID = db.Column(db.Integer, primary_key=True)
  TeamName = db.Column(db.String(80))
  Game1 = db.Column(db.Integer)
  Game2 = db.Column(db.Integer)
  Game3 = db.Column(db.Integer)
  Game4 = db.Column(db.Integer)
  Game5 = db.Column(db.Integer)
  Game6 = db.Column(db.Integer)
  Game7 = db.Column(db.Integer)
  Game8 = db.Column(db.Integer)
  Game9 = db.Column(db.Integer)
  Game10 = db.Column(db.Integer)
  Game11 = db.Column(db.Integer)
  Game12 = db.Column(db.Integer)
  Game13 = db.Column(db.Integer)
  Game14 = db.Column(db.Integer)
  Game15 = db.Column(db.Integer)
  Game16 = db.Column(db.Integer)
  Game17 = db.Column(db.Integer)

class Players(UserMixin, db.Model):
  PlayerID = db.Column(db.Integer, primary_key=True)
  PlayerFname = db.Column(db.String(80))
  PlayerLname = db.Column(db.String(80))
  TeamID = db.Column(db.Integer)
  Position = db.Column(db.String(2))
  TotalYardage = db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
  remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
  email = StringField('Email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
  username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()

  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and check_password_hash(user.password, form.password.data):
      login_user(user, remember=form.remember.data)
      return redirect(url_for('home'))

    return '<h1>Invalid username or password</h1>'

  return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = RegisterForm()

  if form.validate_on_submit():
    hashed_pass = generate_password_hash(form.password.data, method='sha256')
    user_id = randrange(1000000, 9999999)
    new_user = User(username=form.username.data, email=form.email.data, password=hashed_pass, id=user_id)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for('buildroster'))

  return render_template('signup.html', form=form)

@app.route('/home')
@login_required
def home():
  roster = Roster.query.filter_by(RosterID=current_user.RosterID).first()
  names = getPlayerNames(Players, roster)
  player_stats = getPlayerStats(roster, Players)
  player_scores = getPlayerScores(roster, Team, Players)
  total_score = reduce(lambda acc, curr: acc + player_scores[curr], player_scores, 0)
  return render_template('home.html', username=current_user.username, roster=roster, names=names, player_stats=player_stats, player_scores=player_scores, total_score=total_score)

@app.route('/buildroster')
@login_required
def buildroster():
  #WIP
  qbs = Players.query.filter_by(Position='QB')
  return render_template('buildRoster.html', qbs=qbs)

@app.route('/league')
@login_required
def league():
  rosters = Roster.query.with_entities(Roster.QB, Roster.WR1, Roster.WR2, Roster.RB1, Roster.RB2, Roster.TE, Roster.RosterID)
  league_weekly_scores = []
  for r in rosters:
    weekly_score = getUserWeekByWeekScore(r, Players, Team, User)
    league_weekly_scores.append(weekly_score)

  league_weekly_scores.sort(key=lambda e: e['total'], reverse=True)
  return render_template('league.html', scores=league_weekly_scores)

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))

if __name__ == '__main__':
  app.run()
