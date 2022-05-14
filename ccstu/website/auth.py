from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from pip._vendor import cachecontrol
from google.oauth2 import id_token
import requests
from .models import *
from . import db
import os
import pathlib
import pandas as pd
import datetime

auth = Blueprint('auth', __name__)


os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'

GOOGLE_CLIENT_ID = "1045071512519-d7oifhgkh36b4djmefassuupn22l3p11.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback")


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401) # Authorization required
        else:
            return function()
    return wrapper

# def login_is_required_user(function):
#     def wrapper(*args, **kwargs):
#         if "google_id" not in session:
#             return abort(401) # Authorization required
#         else:
#             return function()
#     return wrapper

@auth.route('/google-login', methods=['GET', 'POST'])
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@auth.route('/callback')
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500) # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token = credentials._id_token,
        request = token_request,
        audience = GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")  ### UNIQUE ID
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    session["picture"] = id_info.get("picture")
    if '@dome.tu.ac.th' in session['email']:
        result = Student.query.filter_by(student_email = session["email"]).first()

        if result is None:
            global email_register
            email_register = session["email"]
            flash("ไม่พบข้อมูล โปรดกรอกข้อมูลเพื่อเข้าสู่ระบบ", category="error")
            return redirect(url_for('auth.student'))
        else:
            flash("Logged in successfully!", category="success")
            return redirect(url_for('views.student'))

    elif session['email'] == 'fords477@gmail.com':
        result = User.query.filter_by(email = session["email"]).first()

        if result is None:
            global email_user_register
            email_user_register = session["email"]
            flash("ไม่พบข้อมูล โปรดกรอกข้อมูลเพื่อเข้าสู่ระบบ", category="error")
            return redirect(url_for('auth.user_em'))
        else:
            flash("Logged in successfully!", category="success")
            return redirect(url_for('views.user_em'))

    else:
        flash("ไม่สามารถเข้าสู่ระบบได้ เนื่องจากอีเมลไม่ใช่รูปแบบของทางมหาลัย", category="error")
        return redirect(url_for('views.home_page'))

@auth.route('/sign-up', methods=['GET', 'POST'], endpoint='student')
@login_is_required
def sign_up():
    if request.method == 'POST':
        NameTH = request.form.get('NameTH')
        NameEN = request.form.get('NameEN')
        student_id = request.form.get('studentid') ######
        gender = request.form.get('genderchoose')
        program = request.form.get('programchoose')
        phone_number = request.form.get('phonenumber')
        start_year = '25' + student_id[:2]
        email = session["email"]
        
        
        if len(NameTH) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        elif len(NameEN) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        elif len(student_id) != 10:
            flash('รหัสนักศึกษาไม่ตรงตามรูปแบบ', category='error')
        else:
            #### add user to database
            student = Student(student_id = student_id, program_id = program, student_nameEN = NameEN,
                                student_nameTH = NameTH, start_year = int(start_year), expected_grad = int(start_year)+3,
                                student_email = email, student_phonenum = phone_number, gender = gender)
            db.session.add(student)
            db.session.commit()

            flash('ลงทะเบียนสำเร็จ!', category='success')
            return redirect(url_for('views.student'))
    return render_template("sign_up.html")

@auth.route('/user-sign-up', methods=['GET', 'POST'], endpoint='user_em')
@login_is_required
def user_em_sign_up():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        NameTH = request.form.get('NameTH')
        NameEN = request.form.get('NameEN')
        gender = request.form.get('genderchoose')
        program = request.form.get('programchoose')
        role = 'เจ้าหน้าที่'
        email = session['email']

        if len(NameTH) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        elif len(NameEN) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        elif len(user_id) != 7:
            flash('รหัสประจำตัวเจ้าหน้าที่ไม่ตรงตามรูปแบบ', category='error')
        else:
            #### add user to database
            user = User(user_id = user_id, program_id = program, nameEN = NameEN,
                                nameTH = NameTH, role = role, gender = gender, email = email)
            db.session.add(user)
            db.session.commit()
            flash('ลงทะเบียนสำเร็จ!', category='success')
            return redirect(url_for('views.user_em'))

    return render_template('user_em_sign_up.html')


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("views.home_page"))
