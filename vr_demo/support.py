from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField,HiddenField
from wtforms.validators import InputRequired, Email, Length
import flask_login

class ContactForm(FlaskForm):
    name = StringField("Contact")
    email = StringField("Email")
    phone = StringField("Phone")
    size = SelectField('Size of Space', choices=[('200 sq.m. or less ', '200 sq.m. or less'),
                                                 ('200-500 sq.m.', '200-500 sq.m.'),
                                                 ('> 500 sq.m.', '> 500 sq.m.'),
                                                 ('> 1000 sq.m.', '> 1000 sq.m.')])
    type = SelectField('Property Type', choices=[('Single Family ','Single Family'),
                                                 ('Condo','Condo'),
                                                 ('Commercial','Commercial'),
                                                 ('Retail','Retail'),
                                                 ('Boat','Boat'),
                                                 ('Aircraft','Aircraft')])
    date = SelectField('Date Needed', choices=[('1-2 days ','1-2 days'),
                                               ('1-4 days','1-4 days'),
                                               ('1-7 days','1-7 days'),
                                               ('7-14 days','7-14 days'),
                                               ('no preference','no preference')])
    submit = SubmitField("Submit Request")

class CreditForm(FlaskForm):
    subscribe_amount = StringField("Topup Amount($NZD):")
    submit = SubmitField("Credit Account")


class SigninForm(FlaskForm):
    # formname = HiddenField()
    username = StringField('用户名', validators=[InputRequired(), Length(min=6, max=15)])
    password = PasswordField('密码', validators=[InputRequired(), Length(min=6, max=80)])
    # remember = BooleanField('remember me')

class SignupForm(FlaskForm):
    # formname = HiddenField()
    email = StringField('电子邮件地址', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('用户名', validators=[InputRequired(), Length(min=6, max=15)])
    password = PasswordField('密码', validators=[InputRequired(), Length(min=6, max=80)])
    agreement = BooleanField()

class User(flask_login.UserMixin):
    """Standard flask_login UserMixin"""
    pass
