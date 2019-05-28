from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True)
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, index=True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String)
    password_hash = db.Column(db.String(255))
    date_joined = db.Column(db.DateTime,default=datetime.utcnow)

    pitches_id = db.relationship('Pitch', backref='user', lazy="dynamic")

    comments = db.relationship('Comment', backref='user', lazy="dynamic")

    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'User {self.username}'


class Pitch(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key=True)
    pitch_title = db.Column(db.String)
    pitch_content = db.Column(db.String(1000))
    category = db.Column(db.String)
    posted = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Saving a pitch
    def save_pitch(self):
        db.session.add(self)
        db.session.commit()

    # getting pitches by category
    @classmethod
    def get_pitches(cls, category):
        pitched = Pitch.query.filter_by(category=category).all()

        return pitched

    # getting a single pitch by id
    @classmethod
    def get_pitch(cls, id):
        pitch = Pitch.query.filter_by(id=id).first()

        return pitch
    
    @classmethod
    def count_pitches(cls,uname):
        user = User.query.filter_by(username=uname).first()
        pitch_list = Pitch.query.filter_by(user_id=user.id).all()

        pitches_count = 0
        for pitch in pitches_list:
            pitches_count += 1

        return pitches_count


class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    pitch_id = db.Column(db.Integer, db.ForeignKey('pitches.id'))
    comment = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def save_commit(self):
        db.session.add(self)
        db.session.commit()

    # getting a comment
    @classmethod
    def get_comments(cls, id):
        comments = Comment.query.filter_by(pitch_id=id).all()

        return comments


class PhotoProfile(db.Model):
    __tablename__ = 'profile_photos'

    id = db.Column(db.Integer, primary_key=True)
    pic_path = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))