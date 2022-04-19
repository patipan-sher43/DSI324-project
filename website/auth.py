# from multiprocessing import AuthenticationError
# from operator import methodcaller
# from flask import Blueprint, render_template, request, flash, redirect, url_for, session, abort
# from google_auth_oauthlib.flow import Flow
# import google.auth.transport.requests
# from pip._vendor import cachecontrol
# from google.oauth2 import id_token
# # from requests import session
# from .models import User
# from werkzeug.security import generate_password_hash, check_password_hash
# from . import db
# from flask_login import login_user, login_required, logout_user, current_user
# import os
# import pathlib

# auth = Blueprint('auth', __name__)
# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'

# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         user = User.query.filter_by(email=email).first()
#         if user:
#             if check_password_hash(user.password, password):
#                 flash('Logged in successfully!', category='success')
#                 login_user(user, remember=True)
#                 return redirect(url_for('views.home'))
#             else:
#                 flash('Incorrect password, try again.', category='error')
#         else:
#             flash('Email does not exist.', category='error')

#     return render_template("login.html", user=current_user)

# ###############################################################################

# @auth.route('/sign-up', methods=['GET', 'POST'])
# def sign_up():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         firstName = request.form.get('firstName')
#         lastName = request.form.get('lastName')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')

#         user = User.query.filter_by(email=email).first()
#         if user:
#             flash('Email already exists.', category='error')
#         elif len(email) < 4:
#             flash('Email must be greater than 3 characters.', category='error')
#         elif len(firstName) < 2:
#             flash('First Name must be greater than 1 character.', category='error')
#         elif len(lastName) < 2:
#             flash('Last Name must be greater than 1 character.', category='error')
#         elif password1 != password2:
#             flash('Password don\'t match.', category='error')
#         elif len(password1) < 7:
#             flash('Password must be at least 7 characters.', category='error')
#         else:
#             # add user to database
#             new_user = User(email=email, first_name=firstName, last_name=lastName, password=generate_password_hash(password1, method='sha256'))
#             db.session.add(new_user)
#             db.session.commit()
#             login_user(user, remember=True)
#             flash('Account created!.', category='success')
#             return redirect(url_for('views.home_page'))

#     return render_template("sign_up.html", user=current_user)