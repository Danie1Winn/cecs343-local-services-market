from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Set later to specify chosen database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from route import *

# Run application - Starts the flask development server
if __name__ == '__main__':
    app.run(debug=True)