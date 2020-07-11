from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired,Length,EqualTo,Email
from wtforms.validators import ValidationError
from app.models import Users
from flask_wtf.file import FileField,FileRequired,FileAllowed
from app.extensions import photos
class RegisterForm(FlaskForm):
    username = StringField('用户名',validators=[DataRequired(),Length(6,20,message='用户名长度必须6~20位')])
    password = PasswordField('密码',validators=[DataRequired(),Length(6,20,message='密码长度必须6~20位')])
    confirm = PasswordField('确认密码',validators=[EqualTo('password',message='两次密码输入必须一致')])
    email = StringField('邮箱',validators=[Email('请填写正确的邮箱格式')])
    submit = SubmitField('立即注册')

    def validate_username(self,field):
        if Users.query.filter_by(username=field.data).first():
            raise ValidationError('该用户已经注册，请选用其它用户名')

    def validate_email(self,field):
        if Users.query.filter_by(email=field.data).first():
            raise ValidationError('该邮箱名已经注册，请选用其它邮箱名')

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(6, 20, message='用户名长度必须6~20位')])
    password = PasswordField('密码', validators=[DataRequired(), Length(6, 20, message='密码长度必须6~20位')])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')

class UploadForm(FlaskForm):
    icon = FileField('头像',validators=[FileRequired('请上传文件'),FileAllowed(photos,message='只能上传图片')])
    submit = SubmitField('提交')

class ChangePasswordForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(6, 20, message='用户名长度必须6~20位')])
    oldpassword = PasswordField('旧密码', validators=[DataRequired(), Length(6, 20, message='密码长度必须6~20位')])
    newpassword = PasswordField('新密码', validators=[DataRequired(), Length(6, 20, message='密码长度必须6~20位')])
    submit = SubmitField('提交')

class ChangeEmailForm(FlaskForm):
    oldemail = StringField('旧邮箱', validators=[Email('请填写正确的邮箱格式')])
    newemail = StringField('新邮箱', validators=[Email('请填写正确的邮箱格式')])
    submit = SubmitField('提交')