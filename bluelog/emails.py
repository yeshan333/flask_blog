# -*- coding: utf-8 -*-
# 评论提醒

import os

from threading import Thread

from flask import url_for, current_app
from flask_mail import Message

from bluelog.extensions import mail


# 异步方式发送
def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)

# 发信函数
def send_mail(subject, to, html):
    app = current_app._get_current_object() # 获取被代理的真实对象
    message = Message(subject, recipients=[to], html=html)
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr

def send_new_comment_email(post,):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) + '#comments'
    # email = current_app.config['BLUELOG_EMAIL'],不清楚当前代理对象为什么是None
    send_mail(subject='New comment', to=current_app.config['BLUELOG_EMAIL'],
              html='<p>New comment in post <i>%s</i>, click the link below to check:</p>'
                   '<p><a href="%s">%s</a></P>'
                   '<p><small style="color: #868e96">Do not reply this email.</small></p>'
                   % (post.title, post_url, post_url))

def send_new_reply_email(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True) + '#comments'
    send_mail(subject='New reply', to=comment.email,
              html='<p>New reply for the comment you left in post <i>%s</i>, click the link below to check: </p>'
                   '<p><a href="%s">%s</a></p>'
                   '<p><small style="color: #868e96">Do not reply this email.</small></p>'
                   % (comment.post.title, post_url, post_url))


