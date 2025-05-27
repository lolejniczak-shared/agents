import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools.openapi_tool.openapi_spec_parser import rest_api_tool, OperationEndpoint
from fastapi.openapi.models import OAuth2
from fastapi.openapi.models import OAuthFlowAuthorizationCode
from fastapi.openapi.models import OAuthFlows
from google.adk.auth import AuthCredential
from google.adk.auth import AuthCredentialTypes
from google.adk.auth import OAuth2Auth
from google.adk.tools.openapi_tool.openapi_spec_parser.openapi_toolset import OpenAPIToolset
from .schemas import openapi_schema
from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset


load_dotenv()

### Using Integration Connector connectors with authentication  

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'gdrive_manager_with_auth'

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
PROJECT_ID=os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION=os.environ["GOOGLE_CLOUD_LOCATION"]
APPLICATION_INTEGRATION_LOCATION = "europe-central2"

auth_scheme = OAuth2(
    flows=OAuthFlows(
        authorizationCode=OAuthFlowAuthorizationCode(
            authorizationUrl="https://accounts.google.com/o/oauth2/auth",
            tokenUrl="https://oauth2.googleapis.com/token",
            scopes={
                "openid": "openid",
                "https://www.googleapis.com/auth/drive.readonly": "readonly",
                "https://www.googleapis.com/auth/drive.metadata": "metadata readonly",
                "https://www.googleapis.com/auth/cloud-platform": "cloud platform"
            },
        )
    )
)

auth_credential = AuthCredential(
    auth_type=AuthCredentialTypes.OAUTH2,
    oauth2=OAuth2Auth(
        client_id=GOOGLE_CLIENT_ID, 
        client_secret=GOOGLE_CLIENT_SECRET
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
            auth_credential=auth_credential,
            auth_scheme=auth_scheme
 )

root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="You are helpful assitant answering all kinds of questions in a very positive way!",
        instruction="If they ask you how you were created, tell them you were created with the Google Agent Framework.",
        generate_content_config=types.GenerateContentConfig(temperature=0.2),
        tools = [gdrive_connection_toolset],
)