from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash
from sqlalchemy import update
import json
views = Blueprint('views', __name__)
from . import db
from .models import Ticket, User, Company
@views.route('/', methods=['GET','POST'])
@login_required
def home():
    mycompany = Company.query.filter_by(id=1).first()

    return render_template("home.html", user=current_user, company=mycompany)

@views.route('/delete-tickets/<int:id>')
def delete_tickets(id):
    ticket =Ticket.query.get(id)
    try:
        db.session.delete(ticket)
        db.session.commit()
        flash("Ticket deleted successfully",category="success")
        return render_template("mytickets.html", user =current_user)
    except:
        pass
    return render_template("mytickets.html", user =current_user)


@views.route('/update-user/<int:id>', methods=['GET','POST'])
def update_user(id):

    if request.method== 'POST':
        role=request.form.get('myrole')
        team=request.form.get('myteam')
        #print(role)
        user =User.query.filter_by(id=id).first()
        try:
            user.role=role
            user.team=team
            db.session.commit()
            flash("User updated successfully",category="success")
            return render_template("home.html", user =current_user)
        except:
            print("error")
    return render_template("home.html", user =current_user)

