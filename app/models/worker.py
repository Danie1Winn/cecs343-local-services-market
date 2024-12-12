from app import db
from sqlalchemy.orm import relationship
from app.models.skill import Skill
from datetime import datetime

class Worker(db.Model):
    __tablename__ = 'workers'

    id = db.Column(db.Integer, primary_key=True)
    profile_picture = db.Column(db.String(200))
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    zip_code = db.Column(db.String(10), nullable=True)
    travel_distance = db.Column(db.Integer, nullable=True)
    user_role = db.Column(db.String(50), default='regular')
    about_me = db.Column(db.Text, nullable=True)
    is_online = db.Column(db.Boolean, default=False)
    auto_offline_time = db.Column(db.DateTime, nullable=True)

    # Relationships
    job_postings = db.relationship('JobPosting', back_populates='worker')
    contracts = db.relationship('Contract', back_populates='worker')
    skills = db.relationship('Skill', back_populates='worker')  # Add this line

    def __repr__(self):
        return f"<Worker {self.name}>"
