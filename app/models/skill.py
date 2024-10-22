from app import db

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(100), nullable=False)
    experience_level = db.Column(db.Integer, nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'))   

    # Relationship - connects the skill to a worker in the database
    worker = db.relationship('Worker', back_populates='skills')

    def __repr__(self):
        return f"<Skill {self.name}>"