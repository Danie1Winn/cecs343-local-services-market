from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from app import db
from app.models.worker import Worker
from app.models.employer import Employer

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST' and 'submit-worker-login' in request.form:
        phone_number = request.form['phone']
        password = request.form['password']
        worker = Worker.query.filter_by(phone_number=phone_number).first()

        if worker and check_password_hash(worker.password, password):
            session['worker_id'] = worker.id
            session['logged_in'] = True
            return redirect(url_for('home.home'))
        else:
            return redirect(url_for('login.login_page'))
    
    if request.method == 'POST' and 'submit-employer-login' in request.form:
        phone_number = request.form['phone']
        password = request.form['password']
        employer = Employer.query.filter_by(phone_number=phone_number).first()

        if employer and check_password_hash(employer.password, password):
            session['employer_id'] = employer.id
            session['logged_in'] = True
            return redirect(url_for('home.home'))
        else:
            return redirect(url_for('login.login_page'))
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.clear()  # Clears all session data
    return redirect(url_for('home.home'))  # Redirect back to the homepage