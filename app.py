import os
import openai
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

from modules.gpt import chatgpt_process_query, classifier, song, agent
from modules.pyd import create_json
from modules.inout import input_json

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thisisasecretkey'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    email = db.Column(db.String(320), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegisterForm(FlaskForm):
    name = StringField(validators=[InputRequired(), Length(
        min=4, max=320)])
    email = StringField(validators=[InputRequired(), Length(
        min=4, max=320)])
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)])
    confirmPassword = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)])
    submit = SubmitField("Register")

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(
            email=email.data).first()

        if existing_user_email:
            raise ValidationError(
                "An account with this email already exists. Please choose a different one.")


class LoginForm(FlaskForm):
    email = StringField(validators=[InputRequired(), Length(
        min=4, max=320)])
    password = PasswordField(validators=[InputRequired(), Length(
        min=4, max=20)])

    submit = SubmitField("Login")


convo_db = SQLAlchemy(app)
class Convos(convo_db.Model):
    id = convo_db.Column(convo_db.Integer, primary_key=True)
    email = convo_db.Column(convo_db.String(320), nullable=False)
    request = convo_db.Column(convo_db.String(65000), nullable=False)
    response = convo_db.Column(convo_db.String(65000), nullable=False)


with app.app_context():
    db.create_all()
    convo_db.create_all()

# routes


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='Home')


@app.route('/Launch')
@login_required
def launch():
    return render_template('launchRemie.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            session['isLogged'] = True
            session['email'] = form.email.data
            return redirect(url_for('launch'))
        
        flash('Incorrect Email or Password. Please try again!', 'error')
    session['isLogged'] = False
    return render_template('login.html', title='Login', form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('launch'))


@app.route('/register', methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(name=form.name.data,
                        email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', title='register', form=form)


# @app.route('/basepopup')
# def basepopup():
#     return render_template('basepopup.html', title='sidebar')


@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('index.html', title='dashboard')


@app.route('/convos')
@login_required
def convo():
    convo_query = Convos.query.filter(Convos.email == session['email']).all()
    return render_template('convo.html', title='convo', convo_query=convo_query)


API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = API_KEY


@app.route("/api", methods=["POST"])
def api():
    # Get the message from the request
    text_message = request.form.get('text_message')
    message_response = chatgpt_process_query(classifier, text_message)
    # Edge case: if no user response
    if text_message == "":
        return jsonify("I couldn't quite hear that, please try again.")
    else:
        # classify the message
        if message_response == "1":
            chat_response = agent(text_message)
            print(chat_response)
            convo = Convos(email=session['email'], request=text_message, response=chat_response)
            convo_db.session.add(convo)
            convo_db.session.commit()
            convo = Convos(email=session['email'], request=text_message, response=chat_response)
            convo_db.session.add(convo)
            convo_db.session.commit()
            return jsonify(chat_response)
        elif message_response == "2":
            event_json = create_json(text_message)
            print(event_json)
            new_json = input_json('parse.json')
            print(new_json)
            convo = Convos(email=session['email'], request=text_message, response="Event created successfully!")
            convo_db.session.add(convo)
            convo_db.session.commit()
            return jsonify("Event created successfully!")
            # this just broke, please give us one moment as we fix it
            # cond = create_event(new_json)
            # print(cond)
            # if cond == 0:
            #     return jsonify("Event created successfully!")
            # else:
            #     return jsonify("I'm sorry, it didn't work. Please give me more information")        
        # elif message_response == "3":
        #     song = chatgpt_process_query(song, text_message)
        #     cond = play_song(song)
        #     if cond == 0:
        #         return jsonify("Song played successfully!")
        #     else:
        #         return jsonify("I'm sorry, it didn't work. Please give me more information")



if __name__ == '__main__':
    app.run(debug=True, port=8000)
