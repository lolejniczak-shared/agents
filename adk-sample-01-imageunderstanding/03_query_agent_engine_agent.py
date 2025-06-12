import vertexai
import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools import google_search  # Import the tool
from vertexai import agent_engines
import json

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


image_gcs_uri = "gs://zabka-pieczywo/audyt_pieczywo3.jpg"

image_message = {
    "role": "user",
    "parts": [
        {
            "file_data": {
                "file_uri": image_gcs_uri,
                "mime_type": "image/jpg",
            },
        },
        {
            "text": "Audit based on this image",
        },
    ]
}

fevent = None
for event in remote_app.stream_query(
    user_id=user_id,
    session_id=remote_session["id"],
    message=image_message,
):
   fevant = event

final_response = event["content"]["parts"][0]["text"]
final_response_as_json = json.loads(final_response)
print(final_response_as_json)

