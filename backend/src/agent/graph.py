from langgraph.graph import END, START, StateGraph
from langgraph.types import Command
from langchain_core.messages import HumanMessage
from .state import AgentStyleState
from .prompt import agent_act_style_prompt
from utils.model_util import get_model


async def Act(state:AgentStyleState)->AgentStyleState:
    agent_style = state['agent_style']
    llm = await get_model()
    human_message =HumanMessage(content=agent_act_style_prompt.format(agent_style=agent_style))
    response = llm.ainvoke([human_message])

def thought(state:AgentStyleState)->AgentStyleState:
    agent_style = state['agent_style']
    messages = state['messages']
    llm = await get_model()

async def get_graph():
    builder = StateGraph()
    builder.add_node("Act",Act)
