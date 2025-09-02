from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField
from wtforms.validators import InputRequired, Length, ValidationError, Email


app = Flask(__name__, template_folder='templates')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'
db = SQLAlchemy(app)

class UserLogin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable = False, unique = True)
    email = db.Column(db.String(50), nullable = False)
    password = db.Column(db.String(30), nullable = False)


class registrationform(FlaskForm):
    username = StringField(validators=[InputRequired(), Length( min=4, max=40)], render_kw={'placeholder': 'username'})
    email = StringField(validators=[InputRequired(), Email(), Length(min=6, max=50)], render_kw={'placeholder': 'email'})
    password = PasswordField(validators=[InputRequired(), Length(min=11, max=30)], render_kw={'placeholder': 'password'})

    submit = SubmitField('Register')


    def validate_username(self, username):
        existing_username = UserLogin.query.filter_by(username = username.data).first()

        if existing_username:
            raise ValidationError('sorry this username is taken') 
        
    def validate_email(self, email):
        existing_email = UserLogin.query.filter_by(email = email.data).first()

        if existing_email:
            raise ValidationError('sorry this email is already being used')


class loginform(FlaskForm):
    username = StringField(validators=[InputRequired(), Length( min=4, max=40)], render_kw={'placeholder': 'username'})
    email = StringField(validators=[InputRequired(), Email(), Length(min=6, max=50)], render_kw={'placeholder': 'email'})
    password = PasswordField(validators=[InputRequired(), Length(min=11, max=30)], render_kw={'placeholder': 'password'})

    submit = SubmitField('Log in')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login(): 
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')







if __name__ == "__main__": 
    app.run(host='0.0.0.0', port=5555)
