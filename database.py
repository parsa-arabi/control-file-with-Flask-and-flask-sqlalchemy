from flask import *
import os
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///name.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

db = SQLAlchemy(app)

class user(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password = db.Column(db.Text)
    does = db.relationship('files', backref='author', lazy=True)
    def __repr__(self):
        return f'user({self.id}-{self.username}-{self.password})'
        # return f'user({self.username}-{self.password})'

class files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text)
    filename = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f'files({self.id}-{self.url}-{self.filename})'
        # return f'({self.name}-{self.filename})'


