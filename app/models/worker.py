from app import db
from app.models.user import User

class Worker(User):
    __tablename__ = 'workers' 
    
    id = db.Column(db.Integer, primary_key=True)  # Ensure the ID field is defined
    profile_picture = db.Column(db.String(200), nullable=True)
    zip_code = db.Column(db.String(10), nullable=False, default="00000")
    travel_distance = db.Column(db.Integer, nullable=False, default=10)  # Distance the worker is willing to travel

    # skills = db.relationship('Skill', back_populates='worker')

    def __repr__(self):
        return f"<Worker {self.name}>"
