import os
from dotenv import load_dotenv
from google.genai import types, Client
from google.adk.tools import agent_tool
from google.adk.agents import LlmAgent, BaseAgent
from google import genai
from google.adk.events import Event
from google.adk.tools import load_artifacts
from google.adk.tools import ToolContext
from google.adk.tools import FunctionTool

## Exper agent (Artist) as tool: Genrate images ...... 
## generate image of a cat sitting on a coach in front of tv eating popcorn

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'artistagent'

# Parent agent uses the AgentTool
root_agent = LlmAgent(
    name=AGENT_APP_NAME,
    model=MODEL,
    description="""An agent that generates images and answer questions about the images.""",
    instruction="""You are an agent whose job is to generate or edit an image based on the user's prompt.""",
    tools=[load_artifacts],
)