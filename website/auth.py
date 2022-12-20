from flask import Blueprint, render_template, request, flash, redirect, url_for, request
from .models import User, Coach, Athlete, OAuth2Token
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from csv import DictReader
from . import oauth
import flask
from website.helper import *



auth = Blueprint('auth', __name__)

@auth.route('/login', methods= ['GET', 'POST'])
def login():

    """login page
    verify login information and log in user
    notify user of login status (success / error)
 
    Returns
    -------
    .html: corresponding home page according to user type
        OR login page
    """

    if request.method == 'POST':
        colby_id = request.form.get('colby_id')
        password = request.form.get('password')

        user = User.query.filter_by(colby_id=colby_id).first()
        coach = Coach.query.filter_by(colby_id=colby_id).first()
        athlete = Athlete.query.filter_by(colby_id=colby_id).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        elif coach:
            if check_password_hash(coach.password, password):
                flash('Logged in successfully!', category='success')
                login_user(coach, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        elif athlete:
            if check_password_hash(athlete.password, password):
                flash('Logged in successfully!', category='success')
                login_user(athlete, remember=True)
                print('In athlete')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')

    return render_template("login.html")


@auth.route('/logout')
@login_required
def logout():

    """log out user

    Returns
    -------
    .html: login page
    """

    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/create-user', methods= ['GET', 'POST'])
# @login_required
def create_user(): 

    """create user and post user data to database
    notify creation status (error/sucess)

    Returns
    -------
    .html: login page 
        OR user creation page
    """

    # if not int(current_user.account_create) == 0:
    #     return "<h1>No Access</h1>"

    watchData=parse_CSV()
    
    dummy_user = User(colby_id="colby_id", first_name="first_name", last_name = "last_name")

    if request.method == 'POST':
        colby_id = request.form.get('colby_id')
        first_name = request.form.get('firstname')
        last_name = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        athlete_data = request.form.get('athlete_data')
        team_data = request.form.get('team_data')
        notes = request.form.get('notes')
        create_account = request.form.get('create_account')
        permission_change = request.form.get('permission_change')
        role = request.form.get('role')
        
        user = User.query.filter_by(colby_id=colby_id).first()
        
        if user:
            flash('User already exists.', category='error')
        elif len(colby_id) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            #add user to database'
            new_user = User(colby_id=colby_id, first_name=first_name, last_name = last_name,
                 password=generate_password_hash(password1, method='sha256'),
                 role = role, athlete_data = athlete_data, team_data = team_data, notes = notes,
                 account_create = create_account, permission_change = permission_change)
            if int(role) == 2:
                print("creating coach")
                coach = Coach(colby_id=colby_id, first_name=first_name, last_name = last_name)
                db.session.add(coach)
            if int(role) == 3:
                athlete = Athlete(colby_id=colby_id, first_name=first_name, last_name = last_name)
                db.session.add(athlete)
            
            db.session.add(new_user)
            db.session.commit()
            #login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

    

        
    return render_template("create_user.html", watchData=watchData, current_user = dummy_user)



@auth.route('/authorize/<string:name>')
def authorize(name):
    """handle the authorization and redirect to home page

    Params
    ______
    name: the name of the api app

    """
    # TODO: Handle when the user rejects to share access


    
    token = oauth.oura.authorize_access_token()

    access_token = token['access_token']
    token_type = token['token_type']
    refresh_token = token['refresh_token']
    expires_at = token['expires_at']

    curr = OAuth2Token.query.filter_by(name = name, user = current_user.id).first()

    if curr !=  None:
        curr.access_token = access_token
        curr.token_type = token_type
        curr.refresh_token = refresh_token
        curr.expires_at = expires_at

    else:
        curr = OAuth2Token(
            name = name,
            access_token = access_token,
            token_type = token_type,
            refresh_token = refresh_token,
            expires_at = expires_at,
            user = current_user.id
            )

    db.session.add(curr)
    db.session.commit()

    return redirect('/')

@auth.route('auth/<string:name>')
def ask_auth(name):
    """request to authorize an api app
        
       params
       ______
       name: name of the api app
            
    """

    redirect_uri = url_for('auth.authorize', name = name, _external = True)
    return oauth.oura.authorize_redirect(redirect_uri)

