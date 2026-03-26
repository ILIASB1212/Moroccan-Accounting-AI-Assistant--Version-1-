import sys
from pathlib import Path
project_root = Path(__file__).parent.parent 
sys.path.insert(0, str(project_root))

from langchain_core.messages import HumanMessage, SystemMessage
import streamlit as st
from dotenv import load_dotenv
import io
from utils.upload_parametre import read_file_content
from src.agent import graph_builder
load_dotenv()

# Streamlit setup
st.title("Simple LangGraph Test")

config = {"configurable": {"thread_id": "AAA"}}

# File uploader - accept multiple file types
uploaded_files = st.file_uploader(
    "Choose a file", 
    type=['txt', 'pdf', 'docx',"png","JPEG"],
    accept_multiple_files=False
)

# Display file info if uploaded
if uploaded_files is not None:
    st.info(f"📄 File loaded: {uploaded_files.name} ({uploaded_files.type})")

# Chat input
test_message = st.chat_input("Enter your query")

# Button to run test
if test_message:
    st.write(f"**Your query:** {test_message}")
    with st.spinner("generating"):
        # Process uploaded files if they exist
        file_content = ""
        if uploaded_files is not None:
            file_content = read_file_content(uploaded_files)
            
            if file_content:
                # Combine file content with the query
                enhanced_query = f"""Here is the file uploaded content: {file_content} , User query: {test_message}"""
            else:
                enhanced_query = test_message
                
        else:
            enhanced_query = test_message
        
        try:
            # Invoke the graph builder
            result = graph_builder.invoke(
                {'messages': HumanMessage(content=enhanced_query)},
                config=config
            )
            
            # Checking tool calling if and else
            if result["messages"][1].tool_calls:
                for tool_call in result["messages"][1].tool_calls:
                    st.write(f"the source: {tool_call['name']}")
                    st.markdown(f"Response: 📝 {result['messages'][-1].content}")
            else:
                st.write("the source: LLM (no tools used)")
                st.markdown(f"Response: 📝 {result['messages'][-1].content}")
            
        except Exception as e:
            st.error(f"Error processing your request: {str(e)}")
            st.exception(e)  # This will show the full traceback for debugging