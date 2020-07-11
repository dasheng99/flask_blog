import os

base_dir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = '123456'
    BOOTSTRAP_SERVE_LOCAL = True
    MAIL_SERVER = os.environ.get('MAIL_SERVER','smtp.qq.com')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME','1449764458@qq.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD','tyomjckvkjxyihdi')

    MAX_CONTENT_LENGTH = 8 * 1024 * 1024

    UPLOADED_PHOTOS_DEST = os.path.join(base_dir,'static/uploads')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DB_USERNAME = 'root'
    DB_PASSWORD = '123456'
    DB_HOST = '127.0.0.1'
    DB_PORT = '3306'
    DB_NAME = 'blog'
    DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8'%(DB_USERNAME,DB_PASSWORD,DB_HOST,DB_PORT,DB_NAME)

    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(base_dir,'bbs+test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(base_dir, 'bbs+production.sqlite')


config = {
    'development':DevelopmentConfig,
    'testing':TestConfig,
    'production':ProductionConfig,
    'default':DevelopmentConfig
}