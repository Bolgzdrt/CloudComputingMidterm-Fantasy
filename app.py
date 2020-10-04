from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

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
  fname = db.Column(db.String(80))
  lname = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
  password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
  remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
  fname = StringField('First Name', validators=[InputRequired(), Length(max=80)])
  lname = StringField('Last Name', validators=[InputRequired(), Length(max=80)])
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
    if user:
      if check_password_hash(user.password, form.password.data):
        login_user(user, remember=form.remember.data)
        return redirect(url_for('home'))

    return '<h1>Invalid username or password</h1>'

  return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = RegisterForm()

  if form.validate_on_submit():
    hashed_pass = generate_password_hash(form.password.data, method='sha256')
    new_user = User(fname=form.fname.data, lname=form.lname.data, username=form.username.data, email=form.email.data, password=hashed_pass)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user)
    return redirect(url_for('home'))

  return render_template('signup.html', form=form)

@app.route('/home')
@login_required
def home():
  return render_template('home.html', firstname=current_user.fname, lastname=current_user.lname, email=current_user.email)

@app.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('index'))

if __name__ == '__main__':
  app.run()