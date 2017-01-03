CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-gusess'

OPENID_PROVIDERS = [
    { 'name': 'Baidu', 'url': 'https://www.baidu.com' },
    { 'name': 'MyOpenID', 'url': 'http://sakuoz.openid.org.cn/' }
]

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')    # 数据库路径
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')       # 存储数据文件的文件夹
