from urllib import request
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import User, Athlete, Coach, Team, Note
from . import db
import json
from csv import DictReader
import pandas as pd
from . import oauth
from werkzeug.security import generate_password_hash
from website.helper import *

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    """redirect to user's home page
 
    Returns
    -------
    .html: corresponding home page according to user type
    """
    
    role = current_user.role
    print(current_user)
    print(role)
    watchData=parse_CSV()
    if int(role) == 0:
        return render_template("admin_view.html", user=current_user, teams = Team.query.all(), watchData=watchData)
    elif int(role) == 1:
        return render_template("peak_view.html", user=current_user, teams = Team.query.all(), watchData=watchData)
    elif int(role) == 2:
        coach = Coach.query.filter_by(colby_id=current_user.colby_id).first()
        team = Team.query.filter_by(coach_id=coach.id).first()
        if not team:
            return "<h1>NO ACCESS</h1>"
        return redirect(url_for("views.coach_dashboard", id = team.id))
    elif int(role) == 3:
        return redirect(url_for("views.athlete_dashboard"))
    else:
        return render_template("login.html")


#creates team page
@views.route('/create-team', methods = ['GET', 'POST'])
@login_required
def create_team():

    """create team and post team data to database
    notify user of creation status (error/sucess)
 
    Returns
    -------
    .html: create team page
    """

    if int(current_user.team_data) != 0:
        return "<h1>No Access</h1>"

    watchData=parse_CSV()

    if request.method == 'POST':

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
        return render_template('create_team.html', user=current_user, athletes = Athlete.query.filter_by(team_id = None), coaches = Coach.query.all(), watchData=watchData)
        
    return render_template('create_team.html', user=current_user, athletes = Athlete.query.filter_by(team_id = None), coaches = Coach.query.all(), watchData=watchData)


#coach Dasboard page
@views.route('/team/<string:id>', methods = ['GET', 'POST'])
@login_required
def coach_dashboard(id):

    """redirect to coach dashboard if user has access
 
    Returns
    -------
    .html: coach's dashboard
    """

    role = int(current_user.role)
    if role > 2:
        return "<h1>No Access</h1>"

    coach = Coach.query.filter_by(colby_id=current_user.colby_id).first()
    currentTeam = Team.query.get(id)
    watchData=parse_CSV()

    return render_template("coach_dashboard.html", coach=coach, current_user=current_user, team=currentTeam, watchData=watchData)

#Coach Athlete Page
@views.route('team/coach/athlete/<string:id>', methods = ['GET', 'POST'])
@login_required
def athlete_coach_dashboard(id):

    """redirect to coach's view of athlete if user has access
 
    Returns
    -------
    .html: coach's view page of athletes
    """


    role = int(current_user.role)
    if role > 2:
        return "<h1>No Access</h1>"

    athlete = Athlete.query.get(id)
    coach = Coach.query.filter_by(colby_id=current_user.colby_id).first()
    watchData=parse_CSV()
    currentTeam = Team.query.get(athlete.team_id)


    return render_template(
        "athleteCoachView.html",
        athlete=athlete,
        coach=coach,
        current_user=current_user,
        team=currentTeam,
        watchData=watchData
        )


#Athlete Page
@views.route('/athlete', methods = ['GET', 'POST'])
@login_required
def athlete_dashboard():

    """redirect to athlete dashboard if user has access
 
    Returns
    -------
    .html: athlete's dashboard
    """

    role = int(current_user.role)
    if role == 2:
        return "<h1>No Access</h1>"
    athlete = Athlete.query.filter_by(colby_id = current_user.colby_id).first()
    watchData=parse_CSV()

    res = get_oura_recovery('2022-11-10', '2022-11-17')


    if type(res) != str and res.status_code == 200:
        sleepScore = res.json()['data'][0]['score']
    else:
        sleepScore = "N/A"


    #print(res)

    return render_template("athleteView.html", athlete=athlete, current_user=current_user, watchData=watchData, sleepScore = sleepScore)


# Handles everything on the permissions page
@views.route('admin/permissions', methods = ['GET', 'POST'])
@login_required
def permission_page():
        
    """redirect to the permission edit page if user has access
    post edits of permission settings to database
 
    Returns
    -------
    .html: permission page
    """

    if int(current_user.permission_change) != 0:
        return "<h1>No Access</h1>"

    watchData=parse_CSV()
    if request.method == 'POST':

        

        colby_id = request.form.get('user_to_change')
        athlete_data = request.form.get('athlete_data')
        team_data = request.form.get('team_data')
        notes = request.form.get('notes')
        create_account = request.form.get('create_account')
        permission_change = request.form.get('permission_change')
        role = request.form.get('role')

        user = User.query.filter_by(colby_id=colby_id).first()


        if int(user.role) != int(role):
            # When user is an athlete, delete them from coach table
            if int(user.role) == 2:
                coach = Coach.query.filter_by(colby_id=colby_id).first()
                team = Team.query.filter_by(coach_id=coach.id).first()

                # Making sure that coach had a team
                if team:
                    team.coach_id = None
                db.session.delete(coach)
                db.session.commit()

            # When user is a coach, delete them from athlete table
            if int(user.role) == 3:
                athlete = Athlete.query.filter_by(colby_id=colby_id).first()
                db.session.delete(athlete)
                db.session.commit()

            # When new role is athlete add user to athlete table
            if int(role) == 2:
                coach = Coach(colby_id=colby_id, first_name=user.first_name, last_name = user.last_name)
                db.session.add(coach)
                db.session.commit()

            # When new role is coach add user to coach table
            if int(role) == 3:
                athlete = Athlete(colby_id=colby_id, first_name=user.first_name, last_name = user.last_name)
                db.session.add(athlete)
                db.session.commit()


            user.role = role

        


        user.athlete_data = athlete_data
        user.team_data = team_data
        user.notes = notes
        user.create_account = create_account
        user.permission_change = permission_change
        

        db.session.commit()


    return render_template('permission.html', current_user = current_user, users = User.query.all(), watchData=watchData)
    


