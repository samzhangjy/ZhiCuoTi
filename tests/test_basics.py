# -*- coding: utf-8 -*-
"""
最基本的测试
"""

import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    """最基本的测试项目"""

    def setUp(self):
        """建立测试环境"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """删除测试环境"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_app_exists(self):
        """测试应用是否存在"""
        self.assertFalse(current_app is None)
    
    def test_app_is_testing(self):
        """测试应用是否在测试状态"""
        self.assertTrue(current_app.config['TESTING'])
    
    def test_app_is_tracking_modifactions(self):
        """测试应用是否在追踪数据库更改"""
        self.assertFalse(current_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'])
