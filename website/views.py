from urllib import request
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():

    if current_user.role == 0:
        return render_template("admin_view.html", user=current_user)
    if current_user.role == 1:
        return render_template("peak_view.html", user=current_user)
    if current_user.role == 2:
        return render_template("coach_dashboard.html", user=current_user)
    if current_user.role == 3:
        return render_template("athlete_view.html", user=current_user)

    #return render_template("home.html", user=current_user)

@views.route('/create_user', methods = ['GET', 'POST'])
def create_user():
    return render_template("create_user.html")
@views.route('/coach_view')
def coach_view():
    return render_template("coach_dashboard.html")