import vertexai
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search  # Import the tool
from vertexai import agent_engines
from agentspace_manager import AgentspaceManager

load_dotenv()

PROJECT_ID=os.getenv('GOOGLE_CLOUD_PROJECT_NUMBER')
LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION')
AGENT_ENGINE_ID = os.getenv('REASONING_ENGINE_ID_4_AGENTOAUTH')
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
AGENTSPACE_APP_ID = os.getenv('AGENTSPACE_APP_ID')
AGENT_ENGINE_RESOURCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{AGENT_ENGINE_ID}"
AGENT_AUTH_OBJECT_ID = os.getenv('AGENT_AUTH_OBJECT_ID')

auth_object_id = AGENT_AUTH_OBJECT_ID

client = AgentspaceManager(project_id=PROJECT_ID,app_id=AGENTSPACE_APP_ID)

auth_uri = client.generate_auth_uri(
    base_auth_uri="https://accounts.google.com/o/oauth2/v2/auth",
    client_id=GOOGLE_CLIENT_ID,
    scopes=["openid",
            "https://www.googleapis.com/auth/drive.readonly",
            "https://www.googleapis.com/auth/drive.metadata",
            ]
)

resp = client.create_authorization(auth_id=auth_object_id, 
            client_id = GOOGLE_CLIENT_ID, 
            client_secret= GOOGLE_CLIENT_SECRET,
            auth_uri=auth_uri,
            token_uri="https://oauth2.googleapis.com/token"
            )
##print response
print(resp)


"""
##delete
resp = client.delete_authorization(auth_id=auth_object_id)
##print response
print(resp)
"""


