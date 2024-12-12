from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from app import db
from app.models.job_posting import JobPosting
from app.models.contract import Contract
from datetime import datetime, timedelta

employer_bp = Blueprint('employer', __name__)

@employer_bp.route('/profile', methods=['GET'])
def employer_profile():
    employer_id = session.get('employer_id')
    if not employer_id:
        flash("You must be logged in as an employer to view this page.", "danger")
        return redirect(url_for('login.login_page'))

    # Fetch pending and active jobs
    pending_requests = Contract.query.filter_by(employer_id=employer_id, status='pending').all()
    active_jobs = Contract.query.filter_by(employer_id=employer_id, status='accepted').all()

    return render_template('employer_profile.html', pending_requests=pending_requests, active_jobs=active_jobs)

# Route to create a job request
@employer_bp.route('/create_request', methods=['POST'])
def create_request():
    employer_id = session.get('employer_id')
    if not employer_id:
        flash("You must be logged in as an employer to create a job request.", "danger")
        return redirect(url_for('login.login_page'))

    # Get form data
    worker_id = request.form.get('worker_id')
    description = request.form.get('description')
    job_date = request.form.get('job_date')

    if not worker_id or not description or not job_date:
        flash("All fields are required.", "danger")
        return redirect(url_for('worker.worker_view', worker_id=worker_id))

    # Parse job_date
    try:
        job_date = datetime.strptime(job_date, '%Y-%m-%dT%H:%M')
    except ValueError:
        flash("Invalid date format. Use YYYY-MM-DDTHH:MM.", "danger")
        return redirect(url_for('worker.worker_view', worker_id=worker_id))

    # Create the contract
    new_contract = Contract(
        worker_id=worker_id,
        employer_id=employer_id,
        description=description,
        job_date=job_date,
        status='pending',
    )
    db.session.add(new_contract)
    db.session.commit()

    flash("Job request sent successfully.", "success")
    return redirect(url_for('employer.employer_profile'))

# Route to cancel a pending job request
@employer_bp.route('/cancel_request/<int:job_id>', methods=['POST'])
def cancel_request(job_id):
    contract = Contract.query.get_or_404(job_id)
    employer_id = session.get('employer_id')

    if contract.employer_id != employer_id:
        flash("You are not authorized to cancel this request.", "danger")
        return redirect(url_for('employer.employer_profile'))

    db.session.delete(contract)
    db.session.commit()
    flash("Job request canceled successfully.", "success")
    return redirect(url_for('employer.employer_profile'))

# Route to request cancellation of an active job
@employer_bp.route('/request_cancellation/<int:job_id>', methods=['POST'])
def request_cancellation(job_id):
    contract = Contract.query.get_or_404(job_id)
    employer_id = session.get('employer_id')

    if contract.employer_id != employer_id or contract.status != 'accepted':
        flash("You are not authorized to request cancellation for this job.", "danger")
        return redirect(url_for('employer.employer_profile'))

    # Update contract status to 'cancel_requested'
    contract.status = 'cancel_requested'
    db.session.commit()
    flash("Cancellation request sent to worker.", "success")
    return redirect(url_for('employer.employer_profile'))

@employer_bp.route('/complete_job/<int:job_id>', methods=['POST'])
def complete_job(job_id):
    # Fetch the contract by ID
    contract = Contract.query.get_or_404(job_id)

    # Ensure the employer owns the job
    employer_id = session.get('employer_id')
    if contract.employer_id != employer_id:
        flash("You are not authorized to complete this job.", "danger")
        return redirect(url_for('employer.employer_profile'))

    # Mark the job as completed
    if contract.status == 'accepted':
        contract.status = 'completed'
        db.session.commit()
        flash("Job marked as completed successfully.", "success")
    else:
        flash("Job cannot be completed because it is not in an active state.", "danger")

    return redirect(url_for('employer.employer_profile'))
