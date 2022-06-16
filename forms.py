from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    username = StringField(label = "Username", validators = [InputRequired()])
    password = PasswordField(label= "Password", validators=[InputRequired()])

class ArticleForm(FlaskForm):
    title = StringField(label="Title", validators=[InputRequired()])
    content = TextAreaField()
