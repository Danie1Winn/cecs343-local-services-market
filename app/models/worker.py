from app import db
from app.models.user import User

class Worker(User):
    __tablename__ = 'workers' 
    
    profile_picture = db.Column(db.String(200), nullable=True)
    
    #skills = db.relationship('Skill', back_populates='worker')

    def __repr__(self):
        return f"<Worker {self.name}>"