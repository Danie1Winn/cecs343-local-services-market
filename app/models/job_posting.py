from app import db

class JobPosting(db.Model):
    __tablename__ = 'job_postings'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'))

    employer = db.relationship('Employer', back_populates='job_postings')

    def __repr__(self):
        return f"<JobPosting {self.title}>"
