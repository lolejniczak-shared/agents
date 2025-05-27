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


## Genrate images ...... 
load_dotenv()



MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'hrmanager'

GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')

auth_scheme = OAuth2(
    flows=OAuthFlows(
        authorizationCode=OAuthFlowAuthorizationCode(
            authorizationUrl="https://accounts.google.com/o/oauth2/auth",
            tokenUrl="https://oauth2.googleapis.com/token",
            scopes={
                "openid": "openid",
                "https://www.googleapis.com/auth/cloud-platform": "cloud platform",
                "https://www.googleapis.com/auth/userinfo.email": "user email",
                "https://www.googleapis.com/auth/userinfo.profile": "user profile"
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

print(openapi_schema)

toolset = OpenAPIToolset(
    spec_str=openapi_schema, 
    spec_str_type="yaml",
    auth_credential=auth_credential,
    auth_scheme=auth_scheme
)


root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="You are HR manager",
        instruction="You are helpful assistant answering questions about users. Whenever asked about 'me', 'my' use People API ",
        tools=[toolset.get_tool("people_get")]
)