# from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, session, abort
# from flask_login import login_required, current_user
# from google_auth_oauthlib import flow
# from authlib.integrations.flask_client import OAuth
# from .auth import login_is_required

# from website.auth import GOOGLE_CLIENT_ID
# from .models import Note
# from . import db
# import json, os

# views = Blueprint('views', __name__)
# oauth = OAuth(views)

# os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = '1'



# # @views.route('/google/')
# # def google():
   
# #     # Google Oauth Config
# #     # Get client_id and client_secret from environment variables
# #     # For developement purpose you can directly put it
# #     # here inside double quotes
# #     GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
# #     GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
     
# #     CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
# #     oauth.register(
# #         name='google',
# #         client_id=GOOGLE_CLIENT_ID,
# #         client_secret=GOOGLE_CLIENT_SECRET,
# #         server_metadata_url=CONF_URL,
# #         client_kwargs={
# #             'scope': 'openid email profile'
# #         }
# #     )
     
# #     # Redirect to google_auth function
# #     redirect_uri = url_for('google_auth', _external=True)
# #     return oauth.google.authorize_redirect(redirect_uri)

# # @views.route('/google/auth/')
# # def google_auth():
# #     token = oauth.google.authorize_access_token()
# #     user = oauth.google.parse_id_token(token)
# #     print(" Google User ", user)
# #     return redirect('/home')

# @views.route('/')
# def home_page():
#     return render_template('home_all.html')

# @views.route('/home', methods=['GET', 'POST'])
# # @login_required
# @login_is_required
# def home():
#     # if request.method == 'POST':
#     #     note = request.form.get('note')

#     #     if len(note) < 1:
#     #         flash('Note is too short!', category='error')
#     #     else:
#     #         new_note = Note(data=note, user_id=current_user.id)
#     #         db.session.add(new_note)
#     #         db.session.commit()
#     #         flash('Note added!', category='success')
    

    
#     return render_template("home.html")

# @views.route('/curriculum', methods=['GET', 'POST'])
# @login_is_required
# def curriculum_page():
#     return render_template('student_curriculum.html')

# @views.route('/e-check-s', methods=['GET', 'POST'])
# def em_check_curriculum_page():
#     return render_template('em_check_s.html', user=current_user)

# @views.route('/e-overall', methods=['GET', 'POST'])
# def em_overall_page():
#     return render_template('em_overall.html', user=current_user)

# @views.route('/de-overall', methods=['GET', 'POST'])
# def de_overall_page():
#     return render_template('de_overall.html', user=current_user)

# @views.route('/delete-note', methods=['POST'])
# def delete_note():
#     note = json.loads(request.data)
#     noteId = note['noteId']
#     note = Note.query.get(noteId)
#     if note:
#         if note.user_id == current_user.id:
#             db.session.delete(note)
#             db.session.commit()
    
#     return jsonify({})