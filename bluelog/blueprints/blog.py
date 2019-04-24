# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, url_for, request, current_app, Blueprint, abort, make_response
from flask_login import current_user

from bluelog.emails import send_new_comment_email, send_new_reply_email
from bluelog.extensions import db
from bluelog.forms import CommentForm, AdminCommentForm
from bluelog.models import Post, Category, Comment
from bluelog.utils import redirect_back

blog_bp = Blueprint('blog', __name__)



@blog_bp.route('/')
def index():
    """ posts = Post.query.order_by(Post.timestamp.desc()).all() """
    page = request.args.get('page', 1, type=int) # 通过查询字符串获取当前页数
    per_page = current_app.config['BLUELOG_POST_PER_PAGE'] # 每页数量
    # paginate方法的page默认值为1，per_page的默认值为20,pagination为分页对象
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items # 当前页数的记录列表
    return render_template('blog/index.html', pagination=pagination, posts=posts)

@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')

@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    # 使用with_parent筛选所属分类文章
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)

@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    # 通过filter_by过滤器获取通过审核的评论
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
        page, per_page)
    # 评论分页
    comments = pagination.items

    if current_user.is_authenticated: # 已登录，使用管理员表单
        form = AdminCommentForm()
        form.author.data = current_user.name
        form.email.data = current_app.config['BLUELOG_EMAIL']
        form.site.data = url_for('.index')
        from_admin = True
        reviewed = True
    else:
        form = CommentForm()
        from_admin = False
        reviewed = False
    
    if form.validate_on_submit():
        author = form.author.data
        email = form.email.data
        site = form.site.data
        body = form.body.data
        comment = Comment(
            author=author, email=email, site=site, body=body,
            from_admin=from_admin, post=post, reviewed=reviewed
        )
        replied_id = request.args.get('reply')
        if replied_id:
            replied_comment = Comment.query.get_or_404(replied_id)
            comment.replied = replied_comment
            send_new_reply_email(replied_comment)
        db.session.add(comment)
        db.session.commit()
        
        # 消息闪现提醒
        if current_user.is_authenticated:
            flash('Comment published.', 'success')
        else:
            flash('Thanks, your comment will be published after reviewed.', 'info')
            # admin_email = current_app.config['BLUELOG_EMAIL']
            send_new_comment_email(post)
        return redirect(url_for('.show_post', post_id=post_id))
    return render_template('blog/post.html', post=post, comments=comments, pagination=pagination, form=form)

# 回复功能
@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if not comment.post.can_comment:
        flash('Comment is disabled.', 'warning')
        return redirect(url_for('.show_post', post_id=comment.post.id))
    return redirect(
        url_for('.show_post', post_id=comment.post_id, reply=comment_id, author=comment.author) + '#comment-form')

# 主题切换
@blog_bp.route('/change-theme/<theme_name>')
def change_theme(theme_name):
    if theme_name not in current_app.config['BLUELOG_THEMES'].keys():
        abort(404)
    
    response = make_response(redirect_back()) # 生成一个重定向啊应
    response.set_cookie('theme', theme_name, max_age=30*24*60*60)
    return response

# 搜索功能
@blog_bp.route('/search')
def search():
    q = request.args.get('q', '')
    if q == '':
        flash('Enter keywords about category or post title', 'warning')
        return redirect_back()
    
    # 获取查询类型，再模板中给出
    what = request.args.get('what', 'title')
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']

    if what == 'title':
        pagination = Post.query.whooshee_search(q).paginate(page, per_page)
    elif what == 'category':
        pagination = Category.query.whooshee_search(q).paginate(page, per_page)
    else:
        redirect_back()

    results = pagination.items

    return render_template('search.html', q=q, results=results, pagination=pagination, what=what)
