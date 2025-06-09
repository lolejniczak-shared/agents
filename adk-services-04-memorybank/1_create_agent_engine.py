import os
from dotenv import load_dotenv
from google.auth import default, transport
from google.auth.transport.requests import Request
import requests




load_dotenv()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
REGION = os.getenv('GOOGLE_CLOUD_LOCATION')
USE_VERTEXAI = os.getenv('GOOGLE_GENAI_USE_VERTEXAI')
MEMOERY_GENERATION_MODEL_NAME="gemini-2.0-flash"
EMBEDDING_MODEL_NAME="text-multilingual-embedding-002"

creds, project_id = default()
auth_req = Request()  # Use google.auth here
creds.refresh(auth_req)

url = f"https://{REGION}-aiplatform.googleapis.com/v1beta1/projects/{PROJECT_ID}/locations/{REGION}/reasoningEngines"

response = requests.post(
    url=url,
    json={
        "contextSpec": {
            "memoryBankConfig": {
                "generationConfig": {
                    "model": f"projects/{PROJECT_ID}/locations/{REGION}/publishers/google/models/{MEMOERY_GENERATION_MODEL_NAME}"
                },
                "similaritySearchConfig": {
                    "embeddingModel": f"projects/{PROJECT_ID}/locations/{REGION}/publishers/google/models/{EMBEDDING_MODEL_NAME}"
                }
            }
        }
    },
    headers={
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {creds.token}"
    }

)
resp = response.json()
print(resp)

split_name = resp["name"].split("/")
agent_engine_name = "/".join(split_name[:-2])
print(agent_engine_name)