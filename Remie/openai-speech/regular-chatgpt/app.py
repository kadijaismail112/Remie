import openai

API_KEY = ""
openai.api_key = API_KEY


chat_log = []

while True:
    user_message = input()
    if user_message.lower() == "quit":
        break
    else:
        chat_log.append({"role": "user", "content": user_message})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=chat_log
        )
        assistant_response = response['choices'][0]['message']['content']
        clean_assistant_response = assistant_response.strip("\n").strip()
        print("ChatGPT:", clean_assistant_response)
        chat_log.append({"role": "assistant", "content": clean_assistant_response})