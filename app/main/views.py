# -*- coding: utf-8 -*-
"""
应用主视图
"""

import os
from uuid import uuid1
from datetime import datetime

from flask import abort, flash, redirect, render_template, request, url_for, current_app
from flask_login import current_user, login_required

from ..decorators import student_required, teacher_required
from ..extensions import db
from ..models import Class, Problem, Subject, Tag, User, UserType
from ..utils import allowed_file
from . import main


@main.route('/')
def index():
    """应用首页"""
    return render_template('main/index.html')


@main.route('/problems/')
@login_required
@student_required
def problems():
    """查看当前用户的所有错题"""
    # 获取所有错题
    all_problems = current_user.problems.all()
    return render_template('main/problems.html', problems=all_problems)


@main.route('/problems/<int:id>/')
@login_required
@student_required
def problem(id):
    """查看当前用户的指定错题"""
    # 获取错题
    problem = current_user.problems.filter_by(id=id).first()
    if problem is None:
        abort(404)
    return render_template('main/problem.html', problem=problem)


@main.route('/problems/add/', methods=['GET', 'POST'])
@login_required
@student_required
def add_problem():
    """添加错题"""
    if request.method == 'POST':
        body = request.form.get('body-text')
        original_answer = request.form.get('original-answer-text')
        correct_answer = request.form.get('correct-answer-text')
        description = request.form.get('description-text')
        subject = request.form.get('subject')
        title = request.form.get('title')
        date = request.form.get('date')
        date = str(date).split('/')
        date = datetime(int(date[0]), int(date[1]), int(date[2]))
        tags = str(request.form.get('tags')).split('，')
        subject = Subject.query.get(int(subject))
        things = ['body', 'original-answer', 'correct-answer', 'description']
        is_image = [False, False, False, False]
        text = [body, original_answer, correct_answer, description]
        i = 0
        for thing in things:
            if request.form.get('%s-is-image' % thing) == 'True':
                photos = request.files.getlist('%s-image' % thing)
                for photo in photos:
                    if allowed_file(photo.filename):
                        filename = str(uuid1()) + '.' + \
                            photo.filename.rsplit('.', 1)[1]
                        photo.save(os.path.join(
                            current_app.config['UPLOADS_FOLDER'], filename))
                        is_image[i] = True
                        if text[i] is None:
                            text[i] = filename
                        else:
                            text[i] += (',' + filename)
                    else:
                        flash('请上传图片', 'warning')
                        return redirect(url_for('main.add_problem'))
            i += 1
        # 创建错题
        problem_ = Problem(body=text[0].replace('\r\n', '<br>'), original_answer=text[1].replace('\r\n', '<br>'),
                           correct_answer=text[2].replace('\r\n', '<br>'), description=text[3].replace('\r\n', '<br>'),
                           author=current_user, subject=subject, body_is_image=is_image[0],
                           original_answer_is_image=is_image[1], correct_answer_is_image=is_image[2],
                           description_is_image=is_image[3], title=title, timestamp=date)
        db.session.add(problem_)
        db.session.commit()
        # 添加没有的标签
        for tag in tags:
            if tag != '' and not current_user.tags.filter_by(name=tag).first():
                tag = Tag(name=tag, owner=current_user, subject=subject)
                db.session.add(tag)
            elif current_user.tags.filter_by(name=tag).first() and current_user.tags.filter_by(name=tag).first().subject != subject and (not current_user.tags.filter_by(subject=subject).first()):
                tag = Tag(name=tag, owner=current_user, subject=subject)
                db.session.add(tag)
            else:
                tags_ = Tag.query.filter_by(name=tag).all()
                for tag_ in tags_:
                    if tag_.subject == subject:
                        tag = tag_
                        break
            try:
                tag.add_problem(problem_)
            except AttributeError:
                tag = Tag(name=tag, owner=current_user, subject=subject)
                tag.add_problem(problem_)
        db.session.commit()
        flash('错题添加成功', 'success')
        return redirect(url_for('main.problems'))
    return render_template('main/add-problem.html', subjects=Subject.query.all())


