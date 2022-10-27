from urllib import request
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Athlete, Coach, Team, Note
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    role = current_user.role
    print(current_user)
    print(role)
    if int(role) == 0:
        return render_template("admin_view.html", user=current_user, teams = Team.query.all())
    elif int(role) == 1:
        return render_template("peak_view.html", user=current_user)
    elif int(role) == 2:
        coach = Coach.query.filter_by(colby_id=current_user.colby_id).first()
        team = Team.query.filter_by(coach_id=coach.id).first()
        return redirect(url_for("views.coach_dashboard", id= team.id))
    elif int(role) == 3:
        athlete = Athlete.query.filter_by(colby_id=current_user.colby_id).first()
        return redirect(url_for("views.athlete_dashboard", id = athlete.id))
    else:
        return render_template("login.html")

@views.route('/create-team', methods = ['GET', 'POST'])
def create_team():

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
            return render_template('create_team.html', user=current_user, athletes = Athlete.query.all(), coaches = Coach.query.all())

        if len(team_name) < 1 or len(athletes) < 1:
             flash('Please input a valid team name', category = 'error')
             return render_template('create_team.html', user=current_user, athletes = Athlete.query.all(), coaches = Coach.query.all())
        else:
            new_team = Team(team_name=team_name, coach_id = coach.id)
            db.session.add(new_team)
            db.session.commit()

            for athlete in athletes:
                ath = Athlete.query.filter_by(colby_id=athlete).first()
                ath.team_id = new_team.id
                db.session.commit()

        flash('Team created Succesfully', category='success')
        return render_template('create_team.html', user=current_user, athletes = Athlete.query.all(), coaches = Coach.query.all())
        
    return render_template('create_team.html', user=current_user, athletes = Athlete.query.all(), coaches = Coach.query.all())


#coach Dasboard page
@views.route('/team/<string:id>', methods = ['GET', 'POST'])
def coach_dashboard(id):
    coach = Coach.query.filter_by(colby_id=current_user.colby_id).first()
    currentTeam = Team.query.get(id)

    return render_template("coach_dashboard.html", coach=coach, current_user=current_user, team=currentTeam)

#Coach Athlete Page
@views.route('/coach/athlete/<string:id>', methods = ['GET', 'POST'])
def athlete_coach_dashboard(id):
    athlete = Athlete.query.get(id)
    coach = Coach.query.filter_by(colby_id=current_user.colby_id).first()
    currentTeam = Team.query.get(athlete.team_id)

    return render_template("athleteCoachView.html", athlete=athlete, coach=coach, current_user=current_user, team=currentTeam)

# Handles everything on the permissions page
@views.route('admin/permissions', methods = ['GET', 'POST'])
def permission_page():
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
        user.notes = user.notes
        user.create_account = create_account
        user.permission_change = permission_change
        

        db.session.commit()


    return render_template('permission.html', current_user = current_user, users = User.query.all())
#Athlete Page
@views.route('/athlete/<string:id>', methods = ['GET', 'POST'])
def athlete_dashboard(id):
    athlete = Athlete.query.get(id)

    return render_template("athleteView.html", athlete=athlete, current_user=current_user)


#Peak Notes
@views.route('/new-note',methods=['GET','POST'])
def create_note():
    athletes = Athlete.query.all()
    
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

    return render_template("create_note.html", athletes=athletes)