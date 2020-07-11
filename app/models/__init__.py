from .posts import Posts
from .users import Users
from app.extensions import db

collections = db.Table('collections',
    db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
    db.Column('posts_id',db.Integer,db.ForeignKey('posts.id')),


)