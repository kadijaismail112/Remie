import openai
import os
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.agents import initialize_agent
from langchain.agents.self_ask_with_search.output_parser import SelfAskOutputParser

openai.api_key = os.environ["OPENAI_API_KEY"]

classification = """You are a chatbot assistant that helps people with their daily tasks. I want for you to classify questions given what you think they are.
the possible classes are:
- A general question, that can be answered by the chatbot = 1
- A request to create a calendar event, that should be sent to google = 2
- A request to send an email, that should be sent to google = 3
- A request to play a song, that should be sent to spotify = 4

Please only give me a number corresponding to what you think the class is. 
If you think the question is a general question that can be answered ovre the internet, then give me a 1. 
If you think the question is a request to create a calendar event, then give me a 2. 
If you think the question is a request to send an email, then give me a 3.
If you think the question is a request to play a song, then give me a 4.


Question: What is the weather like today?
Response: 1

Question: Create a calendar event for tomorrow at 3pm
Response: 2

Question: Send an email to my boss about the meeting
Response: 3

Question: Play Work by Rihanna on Spotify
Response: 4
"""

classifier = [{"role": "system", "content": classification}]
chat_log = []

def chatgpt_process_query(chat_log, message):
    chat_log.append({"role": "user", "content": message})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_log
    )
    assistant_response = response['choices'][0]['message']['content']

    clean_assistant_response=assistant_response.strip("\n").strip()
    print("ChatGPT:", clean_assistant_response)
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