#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort, jsonify
from website.auth import login_is_required
from . import connection
from flask_mysqldb import MySQLdb
import ast
# from .models import *
# from . import db
import json, os
import datetime
import decimal

views = Blueprint('views', __name__)


# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'

@views.route('/')
def home_page():
    return render_template('home_all.html')

@views.route('/api-service', methods=['GET', 'POST'])
def api_page():
    result = None
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        choice = request.form.get('api-topic')
        if choice == 'subject-ALL':
            # qall = Subjects.query.all()
            cursor.execute("SELECT * FROM subjects")
            qall = cursor.fetchall()

            cols = ['subject_id', 'subject_type_id', 'subject_name', 'credits', 'havePrerequisite', 'prerequisite_id']
            get_list = []
            for item in qall:
                item_dict = {}
                item_dict['subject_id'] = item['subject_id']
                item_dict['subject_type_id'] = item['subject_type_id']
                item_dict['subject_name'] = item['subject_name']
                item_dict['credits'] = item['credits']
                item_dict['havePrerequisite'] = item['havePrerequisite']
                item_dict['prerequisite_id'] = item['prerequisite_id']
                get_list.append(item_dict)
            print(get_list[0])
            result = get_list
            # result = json.dumps(get_list, indent=2, sort_keys=True, ensure_ascii=False).encode('utf-8')
            # result = result.decode()
        elif choice == 'subject-type':
            # qall = Subject_type.query.all()
            cursor.execute("SELECT * FROM subject_type")
            qall = cursor.fetchall()
            # cols = ['subject_type_id', 'subject_type_name', 'sub_type_name']
            # get_list = [{col: getattr(d, col) for col in cols} for d in qall]
            # string = "\"" + str(get_list) + "\""
            # print(string)
            # load_js = json.loads(string)
            result = json.dumps(qall, indent=2, sort_keys=True, ensure_ascii=False).encode('utf-8')
            result = result.decode()
            # return redirect(url_for('views.api_result', result = result))
    return render_template('api_page.html', result = result)

# @views.route('/api-service/result', methods=['GET', 'POST'])
# def api_result():
#     return jsonify(result = result)

@views.route('/student/home', methods=['GET', 'POST'], endpoint='student')
@login_is_required
def student_home():
    
    image = session["picture"]

    # student = Student.query.filter_by(student_email = session["email"]).first()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM student WHERE student_email = %s", (session["email"],))
    student = cursor.fetchone()
    cursor.close()

    # if student.gender == 'M':
    #     gender = 'ชาย'
    # elif student.gender == 'F':
    #     gender = 'หญิง'
    # else:
    #     gender = 'อื่นๆ'
    
    if student['gender'] == 'M':
        gender = 'ชาย'
    elif student['gender'] == 'F':
        gender = 'หญิง'
    else:
        gender = 'อื่นๆ'

    return render_template("home.html", result = student, gender = gender, image = image)

@views.route('/student/edit', methods=['GET', 'POST'])
def student_edit_info():
    # student = Student.query.filter_by(student_email = session['email']).first()

    if request.method == 'POST':
        NameTH = request.form.get('NameTH')
        NameEN = request.form.get('NameEN')
        gender = request.form.get('genderchoose')
        phone_number = request.form.get('phonenumber')
        email = session["email"]

        if len(NameTH) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        elif len(NameEN) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        else:
            ### Update user to database
            # student.student_id = student.student_id
            # student.program_id = student.program_id
            # student.student_nameEN = NameEN
            # student.student_nameTH = NameTH
            # student.gender = gender
            # student.student_phonenum = phone_number
            # student.start_year = student.start_year
            # student.expected_grad = student.expected_grad
            # student.student_email = email

            # db.session.add(student)
            # db.session.commit()

            cursor = connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("UPDATE student SET student_nameEN= %s, student_nameTH= %s, student_email= %s, student_phonenum= %s, gender= %s WHERE student_email = %s", (NameEN, NameTH, email, phone_number, gender, session["email"]))
            connection.commit()
            cursor.close()

            flash('แก้ไขข้อมูลสำเร็จ!.', category='success')
            return redirect(url_for('views.student'))
    return render_template('student_home_edit.html')

