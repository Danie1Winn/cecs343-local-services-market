from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app import db
from app.models.job_posting import JobPosting
from app.models.contract import Contract

employer_bp = Blueprint('employer', __name__)

@employer_bp.route('/employer')
def employer_page():
    employer_id = session.get('employer_id')
    if not employer_id:
        flash("You must be logged in as an employer to view this page.", "danger")
        return redirect(url_for('login.login_page'))

    # Fetch pending and active jobs
    pending_jobs = Contract.query.filter_by(employer_id=employer_id, status='pending').all()
    active_jobs = Contract.query.filter_by(employer_id=employer_id, status='accepted').all()

    return render_template('employer_dashboard.html', pending_jobs=pending_jobs, active_jobs=active_jobs)

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

# Route to cancel a pending job request
@employer_bp.route('/cancel_request/<int:job_id>', methods=['POST'])
def cancel_request(job_id):
    contract = Contract.query.get_or_404(job_id)
    employer_id = session.get('employer_id')

    if contract.employer_id != employer_id:
        flash("You are not authorized to cancel this request.", "danger")
        return redirect(url_for('employer.employer_page'))

    db.session.delete(contract)
    db.session.commit()
    flash("Job request canceled successfully.", "success")
    return redirect(url_for('employer.employer_page'))

# Route to request cancellation of an active job
@employer_bp.route('/request_cancellation/<int:job_id>', methods=['POST'])
def request_cancellation(job_id):
    contract = Contract.query.get_or_404(job_id)
    employer_id = session.get('employer_id')

    if contract.employer_id != employer_id or contract.status != 'accepted':
        flash("You are not authorized to request cancellation for this job.", "danger")
        return redirect(url_for('employer.employer_page'))

    # Update contract status to 'cancel_requested'
    contract.status = 'cancel_requested'
    db.session.commit()
    flash("Cancellation request sent to worker.", "success")
    return redirect(url_for('employer.employer_page'))
