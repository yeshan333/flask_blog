# -*= coding: utf-8 -*=
# 配置文件

import os
import sys

# 定位到项目的根目录（绝对路径）
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = ('Bluelog Admin', MAIL_USERNAME)
    
    # 博文配置
    BLUELOG_EMAIL = os.getenv('BLUELOG_EMAIL')
    BLUELOG_POST_PER_PAGE = 10
    BLUELOG_MANAGE_POST_PER_PAGE = 15
    BLUELOG_COMMENT_PER_PAGE = 15
    # 主题选择
    BLUELOG_THEMES = {'perfect_blue':'Perfect Blue', 'black_swan':'Black Swan', 'nice_green':'Nice green'}

# 开发环境
class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI= prefix + os.path.join(basedir, 'data-dev-.db')

# 生产环境从环境变量中获取DBMS的URI
class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}

"""
1. 这里使用了一个存储配置名称和对应配置类的字典
2. 从配置文件导入config字典,创建程序实例后，可通过app.config.from_object()方法加载配置，传入配置类
"""