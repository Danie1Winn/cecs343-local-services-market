from flask import Blueprint, request, redirect, render_template, url_for, current_app
from werkzeug.security import generate_password_hash
from app.models.worker import Worker
from app.models.employer import Employer
from app import db
import os

#Gmail: locallink187@gmail.com
#App Password: ldje oxvf bfwy fbzu
signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup', methods=['POST', 'GET'])
def signup_page():
    if request.method == 'POST' and 'submit-worker-signup' in request.form:
        name = request.form['name']
        phone_number = request.form['phone']
        password = request.form['password']
        profile_picture = request.files['profile-picture']

        profile_picture_path = None
        if profile_picture:
            upload_folder = current_app.config.get('UPLOAD_FOLDER', os.path.join(current_app.root_path, 'static/uploads/profile_pics'))
            os.makedirs(upload_folder, exist_ok=True)

            profile_picture_path = os.path.join(upload_folder, profile_picture.filename)
            profile_picture.save(profile_picture_path)
            profile_picture_path = os.path.relpath(profile_picture_path, current_app.root_path)
        
        hashed_password = generate_password_hash(password)

        new_worker = Worker(name=name, phone_number=phone_number, password=hashed_password, profile_picture=profile_picture_path)

        try:
            db.session.add(new_worker)
            db.session.commit()
            return redirect(url_for('login.login_page'))
        except Exception as e:
            return redirect(url_for('signup.signup_page'))
        
    elif request.method =='POST' and 'submit-employer-signup' in request.form:
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        
        hashed_password = generate_password_hash(password)

        new_employer = Employer(name=name, phone_number=phone, password=hashed_password)

        try:
            db.session.add(new_employer)
            db.session.commit()
            return redirect(url_for('login.login_page'))
        except Exception as e:
            return redirect(url_for('signup.signup_page'))
    
    else:
        return render_template('signup.html')
    

