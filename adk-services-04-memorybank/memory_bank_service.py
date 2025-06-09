from google import adk
from google.adk.memory import BaseMemoryService
from google.auth import default
from  google.auth.transport.requests import Request
from google.genai import types
from google.adk.memory.base_memory_service import SearchMemoryResponse, MemoryEntry
import pprint
import requests
from google.adk.sessions import Session

class AgentEngineMemoryBankService(BaseMemoryService):
  """Memory service for Agent Engine Memory Bank."""

  def __init__(self, agent_engine_name):
    ##The name should be in the following format: projects/{your project}/locations/{your location}/reasoningEngine/{your Agent Engine ID}
    self.agent_engine_name = agent_engine_name
    self.url = f"https://us-central1-aiplatform.googleapis.com/v1beta1/{self.agent_engine_name}"
    self.credentials, _ = default()

  async def add_session_to_memory(self, session: Session):
    """Adds a session to Agent Engine Memory Bank.

    A session can be added multiple times during its lifetime.

    Args:
        session: The session to add.
    """
    auth_req = Request()
    self.credentials.refresh(auth_req)

    response = requests.post(
        url=f"{self.url}/memories:generate",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {self.credentials.token}",
        },
        json={
            "vertex_session_source": {
                "session": f"{self.agent_engine_name}/sessions/{session.id}"
            }
        }
    )
    ##print(response)
    return response
 
  async def search_memory(
      self, app_name: str, user_id: str, query: str
  ) -> adk.memory.base_memory_service.SearchMemoryResponse:
    """Searches for memories that match the query."""
    auth_req = Request()
    self.credentials.refresh(auth_req)

    filter = f"userId=%22{user_id}%22"

    response = requests.get(
        url=f"{self.url}/memories?filter={filter}",
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {self.credentials.token}",
        },
    )

    memory_events = []
    for memory in response.json().get("memories", []):
        memory_events.append(
            MemoryEntry(
                author="user",
                content=types.Content(
                  parts=[types.Part(text=memory.get("fact"))],
                  role="user"),
                timestamp=memory.get("updateTime")
            )
        )

    return SearchMemoryResponse(memories=memory_events)