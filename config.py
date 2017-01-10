CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-gusess'

OPENID_PROVIDERS = [
    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
    { 'name': 'MyOpenID', 'url': 'http://sakuoz.openid.org.cn/' },
    { 'name': 'QQ', 'url': 'https://graph.z.qq.com/moc2/me' }
]

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')    # 数据库路径
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')       # 存储数据文件的文件夹

# mail server settings
MAIL_SERVER = 'localhost'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['951463382@qq.com']

# 分页-单页Blog显示数量
POSTS_PER_PAGE = 3
