# -*- coding: utf-8 -*-
"""
实例化扩展
"""

from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment

bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = '请登录以访问该页面'
login_manager.login_message_category = 'warning'
moment = Moment()
