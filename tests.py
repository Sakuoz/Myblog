#!flask/Scripts/python
import os
import unittest

from config import basedir
from app import app, db
from app.models import User

class TestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_avatar(self):
        u = User(nickname = 'Sakura', email = 'Sakura@example.com')
        avatar = u.avatar(128)
        expected = 'http://www.gravatar.com/avatar/689e2c062cb986c5d29ce13e416321c1?d=mm&s=128'
        assert avatar[0:len(expected)] == expected

    def test_make_unique_nickname(self):
        u = User(nickname = 'Sakura', email = 'Sakura@example.com')
        db.session.add(u)
        db.session.commit()
        nickname = User.make_unique_nickname('Sakura')
        assert nickname != 'Sakura'
        u = User(nickname = nickname, email = 'Asuna@example.com')
        db.session.add(u)
        db.session.commit()
        nicakname2 = User.make_unique_nickname('Sakura')
        assert nicakname2 != 'Sakura'
        assert nicakname2 != nickname

    def test_follow(self):
        u1 = User(nickname = 'Sakura', email = 'Sakura@example.com')
        u2 = User(nickname = 'Asuna', email = 'Sakura@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        assert u1.unfollow(u2) == None
        u = u1.follow(u2)
        db.session.add(u)
        db.session.commit()
        assert u1.follow(u2) == None
        assert u1.is_following(u2)
        assert u1.followed.count() == 1
        assert u1.followed.first().nickname == 'Asuna'
        assert u2.followers.count() == 1
        assert u2.followers.first().nickname == 'Sakura'
        u = u1.unfollow(u2)
        assert u != None
        db.session.add(u)
        db.session.commit()
        assert u1.is_following(u2) == False
        assert u1.followed.count() == 0
        assert u2.followers.count() == 0

if __name__ == '__main__':
    unittest.main()
