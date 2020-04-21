# 智错题

智错题是一款在线错题本，目的是让错题管理更简单，更方便。它使用[Python3](https://www.python.org)编写，使用Python的轻量级web框架[Flask](https://flask.palletsprojects.com)作为框架，用[MySQL](https://www.mysql.com/)作为数据库。

## 在线演示

在线演示地址：[zhicuoti.herokuapp.com](https://zhicuoti.herokuapp.com)。

注：由于服务器原因，在线演示地址暂不支持图片上传功能，如需体验完整功能请在本地部署，敬请谅解！

## 部署

要部署智错题，首先要安装[Python3.x](https://www.python.org/downloads/)，Python包管理器[pip](https://pip.pypa.io/en/stable/installing/)（若是从python.org安装的Python，一般会自带），和[MySQL](https://dev.mysql.com/downloads/mysql/8.0.html)。有了这些依赖后，就可以执行下面这些步骤了。注：下列命令请都在终端内执行，并提前切换到源代码目录下。

1. 创建虚拟环境：

   首先，输入下面的命令以创建虚拟环境（请先切换到源代码目录）：

   ```bash
   pip3 install virtualenv
   virtualenv venv -p 3
   ```

2. 从`requirements.txt`中安装依赖：

   ```bash
   pip install -r requirements.txt
   ```

3. 创建MySQL数据库：

   要创建MySQL数据库，首先打开mysql终端，输入下面的命令：

   ```sql
   CREATE DATABASE zhicuoti;
   ```

   如果一切顺利的话，会输出以下结果：

   ```sql
   Query OK, 1 row affected (0.00 sec)
   ```

4. 定制.env：
   智错题需要知道一些数据库信息才能存储数据。更改根目录下的.env文件，追加如下内容：

   ```text/plain
   DATABASE_NAME=<数据库名称>
   DATABASE_PASSWORD=<数据库密码>
   DATABASE_USERNAME=<数据库用户名，默认为root>
   DATABASE_PORT=<数据库端口，默认为3306>
   ```

   注：将上面的<数据库名称>，<数据库密码>，<数据库用户名，默认为root>，<数据库端口，默认为3306>替换为真实信息，其中后两个为可选项。

5. 运行智错题部署命令：

   智错题部署命令将自动执行绝大多数智错题除1，2，3，4项的所有依赖。在终端中运行下面的命令：

   ```bash
   flask deploy
   ```

6. 运行程序：

   要运行智错题，在终端输入下面的命令：

   ```bash
   gunicorn zhicuoti:app
   ```

   这将在电脑的8000端口上监听访问，您可以到[127.0.0.1:8000](127.0.0.1:8000)来访问智错题。

7. 运行单元测试（可选）：

   如果要运行单元测试，可以执行下面的命令：

   ```bash
   flask test
   ```
