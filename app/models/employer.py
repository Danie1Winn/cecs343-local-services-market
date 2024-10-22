from app import db
from app.models.user import User

class Employer(User):
    __tablename__ = 'employers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    job_postings = db.relationship('JobPosting', back_populates='employer', lazy=True)

    def __repr__(self):
        return f"<Employer {self.name}>"