@views.route('/student/curriculum', methods=['GET', 'POST'])
def curriculum_page():
    # result = Student.query.filter_by(student_email = session["email"]).first()
    # start_year = result.start_year

    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM student WHERE student_email = %s", (session["email"],))
    result = cursor.fetchone()  
    start_year = result['start_year']

    semester_result = None
    subject_list = None
    subject_item = None
    subject_dict = None
    sub_sem_list = None
    section_list = None
    if request.method == 'POST':
        semester = request.form.get("academic-year")
        sem_list = semester.split('/')
    
        # semester_result = Registrations.query.filter_by(student_id = result.student_id, semester = int(sem_list[1]), academic_year = int(sem_list[0])).first()
        cursor.execute("SELECT * FROM registrations WHERE student_id = %s and semester = %s and academic_year = %s", (result['student_id'], int(sem_list[1]), int(sem_list[0])))
        semester_result = cursor.fetchone()

        if semester_result is not None:
            # subject_list = semester_result.subject_id.split(',')
            subject_list = semester_result['subject_id'].split(',')
           
            subject_dict = {}
            for i in subject_list:
                # subject_item = Subjects.query.filter_by(subject_id = i).first()
                # subject_dict[i] = [subject_item.subject_name, subject_item.credits]

                cursor.execute("SELECT * FROM subjects WHERE subject_id = %s", (i,))
                subject_item = cursor.fetchone()
                subject_dict[i] = [subject_item['subject_name'], subject_item['credits']]

            # section_list = semester_result.section.split(',')
            section_list = semester_result['section'].split(',')

            if result['program_id'] == 'DSI':
                curri_format_id = 'D' + sem_list[0] + sem_list[1]
                # sub_sem_list = Curriculum_format.query.filter_by(curriculum_formatID = curri_format_id).first()
                cursor.execute("SELECT * FROM curriculum_format WHERE curriculum_formatID = %s", (curri_format_id,))
                sub_sem_list = cursor.fetchone()
    else: 
        semester = "..."

    return render_template('student_curriculum.html', semester = semester, start_year = start_year, sem_result = semester_result, subject_list = subject_list, subject_dict = subject_dict, sub_sem_list = sub_sem_list, section = section_list)



@views.route('/student/test-regis', methods=['GET', 'POST'])
def student_test_regis():
    # result = Student.query.filter_by(student_email = session['email']).first()
    # start_year = result.start_year

    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM student WHERE student_email = %s", (session["email"],))
    result = cursor.fetchone()
    start_year = result['start_year']

    final_match, acad_year, semester, result_curr_format, list_final_match = None, None, None, None, None
    if request.method == 'POST':
        form_result = request.form.get('academic-year').split('/')
        module4 = request.form.get('module')
        semester, acad_year = form_result[0], form_result[1]
        sub_list = []
        correct_sub = True

        final_match = None

        form_sub = [request.form.get('s1'), request.form.get('s2'), request.form.get('s3'),
                    request.form.get('s4'), request.form.get('s5'), request.form.get('s6'),
                    request.form.get('s7'), request.form.get('s8'), request.form.get('s9')]

        for i in form_sub:
            if i != 'None':
                if len(i) < 5:
                    correct_sub = False
                else:
                    sub_list.append(i)
        if correct_sub:
            if result['program_id'] == 'DSI':
                curri_format_id = 'D' + semester

                cursor.execute('SELECT * FROM curriculum_format WHERE curriculum_formatID = %(id)s', {'id': curri_format_id})
                result_curr_format = cursor.fetchone()

                # result_curr_format = Curriculum_format.query.filter_by(curriculum_formatID = curri_format_id).first()

                final_match = None
                if result_curr_format is not None:
                    if curri_format_id != 'D41' and module4 == 'None':
                        final_match = {}
                        for sub in sub_list:
                            if sub in result_curr_format['subject_id']:
                                final_match[sub] = 'ลงถูกต้องตามแผนการเรียน'
                            else:
                                if curri_format_id == 'D22' and (sub == 'BA291' or sub == 'PY252'):
                                    final_match[sub] = 'ลงถูกต้องตามแผนการเรียน (วิชาเลือกเสรี)'
                                else:
                                    final_match[sub] = 'ลงผิดลำดับ / ล่าช้า'
                        list_final_match = list(final_match.keys())
                    elif curri_format_id != 'D41' and module4 != 'None':
                        flash(f'ไม่สามารถลงทะเบียนได้ เนื่องจากภาคเรียนที่ {semester[1]}/{acad_year} ไม่มีการเลือกหมวดวิชา! กรุณาระบุช่องเลือกหมวดวิชาเป็น "ไม่มี"', category='error')
                    else:
                        final_match = {}
                        dict_module = ast.literal_eval(result_curr_format['subject_id'])
                        if module4 != 'None':
                            for sub in sub_list:
                                if sub in dict_module[module4]:
                                    final_match[sub] = 'ลงถูกต้องตามแผนการเรียน'
                                else:
                                    final_match[sub] = 'ลงผิดลำดับ / ล่าช้า'
                            list_final_match = list(final_match.keys())
                        else:
                            flash(f'กรุณาเลือกหมวดวิชาที่จะลงทะเบียนในภาคเรียนที่ 1/{acad_year}', category='error')
                else:
                    flash('ไม่พบข้อมูล!', category='error')
        else:
            flash('รหัสวิชาต้องมีความยาว 5 ตัวขึ้นไป และต้องลงอย่างน้อย 1 วิชา', category='error')

    return render_template('student_test_regis.html', start_year = start_year, final_match = final_match, academic_year = acad_year, semester = semester, result_format = result_curr_format, idx = list_final_match)

