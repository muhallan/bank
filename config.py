import os


class Config:
    """
    The base class configuration
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'SQLALCHEMY_DATABASE_URI', 'sqlite:///bank_db.db')
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SECRET_KEY = os.getenv('SECRET', 'averyrandomstringthatshardtodecode')


class Production(Config):
    """
    Production configuration
    """
    DEBUG = False


class Testing(Config):
    """
    Testing configuration
    """
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bank_testing_db'
    TESTING = True
    SECRET_KEY = 'averyrandomstringthatshardtodecode'


class Development(Config):
    """
    Development configuration
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True


config_dict = {
    'production': Production,
    'development': Development,
    'testing': Testing
}
