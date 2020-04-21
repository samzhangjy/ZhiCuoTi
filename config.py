# -*- coding: utf-8 -*-
"""
应用配置文件
"""

import os


class BaseConfig(object):
    """配置基类"""
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL'
    ) or 'mysql+pymysql://%s:%s@localhost:%s/%s?charset=utf8mb4' % (
        os.environ.get('DATABASE_USERNAME') or 'root',
        os.environ.get('DATABASE_PASSWORD'), os.environ.get('DATABASE_PORT')
        or '3306', os.environ.get('DATABASE_NAME'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '0a4f4102-823b-11ea-9002-38f9d3e4f2a2'
    UPLOADS_FOLDER = os.path.abspath(os.path.dirname(__file__)) + '/app/static/uploads'
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


class DevelopmentConfig(BaseConfig):
    """开发配置"""
    DEBUG = True


class TestingConfig(BaseConfig):
    """测试配置"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or 'sqlite://'  # 测试环境默认使用内存中的sqlite数据库


class ProductionConfig(BaseConfig):
    """生产配置"""
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
