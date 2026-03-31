import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent 
sys.path.insert(0, str(project_root))

from langchain_core.messages import AIMessage, HumanMessage,SystemMessage
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, START, END
import streamlit as st
from typing import Annotated
from langgraph.graph.message import add_messages
import os
from dotenv import load_dotenv
from utils.web_search_tool import search
from utils.rag_web_base_loader_tool import web_loader_tool
from utils.finance_law import finance_law_tool
from utils.tax import CGI_tool
from langgraph.prebuilt import ToolNode
from langgraph.prebuilt import tools_condition
from utils.cgnc import cgnc_tool
from utils.plan_comptable import plan_comptable_tool

load_dotenv()
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
llm_groq=ChatGroq(model="llama-3.3-70b-versatile")

class State(TypedDict):
    messages:Annotated[list,add_messages]


tools=[cgnc_tool,search,web_loader_tool,finance_law_tool,CGI_tool,plan_comptable_tool]
llm_with_tools=llm_groq.bind_tools(tools)

def superbot(state:State):
    return {"messages":[llm_groq.invoke(state['messages'])]}

ACCOUNTING_KEYWORDS = [
    "cgnc", "comptabilité", "accounting", "morocco", "maroc", 
    "financial", "tax", "fiscal", "plan comptable", "audit",
    "bilan", "compte de résultat", "immobilisation", "amortissement",
    "provision", "stock", "créance", "dette", "CGNC"
]

def tool_calling_llm(state:State):
    prompt = """You are a Moroccan accounting expert assistant. 
    
    TOOL USAGE RULES:
    1. For ANY question about Moroccan accounting, CGNC, or finance in Morocco → use 'cgnc_accounting_tool' FIRST
    2. Only use 'google_search' for current events, news, or non-accounting questions
    3. NEVER answer accounting questions without using a tool first
    
    Examples:
    - "What is CGNC?" → use cgnc_accounting_tool
    - "Comment calculer l'amortissement?" → use cgnc_accounting_tool
    - "Latest news in Morocco" → use google_search
    - "Read this webpage" → use rag_web_loader
    
    Current question: {question}
    """
    last_message = state["messages"][-1].content if state["messages"] else ""
    
    formatted_prompt = prompt.replace("{question}", last_message)
    system_message = SystemMessage(content=formatted_prompt)
    all_messages = [system_message] + state["messages"]
    return {"messages":[llm_with_tools.invoke(all_messages)]}


def agent_structring_response(state:State):
    prompt = """You are a response structuring assistant. Follow these rules strictly:
    
    1. If the response came from 'cgnc_accounting_tool', format it professionally as accounting advice
    2. If the response came from 'google_search', cite the source as "Web Search"
    3. If the response is empty, say "I couldn't find specific information on this topic. Try rephrasing your question."
    4. For accounting questions, always mention that the information comes from CGNC standards
    
    Current response to structure: {response}
    """
    
    last_response = state["messages"][-1].content if state["messages"] else ""
    formatted_prompt = prompt.replace("{response}", last_response)
    system_message = SystemMessage(content=formatted_prompt)
    all_messages = [system_message] + state["messages"]
    return {"messages":[llm_with_tools.invoke(all_messages)]}

def route_by_keyword(state: State) -> dict:
    """Pre-process to force accounting tool for relevant queries"""
    last_message = state["messages"][-1].content.lower() if state["messages"] else ""
    accounting_keywords = ["cgnc", "comptabilité", "accounting", 
                          "financial", "amortissement", "bilan"]
    
    if any(keyword in last_message for keyword in accounting_keywords):
        forced_prompt = """IMPORTANT:if This is an accounting question about Morocco. 
        You MUST use the 'cgnc_accounting_tool' to answer this question.
        Do not use any other tool until you've tried this one.
        
        Question: {question}"""
        formatted_prompt=forced_prompt.replace("{question}", last_message)
        system_message = SystemMessage(content=formatted_prompt)
        return {"messages": [system_message] + state["messages"]}
    
    return state

graph = StateGraph(State)
graph.add_node("tool_calling_llm", tool_calling_llm)
graph.add_node("tools", ToolNode(tools))
graph.add_node("structures", agent_structring_response)
graph.add_node("route_by_keyword", route_by_keyword)
graph.add_edge(START, "route_by_keyword")
graph.add_edge("route_by_keyword", "tool_calling_llm")
graph.add_conditional_edges(
    "tool_calling_llm",
    tools_condition,
    {
        "tools": "tools",
        "__end__": END
    }
)
graph.add_edge("tools", "structures")
graph.add_conditional_edges(
    "structures",
    tools_condition,
    {
        "tools": "tools",
        "__end__": END
    }
)

# Compile
from langgraph.checkpoint.memory import MemorySaver

memory = MemorySaver()

# Compile the graph with memory
graph_builder = graph.compile(checkpointer=memory)



