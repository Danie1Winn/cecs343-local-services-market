from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional

class WorkerProfileForm(FlaskForm):
    about_me = TextAreaField('About Me', validators=[DataRequired()])
    zip_code = StringField('ZIP Code', validators=[DataRequired()])
    travel_distance = IntegerField('Travel Distance (miles)', validators=[DataRequired(), NumberRange(min=1)])
    skill_name = StringField('Skill Name', validators=[Optional()])
    experience_level = IntegerField('Experience Level (1-5)', validators=[Optional(), NumberRange(min=1, max=5)])
    description = TextAreaField('Skill Description', validators=[Optional()])
    rate_type = SelectField(
        'Rate Type',
        choices=[('fixed', 'Fixed'), ('hourly', 'Hourly'), ('negotiable', 'Negotiable')],
        default='negotiable'
    )
    rate_value = FloatField(
        'Rate Value',
        validators=[Optional(), NumberRange(min=0)],
        render_kw={"placeholder": "Leave blank if negotiable"}
    )
    submit = SubmitField('Save Changes')
