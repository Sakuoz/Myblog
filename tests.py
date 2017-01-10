#!flask/Scripts/python
import os
import unittest

from config import basedir
from app import app, db
from datetime import datetime, timedelta
from app.models import User, Post

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

    def test_follow_posts(self):
        # make four users
        u1 = User(nickname = 'Sakura', email = 'Sakura@example.com')
        u2 = User(nickname = 'Asuna', email = 'Asuna@example.com')
        u3 = User(nickname = 'mary', email = 'mary@example.com')
        u4 = User(nickname = 'david', email = 'david@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        # make four posts
        utcnow = datetime.utcnow()
        p1 = Post(body = "post from Sakura", author = u1, timestamp = utcnow + timedelta(seconds = 1))
        p2 = Post(body = "post from Asuna", author = u2, timestamp = utcnow + timedelta(seconds = 2))
        p3 = Post(body = "post from mary", author = u3, timestamp = utcnow + timedelta(seconds = 3))
        p4 = Post(body = "post from david", author = u4, timestamp = utcnow + timedelta(seconds = 4))
        db.session.add(p1)
        db.session.add(p2)
        db.session.add(p3)
        db.session.add(p4)
        db.session.commit()
        # setup the followers
        u1.follow(u1) # Sakura follows himself
        u1.follow(u2) # Sakura follows Asuna
        u1.follow(u4) # Sakura follows david
        u2.follow(u2) # Asuna follows herself
        u2.follow(u3) # Asuna follows mary
        u3.follow(u3) # mary follows herself
        u3.follow(u4) # mary follows david
        u4.follow(u4) # david follows himself
        db.session.add(u1)
        db.session.add(u2)
        db.session.add(u3)
        db.session.add(u4)
        db.session.commit()
        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        assert len(f1) == 3
        assert len(f2) == 2
        assert len(f3) == 2
        assert len(f4) == 1
        assert f1 == [p4, p2, p1]
        assert f2 == [p3, p2]
        assert f3 == [p4, p3]
        assert f4 == [p4]

if __name__ == '__main__':
    unittest.main()
