<<<<<<< HEAD:server/app.py
from flask import Flask, render_template, jsonify, request
from model import chatgpt_process_query, classifier, chat_log
=======
import openai
from flask import Flask, render_template,  jsonify, request
>>>>>>> 2d042fa (clean up codebase):app.py

app = Flask(__name__)

#routes
<<<<<<< HEAD:server/app.py
@app.route('template/')

@app.route('template/login')
def login():
    return render_template('login.html',title='sidebar')

@app.route('/register')
def register():
    return render_template('register.html',title='register')

@app.route('/basepopup')
def basepopup():
    return render_template('basepopup.html',title='sidebar')

@app.route('/dashboard')
def dash():
    return render_template('index.html',title='dashboard')

=======
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
@app.route('/dashboard')
def dash():
    return render_template('index.html',title='dashboard')
>>>>>>> 2d042fa (clean up codebase):app.py
@app.route('/convos')
def convo():
    return render_template('convo.html',title='convo')

API_KEY = "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"
openai.api_key = API_KEY

@app.route("/api", methods=["POST"])
def api():
    # print("backend grab form", request.form)
    # print("backend grab form per: ", request.form.get('username'), request.form.get('password'))

    text_message = request.form.get('text_message')
    print("response:" + text_message)
    response_message=chatgpt_process_query(text_message)

    return jsonify(response_message)


chat_log = []

def chatgpt_process_query(message):
    chat_log.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_log
    )
    assistant_response = response['choices'] [0] ['message'] ['content']

    clean_assistant_response=assistant_response.strip("\n").strip()
    print("ChatGPT:", clean_assistant_response)
    chat_log.append({"role": "assistant", "content": clean_assistant_response})

    return clean_assistant_response 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)