from time import timezone
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    colby_id = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(sb.String(150))
    password = db.Column(db.String(150))

    role = db.Column(db.String(150))

    notes = db.Column(db.Integer)
    peak_data= db.Column(db.Integer)
    athlete_data = db.Column(db.Integer)
    team_data = db.Column(db.Integer)
    account_create = db.Column(db.Integer)
    permission_change = db.Column(db.Integer)