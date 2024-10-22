class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///local_services.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'secret_key'
    WTF_CSRF_ENABLED = True