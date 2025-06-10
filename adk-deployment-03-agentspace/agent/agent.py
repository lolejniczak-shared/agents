import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import google_search  # Import the tool
from functools import partial
from typing import Optional
from google.genai import types
load_dotenv()

def update_ui_status(callback_context: CallbackContext, status_msg: str) -> Optional[types.Content]:
      """Updates the status of the execution on the Agentspace UI.
      Args:
      callback_context: The callback context.
      status_msg: The status message to display on the UI.
      """
      callback_context.state["ui:status_update"] = status_msg


root_agent = LlmAgent(
   name="basic_search_agent",
   model="gemini-2.0-flash-001", ### model that supports live streaming
   description="Agent to answer questions using Google Search.",
   instruction="You are an expert researcher. You always stick to the facts.",
   tools=[google_search],
   before_agent_callback=partial(
      update_ui_status, status_msg="Starting handling user question"
   ),
   after_agent_callback=partial(
      update_ui_status, status_msg="Answer generation complete"
   ),
)