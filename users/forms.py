import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, ValidationError, Length, EqualTo


def character_check(form, field):
    excluded_chars = "*?!'^+%&/()=}][{$#@<>"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")


class RegisterForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    firstname = StringField(validators=[Required(), character_check])
    lastname = StringField(validators=[Required(), character_check])
    phone = StringField(validators=[Required()], )
    password = PasswordField(validators=[Required(), Length(min=6, max=12, message='The password must be between '
                                                                                   '6 and 12 characters long')])
    confirm_password = PasswordField(validators=[Required(), EqualTo('password', message='Both password'
                                                                                         'fields must match')])
    pin_key = StringField(validators=[Required(), Length(min=32, max=32, message='The PIN must be 32 digits long')])
    submit = SubmitField(validators=[Required()])

    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])(?=.*[a-z])(?=.*\W)')
        if not p.match(self.password.data):
            raise ValidationError("Password must contain at least 1 digit, an uppercase and a lowercase letter,"
                                  "and a special character.")

    def validate_phone(self, phone):
        ph = re.compile(r'[0-9]{4}-[0-9]{3}-[0-9]{4}')
        if not ph.match(self.phone.data):
            raise ValidationError("The phone must be in the format XXXX-XXX-XXXX")


class LoginForm(FlaskForm):
    email = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    pin = StringField(validators=[Required()])
    submit = SubmitField()
