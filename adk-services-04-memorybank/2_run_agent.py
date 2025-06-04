import os
import google.adk
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService, VertexAiSessionService
from google.adk.runners import Runner
from agent import root_agent
from memory_bank_service import  AgentEngineMemoryBankService
from google.genai import types
import asyncio

load_dotenv()
PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
REGION = os.getenv('GOOGLE_CLOUD_LOCATION')
USE_VERTEXAI = os.getenv('GOOGLE_GENAI_USE_VERTEXAI')
AGENT_ENGINE_RESOURCE_NAME = os.getenv('AGENT_ENGINE_RESOURCE_NAME')


session_service = VertexAiSessionService(PROJECT_ID, REGION)
memory_service = AgentEngineMemoryBankService(AGENT_ENGINE_RESOURCE_NAME)

APP_NAME= "memory_bank_agent"
USER_ID="lolejniczak"

runner = Runner(
        agent=root_agent,
        app_name=AGENT_ENGINE_RESOURCE_NAME, ##???? 
        session_service=session_service,
        memory_service=memory_service)

async def call_agent(query, session, user_id):
  content = types.Content(role='user', parts=[types.Part(text=query)])
  events = runner.run(user_id=user_id, session_id=session, new_message=content)

  for event in events:
      if event.is_final_response():
          final_response = event.content.parts[0].text
          print("Agent Response: ", final_response)


async def main():   
    ##test - session1
    session1 = await session_service.create_session(
    app_name=AGENT_ENGINE_RESOURCE_NAME,
    user_id=USER_ID
    )

    await call_agent("Can you update the temperature to my preferred temperature?", session1.id, USER_ID)
    await call_agent("I like it at 71 degrees", session1.id, USER_ID)
    ##await runner.session_service.close_session(session1.id) ##When you close the session, ADK triggers a memory generation request based on the session's contents 
    await memory_service.add_session_to_memory(session1)


    ##test - session2
    session2 = await session_service.create_session(
    app_name= AGENT_ENGINE_RESOURCE_NAME,
    user_id=USER_ID
    )

    await call_agent("Set temperature to my preferences?", session2.id, USER_ID)

if __name__ == "__main__":
    asyncio.run(main())