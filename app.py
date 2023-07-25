import openai
<<<<<<< HEAD
from flask import Flask, render_template,  jsonify, request

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
=======
from flask import Flask, render_template, jsonify, request
from model import chatgpt_process_query, classifier, chat_log

app = Flask(__name__)

openai.api_key = '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'

#routes
@app.route('/')

@app.route('/login')
def login():
    return render_template('/login.html',title='sidebar')

@app.route('/register')
def register():
    return render_template('/register.html',title='register')

@app.route('/basepopup')
def basepopup():
    return render_template('/basepopup.html',title='sidebar')
@app.route('/dashboard')
def dash():
    return render_template('/index.html',title='dashboard')

@app.route('/convos')
def convo():
    return render_template('/convo.html',title='convo')

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

>>>>>>> 12970d4 (trying to figure things out)
if __name__ == '__main__':
    app.run(debug=True)