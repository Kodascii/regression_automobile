from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User
from .form_fill import fill_form


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        if user is not None:
            raise ValidationError('Please use a different email address.')


     
class PredictForm(FlaskForm):
    column_names = fill_form()
    # Dropdown fields
    dropdown1 = SelectField('Name', choices = column_names['Name'])
    dropdown2 = SelectField('Location', choices = column_names['Location'])
    dropdown3 = SelectField('Year', choices = column_names['Year'])
    dropdown4 = SelectField('Fuel Type', choices = column_names['Fuel_Type'])
    dropdown5 = SelectField('Transmission', choices = column_names['Transmission'])
    dropdown6 = SelectField('Owner Type', choices = column_names['Owner_Type'])

    # Text input fields
    text_input1 = StringField('Text Input 1', validators=[DataRequired()])
    text_input2 = StringField('Text Input 2', validators=[DataRequired()])
    text_input3 = StringField('Text Input 3', validators=[DataRequired()])
    text_input4 = StringField('Text Input 4', validators=[DataRequired()])
    text_input5 = StringField('Text Input 5', validators=[DataRequired()])

    # Submit button
    submit = SubmitField('Submit')