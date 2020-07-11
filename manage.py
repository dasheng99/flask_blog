from flask_script import Manager
from app import create_app
from app.extensions import db
from flask_migrate import MigrateCommand
from app.models import Posts,Users
app = create_app('default')
manager = Manager(app)
manager.add_command('db',MigrateCommand)

@manager.command
def create_test_post():
    for x in range(1,200):
        content = '内容：%s'%x
        author = Users.query.filter_by(id=1).first()
        post = Posts(content=content,user=author)
        db.session.add(post)
        db.session.commit()


if __name__ == '__main__':
    manager.run()