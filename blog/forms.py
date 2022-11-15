from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, PasswordField, StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired("Campo obbligatorio!")])
    password = PasswordField("Password", validators=[DataRequired("Campo obbligatorio")])
    remember_me = BooleanField("Ricordami")
    submit = SubmitField("Login")

class PostForm(FlaskForm):
    title = StringField("Titolo",
        validators=[DataRequired("Campo obbligatorio!"), Length(min=3, max=120,
        message="Assicurati che il titolo abbia tra i 3 e i 120 caratteri")])

    description = TextAreaField("Descrizione",
        validators=[Length(max=240, message="Il massimo per la descrizione è 240 caratteri")])  

    body1 = StringField("Primo paragrafo")
    body2 = StringField("Secondo paragrafo (facoltativo)")
    body3 = StringField("Terzo paragrafo (facoltativo)")
    body4 = StringField("Ultimo paragrafo (facoltativo)")

    testimonial1 = StringField("Prima testimonianza")
    testimonial2 = StringField("Seconda testimonianza")

    cover = FileField("Copertina", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    img1 = FileField("Prima immagine", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    img2 = FileField("Seconda immagine", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    img3 = FileField("Terza immagine", validators=[FileAllowed(["jpg", "jpeg", "png"])])
        
    submit = SubmitField("Pubblica")

ch=[("BOSS", "BOSS"),  ("pres_editor", "pres_editor"), ("testimonial", "testimonial")]
class UserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired("Campo obbligatorio!")])
    password = PasswordField("Password", validators=[DataRequired("Campo obbligatorio")])
    email = StringField("Email", validators=[DataRequired("Campo obbligatorio!")])
    role = SelectField("Ruolo", choices=ch, validators=[DataRequired("Campo obbligatorio!")])
    icon = FileField("Copertina", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    submit = SubmitField("Fatto")