import vertexai
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search  # Import the tool
from vertexai import agent_engines
from agentspace_manager import AgentspaceManager

load_dotenv()

##PROJECT_ID=os.getenv('GOOGLE_CLOUD_PROJECT')
PROJECT_ID=os.getenv('GOOGLE_CLOUD_PROJECT_NUMBER')
LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION')
AGENT_ENGINE_ID = os.getenv('REASONING_ENGINE_ID')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
AGENTSPACE_APP_ID = os.getenv('AGENTSPACE_APP_ID')
AGENT_ENGINE_RESOURCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{AGENT_ENGINE_ID}"
AGENT_AUTH_OBJECT_ID = os.getenv('AGENT_AUTH_OBJECT_ID')


client = AgentspaceManager(project_id=PROJECT_ID,app_id=AGENTSPACE_APP_ID)


resp = client.register_agent(
        auth_ids=[AGENT_AUTH_OBJECT_ID],
        display_name = "v2HelloWorldWithStatusupdates",
        description = "Agent that answers questions about the world",
        tool_description = "Agent that answers questions about the world",
        adk_deployment_id = AGENT_ENGINE_ID,
        icon_uri="https://raw.githubusercontent.com/google/material-design-icons/master/src/action/android/materialicons/24px.svg"
)

print(resp)