@main.route('/problems/delete/<int:id>/')
@login_required
@student_required
def delete_problem(id):
    problem = Problem.query.get_or_404(id)
    for tag in problem.tags:
        tag.remove_problem(problem)
        if tag.problems.all() == []:
            db.session.delete(tag)
    if problem.body_is_image:
        for img in problem.body.split(','):
            if img != '':
                os.remove(os.path.abspath(os.path.join(current_app.config['UPLOADS_FOLDER'], img)))
    if problem.original_answer_is_image:
        for img in problem.original_answer.split(','):
            if img != '':
                os.remove(os.path.abspath(os.path.join(current_app.config['UPLOADS_FOLDER'], img)))
    if problem.correct_answer_is_image:
        for img in problem.correct_answer.split(','):
            if img !='':
                os.remove(os.path.abspath(os.path.join(current_app.config['UPLOADS_FOLDER'], img)))
    if problem.description_is_image:
        for img in problem.description.split(','):
            if img is not None:
                os.remove(os.path.abspath(os.path.join(current_app.config['UPLOADS_FOLDER'], img)))
    db.session.delete(problem)
    db.session.commit()
    flash('错题已删除', 'success')
    return redirect(url_for('main.problems'))


@main.route('/tags/')
@login_required
@student_required
def tags():
    """查看所有标签"""
    # 获取当前用户的所有标签
    tags = current_user.tags.all()
    return render_template('main/tags.html', tags=tags)


@main.route('/tags/<id>/')
@login_required
@student_required
def tag(id):
    """查看标签"""
    # 获取标签
    tag = current_user.tags.filter_by(id=id).first()
    # 确认标签是否为空
    if tag is None:
        abort(404)
    return render_template('main/tag.html', tag=tag, problems=tag.problems.all())


@main.route('/statistics/')
@login_required
@student_required
def statistics():
    """统计错题"""
    # 获取所有标签和错题
    tags = current_user.tags.all()
    problems = current_user.problems.all()
    return render_template('main/statistics.html', tags=tags, problems=problems)


@main.route('/class/add/', methods=['GET', 'POST'])
@login_required
@teacher_required
def add_class():
    """添加班级"""
    if request.method == 'POST':
        name = request.form.get('name')
        join_code = ''.join(str(uuid1()).split('-'))[:4]
        class_ = Class(name=name, join_code=join_code)
        db.session.add(class_)
        db.session.commit()
        class_.join_user(current_user)
        flash('班级添加成功！', 'success')
        return redirect(url_for('main.code_class', name=name))
    subjects = Subject.query.all()
    return render_template('main/add-class.html', subjects=subjects)


@main.route('/class/<name>/code/')
@login_required
@teacher_required
def code_class(name):
    """查看班级码"""
    class_ = Class.query.filter_by(name=name).first()
    if class_ is None:
        abort(404)
    if current_user not in class_.users:
        abort(403)
    return render_template('main/code-class.html', class_=class_)


@main.route('/class/join/', methods=['GET', 'POST'])
@login_required
def join_class():
    """加入班级"""
    if request.method == 'POST':
        name = request.form.get('name')
        code = str(request.form.get('code'))
        class_ = Class.query.filter_by(name=name).first()
        if class_ is None:
            flash('班级不存在', 'error')
            return redirect(url_for('main.join_class'))
        if current_user in class_.users.all():
            flash('您已经了加入此班级', 'warning')
            return redirect(url_for('main.join_class'))
        if code == class_.join_code:
            class_.join_user(current_user)
            flash('加入班级成功', 'success')
            return redirect(url_for('main.index'))
        flash('班级码不正确', 'warning')
        return redirect(url_for('main.join_class'))
    return render_template('main/join-class.html')


@main.route('/class/<name>/')
@login_required
def view_class(name):
    """查看班级"""
    class_ = Class.query.filter_by(name=name).first()
    if class_ is None:
        abort(404)
    if current_user not in class_.users.all():
        abort(403)
    teachers = class_.users.filter_by(
        usertype=UserType.query.filter_by(name='teacher').first()).all()
    students = class_.users.filter_by(
        usertype=UserType.query.filter_by(name='student').first()).all()
    tagall = {}
    problems = 0
    for stu in class_.users.filter_by(usertype=UserType.query.filter_by(name='student').first()).all():
        for tag in stu.tags.all():
            if tag.subject == current_user.subject:
                problems += 1
                name = "%s（%s）" % (tag.name, tag.subject.name)
                try:
                    value = tagall[name] + len(tag.problems.all())
                except KeyError:
                    tagall[name] = len(tag.problems.all())
    return render_template('main/view-class.html', class_=class_, teachers=teachers, students=students, tags=tagall, problems=problems)


