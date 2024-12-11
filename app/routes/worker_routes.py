from flask import Blueprint, flash, url_for, redirect, render_template, request, session
from app import db
from app.models.worker import Worker
from app.models.skill import Skill
from app.models.job_posting import JobPosting
from app.models.contract import Contract
from app.forms import WorkerProfileForm
from datetime import datetime, timedelta

worker_bp = Blueprint('worker', __name__)

# Worker View Profile (Read-Only)
@worker_bp.route('/view/<int:worker_id>', methods=['GET'])
def worker_view(worker_id):
    worker = Worker.query.get_or_404(worker_id)
    skills = Skill.query.filter_by(worker_id=worker_id).all()

    # Check for employer login
    employer_id = session.get('employer_id')
    if employer_id:
        pending_jobs = Contract.query.filter_by(worker_id=worker_id, status='pending').all()
        cancel_requests = Contract.query.filter_by(worker_id=worker_id, status='cancel_requested').all()
        return render_template(
            'worker_view.html',
            worker=worker,
            skills=skills,
            pending_jobs=pending_jobs,
            cancel_requests=cancel_requests,
        )

    return render_template('worker_view.html', worker=worker, skills=skills)

@worker_bp.route('/worker_accept_job/<int:job_id>', methods=['POST'])
def worker_accept_job(job_id):
    contract = Contract.query.get_or_404(job_id)
    worker_id = session.get('worker_id')

    if contract.worker_id != worker_id:
        flash("You are not authorized to accept this job.", "danger")
        return redirect(url_for('worker.worker_view', worker_id=worker_id))

    contract.status = 'accepted'
    db.session.commit()
    flash("Job accepted successfully!", "success")
    return redirect(url_for('worker.worker_view', worker_id=worker_id))

@worker_bp.route('/reject_job/<int:job_id>', methods=['POST'])
def reject_job(job_id):
    contract = Contract.query.get_or_404(job_id)
    worker_id = session.get('worker_id')

    if contract.worker_id != worker_id:
        flash("You are not authorized to reject this job.", "danger")
        return redirect(url_for('worker.worker_view', worker_id=worker_id))

    db.session.delete(contract)
    db.session.commit()
    flash("Job rejected successfully!", "success")
    return redirect(url_for('worker.worker_view', worker_id=worker_id))

@worker_bp.route('/approve_cancellation/<int:job_id>', methods=['POST'])
def approve_cancellation(job_id):
    contract = Contract.query.get_or_404(job_id)
    worker_id = session.get('worker_id')

    if contract.worker_id != worker_id:
        flash("You are not authorized to approve this cancellation.", "danger")
        return redirect(url_for('worker.worker_view', worker_id=worker_id))

    contract.status = 'canceled'
    db.session.commit()
    flash("Cancellation approved successfully.", "success")
    return redirect(url_for('worker.worker_view', worker_id=worker_id))

# Worker Profile for Editing
@worker_bp.route('/profile/<int:worker_id>', methods=['GET', 'POST'])
def worker_profile(worker_id):
    worker = Worker.query.get_or_404(worker_id)

    if session.get('worker_id') != worker_id:
        flash("You are not authorized to edit this profile.", "danger")
        return redirect(url_for('home.home'))

    form = WorkerProfileForm(obj=worker)

    if form.validate_on_submit():
        worker.about_me = form.about_me.data
        worker.zip_code = form.zip_code.data
        worker.travel_distance = form.travel_distance.data
        db.session.commit()

        # Add a new skill if skill fields are filled
        if form.skill_name.data and form.experience_level.data:
            new_skill = Skill(
                skill_name=form.skill_name.data,
                experience_level=form.experience_level.data,
                description=form.description.data or "No description provided",
                rate_type=form.rate_type.data,
                rate_value=form.rate_value.data if form.rate_type.data != 'negotiable' else None,
                worker_id=worker_id
            )
            db.session.add(new_skill)
            db.session.commit()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('worker.worker_profile', worker_id=worker_id))

    worker_skills = Skill.query.filter_by(worker_id=worker_id).all()
    job_requests = JobPosting.query.filter_by(worker_id=worker_id, status='open').all()

    return render_template('worker_profile.html', worker=worker, form=form, skills=worker_skills, job_requests=job_requests)

@worker_bp.route('/update_skill/<int:skill_id>', methods=['POST'])
def update_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    worker_id = session.get('worker_id')

    if skill.worker_id != worker_id:
        flash("You are not authorized to edit this skill.", "danger")
        return redirect(url_for('worker.worker_profile', worker_id=worker_id))

    skill.skill_name = request.form.get('skill_name')
    skill.experience_level = request.form.get('experience_level')
    skill.description = request.form.get('description')
    skill.rate_type = request.form.get('rate_type')
    skill.rate_value = None if skill.rate_type == 'negotiable' else request.form.get('rate_value')
    db.session.commit()

    flash("Skill updated successfully!", "success")
    return redirect(url_for('worker.worker_profile', worker_id=worker_id))

# Route to delete a skill
@worker_bp.route('/delete_skill/<int:skill_id>', methods=['POST'])
def delete_skill(skill_id):
    skill = Skill.query.get_or_404(skill_id)
    worker_id = session.get('worker_id')

    if skill.worker_id != worker_id:
        flash("You are not authorized to delete this skill.", "danger")
        return redirect(url_for('worker.worker_profile', worker_id=worker_id))

    db.session.delete(skill)
    db.session.commit()

    flash("Skill deleted successfully!", "success")
    return redirect(url_for('worker.worker_profile', worker_id=worker_id))

# Route to contact a worker
@worker_bp.route('/contact/<int:worker_id>', methods=['POST'])
def contact(worker_id):
    worker = Worker.query.get_or_404(worker_id)
    message = request.form.get('message')

    if not message:
        flash("Message cannot be empty.", "danger")
        return redirect(url_for('worker.worker_view', worker_id=worker_id))

    flash(f"Your message has been sent to {worker.name}.", "success")
    return redirect(url_for('worker.worker_view', worker_id=worker_id))

# Route to go online
@worker_bp.route('/go_online/<int:worker_id>', methods=['POST'])
def go_online(worker_id):
    worker = Worker.query.get_or_404(worker_id)

    if session.get('worker_id') != worker_id:
        flash("You are not authorized to change this status.", "danger")
        return redirect(url_for('home.home'))

    auto_offline_minutes = request.form.get('auto_offline_time')
    if auto_offline_minutes:
        worker.auto_offline_time = datetime.utcnow() + timedelta(minutes=int(auto_offline_minutes))
    else:
        worker.auto_offline_time = None  # Manual offline

    worker.is_online = True
    db.session.commit()

    flash("You are now online!", "success")
    return redirect(url_for('worker.worker_profile', worker_id=worker_id))

# Route to go offline
@worker_bp.route('/go_offline/<int:worker_id>', methods=['POST'])
def go_offline(worker_id):
    worker = Worker.query.get_or_404(worker_id)

    if session.get('worker_id') != worker_id:
        flash("You are not authorized to change this status.", "danger")
        return redirect(url_for('home.home'))

    worker.is_online = False
    worker.auto_offline_time = None  # Reset auto-offline time
    db.session.commit()

    flash("You are now offline.", "success")
    return redirect(url_for('worker.worker_profile', worker_id=worker_id))