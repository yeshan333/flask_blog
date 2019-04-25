# -*- coding: utf-8 -*-
# 扩展实例化

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor
from flask_mail import Mail
from flask_moment import Moment
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from flask_whooshee import Whooshee

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
mail = Mail()
ckeditor = CKEditor()
login_manage = LoginManager()
csrf = CSRFProtect()
whooshee = Whooshee()

# 用户加载，返回当前用户对应的模型类对象，未登录，默认返回flask-login内置的AnonymousUserMixin对象
@login_manage.user_loader
def load_user(user_id):
    from cms.models import Admin
    user = Admin.query.get(int(user_id))
    return user

login_manage.login_view = 'auth.login'
login_manage.login_message_category = u'扑街，你没登陆'
