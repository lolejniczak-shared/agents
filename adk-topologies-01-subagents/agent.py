import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.agents import LlmAgent


#### Router with sub agents - experts

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'employee_assistant'

expert_marketing = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="Agent to answer questions about marketing strategies",
        instruction="You are marketing specialist",
)

expert_cloud = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="Agent to answer questions about google cloud",
        instruction="You are google cloud specialist",
)

expert_legal = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="Agent to answer questions about legal",
        instruction="You are legal specialist",
)


root_agent = LlmAgent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="You are assistant routing questions to experts",
        instruction="You are helpful assistant that works with experts to answer user questions.",
       sub_agents = [expert_marketing, 
        expert_cloud, 
        expert_legal]
)