# -*- coding: utf-8 -*-
"""
用户认证视图
"""

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user

from . import auth
from ..models import User, UserType, Subject, Problem
from ..extensions import db


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        # 判断同名用户是否存在
        if User.query.filter_by(name=name).first() is not None:
            flash('用户名称已存在', 'warning')
            return redirect(url_for('auth.register'))
        # 创建用户
        user = User(name=name, password=password,
                    usertype=UserType.query.filter_by(name='student').first())
        db.session.add(user)
        db.session.commit()
        flash('注册成功！你现在可以登录了', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')


@auth.route('/teaher-register/', methods=['GET', 'POST'])
def teacher_register():
    """老师版注册"""
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        subject = Subject.query.get(int(request.form.get('subject')))
        # 判断同名用户是否存在
        if User.query.filter_by(name=name).first() is not None:
            flash('用户名称已存在', 'warning')
            return redirect(url_for('auth.register'))
        # 创建用户
        user = User(name=name, password=password, usertype=UserType.query.filter_by(
            name='teacher').first(), subject=subject)
        db.session.add(user)
        db.session.commit()
        flash('注册成功！你现在可以去登录了', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/teacher-register.html', subjects=Subject.query.all())


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'POST':
        name = request.form.get('name')
        password = request.form.get('password')
        remember = request.form.get('rememberMe')
        if remember == 'on':
            remember = True
        else:
            remember = False
        # 获取用户
        user = User.query.filter_by(name=name).first()
        # 检测用户是否存在及密码是否正确
        if user is not None and user.verify_password(password):
            # 如果是，登录用户
            login_user(user, remember=remember)
            flash('登录成功！', 'success')
            # 获取下一步到达的URL
            next_ = request.args.get('next')
            if next_ is not None:
                return redirect(next_)
            return redirect(url_for('main.index'))
        # 否则拒绝登录
        flash('用户名或密码错误', 'warning')
        return redirect(url_for('auth.login'))
    return render_template('auth/login.html')


@auth.route('/logout/')
@login_required
def logout():
    """登出用户"""
    logout_user()
    flash('你已登出', 'success')
    return redirect(url_for('main.index'))
