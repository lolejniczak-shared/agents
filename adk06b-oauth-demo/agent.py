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
            authorizationUrl="https://allegro.pl.allegrosandbox.pl/auth/oauth/authorize",
            tokenUrl="https://allegro.pl.allegrosandbox.pl/auth/oauth/token",
            scopes={
                "allegro:api:sale:offers:read": "Odczyt danych o ofertach",
                "allegro:api:profile:read": "Odczyt danych osobowych z konta",
                "allegro:api:bids": "Składanie ofert kupna w licytacjach",
                "allegro:api:orders:read": "Odczyt informacji o zamówieniach",
                "allegro:api:ratings": "Odczyt ocen od kupujących"
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

environment = os.environ["environment"]
modified_schema_string = openapi_schema.replace('{environment}', environment)

##print(modified_schema_string)

toolset = OpenAPIToolset(
    spec_str=modified_schema_string, 
    spec_str_type="yaml",
    auth_credential=auth_credential,
    auth_scheme=auth_scheme
)

root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="You are helpful assitant answering all kinds of questions in a very positive way!",
        instruction="You are Allegro Merchant assistant. Use available tools to answer user questions",
        generate_content_config=types.GenerateContentConfig(temperature=0.2),
        tools = [toolset.get_tool("get_user_ratings_using_get")],
)