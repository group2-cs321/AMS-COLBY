'''
File with functions used in the backend
'''

#Imports
from werkzeug.security import generate_password_hash
from models import User, Coach, Athlete
from . import db


#Functions
def new_user(colby_id, first_name, last_name, password, role, athlete_data, team_data, notes, create_account, permission_change):
    """new_user
    
    Creates a new user and commits to the database
 
    Parameters
    -------
    colby_id: string
    first_name: string
    last_name: string
    pasword: string
    role: int
    athlete_data: int
    team_data: int
    notes: int
    create_account: int
    permission_change: int

    Return
    ------
    """

    #add user to database
    new_user = User(colby_id=colby_id, first_name=first_name, last_name = last_name,
               password=generate_password_hash(password, method='sha256'),
               role = role, athlete_data = athlete_data, team_data = team_data, notes = notes,
               account_create = create_account, permission_change = permission_change)

    db.session.add(new_user)
    db.session.commit()

    return

def new_athlete(colby_id, first_name, last_name):
    """new_athlete
    
    Creates a new athlete and commits to the database
 
    Parameters
    -------
    colby_id: string
    first_name: string
    last_name: string

    Return
    ------
    """

    #add athelte to database
    athlete = Athlete(colby_id=colby_id, first_name=first_name, last_name = last_name)
    db.session.add(athlete)
    db.session.commit()

    return

def new_coach(colby_id, first_name, last_name):
    """new_coach
    
    Creates a new coach and commits to the database
 
    Parameters
    -------
    colby_id: string
    first_name: string
    last_name: string
    
    Return
    ------
    """

    #add athelte to database
    coach = Coach(colby_id=colby_id, first_name=first_name, last_name = last_name)
    db.session.add(coach)
    db.session.commit()

    return





