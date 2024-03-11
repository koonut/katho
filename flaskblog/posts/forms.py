from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,IntegerField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Name of the Library', validators=[DataRequired()])
    content = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Library')

class ExperienceForm(FlaskForm):
    etitle = StringField('Name of the Experience:', validators=[DataRequired()])
    econtent = TextAreaField('Description:', validators=[DataRequired()])
    author = TextAreaField('Author', validators=[DataRequired()])
    virtual_tour = SubmitField('Virtual Tour')
    switching_perspective = SubmitField('Switching Perspective')
    conversation = SubmitField('Conversation')
    submit = SubmitField('Add Experience')

class FeedbackForm(FlaskForm):
    etitle = StringField('Name of the Experience:', validators=[DataRequired()])
    score_name = TextAreaField('points:', validators=[DataRequired()])
    value1 = IntegerField('points :', validators=[DataRequired()])
    value2 = IntegerField('points :', validators=[DataRequired()])
    value3 = IntegerField('points :', validators=[DataRequired()])
    submit = SubmitField('Save')
    cancel = SubmitField('Cancel')

class ConversationVideoForm(FlaskForm):
    videoUrl='D:\Koonut'
    file_name='123'
    submit = SubmitField('Save')