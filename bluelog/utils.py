# -*- coding: utf-8 -*-

"""
- 辅助函数：
  - redirect_back : 重定向回上一个页面，默认为主页
  - is_safe_url : URL安全验证，defense Open Redirect 
"""

try:
    from urlparse import urlparse, urljoin
except ImportError:
    from urllib.parse import urlparse, urljoin

from flask import request, redirect, url_for

def is_safe_url(target):
    ref_url = urlparse(request.host_url) # request.host_url获取程序内的主机URL
    test_url = urlparse(urljoin(request.host_url, target)) # 使用urljoin将目标url转换成绝对url
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):  # 用来判断目标是否属于本应用，防止open redirect漏洞
            return url_for(target)
    return redirect(url_for(default, **kwargs))
