from app import db

class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    
    # Foreign key - links data between two tables in the database
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)

    # Relationship - connects the skill to a worker in the database
    worker = db.relationship('Worker', back_populates='skills')

    def __repr__(self):
        return f"<Skill {self.name}>"