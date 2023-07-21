from flask import Flask, render_template

app = Flask(__name__)

#routes
@app.route('/')
@app.route('/sidebar')
def sidebar():
    return render_template('index.html',title='sidebar')

# @app.route('/index')
# def index():
#     return render_template('index.html',title='index')

# @app.route('/login')
# def index():
#     return render_template('login.html',title='login')

# @app.route('/register')
# def index():
#     return render_template('register.html',title='register')
if __name__ == '__main__':
    app.run(debug=True)