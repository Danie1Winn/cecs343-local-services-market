from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import check_password_hash
from app import db
from app.models.worker import Worker

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST', 'GET'])
def login_page():
    print("Working1")
    print(request.method)
    print(request.form)
    if request.method == 'POST' and 'submit-worker-login' in request.form:
        phone_number = request.form['phone']
        password = request.form['password']
        print("Working")
        worker = Worker.query.filter_by(phone_number=phone_number).first()

        if worker and check_password_hash(worker.password, password):
            session['worker_id'] = worker.id
            print("WOrked")
            return redirect(url_for('home.home'))
        else:
            return redirect(url_for('login.login_page'))
    
    return render_template('login.html')