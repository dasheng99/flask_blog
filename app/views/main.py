from flask import Blueprint,render_template,redirect,url_for,flash,request
from app.models import Posts
from app.forms import PostForm
from app.extensions import db
from flask_login import current_user
main = Blueprint('main', __name__)


@main.route('/', methods=['POST', 'GET'])
def index():
    form = PostForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            u = current_user._get_current_object()
            p = Posts(content=form.content.data,user=u)
            db.session.add(p)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('请先登录')
            return redirect(url_for('users.login'))
    # posts = Posts.query.filter_by(rid=0).all()
    page = request.args.get('p',1,type=int)
    pagination = Posts.query.filter_by(rid=0).order_by(Posts.timestamp.desc()).paginate(page,per_page=5,error_out=False)
    posts = pagination.items
    return render_template('main/index.html',form=form,posts=posts,pagination=pagination)
