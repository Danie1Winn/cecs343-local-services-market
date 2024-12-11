from app import db
from datetime import datetime

class Contract(db.Model):
    __tablename__ = 'contracts'

    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'), nullable=False)
    job_posting_id = db.Column(db.Integer, db.ForeignKey('job_postings.id'), nullable=True)
    description = db.Column(db.String(500), nullable=True)  # New column for job description
    status = db.Column(db.String(50), default='pending')  # pending, accepted, completed, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    job_date = db.Column(db.DateTime, nullable=False)  # Job date

    # Relationships
    worker = db.relationship('Worker', back_populates='contracts')
    employer = db.relationship('Employer', back_populates='contracts')
    job_posting = db.relationship('JobPosting', backref='contracts')
