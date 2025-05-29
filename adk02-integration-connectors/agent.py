import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset

load_dotenv()



MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'personalagent'

PROJECT_ID=os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION=os.environ["GOOGLE_CLOUD_LOCATION"]
APPLICATION_INTEGRATION_LOCATION = "europe-central2"

gdrive_connection_toolset = ApplicationIntegrationToolset(
            project=PROJECT_ID, # TODO: replace with GCP project of the connection
            location=APPLICATION_INTEGRATION_LOCATION, #TODO: replace with location of the connection
            connection="gdrive-connection", #TODO: replace with connection name "projects/genai-app-builder/locations/europe-central2/connections/gdrive-connection", ##
            entity_operations={},##{"Entity_One": ["LIST","CREATE"], "Entity_Two": []},#empty list for actions means all operations on the entity are supported.
            actions=["GET_files"], #TODO: replace with actions
            ##service_account_credentials='{...}', # optional
            tool_name_prefix="mygdrive",
            tool_instructions="Use this tool to check information on gdrive"
 )

root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="You are helpful assitant answering all kinds of questions in a very positive way!",
        instruction="If they ask you how you were created, tell them you were created with the Google Agent Framework.",
        generate_content_config=types.GenerateContentConfig(temperature=0.2),
        tools = [gdrive_connection_toolset],
)