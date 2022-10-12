from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SelectField, PasswordField, SubmitField, BooleanField
from wtforms import TextAreaField
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired, Length, Email, InputRequired
from nork_town.models import Peoples

class Form_Edit_RegisterPeople(FlaskForm):
    full_name = StringField('Nome Completo', validators=[DataRequired(), Length(6, 30)])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    phone_number = StringField('Telefone', validators=[DataRequired(), Length(10, 16)])
    profile_picture = FileField('Atualizar Foto de Perfil', validators=[FileAllowed(['jpg','png'], "Suportado somente JPG e PNG.")])
    button_edit_professional_profile = SubmitField('Salvar Alterações')

class FormLogin(FlaskForm):
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Senha', validators=[DataRequired(), Length(6, 20)])
    remember_user = BooleanField('Manter Conectado?')
    button_login = SubmitField('Entrar')

class FormNewCar(FlaskForm):

    model = StringField('Qual modelo?', validators=[DataRequired(), Length(6, 20)])
    brand = SelectField(u'Qual a marca?', validators=[InputRequired()], 
                                    choices=[('', "Selecione"), ("Ford","Ford"), ("Chevrolet","Chevrolet"), ("BMW","BMW")], default=None)
    car_type = SelectField(u'Qual tipo?', validators=[InputRequired()], 
                                    choices=[('', "Selecione"), ("Hatch","Hatch"), ("Sedan","Sedan"), ("Conversível","Conversível")], default=None)
    color_car = SelectField(u'Qual a cor?', validators=[InputRequired()], 
                                    choices=[('', "Selecione"), ("Amarelo","Amarelo"), ("Azul","Azul"), ("Cinza","Cinza")], default=None)
    description = TextAreaField('Observação', validators=[DataRequired(), Length(50, 5000)])
    people = SelectField(u'Selecione o proprietário', validators=[InputRequired()], 
                                   choices=Peoples.query.all()
                                   )

    button_new_project = SubmitField('Salvar')