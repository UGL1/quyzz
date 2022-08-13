from flask import Flask
# Here are all the ORM
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# add database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

# init the db
db = SQLAlchemy(app)

""" Example of a one-to-many relationship"""

class TopicDB(db.Model):  # That's the name of the object mapping our table
    __tablename__ = 'topicdb'  # that's... our tablename
    id = db.Column(db.Integer, primary_key=True)  # column#1, primary
    label = db.Column(db.String(50), nullable=False)  # etc

    questions = db.relationship('Question', backref='topic', lazy=True)  # this one allows calls like
    # 1° for a TopicDB t : t.questions lists all the QuestionDB linked to t.
    # 2° for a QuestionDB q : q.topic is the TopicDB linked to it

class Question(db.Model): # Nothing fancy here
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), nullable=False)
    topic_ident = db.Column(db.Integer, db.ForeignKey('topicdb.id'), nullable=False)

""" Example of a many-to-many relationship"""
#
# tags = db.Table('tags',
#     db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True),
#     db.Column('page_id', db.Integer, db.ForeignKey('page.id'), primary_key=True)
# )
#
# class Page(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     tags = db.relationship('Tag', secondary=tags, lazy='subquery',
#         backref=db.backref('pages', lazy=True))
#
# class Tag(db.Model):
#     id = db.Column(db.Integer, primary_key=True)

db.drop_all()
db.create_all()
t1 = TopicDB(label="math")
t2 = TopicDB(label="cs")
db.session.add(t1)
db.session.add(t2)
db.session.commit()

q1 = Question(text="math text", topic_ident=t1.id)
q2 = Question(text="math text too", topic_ident=t1.id)
q3 = Question(text="cd text", topic_ident=t2.id)
q4 = Question(text="cs text too", topic_ident=t2.id)

db.session.add(q1)
db.session.add(q2)
db.session.add(q3)
db.session.add(q4)
db.session.commit()

lst = Question.query.filter_by(topic_ident=t1.id)
for l in lst:
    print(l.text)

for l in t1.questions:
    print(l.text)
    print(l.topic.label)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
