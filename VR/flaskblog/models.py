from datetime import datetime

from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Library', backref='author', lazy=True)
    videos = db.relationship('Video', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


    
class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    experiences = db.relationship('Experience', backref='post', lazy=True)
    
    # date and times
    def __repr__(self):
        return f"Library('{self.title}', '{self.date_posted}')"


class Experience(db.Model):
    eid = db.Column(db.Integer, primary_key=True)
    etitle = db.Column(db.String(100), nullable=False)
    edate_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    econtent = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('library.id'), nullable=False)
    conversation = db.relationship('Conversation', backref='question', lazy=True)

    
    def __repr__(self):
        return f"Experience('{self.etitle}', '{self.edate_posted}')"


class Video(db.Model):# Will use filename and con_id to track BUT cannot get file name from the upload file yet
    id = db.Column(db.Integer, primary_key=True)
    url=db.Column(db.String(100), nullable=False)
    filename = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #eid = db.Column(db.Integer, db.ForeignKey('user.eid'), nullable=False)
    # uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    con_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(500), nullable=False)
    dragV_id=db.Column(db.Integer, db.ForeignKey("dragged_video.id"),nullable=False)
    options = db.relationship('Options', backref='question', lazy=True)


class Options(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    visible = db.Column(db.Integer, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    library_id = db.Column(db.Integer, db.ForeignKey('library.id'), nullable=False)
    experience_id = db.Column(db.Integer, db.ForeignKey('experience.eid'), nullable=False)
    types=db.Column(db.String(200), nullable=False)

class Dragged_video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=False)
    coversation_id=db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)

class Add_on_video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url=db.Column(db.String(100), nullable=False)
    option_id=db.Column(db.Integer, db.ForeignKey('options.id'))

class selected_video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('add_on_video.id'), nullable=False)
    option_id=db.Column(db.Integer, db.ForeignKey('options.id'))


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score_name=db.Column(db.String(200), nullable=False)
    point1=db.Column(db.Float, nullable=False)
    point2=db.Column(db.Float, nullable=False)
    point3=db.Column(db.Float, nullable=False)
    option_id=db.Column(db.Integer, db.ForeignKey('options.id'))

    


