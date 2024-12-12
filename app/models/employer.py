from app import db
from sqlalchemy.orm import relationship

class Employer(db.Model):
    __tablename__ = 'employers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    user_role = db.Column(db.String(50), default='regular') 

    # Relationships
    job_postings = relationship('JobPosting', back_populates='employer')
    contracts = relationship('Contract', back_populates='employer')

    def __repr__(self):
        return f"<Employer {self.name}>"
