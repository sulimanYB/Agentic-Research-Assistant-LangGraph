# LangGraph Agentic Research Assistant
# Import the four custom research tools

from src.tools.pubmed_search import pubmed_search
from src.tools.web_search import web_search
from src.tools.wikipedia_search import wikipedia_search
from src.tools.math_tools import calculator

from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import SystemMessage

# Register the tools available to the agent
tools = [
    pubmed_search,
    web_search,
    wikipedia_search,
    calculator,
]

# LangGraph imports
from typing import Annotated
from typing_extensions import TypedDict

from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from src.config import MODEL_NAME, TEMPERATURE


# Define the conversation state
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# Initialise the LLM and make all four tools available
llm = ChatOpenAI(
    model=MODEL_NAME,
    temperature=TEMPERATURE
)

llm_with_tools = llm.bind_tools(tools)


SYSTEM_PROMPT = """
You are an evidence-focused scientific research assistant.

Tool selection:
- Use pubmed_search for biomedical publications and research evidence.
- Use web_search for current developments and wider web information.
- Use wikipedia_search for general background and established concepts.
- Use calculator for numerical calculations.

Research guidelines:
- Prefer primary scientific sources when discussing research findings.
- Cite retrieved publications using their actual titles and URLs.
- Never invent references, statistics, or study results.
- Distinguish reported findings from your own interpretation.
- Acknowledge limitations when evidence is incomplete.
- Use previous conversation context to understand follow-up questions.
- Keep answers clear, concise, and scientifically accurate.
"""


# Define the agent node
def research_agent(state: AgentState):
    """Select research tools and generate evidence-based responses."""

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"]
    ]

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


# Build the LangGraph workflow
builder = StateGraph(AgentState)

builder.add_node("research_agent", research_agent)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "research_agent")

# Execute tools when requested; otherwise finish
builder.add_conditional_edges("research_agent", tools_condition)

# Return tool results to the agent
builder.add_edge("tools", "research_agent")

# Store conversation history in memory
memory = MemorySaver()

# Compile the graph with checkpointing enabled
graph = builder.compile(checkpointer=memory)


# Verify tool registration
if __name__ == "__main__":
    print("Registered research tools:")
    for tool in tools:
        print(f"- {tool.name}: {tool.description.strip().splitlines()[0]}")