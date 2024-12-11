from flask import Blueprint, flash, url_for, redirect, render_template, request, session
from app import db
from app.models.worker import Worker
from app.models.skill import Skill
from app.models.job_posting import JobPosting
from app.models.contract import Contract
from app.forms import WorkerProfileForm

worker_bp = Blueprint('worker', __name__)

# Worker View Profile (Read-Only)
@worker_bp.route('/view/<int:worker_id>', methods=['GET'])
def worker_view(worker_id):
    worker = Worker.query.get_or_404(worker_id)
    skills = Skill.query.filter_by(worker_id=worker_id).all()
    return render_template('worker_view.html', worker=worker, skills=skills)

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

# Route to accept a job
@worker_bp.route('/accept_job/<int:job_id>', methods=['POST'])
def accept_job(job_id):
    worker_id = session.get('worker_id')
    if not worker_id:
        flash("You must be logged in as a worker to accept a job.", "danger")
        return redirect(url_for('login.login_page'))

    job_posting = JobPosting.query.get_or_404(job_id)

    if job_posting.status != 'open':
        flash("This job is no longer available.", "danger")
        return redirect(url_for('worker.worker_profile', worker_id=worker_id))

    job_posting.status = 'accepted'
    new_contract = Contract(
        worker_id=worker_id,
        employer_id=job_posting.employer_id,
        job_posting_id=job_id,
        status='accepted',
    )

    db.session.add(new_contract)
    db.session.commit()

    flash("Job accepted successfully!", "success")
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
