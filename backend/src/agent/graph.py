from langgraph.graph import END, START, StateGraph
from langgraph.types import Command
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import ToolNode
from typing import Literal
from .state import (
    AgentStyleState,
    InputState,
    OutputState)
from .prompt import (
    agent_act_style_prompt,
    agent_generate_style_prompt,
    judget_style_prompt)
from agent.utils.model_util import get_model
from agent.utils.util import tavily_search    
_llm = None
_tools = None
async def get_local_tools():
    global _tools
    if _tools is None:
        _tools = [
            tavily_search
        ]
    return _tools

async def get_local_model():
    global _llm
    if _llm is None:
        _llm = await get_model()
    return _llm

async def act(state:AgentStyleState)->Command[Literal['tool_node','observation']]:
    print('开始执行')
    agent_style = state['agent_style']
    tools =await get_local_tools()
    llm = await get_local_model()
    
    llm_with_tools = llm.bind_tools(tools)
    human_message =HumanMessage(content=agent_act_style_prompt.format(agent_style=agent_style))
    response = await llm_with_tools.ainvoke([human_message])
    update = {"message":[response]}
    print(response)
    if "tool_calls" in response.additional_kwargs.keys()  and len(response.additional_kwargs['tool_calls']) > 0:
        return Command(goto="tool_node",update=update)
    else :
        return Command(goto="observation",update=update)
  

async def observation(state:AgentStyleState)->AgentStyleState:
    print('观察阶段')
    agent_style = state['agent_style']
    messages = state['messages']
    prompt = state['prompt']
    llm = await get_local_model()
    human_message =HumanMessage(content=agent_generate_style_prompt.format(agent_style=agent_style,messages=messages,prompt=prompt))
    response = await llm.ainvoke([human_message])
    return {'prompt':response.content,'messages':[response]}
async def thought(state:AgentStyleState)->Command[Literal['act','__end__']]:
    print('思考阶段')
    llm = await get_local_model()
    human_message = HumanMessage(content = judget_style_prompt.format(**state))
    response = await llm.ainvoke([human_message])
    if '1' in response.content:
        return Command(goto="__end__",update=None)
    else:
        return Command(goto="act",update=None)

async def get_graph():
    builder = StateGraph(state_schema=AgentStyleState,input_schema=InputState,output_schema=OutputState)
    tools = await get_local_tools()
    tool_node = ToolNode(tools)
    builder.add_node("act",act)
    builder.add_node("tool_node",tool_node)
    builder.add_node("observation",observation)
    builder.add_node("thought",thought)

    builder.add_edge(START, "act")
    builder.add_edge("tool_node", "observation")
    builder.add_edge("observation","thought")
    graph = builder.compile()
    return graph



