from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object('app.config.Config')

    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register the blueprints
    from app.routes.login_page_routes import login_bp
    from app.routes.signup_page_routes import signup_bp
    from app.routes.home_routes import home_bp
    from app.routes.worker_routes import worker_bp
    from app.routes.employer_routes import employer_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(signup_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(worker_bp)
    app.register_blueprint(employer_bp)

    return app
