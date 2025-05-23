from models import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    user_projects = db.relationship('UserProject', backref='project', lazy=True)