@views.route('/add', methods=['GET', 'POST'])
def student_add_subject():
    # student = Student.query.filter_by(student_email = session["email"]).first()

    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM student WHERE student_email = %s", (session["email"],))
    student = cursor.fetchone()

    acad_year, semester = None,None
    if request.method == 'POST':
        form_result = request.form.get('academic-year').split('/')
        module4 = request.form.get('module')
        semester, acad_year = form_result[0], form_result[1]
        sub_list = {}
        section_set = ['650501', '650502']

        #### Check if form invalid
        correct_sub, None_sub = True, False
        correct_sec, None_sec = True, False
        null_val = False

        # final_match = None

        form_sub = [[request.form.get('s1'), request.form.get('c1')], [request.form.get('s2'), request.form.get('c2')], [request.form.get('s3'), request.form.get('c3')],
                    [request.form.get('s4'), request.form.get('c4')], [request.form.get('s5'), request.form.get('c5')], [request.form.get('s6'), request.form.get('c6')],
                    [request.form.get('s7'), request.form.get('c7')], [request.form.get('s8'), request.form.get('c8')], [request.form.get('s9'), request.form.get('c9')]]

        for i in form_sub:
            if i[0] == "" and i[1] == "":
                null_val = True
                break
            elif i[0] != 'None' and i[1] != 'None':
                if len(i[0]) < 5:
                    correct_sub = False
                elif len(i[1]) < 6:
                    correct_sec = False
                else:
                    sub_list[i[0]] = i[1]
            elif i[0] == 'None' and i[1] != 'None':
                None_sub = True
            elif i[1] == 'None' and i[0] != 'None':
                None_sec = True
            
        if null_val:
            flash('กรุณาระบุอย่างน้อย 1 วิชา', category='error')
        elif correct_sub and correct_sec and None_sub == False and None_sec == False:
            if student['program_id'] == 'DSI':
                if module4 == 'None' and semester != '41':
                    ##### Collect credits from all subjects
                    credits = 0
                    wrong_sub, wrong_cd = [], []
                    for k,v in sub_list.items():
                        # subject = Subjects.query.filter_by(subject_id = k).first()

                        cursor.execute("SELECT * FROM subjects WHERE subject_id = %s", (k,))
                        subject = cursor.fetchone()

                        if subject is not None and v in section_set:
                            # credits += subject.credits
                            credits += subject['credits']
                        else:
                            if subject is None:
                                wrong_sub.append(k)
                            else:
                                wrong_cd.append(v)

                    if wrong_sub != []:
                        flash(f'วิชา {wrong_sub[0]} ไม่พบในฐานข้อมูลรายวิชา! โปรดกรอกรหัสวิชาใหม่อีกครั้ง', category='error')
                    elif wrong_cd != []:
                        flash(f'รหัสกลุ่มเรียน {wrong_cd[0]} ไม่พบในฐานข้อมูล! โปรดกรอกกลุ่มเรียนใหม่อีกครั้ง', category='error')
                    else:
                        ##### Convert to text : subject_id
                        text_sub = ""
                        text_sec = ""
                        for k,v in sub_list.items():
                            text_sub = text_sub + k + ","
                            text_sec = text_sec + v + ","

                        text_sub, text_sec = text_sub[:-1], text_sec[:-1]

                        # check_regis = Registrations.query.filter_by(academic_year = int(semester[0]), semester = int(semester[1])).first()

                        cursor.execute("SELECT * FROM registrations WHERE academic_year = %s and semester = %s", (int(semester[0]), int(semester[1])))
                        check_regis = cursor.fetchone()

                        if check_regis is None:
                            # last_item = Registrations.query.all()
                            cursor.execute("SELECT * FROM registrations")
                            last_item = cursor.fetchone()
                            # if last_item != []:
                            #     num = int(last_item[-1].registration_id) + 1
                            #     regis_id = '0'*(10-len(str(num))) + str(num)
                            #     curr = Registrations(registration_id = regis_id, student_id = student.student_id, subject_id = text_sub, all_credits = credits, academic_year = semester[0], semester = semester[1], section = text_sec, timestamp = datetime.datetime.now().date())
                            #     db.session.add(curr)
                            #     db.session.commit()
                            #     flash('บันทึกข้อมูลสำเร็จ! คุณสามารถเช็คข้อมูลการลงทะเบียนที่เพิ่มล่าสุดได้ที่เมนู "ข้อมูลการลงทะเบียน"', category='success')
                            if last_item is not None:
                                num = int(len(last_item)) + 1
                                regis_id = '0'*(10-len(str(num))) + str(num)
                                cursor.execute("INSERT INTO registrations(registration_id, student_id, subject_id, all_credits, academic_year, semester, section, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (regis_id, student['student_id'], text_sub, credits, semester[0], semester[1], text_sec, datetime.datetime.now().date()))
                                connection.commit()
                                flash('บันทึกข้อมูลสำเร็จ! คุณสามารถเช็คข้อมูลการลงทะเบียนที่เพิ่มล่าสุดได้ที่เมนู "ข้อมูลการลงทะเบียน"', category='success')
                            else:
                                # curr = Registrations(registration_id = '0000000001', student_id = student.student_id, subject_id = text_sub, all_credits = credits, academic_year = semester[0], semester = semester[1], section = text_sec, timestamp = datetime.datetime.now().date())
                                # db.session.add(curr)
                                # db.session.commit()

                                cursor.execute("INSERT INTO registrations(registration_id, student_id, subject_id, all_credits, academic_year, semester, section, timestamp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", ('0000000001', student['student_id'], text_sub, credits, semester[0], semester[1], text_sec, datetime.datetime.now().date()))
                                connection.commit()
                                flash('บันทึกข้อมูลสำเร็จ! คุณสามารถเช็คข้อมูลการลงทะเบียนที่เพิ่มล่าสุดได้ที่เมนู "ข้อมูลการลงทะเบียน"', category='success')
                        else:
                            # flash('ไม่สามารถเพิ่มรายวิชาในภาคการศึกษาซ้ำได้!', category='error')
                            # check_regis.registration_id = check_regis.registration_id
                            # check_regis.student_id = check_regis.student_id
                            # check_regis.subject_id = text_sub
                            # check_regis.all_credits = credits
                            # check_regis.academic_year = int(semester[0])
                            # check_regis.semester = int(semester[1])
                            # check_regis.section = text_sec
                            # check_regis.timestamp = datetime.datetime.now().date()

                            # db.session.add(check_regis)
                            # db.session.commit()

                            cursor.execute("UPDATE registrations SET registration_id = %s, student_id = %s, subject_id = %s, all_credits = %s, academic_year = %s, semester = %s, section = %s, timestamp = %s", (check_regis['registration_id'], check_regis['student_id'], text_sub, credits, semester[0], semester[1], text_sec, datetime.datetime.now().date()))
                            connection.commit()
                            flash('บันทึกข้อมูลสำเร็จ! คุณสามารถเช็คข้อมูลการลงทะเบียนที่เพิ่มล่าสุดได้ที่เมนู "ข้อมูลการลงทะเบียน"', category='success')
                        cursor.close()

                elif semester != '41' and module4 != 'None':
                        flash(f'ไม่สามารถเพิ่มรายวิชาได้ เนื่องจากภาคเรียนที่ {semester[1]}/{acad_year} ไม่มีการเลือกหมวดวิชา! กรุณาระบุช่องเลือกหมวดวิชาเป็น "ไม่มี"', category='error')
                else:
                    pass
                    
        
        elif correct_sub == False:
            flash('รหัสวิชาต้องมีความยาว 5 ตัวขึ้นไป', category='error')
        elif correct_sec == False:
            flash('รหัสกลุ่มเรียนต้องมีความยาว 6 ตัว', category='error')
        elif None_sub:
            flash('ไม่สามารถเพิ่มรายวิชาได้ เนื่องจากมีการระบุกลุ่มเรียน แต่ไม่มีการระบุรหัสวิชา!', category='error')
        elif None_sec:
            flash('ไม่สามารถเพิ่มรายวิชาได้ เนื่องจากมีการระบุรหัสวิชา แต่ไม่มีการระบุกลุ่มเรียนของวิชานั้น!', category='error')
        
    return render_template('student_add_subject.html', start_year = student['start_year'])

#----------------------------------------------------------#

@views.route('/user/home', methods=['GET', 'POST'], endpoint='user_em')
@login_is_required
def user_em_home():
    
    image = session["picture"]
    # user = User.query.filter_by(email = session["email"]).first()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM user WHERE email = %s", (session["email"],))
    user = cursor.fetchone()
    cursor.close()

    # if user.gender == 'M':
    #     gender = 'ชาย'
    # elif user.gender == 'F':
    #     gender = 'หญิง'
    # else:
    #     gender = 'อื่นๆ'

    if user['gender'] == 'M':
        gender = 'ชาย'
    elif user['gender'] == 'F':
        gender = 'หญิง'
    else:
        gender = 'อื่นๆ'
    
    return render_template("user_em_home.html", result = user, gender = gender, image = image)

@views.route('/user/edit', methods=['GET', 'POST'], endpoint='user_em_edit')
@login_is_required
def user_em_edit_info():
    # user = User.query.filter_by(email = session['email']).first()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        NameTH = request.form.get('NameTH')
        NameEN = request.form.get('NameEN')
        gender = request.form.get('genderchoose')

        if len(NameTH) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        elif len(NameEN) <= 5:
            flash('ชื่อ-นามสกุล ต้องมีความยาวมากกว่า 5 ตัวอักษร', category='error')
        else:
            ### Update user to database
            # user.user_id = user.user_id
            # user.program_id = user.program_id
            # user.nameTH = NameTH
            # user.nameEN = NameEN
            # user.role = user.role
            # user.gender = gender
            # user.email = session['email']

            # db.session.add(user)
            # db.session.commit()

            cursor.execute("UPDATE user SET nameEN= %s, nameTH= %s, gender= %s WHERE email = %s", (NameEN, NameTH, gender, session["email"]))
            connection.commit()
            cursor.close()
            flash('แก้ไขข้อมูลสำเร็จ!.', category='success')
            return redirect(url_for('views.user_em'))

    return render_template('user_em_home_edit.html')

# @views.route('/user/home', methods=['GET', 'POST'], endpoint='user_de')
# @login_is_required
# def user_de_home():
    
#     image = session["picture"]
#     user = User.query.filter_by(email = session["email"]).first()
#     if user.gender == 'M':
#         gender = 'ชาย'
#     elif user.gender == 'F':
#         gender = 'หญิง'
#     else:
#         gender = 'อื่นๆ'
    
#     return render_template("user_de_home.html", result = user, gender = gender, image = image)

@views.route('/user/check', methods=['GET', 'POST'], endpoint='user_em_check')
def user_em_check_student_page():
    Not_found = False
    # user = User.query.filter_by(email = session['email']).first()
    cursor = connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM user WHERE email = %s", (session["email"],))
    user = cursor.fetchone()
    # student = Student.query.filter_by(program_id = user.program_id).all()
    cursor.execute("SELECT * FROM student WHERE program_id = %s", (user['program_id'],))
    student = cursor.fetchall()
    minus_year = datetime.datetime.now().year + 543 if datetime.datetime.now().day >= 1 and datetime.datetime.now().month >= 8 else datetime.datetime.now().year + 542
    # if request.method == 'POST':
    #     name = request.form.get('name')
    #     year_study = request.form.get('year-study')
    #     gender = request.form.get('gender')
        
    #     year = minus_year - int(year_study)
    #     student = Student.query.filter_by(program_id = user.program_id, student_nameTH = name, start_year = year, gender = gender).first()
    #     if student is None:
    #         Not_found = True

    #     if Not_found:
    #         flash('ไม่พบข้อมูลที่ต้องการ', category='error')
    # else:
    #     student = Student.query.filter_by(program_id = user.program_id).all()
    return render_template('user_em_check.html', student = student, minus_year = minus_year)

@views.route('/user/overall', methods=['GET', 'POST'], endpoint='user_em_all')
def user_em_overall_page():
    return render_template('user_em_overall.html')

@views.route('/de-overall', methods=['GET', 'POST'])
def de_overall_page():
    return render_template('de_overall.html')
