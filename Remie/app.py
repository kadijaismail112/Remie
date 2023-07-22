from flask import Flask, render_template

app = Flask(__name__)

#routes
@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html',title='sidebar')
@app.route('/register')
def register():
    return render_template('register.html',title='register')
@app.route('/basepopup')
def basepopup():
    return render_template('basepopup.html',title='sidebar')
@app.route('/index')
def index():
    return render_template('index.html',title='index')
if __name__ == '__main__':
    app.run(debug=True)