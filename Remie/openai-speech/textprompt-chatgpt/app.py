import openai
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

API_KEY = ""
openai.api_key = API_KEY

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def api():

    text_message = request.form.get('text_message')

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
    app.run(debug=True)