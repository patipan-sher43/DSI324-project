from flask import Flask, session, abort, redirect, request, url_for, render_template, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from google_auth_oauthlib.flow import Flow
import google.auth.transport.requests
from pip._vendor import cachecontrol
from google.oauth2 import id_token
import requests
import os, io
import pathlib
import base64
from PIL import Image

global subject_all
subject_all = {
    '1':['DSI100', 'DSI200', 'TU100', 'TU104', 'TU108'],
    '2':['DSI201', 'DSI202', 'DSI203', 'DSI205', 'TU105', 'TU106'],
    '3':['DSI204', 'DSI206', 'DX312', 'DX313', 'EL217', 'TU101', 'TU131'],
    '4':['DSI207', 'DX310', 'DX311', 'DX314', 'TU107']
}


app = Flask(__name__)
app.secret_key = "DSI324-project"
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:fordzaa55@localhost/curriculum_dataset'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'fordzaa55'
app.config['MYSQL_DB'] = 'curriculum_dataset'

mysql = MySQL(app)

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

@app.route('/google-login', methods=['GET', 'POST'])
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route('/callback')
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

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    if '@dome.tu.ac.th' in session['email']:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM student WHERE student_email = %(email)s', {'email': session["email"]})
        result = cursor.fetchone()
        if result is None:
            return redirect('/sign-up')
        else:
            return redirect("/home")

# @app.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         NameTH = request.form.get('NameTH')
#         NameEN = request.form.get('NameEN')
#         student_id = request.form.get('studentid')
#         gender = request.form.get('genderchoose')
#         program = request.form.get('programchoose')
#         phone_number = request.form.get('phonenumber')
#         start_year = request.form.get('startyear')

#         
#         if len(firstName) <= 1:
#             flash('ชื่อต้องมีความยาวมากกว่า 1 ตัวอักษร', category='error')
#         elif len(lastName) <= 1:
#             flash('นามสกุลต้องมีความยาวมากกว่า 1 ตัวอักษร', category='error')
#         elif len(student_id) != 10:
#             flash('รหัสนักศึกษาไม่ตรงตามรูปแบบ', category='error')
#         elif len(start_year) != 4 or start_year[0] != '2' or start_year[1] != '5':
#             flash('ปีการศึกษาไม่ถูกต้อง', category='error')
#         else:
#             # add user to database
#             insertcmd = f"INSERT into student(student_id, program_id, student_nameEN, student_nameTH, start_year, expected_grad, student_email, student_phonenum, gender) VALUES ({student_id},{program},{NameEN},{NameTH},{start_year},{str(int(start_year)+3)},{session['email']},{phone_number},{gender});"
#             cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # cursor.execute(insertcmd)
            # mysql.connect().commit()
#             flash('Account created!.', category='success')
#             return redirect('/home')
        # else:
        #     session.clear()
#     return render_template("sign_up.html")


@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/')
def home_page():
    return render_template('home_all.html')

@app.route('/home')
@login_is_required
def home():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM student WHERE student_email = %(email)s', {'email': session["email"]})
    result = cursor.fetchone()
    if result['gender'] == 'M':
        gender = 'ชาย'
    elif result['gender'] == 'F':
        gender = 'หญิง'
    else:
        gender = 'อื่นๆ'
    return render_template("home.html", result = result, gender = gender)

@app.route('/curriculum', methods=['GET', 'POST'])
def curriculum_page():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM student WHERE student_email = %(email)s', {'email': session["email"]})
    result = cursor.fetchone()
    start_year = result['start_year']
    semester_result = None
    subject_list = None
    subject_item = None
    subject_dict = None
    sub_sem_list = None
    if request.method == 'POST':
        semester = request.form.get("academic-year")
        sem_list = semester.split('/')
        sem_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sem_cursor.execute('SELECT * FROM registrations WHERE student_id = %(student_id)s and semester = %(semester)s and academic_year = %(acad_year)s', {'student_id': result["student_id"], 'semester': int(sem_list[1]), 'acad_year': int(sem_list[2])})
        semester_result = sem_cursor.fetchone()
        if semester_result is not None:
            subject_list = semester_result['subject_id'].split(',')
            subject_cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            subject_dict = {}
            for i in subject_list:
                subject_cursor.execute('SELECT * FROM subjects WHERE subject_id = %(subject_id)s', {'subject_id': i})
                subject_item = subject_cursor.fetchone()
                subject_dict[i] = [subject_item['subject_name'], subject_item['credits']]
            sub_sem_list = subject_all[sem_list[0]]
    else: 
        semester = "..."

    return render_template('student_curriculum.html', semester = semester, start_year = start_year, sem_result = semester_result, subject_list = subject_list, subject_dict = subject_dict, sub_sem_list = sub_sem_list)

@app.route('/e-check-s', methods=['GET', 'POST'])
def em_check_curriculum_page():
    return render_template('em_check_s.html')

@app.route('/e-overall', methods=['GET', 'POST'])
def em_overall_page():
    return render_template('em_overall.html')

@app.route('/de-overall', methods=['GET', 'POST'])
def de_overall_page():
    return render_template('de_overall.html')



if __name__ == '__main__':
    app.run(debug=True)