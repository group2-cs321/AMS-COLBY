from urllib import request
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Athlete, Coach, Team, Note
from werkzeug.security import generate_password_hash
from . import db
import json
from csv import DictReader
import pandas as pd


views = Blueprint('views', __name__)

def parse_CSV():

    """parse CSV file
    
    Reads an athelete data csv file
 
    Returns
    -------
    watchData: nested list of strings and floats
    """

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

def importCSV (fileAdress):
    '''
    ImportCSV will read a csv file and create the set of users, CSV should follow the next format: [Colby ID, Name, Last Name]

    Parameters:
    -----------
    filepath: string. location of the data 

    Output:
    ------------
    repeatUsers: list. a list of Colby_IDs
    ''' 

    #reads the data and converts it to numpy
    data = pd.read_csv(fileAdress)
    data = data.to_numpy()

    repeatUsers=[]

    #goes though the data an obtains the information from teh CSV
    for athlete in data:
        colby_id = data[0]
        first_name = data[1]
        last_name = data[2]
        password1 = 12345678
        athlete_data = 3
        team_data = 3
        notes = 3
        create_account = 3
        permission_change = 3
        role = 3

        user = User.query.filter_by(colby_id=colby_id).first()

        if user:
            repeatUsers.append(colby_id)
        else:
            #add user to database
            new_user = User(colby_id=colby_id, first_name=first_name, last_name = last_name,
                 password=generate_password_hash(password1, method='sha256'),
                 role = role, athlete_data = athlete_data, team_data = team_data, notes = notes,
                 account_create = create_account, permission_change = permission_change)
            if int(role) == 3:
                athlete = Athlete(colby_id=colby_id, first_name=first_name, last_name = last_name)
                db.session.add(athlete)
            
            db.session.add(new_user)
            db.session.commit()
    
    if len(repeatUsers) != 0:
        flash("These students have already an account: " + repeatUsers + ". The rest of the users have been created", category='error')

    elif len(repeatUsers) == 0:
        flash("All users have been succesfully created", category='success')

    return repeatUsers

    

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
        return render_template('create_team.html', user=current_user, athletes = Athlete.query.all(), coaches = Coach.query.all(), watchData=watchData)
        
    return render_template('create_team.html', user=current_user, athletes = Athlete.query.all(), coaches = Coach.query.all(), watchData=watchData)


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
@views.route('/coach/athlete/<string:id>', methods = ['GET', 'POST'])
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


    return render_template("athleteCoachView.html", athlete=athlete, coach=coach, current_user=current_user, team=currentTeam, watchData=watchData)

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


    return render_template("athleteView.html", athlete=athlete, current_user=current_user, watchData=watchData)


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
@views.route('/edit-team',methods=['GET','POST'])
@login_required
def edit_team():

    """redirect to the team edit page if user has access
    post edits of team information to database
    notify user of edit status (sucess)
 
    Returns
    -------
    .html: edit team page
    """

    watchData=parse_CSV()
    if request.method == 'POST':
        team = request.form.get('team')
        athletes_add = request.form.getlist('athletes_add')
        athletes_del = request.form.getlist('athletes_del')
 
        coachnew = Coach.query.filter_by(colby_id=request.form.get('coaches')).first()


        teamdb = Team.query.filter_by(team_name=team).first()

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
        return redirect(url_for('views.edit_team'))


    return render_template("edit_team.html", teams = Team.query.all(), user=current_user, athletes = Athlete.query.all(), coaches = Coach.query.all(), watchData=watchData)


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
        repeat = importCSV(csvFile)

        print(repeat)

    return render_template("<h1> Access</h1>",current_user=current_user)

