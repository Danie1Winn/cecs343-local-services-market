from flask import Blueprint, render_template

signup_bp = Blueprint('signup', __name__)

@signup_bp.route('/signup')
def signup_page():
    return render_template('signup.html') 