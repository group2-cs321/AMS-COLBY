from urllib import request
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Athlete, Coach, Team
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

#Athlete Page
@views.route('/athlete/<string:id>', methods = ['GET', 'POST'])
def athlete_dashboard(id):
    athlete = Athlete.query.get(id)

    return render_template("athleteView.html", athlete=athlete, current_user=current_user)


