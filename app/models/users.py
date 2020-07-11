from app.extensions import db
from app.models import Posts
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.extensions import login_manager
from flask_login import UserMixin
class Users(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64), unique=True)
    confirmed = db.Column(db.Boolean, default=False)
    icon = db.Column(db.String(64), default='default.jpg')
    posts = db.relationship('Posts', backref='user')


    favorites =db.relationship('Posts',secondary='collections',backref=db.backref('users',lazy='dynamic'),lazy='dynamic')

    @property
    def password(self):
        raise AttributeError('密码不可读')

    @password.setter
    def password(self, passwrod):
        self.password_hash = generate_password_hash(passwrod)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_active_token(self,expires_in=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expires_in)
        return s.dumps({'id':self.id})
    @staticmethod
    def check_activate_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False

        u = Users.query.get(data.get('id'))
        if not u:
            return False
        if not u.confirmed:
            u.confirmed =True
            db.session.commit()
        return True

    def is_favorite(self,uid):
        favorites = self.favorites.all()
        posts = list(filter(lambda p:p.id == uid,favorites))
        if len(posts)>0:
            return True
        return False

    def add_favorite(self,uid):
        p =Posts.query.get(uid)
        self.favorites.append(p)

    def def_favorite(self,uid):
        p = Posts.query.get(uid)
        self.favorites.remove(p)


@login_manager.user_loader
def load_user(uid):
    return Users.query.get(int(uid))
