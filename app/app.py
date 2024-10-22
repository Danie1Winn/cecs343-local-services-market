from flask import Flask
from routes.home_routes import home_bp
from routes.worker_routes import worker_bp
from routes.employer_routes import employer_bp
'''
Will be used later for database
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
'''
app = Flask(__name__)

'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Set later to specify chosen database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing database
db = SQLAlchemy(app)
migrate = Migrate(app, db)
'''
# Register blueprints for different webpages
app.register_blueprint(home_bp)
app.register_blueprint(worker_bp)
app.register_blueprint(employer_bp)

# Run application - Starts the flask development server
if __name__ == '__main__':
    app.run(debug=True, port=8000)