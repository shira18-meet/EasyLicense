from flask import (
        Blueprint, redirect, render_template,
        Response, request, url_for
)
from flask_login import login_user, login_required, logout_user
from sqlalchemy.exc import IntegrityError

from project import db
from project.forms import RegisterForm, LoginForm
from project.models import User,Teacher,Booking

import firebase_admin

<<<<<<< HEAD
import firebase_admin, firebase_admin.auth, firebase_admin.db, firebase_admin.storage

import json
from pprint import pprint

with open('easylicense-e9174-firebase-adminsdk-tfk2q-14c4144edf.json') as f:
    data = json.load(f)

pprint(data)

cred = firebase_admin.credentials.Certificate('easylicense-e9174-firebase-adminsdk-tfk2q-14c4144edf.json')
default_app = firebase_admin.initialize_app(cred)
=======
#cred = firebase_admin.credentials.Certificate('easylicense-e9174-firebase-adminsdk-tfk2q-14c4144edf.json')
#app = app = firebase_admin.initialize_app(cred)
>>>>>>> a065f1227cc6d7fe6e74fb47b81d337ddaa1bdba

users_bp = Blueprint('users', __name__)


@users_bp.route('/signup', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('psw')
        password2= request.form.get('psw-repeat')
        name= request.form.get('name')
        city=request.form.get('city')
        fee=request.form.get('fee')
        description=request.form.get('description')
        area=request.form.get('area')
        phonenum=request.form.get('phonenum')
        car_type=request.form.get('car_type')
        license_num=request.form.get('license_num')
        languages=request.form.get('languages')
        profilepic=request.form.get('profilepic')
        #if profilepic is None:
            #profilepic=""
        if password== password2:
            user = User.query.filter_by(email=email).first()
            if user is None:
                firebase_admin.auth.create_user(email=email,password=password,display_name=name)
                user=User(email,password)
                db.session.add(user)
                db.session.commit()

<<<<<<< HEAD

                teacher=Teacher(user.id,name,area2,city,description,fee,phonenum,languages,profilepic,car_type,license_num)
                f_teacher={'id':teacher.id,'user_id':teacher.user_id,'name':teacher.name,'area':teacher.area,'city':teacher.city,'description':teacher.description,'cost':teacher.cost,'phone_num':teacher.phone_num,'languages':teacher.languages,'profile_picture':teacher.profile_picture,'car_type':teacher.car_type,'license_num':teacher.license_num}
                firebase_admin.db.Reference.child("teachers").child(firebase_admin.auth.UserInfo.uid).set(f_teacher)

=======
                teacher=Teacher(user.id,name,area,city,description,fee,phonenum,languages,profilepic,car_type,license_num)
>>>>>>> a065f1227cc6d7fe6e74fb47b81d337ddaa1bdba
                db.session.add(teacher)
                db.session.commit()
                login_user(user, remember=True)
                return redirect('profile_template')
            ##next_page = request.args.get('next')
            ##if not next_page or url_parse(next_page).netloc != '':
               ## next_page = url_for('private_route')
            ##return redirect(next_page)
        else:
            return Response("<p>invalid form</p>")

    return render_template('login_signup.html', form=form)
                

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    loginform = LoginForm(request.form)
    if request.method == 'POST':
        if loginform.validate_on_submit():
            email = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user is None or not user.check_password(password):
                return Response("<p>Incorrect username or password</p>")
            login_user(user, remember=True)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('profile_template')
            return redirect(next_page)
        else:
            return Response("<p>invalid form</p>")
    else:
        return render_template('login.html', loginform=loginform)

@users_bp.route('/login_signup')
def login_signup():
    loginform = LoginForm(request.form)
    return render_template('login_signup.html',loginform=loginform)

@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return Response("<p>Logged out</p>")

@users_bp.route('/teacher/<int:teacher_id>')
def profile(teacher_id):
    teacher = db.session.query().filter_by(id=teacher_id).first()
    return render_template('profile_template.html', teacher=teacher)

@users_bp.route('/booking/<int:teacher_id>')
def booking(teacher_id):
    teacher = db.session.query(Teacher).filter_by(id=teacher_id).first()
    return render_template('booking.html', teacher=teacher)