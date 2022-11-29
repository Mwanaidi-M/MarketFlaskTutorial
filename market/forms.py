from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from .models import Users


class RegisterForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired(message='Username is required'),
                                                          Length(min=2, max=32, message='Username length must be in '
                                                                                        'the range 2-32')])
    email = EmailField(label='Email Address:', validators=[DataRequired(message='Email Address is required'),
                                                           Email(message='Incorrect email format.')])
    pwd1 = PasswordField(label='Password:', validators=[DataRequired(message='Password is required'),
                                                        Length(min=8, message='Password must have at leaset 8 '
                                                                              'characters.')])
    pwd_confirm = PasswordField(label='Confirm Password:',
                                validators=[EqualTo('pwd1', message='Passwords must match!')])
    submit = SubmitField(label='Create Account')

    def validate_username(self, usr):
        user = Users.query.filter_by(user_name=usr.data).first()
        if user is not None:
            raise ValidationError('This username already exists. Please enter a different name.')

    def validate_email(self, u_email):
        user = Users.query.filter_by(user_email=u_email.data).first()
        if user is not None:
            raise ValidationError('Email already exists. Please enter a different email.')


class LoginForm(FlaskForm):
    username = StringField(label='Username:', validators=[DataRequired()])
    pwd = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class BuyItemForm(FlaskForm):
    submit = SubmitField(label='Buy Item')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item')
