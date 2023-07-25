import openai
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes, allowing requests from any origin

API_KEY = "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"
openai.api_key = API_KEY

chat_log = []

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def api():
    text_message = request.form.get('text_message')
    response_message = chatgpt_process_query(text_message)
    return jsonify(response_message)

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
    app.run(debug=True, host="0.0.0.0", port=8000)
