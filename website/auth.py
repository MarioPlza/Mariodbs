from flask import Blueprint, render_template, request , flash , redirect, url_for
from .models import User, Ticket , Company
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    company = Company.query.filter_by(id=1)
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password1')
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home', company=company))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.',category='error')
    return render_template("login.html", user =current_user)

@auth.route('/tickets', methods=['GET','POST'])
def tickets():
    if request.method == 'POST':
        ticket = request.form.get('ticket')
        subject = request.form.get('mysubject')
        print("My subject " + str(subject))
        if len(ticket) <1:
            flash('Note is too short!', category='error')
        elif str(subject)=="Select Subject":
            flash('Please select a subject!', category='error')
        else:
            new_ticket = Ticket(data=ticket, user_id=current_user.id, subject=subject)
            db.session.add(new_ticket)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template("mytickets.html", user =current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    mycompany = Company.query.filter_by(id=1).first()
    if mycompany:
        pass
    else:
        new_company = Company(company_name="testcompany")
        db.session.add(new_company)
        db.session.commit()
        print('company created!')
        new_user = User(email="admin@mycompany.com", first_name="admin",
                       password=generate_password_hash("admin", method='sha256'), role="admin", team="admin",
                       company_id=1)
        db.session.add(new_user)
        db.session.commit()

    if request.method== 'POST':
        email= request.form.get('email')
        first_name= request.form.get('firstName')
        password1= request.form.get('password1')
        password2=request.form.get('password2')
        role = "Operations Analyst"
        team = "Operations"
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email)<4:
            flash('Email must be greater than 4 characters.', category='error')
        elif len(first_name)<2:
            flash('First Name must be greater than 1 characters.', category='error')
        elif password1 !=password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) <7:
            flash('Password must be greater than 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name,password=generate_password_hash(password1, method='sha256'),role=role,team=team,company_id=1)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!', category='success')
            login_user(user, remember=True)
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
