import os


class Config:
    '''
    General configuration parent class
    '''
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = 'xystus'
    UPLOADED_PHOTOS_DEST ='app/static/photos'

    # email configurations
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    SUBJECT_PREFIX = 'Pitch Website'
    SENDER_EMAIL = 'gmail.com'

    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):
    '''
    Production configuration child class
    Args:
        Config: The parent configuration class with General confirguration settings
    '''
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")


class DevConfig(Config):
    '''
    Development  configuration child class
    Args:
        Config: The parent configuration class with General configuration settings
    '''
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://xystus:xystus@localhost/pitch'

    DEBUG = True


config_options = {
    'development': DevConfig,
    'production': ProdConfig
}