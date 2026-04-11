from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv
import os
from langchain_core.tools import Tool
from langchain.tools import tool
#load_dotenv()
#serpapi_key = os.getenv("SERPAPI_API_KEY")


#os.environ["SERPAPI_API_KEY"] = serpapi_key


serpapi_key="77b5c56c9561a90537a44313904fad032f773567630814582bcac8de56b5d7e2"
if not serpapi_key:
    raise ValueError(
        "SERPAPI_API_KEY environment variable is not set. "
        "Please set it in your .env file or pass it as an environment variable."
    )
search_wrapper = SerpAPIWrapper(serpapi_api_key=serpapi_key)

@tool
def google_search(query: str) -> str:
    """Search Google for current information."""
    try:
        # Explicitly pass query to avoid empty strings
        if not query:
            return "Error: Empty search query."
        return search_wrapper.run(query)
    except Exception as e:
        # Log the error to your console so you know WHY it failed
        print(f"SerpAPI Error: {e}") 
        return f"Error: The search tool is currently unavailable. Please rephrase."

from langchain_classic.tools.retriever import create_retriever_tool


search = Tool(
    name="google_search",
    description="Search Google for current information.",
    func=search_wrapper.run # Note: passing the function itself
)
