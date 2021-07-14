"""
Login and Registrationn forms
"""
from wtforms import Form, PasswordField, validators, SubmitField, StringField, SelectField


class Registration(Form):
    """ Defines the registration form

    Args:
        Form: Inherits the wtf form libary

    Returns:
        None
    """
    name = StringField("Name:")
    username = StringField("Username:", [validators.DataRequired()])
    email = StringField('Email Address:', [
                        validators.Length(min=6, max=35), validators.Email()])
    password = PasswordField('New Password:', [
        validators.DataRequired(),validators.Length(min=8),
        validators.Regexp("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\W_]{8,}$",message="All passwords should contain a lowercase, an uppercase and a number"),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password:')
    role = SelectField('Role:', [validators.DataRequired()], choices=[
                       ('admin', 'Admin'), ('astronaut', 'Astronaut')], validate_choice=True)
    submit = SubmitField("Submit")


class Login(Form):
    """ Defines the form used for user login

    Args:
        Form: Inherits the form functions from the wtforms library

    Returns:
        None
    """
    username = StringField("Username:", [validators.DataRequired()])
    password = PasswordField('Your Password', [validators.DataRequired()])
