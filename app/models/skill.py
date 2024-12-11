from app import db

class Skill(db.Model):
    __tablename__ = 'skills'

    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(120), nullable=False)
    experience_level = db.Column(db.Integer, nullable=False)  # Changed to Integer
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)
    description = db.Column(db.Text, default="No description provided", nullable=False)
    rate_type = db.Column(db.String(20), default="negotiable", nullable=False)
    rate_value = db.Column(db.Float, nullable=True)

    # Back reference to Worker
    worker = db.relationship('Worker', back_populates='skills')

    def __repr__(self):
        return f"<Skill {self.skill_name} - Level: {self.experience_level}>"
