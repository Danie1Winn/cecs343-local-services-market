from flask import Blueprint, flash, url_for, redirect, render_template
from app import db
#from app.models.skill import Skill
from app.forms import WorkerSkillForm

worker_bp = Blueprint('worker', __name__)

@worker_bp.route('/worker', methods=['GET', 'POST'])
def worker_page():
    form = WorkerSkillForm()

    if form.validate_on_submit():
        new_skill = Skill(
            skill_name=form.skill_name.data,
            experience_level=form.experience_level.data,
            worker_id=1 # Later, replace with the workers actual ID from the authentication system
        )

        db.session.add(new_skill)
        db.session.commit()

        flash('Skill successfully added!', 'success')
        return redirect(url_for('worker.worker_page'))
        
    else:
        print(form.errors)
    
    worker_skills = Skill.query.filter_by(worker_id=1).all() # Later, replace with the workers actual ID from the authentication system

    return render_template('worker_profile.html', form=form, skills=worker_skills)