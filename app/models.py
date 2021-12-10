from datetime import date
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    songs = db.relationship('Song', backref='listener', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    artist = db.Column(db.String(140))
    link = db.Column(db.String(140))
    energy = db.Column(db.Integer)
    valence = db.Column(db.Integer)
    date = db.Column(db.DateTime, index=True, default=date.today)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
        
    def get_date(self):
        v = self.date.strftime("%b-%d-%Y")
        return v
    def __repr__(self):
        sep = '------------------'
        #  s = 'Date: ' + self.date.strftime("%/b-%/d-%Y") + sep + '\n'
        s = 'Song name: ' + str(self.name) + '\n' + sep + '\n'
        s += 'Song artist: ' + str(self.artist) + '\n'
        s += 'Spotify link: ' + str(self.link) + '\n' + sep + '\n'
        s += 'Energy: ' + str(self.energy) + '\n' + sep + '\n' 
        s += 'Valence: ' + str(self.valence) + '\n' + sep + '\n' 
        return s