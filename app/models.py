# -*- coding: utf-8 -*-
"""
智错题数据库模型
"""

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from .extensions import db, login_manager


class UserType(db.Model):
    """定义用户类型
    :param id: 用户类型编号，为首键 -> int
    :param name: 用户类型名称 -> str
    :param users: 此类型的所有用户，一般不传参 -> AppenderBaseQuery
    """
    __tablename__ = 'usertypes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    users = db.relationship('User', backref='usertype', lazy='dynamic')

    @staticmethod
    def insert_usertypes(usertypes=['student', 'teacher']):
        """加入用户类型
        :param usertypes: 要加入的用户类型名称 -> list[str]
        """
        for usertype in usertypes:
            if UserType.query.filter_by(name=usertype).first() is None:
                usertype = UserType(name=usertype)
                db.session.add(usertype)
        db.session.commit()

    def __repr__(self):
        return '<UserType %s>' % self.name


# 班级管理器，用来建立用户与班级的多对多关联
ClassManager = db.Table(
    'ClassManager',
    db.Column('user_id',
              db.Integer,
              db.ForeignKey('users.id'),
              primary_key=True),
    db.Column('class_id',
              db.Integer,
              db.ForeignKey('classes.id'),
              primary_key=True),
)


# 标签管理器，用来建立错题与标签的多对多关联
TagManager = db.Table(
    'TagManager',
    db.Column('problem_id',
              db.Integer,
              db.ForeignKey('problems.id'),
              primary_key=True),
    db.Column('tag_id',
              db.Integer,
              db.ForeignKey('tags.id'),
              primary_key=True),
)


class User(db.Model, UserMixin):
    """用户模型
    :param id: 用户编号，为首键 -> int
    :param name: 用户名称 -> str
    :param usertype_id: 用户类型编号 -> int
    :param usertype: 用户类型 -> UserType
    :param classes: 用户加入的班级 -> list[Class]
    :param problems: 用户的错题 -> AppenderBaseQuery
    :param tags: 用户的标签 -> AppenderBaseQuery
    :param subject_id: 若当前用户为教师，则为用户所教授的学科编号 -> int
    :param subject: 若当前用户为教师，则为用户所教授的学科 -> Subject
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    usertype_id = db.Column(db.Integer, db.ForeignKey('usertypes.id'))
    password_hash = db.Column(db.String(128))
    problems = db.relationship('Problem', backref='author', lazy='dynamic')
    tags = db.relationship('Tag', backref='owner', lazy='dynamic')
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))

    @property
    def password(self):
        """防止读取密码"""
        raise AttributeError('密码不可读')

    @password.setter
    def password(self, password):
        """将用户密码转换为哈希散列值
        :param password: 要转换的密码 -> str
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """验证密码是否正确
        :param password: 要验证的密码 -> str
        :return: 密码是否正确 -> bool
        """
        return check_password_hash(self.password_hash, password)

    def is_teacher(self):
        """判断是否为老师
        :return: 当前用户是否为老师 -> bool
        """
        return self.usertype == UserType.query.filter_by(name='teacher').first()

    def __repr__(self):
        return '<User %s>' % self.name


class Class(db.Model):
    """班级模型
    :param id: 班级编号，为首键 -> int
    :param name: 班级名称 -> str
    :param users: 班级内所有成员，含老师和学生 -> list[User]
    :param join_code: 班级加入码 -> str
    """
    __tablename__ = 'classes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    users = db.relationship('User',
                            secondary='ClassManager',
                            backref='classes', lazy='dynamic')
    join_code = db.Column(db.String(64))

    def join_user(self, user):
        """加入成员
        :param user: 要加入的成员 -> User
        """
        self.users.append(user)
        db.session.add(self)
        db.session.commit()

    def remove_user(self, user):
        """移除成员
        :param user: 要移除的成员 -> User
        """
        self.users.remove(user)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Class %s>' % self.name


