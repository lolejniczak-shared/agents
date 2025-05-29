from google.adk.agents import Agent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from dotenv import load_dotenv
import requests
import os

from vertexai.preview import example_stores
from google.adk.examples import VertexAiExampleStore
from google.adk.tools import ExampleTool

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'basic_agent'
EXAMPLE_STORE= os.getenv('EXAMPLE_STORE')

def get_exchange_rate(
        currency_from: str = "USD",
        currency_to: str = "EUR",
        currency_date: str = "latest",
    ):
            """Retrieves the exchange rate between two currencies on a specified date.

            Uses the Frankfurter API (https://api.frankfurter.app/) to obtain exchange rate data.

            Args:
                currency_from: The base currency (3-letter currency code). Defaults to "USD" (US Dollar).
                currency_to: The target currency (3-letter currency code). Defaults to "EUR" (Euro).
                currency_date: The date for which to retrieve the exchange rate. Defaults to "latest" for the most recent exchange rate data. Can be specified in YYYY-MM-DD format for historical rates.

            Returns:
                dict: A dictionary containing the exchange rate information.
                    Example: {"amount": 1.0, "base": "USD", "date": "2023-11-24", "rates": {"EUR": 0.95534}}
            """

            response = requests.get(
                f"https://api.frankfurter.app/{currency_date}",
                params={"from": currency_from, "to": currency_to},
            )
            return response.json()

example_store = VertexAiExampleStore(EXAMPLE_STORE)
examples_tool = ExampleTool(example_store)

root_agent = Agent(
        model="gemini-1.5-flash-002",
        name='user_assistant',
        instruction="""
        You are helpful assistant. You provide answers on questions about currency exchange""",
        tools=[get_exchange_rate, examples_tool],
        examples = example_store #####!!!!!!! 
    )