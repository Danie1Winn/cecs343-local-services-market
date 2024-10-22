from app import db
from app.models.user import User

class Worker(User):
    __tablename__ = 'workers' # Specify name in database
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)

    # Input worker info here, for example hourly rate, available hours, etc
    skills = db.relationship('Skill', back_populates='worker')


    def __repr__(self):
        return f"<Worker {self.name}>"