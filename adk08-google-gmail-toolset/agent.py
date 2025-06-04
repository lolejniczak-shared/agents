import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools.google_api_tool import GmailToolset

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'enterpriseagent'

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

gmail_toolset = GmailToolset(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET)

root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="You are helpful assitant orchestrating actions on google tools like gmail!",
        instruction="If they ask you how you were created, tell them you were created with the Google Agent Framework.",
        tools = [gmail_toolset]
)