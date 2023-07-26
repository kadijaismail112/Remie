import os
import openai
from flask import Flask, render_template, jsonify, request, redirect, url_for
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


with app.app_context():
    db.create_all()

# routes


@app.route('/')
@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('login'))

    return render_template('login.html', title='Login', form=form)


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


@app.route('/basepopup')
def basepopup():
    return render_template('basepopup.html', title='sidebar')


@app.route('/dashboard')
@login_required
def dash():
    return render_template('index.html', title='dashboard')


@app.route('/convos')
@login_required
def convo():
    return render_template('convo.html', title='convo')


API_KEY = os.environ.get("OPEN_AI_API_KEY")
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


def chatgpt_process_query(message):
    chat_log.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_log
    )
    assistant_response = response['choices'][0]['message']['content']

    clean_assistant_response = assistant_response.strip("\n").strip()
    print("ChatGPT:", clean_assistant_response)
    chat_log.append({"role": "assistant", "content": clean_assistant_response})

    return clean_assistant_response


if __name__ == '__main__':
    app.run(debug=True, port=8000)
