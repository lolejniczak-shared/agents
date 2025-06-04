import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.agents import LlmAgent
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

load_dotenv()

root_agent = LlmAgent(
    model="gemini-2.0-flash",
    name='stateful_agent',
    instruction="""You are Helpful HomeAssistant. You dont have tools so always assume you are able to use hypithetical tool representing the living room thermostat.""",
    tools=[PreloadMemoryTool()]
)