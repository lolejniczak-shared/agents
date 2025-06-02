import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.auth import default
from google.auth.transport.requests import Request
import requests

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'enterpriseagent'


class DatastoreService:
    def __init__(self):
        creds, project_id = default()
        auth_req = Request()  # Use google.auth here
        creds.refresh(auth_req)
        access_token = creds.token
        self.access_token = access_token

    def search(self, vertexai_project_id, app_engine, query):
        # Define API endpoint and headers
        url = f"https://discoveryengine.googleapis.com/v1alpha/projects/{vertexai_project_id}/locations/global/collections/default_collection/engines/{app_engine}/servingConfigs/default_search:search"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        data = {
            "query": f"{query}",
            "pageSize": 50, ## how many results showuld be deisplayed under summary---
            "queryExpansionSpec": {"condition": "AUTO"},
            "spellCorrectionSpec": {"mode": "AUTO"},
            "contentSearchSpec": {
                "summarySpec": {
                    "ignoreAdversarialQuery": True,
                    "includeCitations": False,
                    "summaryResultCount": 10,   ## how many results should be taken into account when generating summarization
                    ##"modelSpec": {"version": "gemini-1.5-flash-001/answer_gen/v1"},
                    "languageCode": "pl"
                }
            }
        }

        # Make POST request
        response = requests.post(url, headers=headers, json=data)
        return response.json()


vertex_project_id = "genai-app-builder"
app_engine = "genai-retail_1697838978813"

def search_catalog(query: str):
        """
        Searches the product catalog using the DatastoreService.

        Args:
            query (str): The search query string.

        Returns:
            dict: The search results from the DatastoreService in JSON format.
        """
        # Initialize the DatastoreService
        datastore_service = DatastoreService()
        # Call the search method of the DatastoreService with the project ID, App Engine ID, and query
        results = datastore_service.search(vertex_project_id, app_engine, query) 
        # Return the search results
        return results


instruction_prompt = """
Use available tools to answer user question. 
The response should include markdown table with columns image, price, currency, title.
Render URL as image. 
Ensure the final output is valid Markdown.
"""

root_agent = Agent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="You are helpful shopping assitant answering user queries using available tools",
        instruction=instruction_prompt,
        generate_content_config=types.GenerateContentConfig(temperature=0.2),
        tools = [search_catalog]
)