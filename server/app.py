from flask import Flask, render_template, jsonify, request
from model import chatgpt_process_query, classifier, chat_log

app = Flask(__name__)

#routes
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

@app.route('/convos')
def convo():
    return render_template('convo.html',title='convo')

def api():
    # Get the message from the request
    text_message = request.form.get('text_message')
    message_response = chatgpt_process_query(classifier, text_message)

    if message_response == "1":
        chat_response = chatgpt_process_query(chat_log, text_message)
        return jsonify(chat_response)
    else:
        print("Sorry :( I don't know how to do that yet.")
    # elif message_response == "2":
    #     print("2")
    #     return jsonify({"Response": f"Creating invite: {text_message}"})
    # elif message_response == "3":
    #     print("3")
    #     return jsonify({"Response": f"Sending email: {text_message}"})
    # elif message_response == "4":
    #     print("4")
    #     return jsonify({"Response": f"Playing song: {text_message}"})
    # else:
    #     print("5")
    #     return "didnt work :/"

if __name__ == '__main__':
    app.run(debug=True)