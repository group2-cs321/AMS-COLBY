from urllib import request
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Athlete, Coach, Team, Note
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
        if not team:
            return "<h1>NO ACCESS</h1>"
        return redirect(url_for("views.coach_dashboard", id = team.id))
    elif int(role) == 3:
        return redirect(url_for("views.athlete_dashboard"))
    else:
        return render_template("login.html")


@views.route('/create-team', methods = ['GET', 'POST'])
@login_required
def create_team():

    if int(current_user.team_data) != 0:
        return "<h1>No Access</h1>"

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
@login_required
def coach_dashboard(id):
    role = int(current_user.role)
    if role > 2:
        return "<h1>No Access</h1>"

    coach = Coach.query.filter_by(colby_id=current_user.colby_id).first()
    currentTeam = Team.query.get(id)
    watchData=parse_CSV()

    return render_template("coach_dashboard.html", coach=coach, current_user=current_user, team=currentTeam, watchData=watchData)

#Coach Athlete Page
@views.route('/coach/athlete/<string:id>', methods = ['GET', 'POST'])
@login_required
def athlete_coach_dashboard(id):

    role = int(current_user.role)
    if role > 2:
        return "<h1>No Access</h1>"

    athlete = Athlete.query.get(id)
    coach = Coach.query.filter_by(colby_id=current_user.colby_id).first()
    watchData=parse_CSV()
    currentTeam = Team.query.get(athlete.team_id)


    return render_template("athleteCoachView.html", athlete=athlete, coach=coach, current_user=current_user, team=currentTeam, watchData=watchData)

#Athlete Page
@views.route('/athlete', methods = ['GET', 'POST'])
@login_required
def athlete_dashboard():
    role = int(current_user.role)
    if role == 2:
        return "<h1>No Access</h1>"
    athlete = Athlete.query.filter_by(colby_id = current_user.colby_id).first()
    watchData=parse_CSV()


    return render_template("athleteView.html", athlete=athlete, current_user=current_user, watchData=watchData)


# Handles everything on the permissions page
@views.route('admin/permissions', methods = ['GET', 'POST'])
@login_required
def permission_page():
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



@views.route('/generate-report', methods = ['GET', 'POST'])
@login_required
def generate_report():

    #Deny access if athlete
    if int(current_user.permission_change) == 3:
        return "<h1>No Access</h1>"

    teams = Team.query.all()
   
    if request.method == 'POST':
        #have user select what team they want to get report on
        #query athlete_data from all athletes on requested team
        #display that data on front end by rendering a report html
        
        team_name = request.form.get('team')
        team_id = Team.query.filter_by(team_name=team_name).first()
        team_players = Athlete.query.filter_by(team_id=team_id).all()
        
        report_data = {}
        
        for athlete in team_players:
            #the line below I believe returns the athlete id. We need to return the athlete's jump data but it isnt in db
            athlete_data = Athlete.query.filter_by(colby_id=athlete).first()
            report_data[athlete] = athlete_data
            
    return render_template('generate_report.html', teams=teams)