from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Athlete, Coach
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods= ['GET', 'POST'])
def login():

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
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('User does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/create-user', methods= ['GET', 'POST'])
def create_user(): #TODO: We need to add a way to handle the permissions form

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
        if user: #TODO: Find better checks
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
            if int(role) == 2:
                new_user = Coach(colby_id=colby_id, first_name=first_name, last_name = last_name,
                 password=generate_password_hash(password1, method='sha256'),
                 role = role, athlete_data = athlete_data, team_data = team_data, notes = notes,
                 account_create = create_account, permission_change = permission_change)
            if int(role) == 3:
                new_user = Athlete(colby_id=colby_id, first_name=first_name, last_name = last_name,
                 password=generate_password_hash(password1, method='sha256'),
                 role = role, athlete_data = athlete_data, team_data = team_data, notes = notes,
                 account_create = create_account, permission_change = permission_change)
            else:
                new_user = User(colby_id=colby_id, first_name=first_name, last_name = last_name,
                 password=generate_password_hash(password1, method='sha256'),
                 role = role, athlete_data = athlete_data, team_data = team_data, notes = notes,
                 account_create = create_account, permission_change = permission_change) #TODO: Figure out parameters for permissions
            db.session.add(new_user)
            db.session.commit()
            #login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))

        

    return render_template("create_user.html")


