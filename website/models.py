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
    #teams = db.relationship('Team')


class Coach(User):
    #teams = db.relationship('Team')
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    #teams = db.relationship('Team', secondary='CoachTeam', backref = 'Coach')

    teams = db.relationship('Team')

class Athlete(User):
    status = db.Column(db.Integer)
    in_season = db.Column(db.Boolean)


class Team(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(150), unique=True)
    # coaches = db.Column(db.Integer, db.ForeignKey('user.id')) #db.relationship('Coach', secondary='CoachTeam', backref = 'Team')
    athletes = db.Column(db.Integer, db.ForeignKey('user.id'))

    athletes = db.relationship('User')


    
