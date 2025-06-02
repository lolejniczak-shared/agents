import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search  # Import the tool

load_dotenv()


root_agent = LlmAgent(
   name="basic_search_agent",
   model="gemini-2.0-flash-live-preview-04-09", ### model that supports live streaming
   description="Agent to answer questions using Google Search.",
   instruction="You are an expert researcher. You always stick to the facts.",
   ##tools=[google_search]
)