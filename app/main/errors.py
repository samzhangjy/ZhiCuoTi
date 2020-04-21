# -*- coding: utf-8 -*-
"""
应用错误处理
"""

from flask import render_template

from . import main


@main.app_errorhandler(404)
def not_found(e):
    """404未找到"""
    return render_template('errors/404.html'), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    """500服务器错误"""
    return render_template('errors/500.html'), 500
