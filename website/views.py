from urllib import request
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Athlete, Coach
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    role = current_user.role
    print(role)

    if int(role) == 0:
        return render_template("admin_view.html", user=current_user)
    elif int(role) == 1:
        return render_template("peak_view.html", user=current_user)
    elif int(role) == 2:
        return render_template("coach_dashboard.html", user=current_user)
    elif int(role) == 3:
        return render_template("athleteView.html", user=current_user)
    else:
        return render_template("login.html", user=current_user)

@views.route('/permissions', methods = ['GET'])
def permissions():

    if int(current_user.permission_change) != 0:
        return redirect(url_for('views.home'))

    else:
        return render_template('permission.html', user=current_user)

@views.route('/create-team', methods = ['GET', 'POST'])
def create_team():

    if request.method == 'POST':
        # TODO:
        # Create a team with the given name
        # Get the list of athletes from the form and add them to the team
        # For each coach, add the team to the coach field team_id
        pass

        
    print(Athlete.query.all())
    return render_template('create_team.html', user=current_user, athletes = Athlete.query.all(), coaches = Coach.query.all())
