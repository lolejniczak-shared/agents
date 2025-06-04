import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.agents import LlmAgent


#### Router with sub agents - experts

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'employee_assistant'

expert_marketing = LlmAgent(
        model=MODEL,
        name="marketing_expert",
        description="Agent to answer questions about marketing strategies",
        instruction="You are marketing specialist",
)

expert_cloud = LlmAgent(
        model=MODEL,
        name="google_cloud_expert",
        description="Agent to answer questions about google cloud",
        instruction="You are google cloud specialist",
)

expert_legal = LlmAgent(
        model=MODEL,
        name="legal_stuff_expert",
        description="Agent to answer questions about legal",
        instruction="You are legal specialist",
)


root_agent = LlmAgent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="You are assistant transfering questions to the best expert",
        instruction="Route user requests to best experts t oanswer questions",
       sub_agents = [expert_marketing, 
        expert_cloud, 
        expert_legal]
)