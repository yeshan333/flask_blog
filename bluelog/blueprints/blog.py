# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, url_for, request, current_app
from bluelog.models import Post

blog_bp = Blueprint('blog', __name__)

@blog_bp.route('/')
def index():
    """ posts = Post.query.order_by(Post.timestamp.desc()).all() """
    page = request.args.get('page', 1, type=int) # 通过查询字符串获取当前页数
    per_page = current_app.config['BLUELOG_PER_PAGE'] # 每页数量
    # paginate方法的page默认值为1，per_page的默认值为20,pagination为分页对象
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items # 当前页数的记录列表
    return render_template('blog/index.html', pagination=pagination, posts=posts)

@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')

@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    return render_template('blog/category.html')

@blog_bp.route('post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    return render_template('blog/post.html')
