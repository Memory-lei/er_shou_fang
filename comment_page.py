from flask import render_template,request, redirect, url_for, flash,Blueprint

from settings import db
from models import Comment,User

comment_page = Blueprint('comment_page', __name__)

# 添加评论
@comment_page.route('/add_comment/<int:house_id>', methods=['POST'])
def add_comment(house_id):
    if not request.cookies.get('name'):
        flash('请先登录再进行评论。')
        return redirect(url_for('login'))
    
    content = request.form['content']
    user_name = request.cookies.get('name')
    user = User.query.filter_by(name = user_name).first()
    new_comment = Comment(user_id=user.id, house_id=house_id, content=content)
    db.session.add(new_comment)
    db.session.commit()
    flash('评论添加成功。')
    return redirect(url_for('detail_page.detail', hid=house_id))

# 删除评论
@comment_page.route('/delete_comment/<int:comment_id>')
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('评论已删除。')
    return redirect(url_for('user_page.user',name= request.cookies.get('name')))