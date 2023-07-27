import openai
import os
from flask import Flask, render_template,  jsonify, request
from module import chatgpt_process_query, chat_log, classifier

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
 
openai.api_key = os.environ["OPENAI_API_KEY"]

@app.route("/api", methods=["POST"])
def api():
    # Get the message from the request
    text_message = request.form.get('text_message')
    message_response = chatgpt_process_query(classifier, text_message)
    
    # classify the message
    if message_response == "1":
        chat_response = chatgpt_process_query(chat_log, text_message)
        return jsonify(chat_response)
    else:
        print("Not working yet")
        return jsonify("Not working yet")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8000)