# -*- coding: utf-8 -*-
# 工厂函数

import os
import click


from flask import Flask, render_template
from flask_wtf.csrf import CSRFError
from flask_login import current_user

from cms.settings import config
from cms.extensions import bootstrap, db, moment, mail, ckeditor, login_manage, csrf, whooshee
from cms.blueprints.admin import admin_bp
from cms.blueprints.auth import auth_bp
from cms.blueprints.blog import blog_bp
from cms.models import Admin, Category, Comment, Post, Link

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development') 

    app = Flask('cms')
    app.config.from_object(config[config_name])

    register_logging(app)
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    register_errors(app)
    register_shell_context(app)
    register_template_context(app)

    """ 
    # 利用扩展提供的init_app()方法来分离扩展的实例化和初始化操作，实例化操作在extensions模块
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    """
    """
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(auth_bp,url_prefix'/auth')
    """

    return app

def register_logging(app):
    pass

# 注册扩展，扩展初始化
def register_extensions(app):
    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    mail.init_app(app)
    ckeditor.init_app(app)
    login_manage.init_app(app)
    csrf.init_app(app)
    whooshee.init_app(app)

# 注册蓝本
def register_blueprints(app):
    """使用url_prefix参数将蓝本静态文件路径自动设置为“/蓝本前缀/static”"""
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp,url_prefix='/admin')
    app.register_blueprint(auth_bp,url_prefix='/auth')

# 注册自定义shell命令
def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Category=Category, Comment=Comment, Post=Post)

# 模板上下文
def register_template_context(app):
    @app.context_processor
    def make_template_context():
        admin = Admin.query.first()
        categories = Category.query.order_by(Category.name).all()
        links = Link.query.order_by(Link.name).all()
        # 处理未审核评论数量
        if current_user.is_authenticated:
            unread_comments = Comment.query.filter_by(reviewed=False).count()
        else:
            unread_comments = None
        return dict(admin=admin, categories=categories, unread_comments=unread_comments, links=links)

# 注册错误处理函数
def register_errors(app):
    
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('400.html'),400
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    # 自定义CSRF错误响应
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return render_template('errors/400.html', description=e.description), 400

def register_commands(app):
    # 数据库初始化
    @app.cli.command()
    @click.option('--drop', is_flag=True, help="Create after drop.")
    def initdb(drop):
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Drop tables.')
        db.create_all()
        click.echo('Initialized database.')
    
    # 虚拟数据生成
    @app.cli.command()
    @click.option('--category', default=10, help='quantity of categories, default is 10.')
    @click.option('--post', default=50, help='quantity of posts, default is 50.')
    @click.option('--comment', default=10, help='quantity of comments, default is 500.')
    def forge(category, post, comment):
        from cms.fakes import fake_admin, fake_categories, fake_comments, fake_posts, fake_links

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator ......')
        fake_admin()

        click.echo('Generator %d categories ......' % category)
        fake_categories()

        click.echo('Generating %d posts...' % post)
        fake_posts(post)

        click.echo('Generating %d comments...' % comment)
        fake_comments(comment)

        click.echo('Generating 4 links')
        fake_links()

        click.echo('Done.')
    
    # 管理员注册
    @app.cli.command()
    @click.option('--username', prompt=True, help='The username used to login.')
    @click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login ')
    def init(username, password):
        """Building Bluelog, just for you."""

        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('The administrator already exists, updating...')
            admin.username = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account...')
            admin = Admin(
                username=username,
                blog_title='Bluelog',
                blog_sub_title="No, I'm the real thing.",
                name='Admin',
                about='Anything about you.'
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            click.echo('Creating the default category...')
            category = Category(name='Default')
            db.session.add(category)

        db.session.commit()
        click.echo('Done.')
