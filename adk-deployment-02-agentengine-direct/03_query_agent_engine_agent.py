import vertexai
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search  # Import the tool
from vertexai import agent_engines

load_dotenv()

PROJECT_ID=os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION')
STAGING_BUCKET = f"gs://{os.getenv('STAGING_BUCKET')}"
AGENT_ENGINE_ID = os.getenv('REASONING_ENGINE_ID')

AGENT_ENGINE_RESOURCE_NAME = f"projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{AGENT_ENGINE_ID}"
remote_app = agent_engines.get(AGENT_ENGINE_RESOURCE_NAME)

##use
user_id = "u_456"
remote_session = remote_app.create_session(user_id=user_id)

for event in remote_app.stream_query(
    user_id=user_id,
    session_id=remote_session["id"],
    message="Napisz cos ciekawego o systolic arrays",
):
    print(event)
