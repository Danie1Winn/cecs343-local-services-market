from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange

class WorkerProfileForm(FlaskForm):
    about_me = TextAreaField('About Me', validators=[DataRequired()])
    zip_code = StringField('ZIP Code', validators=[DataRequired()])
    travel_distance = IntegerField('Travel Distance (miles)', validators=[DataRequired(), NumberRange(min=1)])
    skill_name = StringField('Skill Name')
    experience_level = IntegerField('Experience Level (1-5)', validators=[NumberRange(min=1, max=5)])
    submit = SubmitField('Save Changes')
