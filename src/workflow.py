from langgraph.graph import MessagesState, StateGraph, START, END
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.agents import AgentAction, AgentFinish

from typing import Optional, TypedDict, Annotated, Sequence, Union
import operator
from .agent import agent, agent_executor, tools, llm, prompt

tools_by_name = {tool.name: tool for tool in tools}
llm_with_tools = llm.bind_tools(tools)




class State(TypedDict):
    input: str
    chat_history: Annotated[Sequence, operator.add]
    agent_outcome: Optional[Union[AgentAction, AgentFinish, None]]
    intermediate_steps: Annotated[list, operator.add]

def llm_call(state: MessagesState):
    return {
        "messages": [
            llm_with_tools.invoke(
                [
                    SystemMessage(
                        content=prompt.format()
                    )
                ]
                + state["messages"]
            )
        ]
    }