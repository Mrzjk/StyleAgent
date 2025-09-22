from typing import TypedDict, Annotated
from pydantic import Field
from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages


class InputState(TypedDict):
    """
    输入参数
    """
    agent_style:Annotated[str,Field(description="智能体的风格")]
    prompt:Annotated[str,Field(description="特色风格智能体的提示")]
    messages:Annotated[list[AnyMessage],add_messages]
class OutputState(TypedDict):
    """
    输出参数
    """

    prompt:Annotated[str,Field(description="特色风格智能体的提示")]

class AgentStyleState(InputState,OutputState):
    pass