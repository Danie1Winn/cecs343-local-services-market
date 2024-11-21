from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize db and migrate globally
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Create the Flask app
    app = Flask(__name__)

    # Configure the app
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/local_services.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional but recommended
    app.config.from_object('app.config.Config')
    app.config['UPLOAD_FOLDER'] = 'app/static/uploads/profile_pics'

    # Initialize the db and migrate with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import models
    from app import models

    # Import blueprints
    from app.routes.login_page_routes import login_bp
    from app.routes.signup_page_routes import signup_bp
    from app.routes.home_routes import home_bp
    from app.routes.worker_routes import worker_bp
    from app.routes.employer_routes import employer_bp

    # Register blueprints with the app
    app.register_blueprint(login_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(worker_bp)
    app.register_blueprint(employer_bp)

    return app