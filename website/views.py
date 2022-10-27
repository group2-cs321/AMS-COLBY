from urllib import request
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Athlete, Coach, Team
from . import db
import json
from csv import DictReader

views = Blueprint('views', __name__)

def parse_CSV():
    watchData=[[],[],[],[],[],[],[],[],[],[]]

    with open("website/static/assets/testdata/watchData.csv", 'r') as f:
         
        dict_reader = DictReader(f)
         
        list_of_dict = list(dict_reader)
        for i in range(5):
            watchData[0].append(list_of_dict[i]["date"])
            watchData[1].append(float(list_of_dict[i]["Restfulness Score"]))
            watchData[2].append(float(list_of_dict[i]["Total Sleep Duration"])/60**2)
            watchData[3].append(float(list_of_dict[i]["REM Sleep Duration"])/60**2)
            watchData[4].append(float(list_of_dict[i]["Light Sleep Duration"])/60**2)
            watchData[5].append(float(list_of_dict[i]["Deep Sleep Duration"])/60**2)
            watchData[6].append(float(list_of_dict[i]["Average Resting Heart Rate"]))
            watchData[7].append(float(list_of_dict[i]["Lowest Resting Heart Rate"]))
            watchData[8].append(float(list_of_dict[i]["Steps"]))
            watchData[9].append(float(list_of_dict[i]["Sleep Score"]))
    return watchData



@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    role = current_user.role
    print(current_user)
    print(role)
    watchData=parse_CSV()
    if int(role) == 0:
        return render_template("admin_view.html", user=current_user, teams = Team.query.all(), watchData=watchData)
    elif int(role) == 1:
        return render_template("peak_view.html", user=current_user, watchData=watchData)
    elif int(role) == 2:
        coach = Coach.query.filter_by(colby_id=current_user.colby_id).first()
        team = Team.query.filter_by(coach_id=coach.id).first()
        return redirect(url_for("views.coach_dashboard", id= team.id, watchData=watchData))
    elif int(role) == 3:
        athlete = Athlete.query.filter_by(colby_id=current_user.colby_id).first()
        return redirect(url_for("views.athlete_dashboard", id = athlete.id, watchData=watchData))
    else:
        return render_template("login.html")


@views.route('/permissions', methods = ['GET'])
def permissions():

    if int(current_user.permission_change) != 0:
        return redirect(url_for('views.home'))

    else:
        return render_template('permission.html', user=current_user)

@views.route('/create-team', methods = ['GET', 'POST'])
def create_team():

    watchData=parse_CSV()

    if request.method == 'POST':
        # TODO:
        # Create a team with the given name
        # Get the list of athletes from the form and add them to the team
        # For each coach, add the team to the coach field team_id
        team_name = request.form.get('team_name')

        athletes = request.form.getlist('athletes')
        coach = Coach.query.filter_by(colby_id=request.form.get('coaches')).first()

        team = Team.query.filter_by(team_name=team_name).first()

        if team:
            flash('Team Already exists', category = 'error')
            return render_template('create_team.html', user=current_user, athletes = Athlete.query.all(), coaches = Coach.query.all(), watchData=watchData)

        if len(team_name) < 1 or len(athletes) < 1:
             flash('Please input a valid team name', category = 'error')
             return render_template('create_team.html', user=current_user, athletes = Athlete.query.all(), coaches = Coach.query.all(), watchData=watchData)
        else:
            new_team = Team(team_name=team_name, coach_id = coach.id)
            db.session.add(new_team)
            db.session.commit()

            for athlete in athletes:
                ath = Athlete.query.filter_by(colby_id=athlete).first()
                ath.team_id = new_team.id
                db.session.commit()

        flash('Team created Succesfully', category='success')
        return render_template('create_team.html', user=current_user, athletes = Athlete.query.all(), coaches = Coach.query.all(), watchData=watchData)
        
    return render_template('create_team.html', user=current_user, athletes = Athlete.query.all(), coaches = Coach.query.all(), watchData=watchData)


#coach Dasboard page
@views.route('/team/<string:id>', methods = ['GET', 'POST'])
def coach_dashboard(id):
    coach = Coach.query.filter_by(colby_id=current_user.colby_id).first()
    currentTeam = Team.query.get(id)
    watchData=parse_CSV()

    return render_template("coach_dashboard.html", coach=coach, current_user=current_user, team=currentTeam, watchData=watchData)

#Coach Athlete Page
@views.route('/coach/athlete/<string:id>', methods = ['GET', 'POST'])
def athlete_coach_dashboard(id):
    athlete = Athlete.query.get(id)
    coach = Coach.query.filter_by(colby_id=current_user.colby_id).first()
    watchData=parse_CSV()
    currentTeam = Team.query.get(athlete.team_id)


    return render_template("athleteCoachView.html", athlete=athlete, coach=coach, current_user=current_user, team=currentTeam, watchData=watchData)

#Athlete Page
@views.route('/athlete/<string:id>', methods = ['GET', 'POST'])
def athlete_dashboard(id):
    athlete = Athlete.query.get(id)
    watchData=parse_CSV()


    return render_template("athleteView.html", athlete=athlete, current_user=current_user, watchData=watchData)


