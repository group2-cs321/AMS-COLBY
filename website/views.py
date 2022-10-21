from urllib import request
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    role = current_user.role
    print(role)

    if int(role) == 0:
        print("in condition")
        return render_template("admin_view.html", user=current_user)
    elif int(role) == 1:
        return render_template("peak_view.html", user=current_user)
    elif int(role) == 2:
        return render_template("coach_dashboard.html", user=current_user)
    elif int(role) == 3:
        return render_template("athlete_view.html", user=current_user)
    else:
        return render_template("login.html", user=current_user)


@views.route('/coach_view')
def coach_view():
    return render_template("coach_dashboard.html")