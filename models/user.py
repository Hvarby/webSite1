from models import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    user_projects = db.relationship('UserProject', backref='user', lazy=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    subordinates = db.relationship('User', backref=db.backref('manager', remote_side='User.id'), lazy=True)
    logs = db.relationship('Log', backref='user', lazy=True)