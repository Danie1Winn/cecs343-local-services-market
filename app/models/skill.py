from app import db

class Skill(db.Model):
    __tablename__ = 'skills'
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(120), nullable=False)
    experience_level = db.Column(db.String(120), nullable=False)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)

    def __repr__(self):
        return f'<Skill {self.skill_name} - Level: {self.experience_level}>'