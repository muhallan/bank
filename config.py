import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')


class Production(Config):
    DEBUG = False


class Testing(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bank_testing_db'
    TESTING = True
    DEBUG = True


class Development(Config):
    DEBUG = True


config_dict = {
    'production': Production,
    'development': Development,
    'testing': Testing
}
