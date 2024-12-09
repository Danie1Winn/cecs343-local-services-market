from flask import Blueprint, request, redirect, render_template, url_for, current_app, session
from werkzeug.security import generate_password_hash
from app.models.worker import Worker
from app.models.employer import Employer
from app import db
import os
import random
import smtplib
from email.mime.text import MIMEText

signup_bp = Blueprint('signup', __name__)

EMAIL_USER = "locallink187@gmail.com"
EMAIL_PASSWORD = "ldjeoxvfbfwyfbzu"

def send_sms_via_email(to_number, carrier, message):
    carriers = {
        'att': 'txt.att.net',
        'verizon': 'vtext.com',
        'tmobile': 'tmomail.net',
    }

    if carrier not in carriers:
        raise ValueError("Carrier not supported")

    to_email = f"{to_number}@{carriers[carrier]}"
    msg = MIMEText(message)
    msg['From'] = EMAIL_USER
    msg['To'] = to_email
    msg['Subject'] = 'Verification Code'

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASSWORD)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"Failed to send SMS: {e}")
        return False

@signup_bp.route('/signup', methods=['POST', 'GET'])
def signup_page():
    if request.method == 'POST':
        session.clear()
        name = request.form['name']
        phone_number = request.form['phone']
        password = request.form['password']
        carrier = "att"
        profile_picture = request.files.get('profile-picture')

        profile_picture_path = None
        if profile_picture:
            upload_folder = current_app.config.get(
                'UPLOAD_FOLDER', os.path.join(current_app.root_path, 'static/uploads/profile_pics')
            )
            os.makedirs(upload_folder, exist_ok=True)
            profile_picture_path = os.path.join(upload_folder, profile_picture.filename)
            profile_picture.save(profile_picture_path)
            profile_picture_path = os.path.relpath(profile_picture_path, current_app.root_path)

        verification_code = f"{random.randint(100000, 999999)}"
        print(verification_code)
        session['verification_code'] = verification_code
        session['name'] = name
        session['phone_number'] = phone_number
        session['password'] = password
        session['profile_picture'] = profile_picture.filename if profile_picture else None
        session['carrier'] = carrier
        session['role'] = 'worker' if 'submit-worker-signup' in request.form else 'employer'

        message = f"Your verification code is: {verification_code}"
        if send_sms_via_email(phone_number, carrier, message):
            return redirect(url_for('signup.verify_page'))
        else:
            return "Failed to send verification code. Please try again."
    
    return render_template('signup.html')

@signup_bp.route('/verify', methods=['POST', 'GET'])
def verify_page():
    if request.method == 'POST':
        user_code = request.form['verification_code']
        if user_code == session.get('verification_code'):
            hashed_password = generate_password_hash(session['password'])
            if session['role'] == 'worker':
                new_user = Worker(
                    name=session['name'],
                    phone_number=session['phone_number'],
                    password=hashed_password,
                    profile_picture=session.get('profile_picture')
                )
            else:
                new_user = Employer(
                    name=session['name'],
                    phone_number=session['phone_number'],
                    password=hashed_password
                )

            try:
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login.login_page'))
            except Exception as e:
                return f"Error: {e}"
    return render_template('verify.html')