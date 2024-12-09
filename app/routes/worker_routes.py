from flask import Blueprint, flash, url_for, redirect, render_template, request
from app import db
from app.models.worker import Worker  # Import the Worker model
# from app.models.skill import Skill
from app.forms import WorkerSkillForm

worker_bp = Blueprint('worker', __name__)

# Worker Profile for Signed-In Workers
@worker_bp.route('/worker', methods=['GET', 'POST'])
def worker_page():
    form = WorkerSkillForm()

    if form.validate_on_submit():
        new_skill = Skill(
            skill_name=form.skill_name.data,
            experience_level=form.experience_level.data,
            worker_id=1  # Later, replace with the worker's actual ID from the authentication system
        )

        db.session.add(new_skill)
        db.session.commit()

        flash('Skill successfully added!', 'success')
        return redirect(url_for('worker.worker_page'))
        
    else:
        print(form.errors)
    
    worker_skills = Skill.query.filter_by(worker_id=1).all()  # Later, replace with the worker's actual ID from the authentication system

    return render_template('worker_profile.html', form=form, skills=worker_skills)

# Route for viewing a specific worker's profile
@worker_bp.route('/worker/<int:worker_id>')
def profile(worker_id):
    worker = Worker.query.get_or_404(worker_id)
    # Fetch skills for the worker (if the Skill model is implemented)
    skills = Skill.query.filter_by(worker_id=worker_id).all() if 'Skill' in globals() else []
    return render_template('worker_view.html', worker=worker, skills=skills)

# Route for handling contact form submission
@worker_bp.route('/worker/<int:worker_id>/contact', methods=['POST'])
def contact(worker_id):
    worker = Worker.query.get_or_404(worker_id)
    message = request.form.get('message')

    # Process the message (e.g., send an email or store it in the database)
    # For now, just log it or print it as a placeholder
    print(f"Message from user for {worker.name}: {message}")

    flash(f"Your message to {worker.name} has been sent!", "success")
    return redirect(url_for('worker.profile', worker_id=worker_id))
