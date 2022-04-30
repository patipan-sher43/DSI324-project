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
            return redirect('/sign-up')
        else:
            flash("Logged in successfully!", category="success")
            return redirect("/home")

    else:
        flash("ไม่สามารถเข้าสู่ระบบได้ เนื่องจากอีเมลไม่ใช่รูปแบบของทางมหาลัย", category="error")
        return redirect('/')

@auth.route('/sign-up', methods=['GET', 'POST'])
@login_is_required
def sign_up():
    if request.method == 'POST':
        NameTH = request.form.get('NameTH')
        NameEN = request.form.get('NameEN')
        student_id = request.form.get('studentid') ######
        gender = request.form.get('genderchoose')
        program = request.form.get('programchoose')
        phone_number = request.form.get('phonenumber')
        # start_year = request.form.get('startyear')
        start_year = '25' + student_id[:2]
        email = session["email"]
        
        
        if len(NameTH) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        elif len(NameEN) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        elif len(student_id) != 10:
            flash('รหัสนักศึกษาไม่ตรงตามรูปแบบ', category='error')
        # elif len(start_year) != 4 or start_year[0] != '2' or start_year[1] != '5':
        #     flash('ปีการศึกษาไม่ถูกต้อง', category='error')
        else:
            #### add user to database
            student = Student(student_id = student_id, program_id = program, student_nameEN = NameEN,
                                student_nameTH = NameTH, start_year = int(start_year), expected_grad = int(start_year)+3,
                                student_email = email, student_phonenum = phone_number, gender = gender)
            db.session.add(student)
            db.session.commit()

            # df = pd.read_csv('default_regis_new.csv', encoding='utf-8')
            # last_item = Registrations.query.all()
            # print(last_item)
            # if last_item != []:
            #     num = int(last_item[-1].registration_id) + 1
                
            #     for i in range(df.shape[0]):
            #         regis_id = '0'*(10-len(str(num))) + str(num + i)
            #         curr = Registrations(registration_id = regis_id, student_id = student_id, subject_id = df.loc[i,'subject'], all_credits = df.loc[i,'credits'], academic_year = df.loc[i,'academic'], semester = df.loc[i,'semester'], section = df.loc[i,'section'], timestamp = datetime.date(df.loc[i,'year'], df.loc[i,'month'], df.loc[i,'day']))
            #         db.session.add(curr)
            #         db.session.commit()

            # else:
            #     for i in range(df.shape[0]):
            #         regis_id = '0'*(9) + str(i + 1)
            #         curr = Registrations(registration_id = regis_id, student_id = student_id, subject_id = df.loc[i,'subject'], all_credits = int(df.loc[i,'credits']), academic_year = int(df.loc[i,'academic']), semester = int(df.loc[i,'semester']), section = df.loc[i,'section'], timestamp = datetime.date(df.loc[i,'year'], df.loc[i,'month'], df.loc[i,'day']))
            #         db.session.add(curr)
            #         db.session.commit()

            flash('ลงทะเบียนสำเร็จ!', category='success')
            return redirect('/home')
    return render_template("sign_up.html")


@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("views.home_page"))
