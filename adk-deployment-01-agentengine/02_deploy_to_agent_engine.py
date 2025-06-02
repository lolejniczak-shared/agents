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



##------- our agent

root_agent = LlmAgent(
   name="basic_search_agent",
   model="gemini-2.0-flash-001", ### model that supports live streaming
   description="Agent to answer questions using Google Search.",
   instruction="You are an expert researcher. You always stick to the facts.",
   tools=[google_search]
)


###------- our agent

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=STAGING_BUCKET,
)

##deploy 
remote_app = agent_engines.create(
    display_name = "Basic Search Agent",
    description = """
    This is basic ADK agent that generates answers using google search grounding
    """,
    agent_engine=root_agent,
    requirements=[
        "google-cloud-aiplatform[adk,agent_engines]==1.95",
        "google-adk==1.1.0"
        ],
)


##use
user_id = "u_456"
remote_session = remote_app.create_session(user_id=user_id)

for event in remote_app.stream_query(
    user_id=user_id,
    session_id=remote_session["id"],
    message="Napisz cos ciekawego o systolic arrays",
):
    print(event)


