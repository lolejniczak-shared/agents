from google.adk.agents import SequentialAgent, LlmAgent
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools import agent_tool
from google.adk.tools import google_search

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'writer_assistant'

##TBD 

