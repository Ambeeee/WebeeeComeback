from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Ricordami")
    submit = SubmitField("Login")

class PostForm(FlaskForm):
    title = StringField("Titolo",
        validators=[DataRequired("Campo obbligatorio!"), Length(min=3, max=120, message="Assicurati che il titolo abbia tra i 3 e i 120 caratteri")])
    
    username = TextAreaField("Descrizione",
        validators=[Length(max=240, message="Il massimo per la descrizione è 240 caratteri")])
        
    body = StringField("Paragrafo #1", validators=[DataRequired("Campo obbligatorio!")])
    submit = SubmitField("Pubblica")
