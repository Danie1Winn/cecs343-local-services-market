from flask import Blueprint, request, redirect, render_template, flash, url_for
from werkzeug.security import generate_password_hash
from app.models.worker import Worker
from app.models.employer import Employer
from app import db

signup = Blueprint('signup', __name__)

@signup.route('/signup/worker', methods=['POST'])
def signup_worker():
    name = request.form['name']
    phone = request.form['phone']
    password = request.form['password']
    profile_picture = request.files['profile-picture']

    # Save profile picture if uploaded
    profile_picture_path = None
    if profile_picture:
        profile_picture_path = f"static/uploads/{profile_picture.filename}"
        profile_picture.save(profile_picture_path)

    hashed_password = generate_password_hash(password)

    new_worker = Worker(name=name, phone=phone, password=hashed_password, profile_picture=profile_picture_path)

    try:
        db.session.add(new_worker)
        db.session.commit()
        flash("Worker signed up successfully!", "success")
        return redirect(url_for('home.home'))
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('signup.signup_page'))

@signup.route('/signup/employer', methods=['POST'])
def signup_employer():
    name = request.form['name']
    phone = request.form['phone']
    password = request.form['password']
    
    hashed_password = generate_password_hash(password)

    new_employer = Employer(name=name, phone=phone, password=hashed_password)

    try:
        db.session.add(new_employer)
        db.session.commit()
        flash("Employer signed up successfully!", "success")
        return redirect(url_for('home.home'))
    except Exception as e:
        flash(f"Error: {str(e)}", "danger")
        return redirect(url_for('signup.signup_page'))