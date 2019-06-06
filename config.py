import os


class Config(object):
    """common configurations"""

    PORT = 5000
    HOST = "127.0.0.1"
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))


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
