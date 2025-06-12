import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.tools import google_search  # Import the tool
from functools import partial
from typing import Optional
from google.genai import types
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from fastapi.openapi.models import OAuth2
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.openapi.models import OAuthFlows
from google.adk.auth import AuthCredential
from google.adk.auth import AuthCredentialTypes
from google.adk.auth import OAuth2Auth
from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset
from google.adk.auth.auth_credential import HttpAuth
from google.adk.auth.auth_credential import HttpCredentials
from google.adk.events import Event
from google.adk.tools.tool_context import ToolContext



load_dotenv()

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
PROJECT_ID=os.environ["ADK_CLOUD_PROJECT"]
LOCATION=os.environ["ADK_CLOUD_LOCATION"]
APPLICATION_INTEGRATION_LOCATION = "europe-central2"


a= """
auth_credential = AuthCredential(
      auth_type=AuthCredentialTypes.HTTP,
      http=HttpAuth(
          scheme="bearer",
          credentials=HttpCredentials(token="eyAkaknabna...."),
      ),
)

gdrive_connection_toolset = ApplicationIntegrationToolset(
            project=PROJECT_ID, # TODO: replace with GCP project of the connection
            location=APPLICATION_INTEGRATION_LOCATION, #TODO: replace with location of the connection
            connection="gdrive-connector-with-auth", #TODO: replace with connection name "projects/genai-app-builder/locations/europe-central2/connections/gdrive-connection", ##
            entity_operations={},##{"Entity_One": ["LIST","CREATE"], "Entity_Two": []},#empty list for actions means all operations on the entity are supported.
            actions=["GET_files"], #TODO: replace with actions
            ##service_account_credentials='{...}', # optional
            tool_name_prefix="mygdrive",
            tool_instructions="Use this tool to work with gdrive",
            ##auth_credential=auth_credential,
            ##auth_scheme=auth_scheme
 )
 """

async def dump_state(prompt: str, tool_context: 'ToolContext'):
        """describe session"""
        key = tool_context.state.get['temp:orcas-authorization-test']
        return  Event(
            invocation_id=tool_context.invocation_id,
            author="tool",
            content=types.Content(role="model", parts=[types.Part(text=f"Keys: {key}")])
        )

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
   description="Agent to answer questions using available tools",
   instruction="You are an expert researcher. You always stick to the facts.",
   tools=[dump_state],
   before_agent_callback=partial(
      update_ui_status, status_msg="Starting handling user question"
   ),
   after_agent_callback=partial(
      update_ui_status, status_msg="Answer generation complete"
   ),
)