from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app import db
from app.models.job_posting import JobPosting

employer_bp = Blueprint('employer', __name__)

@employer_bp.route('/employer')
def employer_page():
    employer_id = session.get('employer_id')
    if not employer_id:
        flash("You must be logged in as an employer to view this page.", "danger")
        return redirect(url_for('login.login_page'))
    return render_template('employer_dashboard.html')

# Route to create a job request
@employer_bp.route('/create_request', methods=['GET', 'POST'])
def create_request():
    employer_id = session.get('employer_id')
    if not employer_id:
        flash("You must be logged in as an employer to create a job request.", "danger")
        return redirect(url_for('login.login_page'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        rate = float(request.form['rate'])

        new_request = JobPosting(
            title=title,
            description=description,
            rate=rate,
            employer_id=employer_id,
        )
        db.session.add(new_request)
        db.session.commit()

        flash("Job request created successfully!", "success")
        return redirect(url_for('employer.employer_page'))

    return render_template('create_request.html')
