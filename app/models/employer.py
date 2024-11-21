from app import db
from app.models.user import User

class Employer(User):
    __tablename__ = 'employers'

    #job_postings = db.relationship('JobPosting', back_populates='employer', lazy=True)

    def __repr__(self):
        return f"<Employer {self.name}>"
