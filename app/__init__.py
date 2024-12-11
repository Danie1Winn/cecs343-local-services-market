from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import os
import subprocess

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
    from app.routes.developer_routes import developer_bp

    # Register blueprints with the app
    app.register_blueprint(login_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(worker_bp)
    app.register_blueprint(employer_bp)
    app.register_blueprint(developer_bp, url_prefix='/developer')

    # Initialize and start the scheduler
    init_scheduler(app)

    return app

def init_scheduler(app):
    """Initializes the APScheduler for auto-offline feature and job expiration."""
    from app.models.worker import Worker  # Import Worker model
    from app.models.contract import Contract  # Import Contract model
    from app import db

    def check_auto_offline():
        """Check and update workers who should go offline."""
        with app.app_context():  # Ensure app context is available
            now = datetime.utcnow()
            workers = Worker.query.filter(Worker.is_online == True, Worker.auto_offline_time <= now).all()
            for worker in workers:
                worker.is_online = False
                worker.auto_offline_time = None
            db.session.commit()

    def expire_jobs():
        """Mark jobs as expired if their scheduled date has passed."""
        with app.app_context():
            now = datetime.utcnow()
            expired_jobs = Contract.query.filter(Contract.status == 'pending', Contract.job_date <= now).all()
            for job in expired_jobs:
                job.status = 'expired'
            db.session.commit()

    scheduler = BackgroundScheduler()
    scheduler.add_job(check_auto_offline, 'interval', minutes=1)  # Runs every 1 minute for auto-offline
    scheduler.add_job(expire_jobs, 'interval', minutes=1)  # Runs every 1 minute for job expiration
    scheduler.start()
