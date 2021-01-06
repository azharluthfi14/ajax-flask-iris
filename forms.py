from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField, PasswordField, FloatField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_wtf.file import FileAllowed, FileField
from flask_login import current_user
from backend.models import User


class register_account(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=25)])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password', message='Password must be match!')])
    submit = SubmitField('Sign up')

    def validate_username(self, username):
        if username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'Username %s already taken. Please choose another username.' % username.data)

    def validate_email(self, email):
        if email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email address already use. Please choose another email address. ')


class login_account(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=8)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign in')


class update_account(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=25)])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    avatar = FileField("Update profile picture", validators=[
                       FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'That username already use. Please choose another username.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'That email address already use. Please choose another email address.')


class classification_form(FlaskForm):
    sepal_length = FloatField('Sepal length', validators=[DataRequired()])
    sepal_width = FloatField('Sepal width', validators=[DataRequired()])
    petal_length = FloatField('Petal length', validators=[DataRequired()])
    petal_width = FloatField('Petal width', validators=[DataRequired()])
    submit = SubmitField('Submit')
