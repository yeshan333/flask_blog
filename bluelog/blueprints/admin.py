# -*- coding: utf-8 -*-

from flask import Blueprint

# 创建蓝本，第一个参数为蓝本的名称，第二个参数是包或模块的名称
# 使用__name__方便判断蓝本的根目录，寻找模板文件夹和静态文件夹
admin_bp = Blueprint('admin',__name__)