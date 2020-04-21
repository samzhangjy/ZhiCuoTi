# -*- coding: utf-8 -*-
"""
数据库测试
"""

import unittest
from datetime import datetime
from flask import current_app
from app import create_app, db

from app.models import User, UserType, Problem, Tag, Subject, Class


class DatabaseTestCase(unittest.TestCase):
    """数据库测试"""

    def setUp(self):
        """建立测试环境"""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        UserType.insert_usertypes()
        Subject.insert_subjects()
    
    def tearDown(self):
        """删除测试环境"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_user_password_hash(self):
        """测试用户的密码哈希值"""
        u = User(password='123')
        self.assertTrue(u.password_hash is not None)
    
    def test_user_password_cannot_be_got(self):
        """测试用户的密码无法被获得"""
        u = User(password='123')
        with self.assertRaises(AttributeError):
            u.password
    
    def test_user_password_verify(self):
        """测试用户的密码验证功能"""
        u = User(password='123')
        self.assertTrue(u.verify_password('123'))
        self.assertFalse(u.verify_password('456'))
    
    def test_user_usertype(self):
        """测试用户的用户类型"""
        u = User(usertype=UserType.query.filter_by(name='student').first())
        self.assertTrue(u.usertype == UserType.query.filter_by(name='student').first())
    
    def test_user_is_teacher(self):
        """测试用户是否为老师的功能（User.is_teacher）"""
        u = User(usertype=UserType.query.filter_by(name='student').first())
        self.assertFalse(u.is_teacher())
        u = User(usertype=UserType.query.filter_by(name='teacher').first())
        self.assertTrue(u.is_teacher())
    
    def test_user_add_problem(self):
        """测试用户的添加错题功能"""
        u = User()
        p = Problem(author=u)
        self.assertIn(p, u.problems.all())
    
    def test_user_add_problem_with_subject(self):
        """测试用户的添加错题功能（带科目）"""
        u = User()
        p = Problem(author=u, subject=Subject.query.first())
        self.assertEqual(Subject.query.first(), p.subject)
    
    def test_user_add_problem_with_tag(self):
        """测试用户的添加错题功能（带标签）"""
        u = User()
        p = Problem(author=u)
        t = Tag(owner=u)
        t.add_problem(p)
        self.assertIn(p, t.problems.all())
    
    def test_user_add_problem_with_tag_but_deleted(self):
        """测试用户的添加错题功能（带标签，但错题在标签加入后被移除了）"""
        u = User()
        p = Problem(author=u)
        t = Tag(owner=u)
        t.add_problem(p)
        t.remove_problem(p)
        self.assertNotIn(p, t.problems.all())
    
    def test_user_find_problem_with_tag(self):
        """测试用户根据标签寻找错题的功能"""
        u = User()
        p = Problem(author=u)
        t = Tag(owner=u)
        t.add_problem(p)
        self.assertEqual(0, t.find_problem(p))
        t.remove_problem(p)
        self.assertIsNone(t.find_problem(p))
    
    def test_user_add_tag(self):
        """测试用户的添加标签功能"""
        u = User()
        t = Tag(owner=u)
        self.assertIn(t, u.tags.all())
    
    def test_user_join_class(self):
        """测试用户加入班级的功能"""
        u = User()
        c = Class()
        c.join_user(u)
        self.assertIn(u, c.users.all())
    
    def test_user_remove_class(self):
        """测试用户被移除班级的功能"""
        u = User()
        c = Class()
        c.join_user(u)
        c.remove_user(u)
        self.assertNotIn(u, c.users.all())
    
    def test_user_classes(self):
        """测试用户是否在班级内（通过User.classes）"""
        u = User()
        c = Class()
        c.join_user(u)
        self.assertIn(c, u.classes)
    
    def test_problem_timestamp(self):
        """测试错题的时间截"""
        u = User()
        p = Problem(author=u)
        db.session.add(p)
        db.session.commit()
        self.assertTrue((datetime.utcnow() - p.timestamp).total_seconds() < 3)
    
    def test_tag_owner(self):
        """测试标签的所有者是否正确"""
        u = User()
        t = Tag(owner=u)
        db.session.add(t)
        db.session.commit()
        self.assertTrue(t.owner == u)
        fake_u = User()
        self.assertFalse(t.owner == fake_u)
