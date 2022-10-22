from time import timezone
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# CoachTeam = db.Table('CoachTeam',
#                     db.Column('id', db.Integer, db.primary_key=True),
#                     db.Column('coach_id', db.Integer, db.ForeignKey('coach.id')),
#                     db.Column('team_id', db.Integer, db.ForeignKey('team.id')))

# AthleteTeam = db.Table('AthleteTeam',
#                     db.Column('id', db.Integer, db.primary_key=True),
#                     db.Column('coach_id', db.Integer, db.ForeignKey('coach.id')),
#                     db.Column('team_id', db.Integer, db.ForeignKey('team.id')))

# create one table per typer of user? Maybe that will work. Then we can only have reference to coaches and athletes in Teams

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    colby_id = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))

    role = db.Column(db.String(150))

    notes = db.Column(db.Integer)
    #peak_data= db.Column(db.Integer)
    athlete_data = db.Column(db.Integer)
    team_data = db.Column(db.Integer)
    account_create = db.Column(db.Integer)
    permission_change = db.Column(db.Integer)


class Athlete(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    colby_id = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))

    role = db.Column(db.String(150))

    notes = db.Column(db.Integer)
    #peak_data= db.Column(db.Integer)
    athlete_data = db.Column(db.Integer)
    team_data = db.Column(db.Integer)
    account_create = db.Column(db.Integer)
    permission_change = db.Column(db.Integer)
    status = db.Column(db.Integer)

    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

class Coach(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    colby_id = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))

    role = db.Column(db.String(150))

    notes = db.Column(db.Integer)
    #peak_data= db.Column(db.Integer)
    athlete_data = db.Column(db.Integer)
    team_data = db.Column(db.Integer)
    account_create = db.Column(db.Integer)
    permission_change = db.Column(db.Integer)


    # team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

    team = db.relationship('Team')


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(150), unique=True)
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'))
    athletes = db.relationship('Athlete')
    


    
