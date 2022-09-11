from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo



class NewUserForm(FlaskForm):
    style={'class': 'ourClasses', 'style': 'width:50%; other_css_style; margin-left:300px;'}
    first_name = StringField('First_Name', validators=[DataRequired()], render_kw=style)
    last_name = StringField('Last_Nane', validators=[DataRequired()], render_kw=style)
    email = StringField('Email', validators=[DataRequired()], render_kw=style)
    username = StringField('UserName', validators=[DataRequired()],render_kw=style)
    password = PasswordField('Password', validators=[DataRequired()],render_kw=style)
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')],render_kw=style)
    submit = SubmitField(render_kw=style)



class LoginForm(FlaskForm):
    style={'class': 'ourClasses', 'style': 'width:50%; other_css_style; margin-left:300px;'}
    username = StringField('Username', validators=[DataRequired()],render_kw=style)
    password = PasswordField('Password', validators=[DataRequired()],render_kw=style)
    submit = SubmitField(render_kw=style)