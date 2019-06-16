import os


class Config(object):
    """common configurations"""

    PORT = 5000
    HOST = "127.0.0.1"
    SECRET_KEY = "0334065c-c3c5-47df-8053-5e11b934eaff"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = os.getenv('USERNAME')
    MAIL_PASSWORD = os.getenv('PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('USERNAME')
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

    #administrators
    ADMINS = ['githinji.mwangi@gmail.com']

class DevelopmentConfig(Config):
    """Development configurations"""

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production Configurations"""

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    """Testing configurations"""

    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URI')


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
