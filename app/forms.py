from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class WorkerSkillForm(FlaskForm):
    skill_name = StringField('Skill Name', validators=[DataRequired()])
    experience_level = IntegerField('Experience Level (1-5)', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Add Skill')