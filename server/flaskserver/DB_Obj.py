# probelma import circolari
from flaskserver import db
from datetime import datetime
from flaskserver import login_manager
from flask_login import UserMixin
from flask import current_app
import numpy as np
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    user = Doctor.query.filter_by(email=user_id).first()
    t = 'Doctor'
    if user is None:
        user = User.query.filter_by(email=user_id).first()
        t = 'User'

    print('Logging in as a', t)
    return user


class MyUser(UserMixin):  # uso per customizzare il passaggio di parametri alla funzione login user senza warning
    def __init__(self, id):
        self.id = id


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False,
                        index=True)  # solo un ruolo a true che è quello di default se non specificato
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='Role', lazy='dynamic')


class Permission:
    ADMIN = 511
    NEW_POST = 1
    VIEW_POST = 2
    UPDATE_POST = 4
    DELETE_POST = 8
    SIGN_UP = 16
    USER_POST = 32
    RESET_PASSWORD = 64
    COMMENT_POST = 128
    roles = {
        'Doctor': (
            NEW_POST + COMMENT_POST + VIEW_POST + DELETE_POST + UPDATE_POST + RESET_PASSWORD + SIGN_UP + USER_POST,
            False),
        'User': (
            COMMENT_POST + RESET_PASSWORD + SIGN_UP + USER_POST, True),
        'Admin': (ADMIN, False),
    }


class UserData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, server_default=db.func.now())
    gps_lat = db.Column(db.String(10), nullable=False)
    gps_long = db.Column(db.String(10), nullable=False)
    temp = db.Column(db.Float, nullable=False)
    BPM = db.Column(db.Integer, nullable=False)
    sat = db.Column(db.Integer, nullable=False)
    health = db.Column(db.Integer, default=0)


class User(db.Model, UserMixin):  # double inheritance
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    cognome = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(6), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    birthplace = db.Column(db.String(40), nullable=False)
    indirizzo = db.Column(db.String(40), nullable=False)
    cf = db.Column(db.String(16), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('roles.name'), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)  # fa una query in background e ottiene tutti i post
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Admin').first().permissions
            if self.role is None:
                self.role = Role.query.filter_by(name='User').first().permissions

    def can(self, permissions):

        return self.role & permissions == permissions

    def is_admin(self):
        return self.can(Permission.ADMIN)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def to_list(self):
        a = ['nome', 'cognome', 'username', 'birthplace', 'email', 'birthdate', 'indirizzo', 'role', 'sex', 'cf']
        return a

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # che hanno fatto gli utenti con lazy =true ottiene tutti i dati con un colpo solo
    # utlizzo di itsdagenrous per i token di 30 secondi
    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.image_file}')"


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # table name è user minuscolo
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    comments = db.relationship('Comment', backref='reference', lazy=True)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(150), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))


class Doctor(db.Model, UserMixin):  # double inheritance
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True)
    cognome = db.Column(db.String(50), nullable=False)
    nome = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(6), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    birthplace = db.Column(db.String(40), nullable=False)
    indirizzo = db.Column(db.String(40), nullable=False)
    cf = db.Column(db.String(16), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('roles.name'), nullable=False)
    posts = db.relationship('Post', backref='doctor', lazy=True)  # fa una query in background e ottiene tutti i post
    users = db.relationship('User', backref='medic', lazy=True)
    def __init__(self, **kwargs):
        super(Doctor, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Admin').first().permissions
            if self.role is None:
                self.role = Role.query.filter_by(name='Doctor').first().permissions

    def can(self, permissions):

        return self.role & permissions == permissions

    def is_admin(self):
        return self.can(Permission.ADMIN)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    def to_list(self):
        a = ['nome', 'cognome', 'username', 'birthplace', 'email', 'birthdate', 'indirizzo', 'role', 'sex', 'cf']
        return a

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    # che hanno fatto gli utenti con lazy =true ottiene tutti i dati con un colpo solo
    # utlizzo di itsdagenrous per i token di 30 secondi
    def __repr__(self):
        return f"User('{self.username}', '{self.email}','{self.image_file}')"
