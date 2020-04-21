# -*- coding: utf-8 -*-
"""
初始化Flask应用
"""

from flask import Flask
from config import config
from .extensions import bootstrap, db, migrate, login_manager, moment


def create_app(config_name):
    """创建应用实例
    :param config_name: 设置名称，可以为development（开发）或production（生产）
    :return: 返回Flask应用实例
    """
    app = Flask(__name__)

    app.config.from_object(config[config_name])  # 从config中导入设置

    # 扩展配置
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    moment.init_app(app)

    # 蓝图配置
    # 主蓝图
    from .main import main as main_bp
    app.register_blueprint(main_bp)  # 注册蓝图到应用

    # 用户认证蓝图
    from .auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    return app
