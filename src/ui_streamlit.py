import sys
from pathlib import Path

project_root = Path(__file__).parent.parent 
sys.path.insert(0, str(project_root))

from langchain_core.messages import  HumanMessage,SystemMessage

from langchain_core.messages import HumanMessage
import streamlit as st
import os
from dotenv import load_dotenv

from agent import graph_builder
load_dotenv()


#streamlit setup
st.title("Simple LangGraph Test")


test_message = st.chat_input("enter your querry")
# Button to run test
if test_message:
    with st.spinner("Running..."):       
        st.write(test_message)
        result = graph_builder.invoke({'messages': HumanMessage(content=test_message)})
        # chekking tool caling if and else 
        if result["messages"][1].tool_calls:
            for tool_call in result["messages"][1].tool_calls:
                print(f"🔧 Tools were called : {tool_call['name']}")
                st.write(f"the sourse  : {tool_call['name']}")
        
        else:
            st.write("🤖 Source: LLM (no tools used)")
            print(f"🔧 Tools were called : LLM (no tools used)")
        # Display results
        st.markdown(f"📝 Response: {result['messages'][-1].content}")

