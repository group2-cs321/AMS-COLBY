from time import timezone
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# User data class
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

    #Tokens
    tokens = db.relationship('OAuth2Token')
    
# Athlete data class
class Athlete(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    colby_id = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    status = db.Column(db.Integer)

    #team_id: connection to Team
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    peakNotes = db.relationship('Note')

# Coach data class
class Coach(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    colby_id = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))

    #teams: relationship to Team
    teams = db.relationship('Team')  

# Team data class
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(150), unique=True)

    #coach_id: connection to Coach
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.id'))

    #athletes: relationship to Athlete
    athletes = db.relationship('Athlete')
    
# Note data class 
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True) #id of the note
    writer_id = db.Column(db.Integer) #the person writing the note, either peak or super admin

    #athlete_id: connection to Athlete
    athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id')) #athlete the note is for
    content = db.Column(db.String(1500)) #the actual note content

class OAuth2Token(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=40))
    token_type = db.Column(db.String(length=40))
    access_token = db.Column(db.String(length=200))
    refresh_token = db.Column(db.String(length=200))
    expires_at = db.Column(db.Integer)
    user = db.Column(db.ForeignKey('user.id'))

    def to_token(self):
        return dict(
            access_token = self.access_token,
            token_type = self.token_type,
            refresh_token = self.refresh_token,
            expires_at = self.expires_at,
        )



