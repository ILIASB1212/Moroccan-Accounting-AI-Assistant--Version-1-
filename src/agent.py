import sys
import os
from pathlib import Path

project_root = Path(__file__).parent.parent 
sys.path.insert(0, str(project_root))

from langchain_core.messages import AIMessage, HumanMessage,SystemMessage
from typing_extensions import TypedDict
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import streamlit as st
from typing import Annotated
import os
from dotenv import load_dotenv
# langgraph  imports
from langgraph.prebuilt import ToolNode
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
# tools imports
from utils.cgnc import cgnc_tool
from utils.tax import CGI_tool
from utils.plan_comptable import plan_comptable_tool
from utils.web_search_tool import google_search,search
from utils.rag_web_base_loader_tool import web_loader_tool
from utils.finance_law import finance_law_tool
# tracing
from langfuse.langchain import CallbackHandler
load_dotenv()
os.environ["LANGFUSE_PUBLIC_KEY"]=os.getenv("LANGFUSE_PUBLIC_KEY")
os.environ["LANGFUSE_SECRET_KEY"]=os.getenv("LANGFUSE_SECRET_KEY")
os.environ["LANGFUSE_BASE_URL"]=os.getenv("LANGFUSE_BASE_URL")
# Initialize with keys from your .env
langfuse_handler = CallbackHandler()
#  env variables
os.environ["GROQ_API_KEY"]=os.getenv("GROQ_API_KEY")
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGCHAIN_PROJECT")
MODELS="openai/gpt-oss-120b"
llm_groq=ChatGroq(model=MODELS)

class State(TypedDict):
    messages:Annotated[list,add_messages]


tools=[cgnc_tool,search,web_loader_tool,finance_law_tool,CGI_tool,plan_comptable_tool]
llm_with_tools=llm_groq.bind_tools(tools)

def superbot(state:State):
    return {"messages":[llm_groq.invoke(state['messages'])]}


rules_2="""always follow to tools descriptions and instructions to select the right tool for the user question. 
If the question is not clear, use google search to find more information about the topic and then select the right tool to answer the question.
 Always use a tool before answering. Never answer accounting or tax questions from memory alone."""

def tool_calling_llm(state: State):
    system_message = SystemMessage(content=f"""You are a Moroccan accounting expert assistant.
                                   {rules_2}
                                    Always use a tool before answering. Never answer accounting or tax questions from memory alone.
""")
    all_messages = [system_message] + state["messages"]
    return {"messages": [llm_with_tools.invoke(all_messages)][-10:]}

source_instruction_3 = {
        "code_general_normalisation_comptable_maroc": "Format as professional accounting advice. Mention this comes from CGNC standards. you must combine this with plan_comptable_general_marocain",
        "code_general_des_impots_morocco": "Format as professional tax advice. Mention this comes from the Code Général des Impôts.",
        "loi_de_finances_maroc": "Format clearly with the fiscal year context. Mention this comes from the Loi de Finances.",
        "plan_comptable_general_marocain": "Present account numbers and journal entries in a clear tabular format. you must combine this with code_general_normalisation_comptable_maroc",
        "google_search": 'Cite the source as "Web Search". Present information clearly.',
        "rag_web_loader": "Summarize the webpage content clearly.",
        
    }

def agent_structuring_response(state: State):
    # Find the last ToolMessage to know which tool was used
    
    system_message = SystemMessage(content=f"""You are a response structuring assistant.

                Instructions: {source_instruction_3}

                if you feel that you need to reuse the tools multiple time reuse multiple tools .
                
                If the response content is empty or unclear, say: "I couldn't find specific information on this topic. Try rephrasing your question."

                Do not add information that wasn't in the original response. Just structure and format it.
                """)

    all_messages = [system_message] + state["messages"][-5:]
    return {"messages": [llm_with_tools.invoke(all_messages)]}

graph = StateGraph(State)
graph.add_node("tool_calling_llm", tool_calling_llm)
graph.add_node("tools", ToolNode(tools))
graph.add_node("structures", agent_structuring_response)
graph.add_edge(START, "tool_calling_llm")
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

memory = MemorySaver()

# Compile the graph with memory
graph_builder = graph.compile(checkpointer=memory)



