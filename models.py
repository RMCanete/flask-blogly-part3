
"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime

from sqlalchemy.orm import backref

db = SQLAlchemy()

DEFAULT_IMAGE = "https://www.freeiconspng.com/uploads/-mario-baseball-superstar-super-bros-png-26.png"
                    # July 2, 2021 - https://www.freeiconspng.com/img/49311 title="Image from freeiconspng.com"  img src="https://www.freeiconspng.com/uploads/-mario-baseball-superstar-super-bros-png-26.png"


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=True, default=DEFAULT_IMAGE)

    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan")


    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class Tag(db.Model):

    __tablename__ = 'tags'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='posts_tags', backref='tags')

class PostTag(db.Model):

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer,  db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer,  db.ForeignKey('tags.id'), primary_key=True)

def connect_db(app):
    db.app = app
    db.init_app(app)