from flask import Flask, render_template, redirect, url_for, flash
from flask.globals import request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from utils import getPlayerNames, getRosterPlayers, getPlayerStats, getPlayerScores, getUserWeekByWeekScore, getSearchInfo
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

class rosterForm(FlaskForm):
  qb = SelectField("QB", coerce=int)
  rb1 = SelectField("RB1", coerce=int)
  rb2 = SelectField("RB2", coerce=int)
  wr1 = SelectField("WR1", coerce=int)
  wr2 = SelectField("WR2", coerce=int)
  te = SelectField("TE", coerce=int)
  
class searchForm(FlaskForm):
  searchName = StringField('Find Player...', validators=[InputRequired(), Length(max=80)])

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

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
  form = searchForm()
  if form.validate_on_submit():
    searchString = form.searchName.data
    searchList = searchString.split()
    if len(searchList) > 1:
      fname = searchList[0]
      lname = searchList[1]
      data = Players.query.filter_by(PlayerLname=lname).filter_by(PlayerFname=fname).first()
    else:
      data = Players.query.filter_by(PlayerLname=searchList[0]).first()
    scoreStats = getSearchInfo(data.TeamID, Team)
    return render_template('search.html', data=data, scoreStats=scoreStats, form=form)

  roster = Roster.query.filter_by(RosterID=current_user.RosterID).first()
  names = getPlayerNames(Players, roster)
  player_stats = getPlayerStats(roster, Players)
  player_scores = getPlayerScores(roster, Team, Players)
  total_score = reduce(lambda acc, curr: acc + player_scores[curr], player_scores, 0)
  return render_template('home.html', username=current_user.username, roster=roster, names=names, player_stats=player_stats, player_scores=player_scores, total_score=total_score, form=form)

@app.route('/buildroster', methods=['GET', 'POST'])
@login_required
def buildroster():
  form = rosterForm()

  qbs = Players.query.filter_by(Position='QB')
  rbs = Players.query.filter_by(Position='RB')
  wrs = Players.query.filter_by(Position='WR')
  tes = Players.query.filter_by(Position='TE')

  form.qb.choices = [(player.PlayerID, (player.PlayerFname + " " + player.PlayerLname + f" - {player.TotalYardage} yards")) for player in qbs]
  form.rb1.choices = [(player.PlayerID, (player.PlayerFname + " " + player.PlayerLname + f" - {player.TotalYardage} yards")) for player in rbs]
  form.rb2.choices = [(player.PlayerID, (player.PlayerFname + " " + player.PlayerLname + f" - {player.TotalYardage} yards")) for player in rbs]
  form.wr1.choices = [(player.PlayerID, (player.PlayerFname + " " + player.PlayerLname + f" - {player.TotalYardage} yards")) for player in wrs]
  form.wr2.choices = [(player.PlayerID, (player.PlayerFname + " " + player.PlayerLname + f" - {player.TotalYardage} yards")) for player in wrs]
  form.te.choices = [(player.PlayerID, (player.PlayerFname + " " + player.PlayerLname + f" - {player.TotalYardage} yards")) for player in tes]

  if form.validate_on_submit():
    if (form.rb1.data == form.rb2.data) or (form.wr1.data == form.wr2.data):
      flash('Must select different players for each roster spot')
    else:
      roster_id = randrange(1000000, 9999999)
      new_roster = Roster(RosterID=roster_id, QB=form.qb.data, RB1=form.rb1.data, RB2=form.rb2.data, WR1=form.wr1.data, WR2=form.wr2.data, TE=form.te.data)
      user = current_user
      user.RosterID = roster_id
      db.session.add(new_roster)
      db.session.commit()
      return redirect(url_for('home'))

  return render_template('buildRoster.html', form=form)

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
