from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.utilities import GoogleSearchAPIWrapper

from langchain.agents import initialize_agent


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
agent_chain = initialize_agent(tools, llm, agent="chat-conversational-react-description",verbose=True, memory=memory)

agent_chain.run(input="what is the weather currently in new york city?")