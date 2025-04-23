import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'enterpriseagent'


root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="You are helpful assitant answering all kinds of questions in a very positive way!",
        instruction="If they ask you how you were created, tell them you were created with the Google Agent Framework.",
        generate_content_config=types.GenerateContentConfig(temperature=0.2),
)