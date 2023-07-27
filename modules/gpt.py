import openai
import os
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.agents import initialize_agent

openai.api_key = os.environ["OPENAI_API_KEY"]

classification = """You are a chatbot assistant that helps people with their daily tasks. I want for you to classify questions given what you think they are.
the possible classes are:
- A general question, that can be answered by the chatbot = 1
- A request to create a calendar event, that should be sent to google = 2
- A request to play a song, that should be sent to spotify = 3

Please only give me a number corresponding to what you think the class is. 
If you think the question is a general question that can be answered ovre the internet, then give me a 1. 
If you think the question is a request to create a calendar event, then give me a 2. 
If you think the question is a request to play a song, then give me a 3.



Question: What is the weather like today?
Response: 1

Question: Create a calendar event for tomorrow at 3pm
Response: 2

Question: Play Work by Rihanna on Spotify
Response: 3
"""

song_name = """ You are a song name generator. I want for you to generate a song name given a sentence.
Do not give me anything else other than a song name.
User: Play Work by Rihanna on Spotify
Response: Work by Rihanna
"""

classifier = [{"role": "system", "content": classification}]
song = [{"role": "system", "content": song_name}]
chat_log = []

def chatgpt_process_query(chat_log, message):
    chat_log.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_log
    )
    assistant_response = response['choices'][0]['message']['content']

    clean_assistant_response=assistant_response.strip("\n").strip()
    chat_log.append({"role": "assistant", "content": clean_assistant_response})
    return clean_assistant_response

# chatgpt_process_query(classifier, "What is the temperature today?")

def agent(message):
    search = GoogleSearchAPIWrapper()
    tools = [
        Tool (
            name = "Search",
            func=search.run,
            description="useful for when you need to answer questions about current events or the current"
        )
    ]

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    llm=ChatOpenAI(temperature=0)
    agent_chain = initialize_agent(tools, llm, agent="chat-conversational-react-description",verbose=False, memory=memory)

    response = agent_chain.run(input=message)
    return response

# print(agent("What is the high temperature today in New York City?"))