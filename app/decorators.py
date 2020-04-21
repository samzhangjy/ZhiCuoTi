# -*- coding: utf-8 -*-
"""
自定义装饰器
"""

from functools import wraps
from flask import abort, current_app
from flask_login import current_user
from .models import UserType


def _teacher_required():
    """教师类型装饰器
    :return: 装饰后的函数 -> function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_teacher():
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def _student_required():
    """学生类型装饰器
    :return: 装饰后的函数 -> function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_user.is_teacher():
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def student_required(f):
    return _student_required()(f)


def teacher_required(f):
    return _teacher_required()(f)
