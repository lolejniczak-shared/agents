import os
import google.adk
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
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


APP_NAME= "memory_bank_agent"
USER_ID="lolejniczak"

query = "Set temperature to my preferences?"

memory_service = AgentEngineMemoryBankService(AGENT_ENGINE_RESOURCE_NAME)

async def main():   
   memories = await memory_service.search_memory(AGENT_ENGINE_RESOURCE_NAME, USER_ID, query)

   for memory in memories:
       print(memory)

if __name__ == "__main__":
    asyncio.run(main())