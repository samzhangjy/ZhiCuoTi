# -*- coding: utf-8 -*-
"""
用户认证蓝图初始化
"""

from flask import Blueprint

auth = Blueprint('auth', __name__, url_prefix='/auth')  # 设置蓝图URL前缀为/auth

from . import views
