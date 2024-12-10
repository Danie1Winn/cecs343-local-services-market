from app import db
from sqlalchemy.orm import relationship

class Worker(db.Model):
    __tablename__ = 'workers'

    id = db.Column(db.Integer, primary_key=True)
    profile_picture = db.Column(db.String(200))
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    zip_code = db.Column(db.String(10), nullable=False)
    travel_distance = db.Column(db.Integer, nullable=False)
    user_role = db.Column(db.String(50), default='regular')  # Added role field

    # Relationships
    job_postings = relationship('JobPosting', back_populates='worker')
    contracts = relationship('Contract', back_populates='worker')

    def __repr__(self):
        return f"<Worker {self.name}>"
