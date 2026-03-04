from langchain_community.utilities import SerpAPIWrapper
from dotenv import load_dotenv
import os
from langchain_core.tools import Tool
load_dotenv()
serpapi_key = os.getenv("SERPAPI_API_KEY")
if not serpapi_key:
    raise ValueError(
        "SERPAPI_API_KEY environment variable is not set. "
        "Please set it in your .env file or pass it as an environment variable."
    )

os.environ["SERPAPI_API_KEY"] = serpapi_key
# Initialize the wrapper. It will use the SERPAPI_API_KEY environment variable.
search_wrapper = SerpAPIWrapper(params={'engine': 'google'})



search = Tool(
    name="google_search",
    description="Search Google for current information. Use this for questions about recent events, news, or facts.",
    func=search_wrapper.run
)



