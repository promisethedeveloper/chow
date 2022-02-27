from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms import validators
from wtforms.validators import InputRequired, Email

class SignUpForm(FlaskForm):
    """Signup a user."""

    first_name = StringField("First name", validators=[InputRequired()])

    last_name = StringField("Last name", validators=[InputRequired()])

    email = StringField("Email", validators=[InputRequired(), Email()])

    password = PasswordField("Password", validators=[InputRequired()])



class LoginForm(FlaskForm):
    """Login a User."""

    email = StringField("Email", validators=[InputRequired()])

    password = PasswordField("Password", validators=[InputRequired()])


class EditUserForm(FlaskForm):
    """Edit a user."""

    first_name = StringField("First name", validators=[InputRequired()])

    last_name = StringField("Last name", validators=[InputRequired()])


class SearchForm(FlaskForm):
    """Collects inputs for restaurant/store form"""
    restaurant = StringField("Restaurant", validators=[InputRequired()])
    
    location = StringField("Location", validators=[InputRequired()])