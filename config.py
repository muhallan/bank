import os


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SECRET_KEY = os.getenv('SECRET')


class Production(Config):
    DEBUG = False


class Testing(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bank_testing_db'
    TESTING = True


class Development(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


config_dict = {
    'production': Production,
    'development': Development,
    'testing': Testing
}