#Peak Notes
@views.route('/new-note',methods=['GET','POST'])
@login_required
def create_note():

    """create notes and post athlete's note data to database
    notify user of creation status (sucess)
 
    Returns
    -------
    .html: create note page
    """

    role = int(current_user.role)
    if role > 1:
        return "<h1>No Access</h1>"

    athletes = Athlete.query.all() #TODO: add watchData
    watchData=parse_CSV()
    if request.method == 'POST':
        writer_id = current_user.colby_id
        athlete_id = request.form.get('athletes')
        content = request.form.get('content')
        clearance = request.form.get('clearance')
        
        athlete = Athlete.query.filter_by(colby_id=athlete_id).first()

        if clearance == "Cleared":
            athlete.status=0
        elif clearance == "Warning":
            athlete.status=1
        elif clearance == "Ineligible":
            athlete.status=2

        new_note = Note (writer_id=writer_id, athlete_id=athlete.id, content=content)    
        db.session.add(new_note)
        db.session.commit()
        flash('Note created!', category='success')
        return redirect(url_for('views.create_note'))

    return render_template("create_note.html", athletes=athletes, watchData=watchData)


#Edit team
@views.route('/edit-team/<string:team_id>',methods=['GET','POST'])
@login_required
def edit_team(team_id):

    """redirect to the team edit page if user has access
    post edits of team information to database
    notify user of edit status (sucess)
 
    Returns
    -------
    .html: edit team page
    """
    team = Team.query.get(int(team_id))

    watchData=parse_CSV()
    if request.method == 'POST':
        athletes_add = request.form.getlist('athletes_add')
        athletes_del = request.form.getlist('athletes_del')
 
        coachnew = Coach.query.filter_by(colby_id=request.form.get('coaches')).first()


        teamdb = Team.query.filter_by(team_name=team.team_name).first()
        #teamdb = Team.query.filter_by(id=team.id).first()

        if teamdb.coach_id != coachnew.id:
            teamdb.coach_id=coachnew.id
            db.session.commit()
        for athlete in athletes_add:
            ath = Athlete.query.filter_by(colby_id=athlete).first()
            if ath.team_id!=teamdb.id:
                ath.team_id=teamdb.id
                db.session.commit()
        for athlete in athletes_del:
            ath = Athlete.query.filter_by(colby_id=athlete).first()
            if ath.team_id==teamdb.id:
                ath.team_id=None
                db.session.commit()
    

         

        flash('Changes successful', category='success')
        #return redirect(url_for('views.edit_team'))



    return render_template(
        "edit_team.html",
        team = team, 
        user=current_user,
        athletes_add = Athlete.query.filter_by(team_id = None),
        athletes_remove = Athlete.query.filter_by(team_id = team.id),
        coaches = Coach.query.all(),
        watchData=watchData
        )

@views.route('/team-select', methods = ['GET'])
def team_select():
    watchData = parse_CSV()
    return render_template('team_selection.html', teams = Team.query.all(), watchData = watchData)

def get_oura_recovery(start_date, end_date):

    data = {}

    if len(current_user.tokens) == 0:
        return 'No token found'
    try:
        res = oauth.oura.get(
        'usercollection/daily_sleep',
        params = {'start_date': start_date, 
        'end_date': end_date }
        )
    except:
        #Todo: Maybe redirect to authorize
        res = "Please re-authorize"

    return res

@views.route("/livesearch",methods=["POST","GET"])
@login_required
def livesearch():
    searchbox = request.form.get("text")
    teams = Team.query
    teams= teams.filter(Team.team_name.like('%' + searchbox + '%'))
    teams = teams.order_by(Team.team_name).all()
    res = {}
    for team in teams:
        res[team.id] = team.team_name
    #return render_template("admin_view.html", user=current_user, teams = teams, watchData={})
    return res
    #return "hello world"


@views.route("/livesearchathletes/<string:team_id>",methods=["POST","GET"])
@login_required
def livesearchathletes(team_id):
    searchbox = request.form.get("text")
    athletes = Athlete.query
    #filter by both text and also team _id
    athletes=athletes.filter_by(team_id=team_id)
    athletes= athletes.filter(Athlete.first_name.like('%' + searchbox + '%'))
    athletes = athletes.order_by(Athlete.first_name).all()
    print(athletes[0].id)
    res = {}
    for athlete in athletes:
        res[athlete.id] = [athlete.first_name, athlete.last_name, athlete.status]
    #return render_template("admin_view.html", user=current_user, teams = teams, watchData={})
    return res

#Create Users from CSV or Excel files Page
@views.route('/users-CSV', methods = ['GET', 'POST'])
@login_required
def users_csv():

    """redirect to Create Users from CSV or Excel files Page if user has access
  
    Returns
    -------
    .html: Create Users from CSV or Excel files Page
    """

    role = int(current_user.role)

    if role != 0 :
        return "<h1>No Access</h1>"

    if request.method == 'POST':
        csvFile = request.files['file']
        importCSV(csvFile)

    return render_template("users_csv.html",current_user=current_user, watchData = {})

    
