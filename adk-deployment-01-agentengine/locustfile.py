import os
import time
import uuid
from locust import HttpUser, task, between
import os
from google import auth as google_auth
from google.auth.transport import requests as google_requests
from dotenv import load_dotenv
from vertexai import agent_engines
import vertexai

load_dotenv()

PROJECT_ID=os.getenv('GOOGLE_CLOUD_PROJECT')
LOCATION = os.getenv('GOOGLE_CLOUD_LOCATION')
STAGING_BUCKET = f"gs://{os.getenv('STAGING_BUCKET')}"
REASONING_ENGINE_ID = os.getenv('REASONING_ENGINE_ID')


# --- Authentication ---
# This function retrieves a fresh identity token from Google.
def get_identity_token():
    """Gets a Google-signed identity token."""
    try:
        credentials, _ = google_auth.default()
        auth_request = google_requests.Request()
        credentials.refresh(auth_request)
        print("Successfully refreshed identity token.")
        return credentials.token
    except Exception as e:
        print(f"FATAL: Could not get Google credentials. "
              f"Ensure you have run 'gcloud auth application-default login'. Error: {e}")
        # In a real test, you might want to exit if auth fails globally.
        return None

class AgentEngineRestUser(HttpUser):
    """
    A user that sends standard queries to the AgentEngine via the REST API.
    """
    # Each user will wait 1-5 seconds between tasks.
    wait_time = between(1, 5)

    # Set the host, which is the base URL for all requests.
    host = f"https://{LOCATION}-aiplatform.googleapis.com"

    def on_start(self):
        """
        Called when a new user starts. Handles setup like authentication.
        """
        self.user_id = f"locust-user-{uuid.uuid4()}"
        self.session_id = f"session-{uuid.uuid4()}"
        
        try:
            token = get_identity_token()
            if not token:
                self.stop() # Stop this user if token generation failed.

            # This header will be used for all subsequent requests by this user.
            self.client.headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json; charset=utf-8",
            }
        except Exception as e:
            print(f"Authentication failed for user: {e}")
            self.stop()

    @task
    def agent_query(self):
        """
        Defines the main user task: making a standard (non-streaming) query.
        """
        # The API endpoint path for a standard query.
        url = f"/v1/projects/{PROJECT_ID}/locations/{LOCATION}/reasoningEngines/{REASONING_ENGINE_ID}:streamQuery?alt=sse"

        # The data payload for the request.
        self.user_id = f"locust-user-{uuid.uuid4()}"
        payload = {
             "class_method": "stream_query", # This key is often optional for the default query method
             "input": {
                "user_id": self.user_id,
                ##"session_id": self.session_id,
                "input": "What is the capital of Poland?"
             }
        }

        # For a standard request, this is all you need. Locust handles the timing,
        # success, and failure reporting automatically.
        self.client.post(url, json=payload)