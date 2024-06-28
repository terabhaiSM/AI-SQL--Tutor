from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin, LoginManager
import datetime
from sqlalchemy import ARRAY

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    rating = db.Column(db.Integer, default=0)
    level = db.Column(db.String(50), default="Beginner")

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    topic_id = db.Column(db.Integer, db.ForeignKey('topic.id'), nullable=False)

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    answer = db.Column(db.String(500), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    questions = db.relationship('Question', backref='topic', lazy=True)

class Workspace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    last_access_date = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    workspace_topics = db.Column(ARRAY(db.Integer))  # Assuming topic ids are integers
    sampledatabase_id = db.Column(db.Integer)

class WorkspaceDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'), nullable=False)
    workspace_practice_seq = db.Column(db.Integer, nullable=True)
    question_desc_json = db.Column(db.JSON, nullable=False)
    answer_desc = db.Column(db.String(2000), nullable=True)
    correct_boolean = db.Column(db.Boolean, default=False)
    feedback_from_AI_json = db.Column(db.JSON, nullable=True)
    AI_rating = db.Column(db.Integer, nullable=True)

# Define relationships
User.workspaces = db.relationship('Workspace', backref='user', lazy=True)
Workspace.details = db.relationship('WorkspaceDetails', backref='workspace', lazy=True)

class ChatWorkspace(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class ChatHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workspace_id = db.Column(db.Integer, db.ForeignKey('workspace.id'), nullable=False)
    sender = db.Column(db.String(10), nullable=False)
    text = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(20), nullable=True)


