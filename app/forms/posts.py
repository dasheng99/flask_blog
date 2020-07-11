from flask_wtf import FlaskForm
from wtforms import TextAreaField,SubmitField
from wtforms.validators import Length
class PostForm(FlaskForm):
    content = TextAreaField('',render_kw={'placeholder':'此时此刻你想说什么....'},validators=[Length(6,140,message='说话注意分寸6~140')])
    submit = SubmitField('发表')