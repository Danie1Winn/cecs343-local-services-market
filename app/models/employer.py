from app import db
from models.user import User

class Employer(User):
    __tablename__ = 'employers' # Specify name in database

    # Link job postings to employer
    job_postings = db.relationship('JobPosting', back_populates='employer')

    def __repr__(self):
        return f"<Employer {self.name}>"