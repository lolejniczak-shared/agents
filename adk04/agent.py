import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.agents import Agent
from google.adk.tools.toolbox_tool import ToolboxTool


load_dotenv()

instruction_prompt = """
        You are a helpful agent who can answer user questions about the hotels in a specific city or hotels by name. Use the tools to answer the question"
        """


MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'travelexpert'

toolbox = ToolboxTool("https://dbtoolbox-680248386202.us-central1.run.app")

# Load single tool
# tools = toolbox.get_tool(tool_name='search-hotels-by-location'),
# Load all the tools
dbtools = toolbox.get_toolset(toolset_name='my_first_toolset')

root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="Agent to answer questions about hotels in a city or hotels by name.",
        instruction=instruction_prompt,
        tools=dbtools
)