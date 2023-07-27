from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)
from langchain.llms import OpenAI

llm = OpenAI(
    streaming=True, callbacks=[FinalStreamingStdOutCallbackHandler()], temperature=0
)

tools = load_tools(["wikipedia", "llm-math"], llm=llm)
agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False
)
agent.run(
    "It's 2023 now. How many years ago did Konrad Adenauer become Chancellor of Germany."
)