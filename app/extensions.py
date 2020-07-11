from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_login import LoginManager
from flask_uploads import UploadSet,IMAGES
from flask_uploads import configure_uploads,patch_request_class
from flask_moment import Moment
db = SQLAlchemy()
migrate = Migrate(db=db)
bootstrap = Bootstrap()
mail = Mail()
login_manager = LoginManager()
photos = UploadSet('photos',IMAGES)
moment = Moment()

def config_extensions(app):
    db.init_app(app)
    migrate.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = '只有登录才可以访问'
    login_manager.login_view = 'users.login'
    login_manager.session_protection = 'strong'
    configure_uploads(app,photos)
    patch_request_class(app,size=None)