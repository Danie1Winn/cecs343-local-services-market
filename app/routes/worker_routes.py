from flask import Blueprint, render_template

worker_bp = Blueprint('worker', __name__)

@worker_bp.route('/worker')
def worker_page():
    return render_template('worker_profile.html')