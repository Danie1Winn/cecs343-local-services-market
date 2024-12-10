from app import db
from sqlalchemy.orm import relationship
from datetime import datetime

class JobPosting(db.Model):
    __tablename__ = 'job_postings'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='open')  # open, accepted, completed, closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Foreign Keys
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'))
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'))

    # Relationships
    employer = relationship('Employer', back_populates='job_postings')
    worker = relationship('Worker', back_populates='job_postings')

    def __repr__(self):
        return f"<JobPosting {self.title}>"
