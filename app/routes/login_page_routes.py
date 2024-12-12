import logging
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from app import db
from app.models.worker import Worker
from app.models.employer import Employer

# Configure logging
logging.basicConfig(level=logging.INFO)

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST', 'GET'])
def login_page():
    if request.method == 'POST':
        phone_number = request.form['phone']
        password = request.form['password']
        
        # Handle worker login
        if 'submit-worker-login' in request.form:
            worker = Worker.query.filter_by(phone_number=phone_number).first()
            logging.info(f"Worker login attempt: phone_number={phone_number}, exists={bool(worker)}")
            
            if worker and check_password_hash(worker.password, password):
                if worker.user_role == 'developer':
                    session['developer_id'] = worker.id
                    session['role'] = 'developer_worker'
                    session['logged_in'] = True
                    flash('Developer worker login successful.', 'success')
                    return redirect(url_for('home.home'))
                else:
                    session['worker_id'] = worker.id
                    session['logged_in'] = True
                    session['role'] = 'worker'
                    flash('Worker login successful.', 'success')
                    return redirect(url_for('home.home'))
            else:
                flash('Invalid worker credentials. Please try again.', 'danger')
                logging.info("Worker login failed.")
                return redirect(url_for('login.login_page'))

        # Handle employer login
        if 'submit-employer-login' in request.form:
            employer = Employer.query.filter_by(phone_number=phone_number).first()
            logging.info(f"Employer login attempt: phone_number={phone_number}, exists={bool(employer)}")
            
            if employer and check_password_hash(employer.password, password):
                if employer.user_role == 'developer':
                    session['developer_id'] = employer.id
                    session['role'] = 'developer_employer'
                    session['logged_in'] = True
                    flash('Developer employer login successful.', 'success')
                    return redirect(url_for('home.home'))
                else:
                    session['employer_id'] = employer.id
                    session['logged_in'] = True
                    session['role'] = 'employer'
                    flash('Employer login successful.', 'success')
                    return redirect(url_for('home.home'))
            else:
                flash('Invalid employer credentials. Please try again.', 'danger')
                logging.info("Employer login failed.")
                return redirect(url_for('login.login_page'))

    logging.info("Rendering login page.")
    return render_template('login.html')

@login_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    logging.info("Session cleared. Logged out.")
    return redirect(url_for('home.home'))
