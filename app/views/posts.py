from flask import Blueprint,jsonify
from flask_login import current_user

posts = Blueprint('posts',__name__)

@posts.route('/collect/<int:pid>')
def collect(pid):
    if current_user.is_favorite(pid):
        current_user.def_favorite(pid)
    else:
        current_user.add_favorite(pid)
    return jsonify({'resulet':'OK'})