@main.route('/class/<name>/manage/')
@login_required
@teacher_required
def manage_class(name):
    """管理班级"""
    class_ = Class.query.filter_by(name=name).first()
    if class_ is None:
        abort(404)
    if current_user not in class_.users.all():
        abort(403)
    teachers = class_.users.filter_by(
        usertype=UserType.query.filter_by(name='teacher').first()).all()
    students = class_.users.filter_by(
        usertype=UserType.query.filter_by(name='student').first()).all()
    return render_template('main/manage-class.html', class_=class_, teachers=teachers, students=students)


@main.route('/class/<name>/remove/<id>/')
@login_required
@teacher_required
def remove_user_from_class(name, id):
    """从班级中移除用户"""
    class_ = Class.query.filter_by(name=name).first()
    user = User.query.get_or_404(id)
    if class_ is None:
        abort(404)
    if current_user not in class_.users.all():
        abort(403)
    class_.remove_user(user)
    flash('移除成员成功', 'success')
    return redirect(url_for('main.manage_class', name=name))


@main.route('/class/<name>/change-name/', methods=['GET', 'POST'])
@login_required
@teacher_required
def change_class_name(name):
    """更改班级名称"""
    class_ = Class.query.filter_by(name=name).first()
    if class_ is None:
        abort(404)
    if current_user not in class_.users.all():
        abort(403)
    if request.method == 'POST':
        new_name = request.form.get('new-name')
        class_.name = new_name
        db.session.add(class_)
        db.session.commit()
        flash('更改名称成功', 'success')
        return redirect(url_for('main.manage_class', name=new_name))
    return render_template('main/change-class-name.html', class_=class_)


@main.route('/class/<name>/student/<id>/')
@login_required
@teacher_required
def view_student_problems(name, id):
    """查看本班指定学生的错题"""
    class_ = Class.query.filter_by(name=name).first()
    if class_ is None:
        abort(404)
    if current_user not in class_.users.all():
        abort(403)
    user = User.query.get_or_404(id)
    problems = user.problems.filter_by(subject=current_user.subject).all()
    return render_template('main/view-student-problems.html', problems=problems, user=user, class_=class_)


@main.route('/class/<name>/student/<id>/<problem>/')
@login_required
@teacher_required
def view_student_problem(name, id, problem):
    """查看本班指定学生的指定错题"""
    class_ = Class.query.filter_by(name=name).first()
    if class_ is None:
        abort(404)
    if current_user not in class_.users.all():
        abort(403)
    user = User.query.get_or_404(id)
    problem = Problem.query.get_or_404(problem)
    return render_template('main/view-student-problem.html', problem=problem, user=user, class_=class_)


@main.route('/class/<name>/student/<id>/tags/')
@login_required
@teacher_required
def view_student_tags(name, id):
    """查看本班指定学生的标签"""
    class_ = Class.query.filter_by(name=name).first()
    if class_ is None:
        abort(404)
    if current_user not in class_.users.all():
        abort(403)
    user = User.query.get_or_404(id)
    tags = user.tags.all()
    return render_template('main/view-student-tags.html', user=user, tags=tags, class_=class_)


@main.route('/class/<name>/student/<id>/tags/<tag>/')
@login_required
@teacher_required
def view_student_tag(name, id, tag):
    """查看本班指定学生的指定标签"""
    class_ = Class.query.filter_by(name=name).first()
    if class_ is None:
        abort(404)
    if current_user not in class_.users.all():
        abort(403)
    user = User.query.get_or_404(id)
    tag = user.tags.filter_by(id=tag).first()
    return render_template('main/view-student-tag.html', user=user, tag=tag, class_=class_, problems=tag.problems.all())


@main.route('/class/<name>/student/<id>/statistics/')
@login_required
@teacher_required
def view_student_statistics(name, id):
    """统计班内指定同学的错题"""
    class_ = Class.query.filter_by(name=name).first()
    if class_ is None:
        abort(404)
    if current_user not in class_.users.all():
        abort(403)
    user = User.query.get_or_404(id)
    tags = user.tags.filter_by(subject=current_user.subject).all()
    problems = user.problems.filter_by(subject=current_user.subject).all()
    return render_template('main/view-student-statistics.html', user=user, tags=tags, problems=problems)


@main.route('/uploads/<filename>')
def uploads_url(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
