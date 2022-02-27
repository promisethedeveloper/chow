import os

uri = os.environ.get('DATABASE_URL', 'postgresql:///first_capstone_db')
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)

class Config(object):
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SECRET_KEY = 'hellosecret1'
    DEBUG_TB_INTERCEPT_REDIRECTS = False
