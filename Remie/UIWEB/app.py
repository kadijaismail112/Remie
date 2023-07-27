import os
import openai
from flask import Flask, render_template, jsonify, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

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

            # Set isLogged to True in the session after successful login
            session['isLogged'] = True
            session['email'] = form.email.data

            return redirect(url_for('launch'))

        flash('Incorrect Email or Password. Please try again!', 'error')

    # If the form is not submitted or login is unsuccessful, set isLogged to False
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
    # print("backend grab form", request.form)
    # print("backend grab form per: ", request.form.get('username'), request.form.get('password'))

    text_message = request.form.get('text_message')
    print("response:" + text_message)
    response_message = chatgpt_process_query(text_message)

    return jsonify(response_message)


chat_log = []

# class Convos(convo_db.Model):
#     id = convo_db.Column(convo_db.Integer, primary_key=True)
#     request = convo_db.Column(convo_db.String(65000), nullable=False)
#     response = convo_db.Column(convo_db.String(320), nullable=False)


def chatgpt_process_query(message):
    chat_history = []
    chat_log.append({"role": "user", "content": message})
    
    convo_query = Convos.query.filter(Convos.email == session['email']).all()
    for convo in convo_query:
        convo_dict = convo.__dict__
        chat_history.append({"role": "user", "content": convo_dict['request']})
        chat_history.append(
            {"role": "assistant", "content": convo_dict['response']})
    
    chat_history.append({"role": "user", "content": message})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history
    )
    assistant_response = response['choices'][0]['message']['content']

    clean_assistant_response = assistant_response.strip("\n").strip()
    print("ChatGPT:", clean_assistant_response)
    chat_log.append({"role": "assistant", "content": clean_assistant_response})

    convo = Convos(email=session['email'], request=message,
                   response=clean_assistant_response)
    convo_db.session.add(convo)
    convo_db.session.commit()

    return clean_assistant_response


if __name__ == '__main__':
    app.run(debug=True, port=8000)
