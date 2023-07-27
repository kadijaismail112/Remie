import openai
import os
from flask import Flask, render_template,  jsonify, request
from module import chatgpt_process_query, chat_log, classifier, agent

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
@app.route('/dashboard')
def dash():
    return render_template('index.html',title='dashboard')
@app.route('/convos')
def convo():
    return render_template('convo.html',title='convo')

API_KEY = os.environ["OPENAI_API_KEY"]
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
            chat_response = agent(chat_log, text_message)
            return jsonify(chat_response)
        elif message_response == "2":
            
        else:
            return jsonify("I'm sorry, I don't understand. Please try again.")
        



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)