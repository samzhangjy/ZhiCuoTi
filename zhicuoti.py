# -*- coding: utf-8 -*-
"""
应用主程序
"""

import os
import sys

import click
from flask_migrate import upgrade

from app import create_app
from app.models import *

# coverage配置
COV = None
if os.environ.get('FLASK_COVERAGE'):
    import coverage
    COV = coverage.coverage(branch=True, include='app/*')
    COV.start()

app = create_app('production')  # 使用工厂包创建应用


@app.shell_context_processor
def shell_context_processor():
    """Shell上下文处理"""
    return dict(db=db, User=User, UserType=UserType, Class=Class, ClassManager=ClassManager, Problem=Problem, Subject=Subject, Tag=Tag, TagManager=TagManager)

@app.cli.command()
def deploy():
    """部署智错题"""
    upgrade()
    UserType.insert_usertypes()
    Subject.insert_subjects()


@app.cli.command()
@click.option('--coverage/--no-coverage', default=False, help='在运行单元测试时运行覆盖度测试')
def test(coverage):
    """运行单元测试"""
    if coverage and not os.environ.get('FLASK_COVERAGE'):
        os.environ['FLASK_COVERAGE'] = '1'
        os.execvp(sys.executable, [sys.executable] + sys.argv)
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    if COV:
        COV.start()
        COV.save()
        print('覆盖度结果：')
        COV.report()
        basedir = os.path.abspath(os.path.dirname(__file__))
        covdir = os.path.join(basedir, 'coverage')
        COV.html_report(directory=covdir)
        print('HTML版：file://%s/index.html' % covdir)
        COV.erase()

if __name__ == '__main__':
    app.run()
