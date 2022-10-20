from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Note
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods= ['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form.get('colby_id')
        password = request.form.get('password')

        user = User.query.filter_by(colby_id=colby_id).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if user.role == 0: #User is super admin 
                    return redirect(url_for('views.admin_view')) # TODO: do these checks in views instead
                elif user.role == 1: #User is peak
                    return redirect(url_for('views.peak_view'))
                elif user.role == 2: # User is a coach
                    return redirect(url_for('views.coach_view'))
                elif user.role == 3: # User is an athlete
                    return redirect(url_for('views.athlete_view'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

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

        user = User.query.filter_by(colby_id=colby_id).first()
        if user: #TODO: Find better checks
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            # add user to database
            new_user = User(colby_id=colby_id, first_name=first_name, last_name = last_name, password=generate_password_hash(password1, method='sha256')) #TODO: Figure out parameters for permissions
            db.session.add(new_user)
            db.session.commit()
            #login_user(user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.admin_view'))

    return render_template("signup.html", user=current_user)