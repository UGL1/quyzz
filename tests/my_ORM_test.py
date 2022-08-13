# Here are all the ORM
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

from mcq_app import app

# add database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

# init the db
db = SQLAlchemy(app)


# ORM definitions

# User database
class UserDB(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(40), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    role = db.Column(db.String(40), nullable=False)

    def __init__(self, user_name, first_name, last_name, email, password, role='user'):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role

    def password_match(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class ProfDB(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('userDB.id'), primary_key=True)
    school = db.Column(db.String(100))


class StudentDB(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('userDB.id'), primary_key=True)


class GroupDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class TeachDB(db.Model):
    prof_id = db.Column(db.Integer, db.ForeignKey('profDB.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groupDB.id'), primary_key=True)


# class MemberDB(db.Model):
#     student_id=db.Column(db.Integer, db.ForeignKey('studentDB.id'), primary_key=True)
#     group_id = db.Column(db.Integer, db.ForeignKey('groupDB.id'), primary_key=True)


class QuestionDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text(), nullable=False)
    answer1 = db.Column(db.Text(), nullable=False)
    answer2 = db.Column(db.Text(), nullable=False)
    answer3 = db.Column(db.Text())
    answer4 = db.Column(db.Text())
    correct = db.Column(db.Integer, nullable=False)
    solution = db.Column(db.Text())
