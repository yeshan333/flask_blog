# -*- coding: utf-8 -*-
# 虚拟信息

import random

from faker import Faker
from sqlalchemy.exc import IntegrityError

from cms.models import Admin, Category, Comment, Post, Link
from cms.extensions import db

fake = Faker()

def fake_admin():
    admin = Admin(
        username = "admin",
        blog_title = "shansan",
        blog_sub_title = "Wonderful !",
        name = "shansan",
        about = "Pythoner"  
    )
    admin.set_password('helloflask')
    db.session.add(admin)
    db.session.commit()

def fake_categories(count=10):
    # 默认分类
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:   # 捕捉分类名冲突，会话回滚
            db.session.rollback()

def fake_posts(count=50):
    for i in range(count):
        post = Post(
            title = fake.sentence(),
            body = fake.text(2000),
            # 分类根据主键值随机获取，
            category = Category.query.get(random.randint(1, Category.query.count())),
            timestamp = fake.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()

def fake_comments(count=500):

    for i in range(count):
        # 过审核
        comment = Comment(
            author = fake.name(),
            email = fake.email(),
            site = fake.url(),
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            reviewed = True,
            post = Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    
    salt = int(count*0.1)
    for i in range(salt):
        # 未审核        
        comment = Comment(
            author = fake.name(),
            email = fake.email(),
            site = fake.url(),
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            reviewed = False,
            post = Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
        
        # 管理员评论
        comment = Comment(
            author = "shansan",
            email = "1329441308@qq.com",
            site = "https://shansan.top",
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            from_admin = True,
            reviewed = True,
            post = Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    for i in range(salt):
        # 回复
        comment = Comment(
            author = fake.name(),
            email = fake.email(),
            site = fake.url(),
            body = fake.sentence(),
            timestamp = fake.date_time_this_year(),
            reviewed = True,
            replied = Comment.query.get(random.randint(1, Comment.query.count())),
            post = Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

def fake_links():
    twitter = Link(name='Twitter', url='#')
    facebook = Link(name='Facebook', url='#')
    linkedin = Link(name='LinkedIn', url='#')
    google = Link(name='Google+', url='#')
    db.session.add_all([twitter, facebook, linkedin, google])
    db.session.commit()
