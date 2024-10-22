from app import db
from models.user import User

class Worker(User):
    __tablename__ = 'workers' # Specify name in database

    skills = db.relationship('Skill', back_populates='worker')
    availability = db.Column(db.String(100))
    # Input worker info here, for example hourly rate, available hours, etc

    def __repr__(self):
        return f"<Worker {self.name}>"