from app import db

class User(db.Model):
    __abstract__ = True # Don't create a table in the database

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(15), unique=True, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"
