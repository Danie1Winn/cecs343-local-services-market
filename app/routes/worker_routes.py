from flask import Blueprint, flash, url_for, redirect, render_template, request, session
from app import db
from app.models.worker import Worker
from app.models.skill import Skill
from app.models.job_posting import JobPosting
from app.models.contract import Contract
from app.forms import WorkerSkillForm

worker_bp = Blueprint('worker', __name__)

# Worker View Profile (Read-Only)
@worker_bp.route('/view/<int:worker_id>', methods=['GET'])
def worker_view(worker_id):
    worker = Worker.query.get_or_404(worker_id)
    worker_skills = Skill.query.filter_by(worker_id=worker_id).all()
    return render_template('worker_view.html', worker=worker, skills=worker_skills)

# Route to contact a worker
@worker_bp.route('/contact/<int:worker_id>', methods=['POST'])
def contact(worker_id):
    worker = Worker.query.get_or_404(worker_id)
    message = request.form.get('message')

    if not message:
        flash("Message cannot be empty.", "danger")
        return redirect(url_for('worker.worker_view', worker_id=worker_id))

    # Placeholder for actual message handling (e.g., database storage or email sending)
    flash(f"Your message has been sent to {worker.name}.", "success")
    return redirect(url_for('worker.worker_view', worker_id=worker_id))

# Worker Profile for Editing
@worker_bp.route('/profile/<int:worker_id>', methods=['GET', 'POST'])
def worker_profile(worker_id):
    worker = Worker.query.get_or_404(worker_id)
    form = WorkerSkillForm()

    if form.validate_on_submit():
        new_skill = Skill(
            skill_name=form.skill_name.data,
            experience_level=form.experience_level.data,
            worker_id=worker_id
        )
        db.session.add(new_skill)
        db.session.commit()

        flash('Skill successfully added!', 'success')
        return redirect(url_for('worker.worker_profile', worker_id=worker_id))

    worker_skills = Skill.query.filter_by(worker_id=worker_id).all()
    return render_template('worker_profile.html', worker=worker, form=form, skills=worker_skills)

# Route to create a post
@worker_bp.route('/create_post', methods=['GET', 'POST'])
def create_post():
    worker_id = session.get('worker_id')
    if not worker_id:
        flash("You must be logged in as a worker to create a post.", "danger")
        return redirect(url_for('login.login_page'))

    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        rate = float(request.form['rate'])

        new_post = JobPosting(
            title=title,
            description=description,
            rate=rate,
            worker_id=worker_id,
        )
        db.session.add(new_post)
        db.session.commit()

        flash("Job post created successfully!", "success")
        return redirect(url_for('worker.worker_page'))

    return render_template('create_post.html')

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
        return redirect(url_for('worker.worker_page'))

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
    return redirect(url_for('worker.worker_page'))
