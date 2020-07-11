from flask import Blueprint,request,render_template,flash,redirect,url_for,current_app
from app.forms import RegisterForm,LoginForm,UploadForm,ChangePasswordForm,ChangeEmailForm
from app.extensions import db,photos
from app.models import Users
from app.email import send_mail
from flask_login import login_user,logout_user,login_required,current_user
import os
from PIL import Image

users = Blueprint('users', __name__)


@users.route('/register/', methods=['POST', 'GET'])
def register():
    form =RegisterForm(request.form)
    if form.validate():
        u = Users(username=form.username.data,
                  password=form.password.data,
                  email=form.email.data)
        db.session.add(u)
        db.session.commit()
        token = u.generate_active_token()
        send_mail(u.email,'账户激活','email/activate',username=u.username,token=token)
        flash('该用户已经注册，请点击邮件中的链接完成激活')
        return redirect(url_for('main.index'))
    return render_template('users/register.html',form=form)


@users.route('/activate/<token>/')
def acticvate(token):
    if Users.check_activate_token(token):
        flash('账户已经激活')
        return redirect(url_for('users.login'))
    else:
        flash('账户激活失败')
        return redirect(url_for('main.index'))

@users.route('/login/',methods=['POST','GET'])
def login():
    form = LoginForm(request.form)
    if form.validate():
        u = Users.query.filter_by(username=form.username.data).first()
        if not u:
            flash('该用户不存在')
        elif not u.confirmed:
            flash('该账户没有激活，请先激活')
        elif u.verify_password(form.password.data):
            login_user(u,remember=form.remember.data)
            flash('登陆成功')
            return redirect(request.args.get('next') or url_for('main.index'))
        else:
            flash('登陆失败')
    return render_template('users/login.html',form=form)


@users.route('/logout/',methods=['POST','GET'])
def logout():
    logout_user()
    flash('退出登录')
    return redirect(url_for('main.index'))

@users.route('/profile/',methods=['POST','GET'])
@login_required
def profile():
    return render_template('users/profile.html')


@users.route('/change_icon/',methods=['POST','GET'])
@login_required
def change_icon():
    form = UploadForm()
    if form.validate():
        suffix = os.path.splitext(form.icon.data.filename)[1]
        filename = random_string()+suffix
        photos.save(form.icon.data,name=filename)
        pathname = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],filename)
        img = Image.open(pathname)
        img.thumbnail((128,128))
        img.save(pathname)
        if current_user.icon != 'default.jpg':
            os.remove(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'],current_user.icon))
        current_user.icon = filename
        db.session.add(current_user)
        db.session.commit()
        flash('图片已经保存')
    img_url = photos.url(current_user.icon)
    return render_template('users/change_icon.html',form=form,img_url=img_url)

@users.route('/change_password/',methods=['POST','GET'])
@login_required
def change_password():
    form = ChangePasswordForm()
    newpassword = form.newpassword.data
    if form.validate():
        if current_user.verify_password(password=form.oldpassword.data):
            current_user.password = newpassword
            db.session.add(current_user)
            db.session.commit()
            flash('密码修改成功')
            return redirect(url_for('main.index'))
        else:
            flash('修改失败')
    return render_template('users/change_password.html',form=form)

@users.route('/change_email/',methods=['POST','GET'])
@login_required
def change_email():
    form = ChangeEmailForm()
    if form.validate():
        if form.oldemail.data == current_user.email:
            current_user.email = form.newemail.data
            current_user.confirmed = 0
            db.session.add(current_user)
            db.session.commit()
            token = current_user.generate_active_token()
            send_mail(current_user.email, '账户激活', 'email/activate', username=current_user.username, token=token)
            flash('邮箱已经修改，请点击邮件中的链接完成激活')
            return redirect(url_for('main.index'))
        else:
            flash('修改失败')
    return render_template('users/change_email.html',form=form)

def random_string(length=32):
    import random
    base_str = 'qwertyuiopasdfghjklzxcvbnm01234567890'
    return ''.join(random.choice(base_str)for i in range(length))