class Subject(db.Model):
    """科目模型
    :param id: 科目编号，为首键 -> int
    :param name: 科目名称 -> str
    :param problems: 科目下所有错题 -> AppenderBaseQuery
    :param teachers: 科目下所有老师 -> AppenderBaseQuery
    :param tags: 科目下所有标签 -> AppenderBaseQuery
    """
    __tablename__ = 'subjects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    problems = db.relationship('Problem', backref='subject', lazy='dynamic')
    teachers = db.relationship('User', backref='subject', lazy='dynamic')
    tags = db.relationship('Tag', backref='subject', lazy='dynamic')

    @staticmethod
    def insert_subjects(subjects=['语文', '数学', '英语', '科学', '地理', '历史', '政治', '化学', '物理', '音乐', '美术', '体育', '品社', '综合', '其他']):
        """加入默认科目
        :param subjects: 要加入的学科名称 -> list[str]
        """
        for subject in subjects:
            if Subject.query.filter_by(name=subject).first() is None:
                subject = Subject(name=subject)
                db.session.add(subject)
        db.session.commit()

    def __repr__(self):
        return '<Subject %s>' % self.name


class Tag(db.Model):
    """标签模型
    :param id: 标签编号，为首键 -> int
    :param name: 标签名称 -> str
    :param problems: 标签下的所有错题 -> list[Problem]
    :param owner_id: 所有者编号 -> int
    :param owner: 所有者 -> User
    :param subject_id: 标签下错题科目的编号 -> int
    :param subject: 标签下错题科目 -> list[Subject]
    """
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    problems = db.relationship(
        'Problem', secondary='TagManager', backref='tags', lazy='dynamic')
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))

    def add_problem(self, problem):
        """在此标签下加入新的错题
        :param problem: 要加入的错题 -> Problem
        """
        self.problems.append(problem)
        db.session.add(self)
        db.session.commit()

    def remove_problem(self, problem):
        """在此标签下移除一个错题
        :param problem: 要移除的错题 -> Problem
        """
        self.problems.remove(problem)
        db.session.add(self)
        db.session.commit()

    def find_problem(self, problem):
        """在此标签内寻找错题，没有则返回None
        :param problem: 要寻找的错题 -> Problem
        """
        try:
            return self.problems.all().index(problem)
        except ValueError:
            return None

    def __repr__(self):
        return '<Tag %s>' % self.name


class Problem(db.Model):
    """错题模型
    :param id: 错题编号，为首键 -> int
    :param body: 错题题目 -> str
    :param original_answer: 错题原答案 -> str
    :param correct_answer: 错题正确答案 -> str
    :param description: 错题解析 -> str
    :param author_id: 错题所有者编号 -> int
    :param author: 错题所有者 -> User
    :param tags: 错题的所有标签 -> AppenderBaseQuery
    :param timestamp: 错题加入的时间 -> datetime
    :param body_is_image: 错题题目是否为图片 -> bool
    :param original_answer_is_image: 错题原答案是否为图片 -> bool
    :param correct_answer_is_image: 错题正确答案是否为图片 -> bool
    :param description_is_image: 错题解析是否为图片 -> bool
    :param title: 错题小标题 -> str
    """
    __tablename__ = 'problems'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    original_answer = db.Column(db.Text)
    correct_answer = db.Column(db.Text)
    description = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    body_is_image = db.Column(db.Boolean, default=False)
    original_answer_is_image = db.Column(db.Boolean, default=False)
    correct_answer_is_image = db.Column(db.Boolean, default=False)
    description_is_image = db.Column(db.Boolean, default=False)
    title = db.Column(db.Text)

    def __repr__(self):
        return '<Problem %d>' % self.id


@login_manager.user_loader
def load_user(user_id):
    """从数据库中加载用户
    :param user_id: 用户编号 -> int
    :return: 查找到的用户 -> User, None
    """
    return User.query.get(user_id)
