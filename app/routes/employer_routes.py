from flask import Blueprint, render_template

employer_bp = Blueprint('employer', __name__)

@employer_bp.route('/employer')
def employer_page():
    return render_template('employer_dashboard.html')