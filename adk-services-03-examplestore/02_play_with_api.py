from google.genai import types
from google import genai
from dotenv import load_dotenv
import os
import requests


load_dotenv()

PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
REGION = os.getenv('GOOGLE_CLOUD_LOCATION')
USE_VERTEXAI = os.getenv('GOOGLE_GENAI_USE_VERTEXAI')

get_exchange_rate_func = types.FunctionDeclaration(
    name="get_exchange_rate",
    description="Get the exchange rate for currencies between countries",
    parameters={
    "type": "object",
    "properties": {
        "currency_date": {
            "type": "string",
            "description": "A date that must always be in YYYY-MM-DD format or the value 'latest' if a time period is not specified"
        },
        "currency_from": {
            "type": "string",
            "description": "The currency to convert from in ISO 4217 format"
        },
        "currency_to": {
            "type": "string",
            "description": "The currency to convert to in ISO 4217 format"
        }
    },
         "required": [
            "currency_from",
      ]
  },
)


client = genai.Client(
    http_options=types.HttpOptions(api_version="v1"),
    vertexai=USE_VERTEXAI,
    project=PROJECT_ID,
    location=REGION
)


question = "What is the exchange rate from polish Zloty to US dollars from yesterday?"

user_content = types.Content(
  role="user",
  parts=[types.Part(text=question)],
)

response = client.models.generate_content(
  model="gemini-2.0-flash",
  contents = user_content,
  config=types.GenerateContentConfig(
  tools=[types.Tool(function_declarations=[get_exchange_rate_func])],
  system_instruction=[types.Part.from_text(text="""You are currency exchange expert. Your goal is to assist users and answer their questions. Today is 18.04.2025""")],
  )
)

print(response) ##FunctionCall


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

print("-----------------------------------")
fc_response = get_exchange_rate(currency_from = 'PLN', currency_to = 'USD', currency_date = 'latest')
print(fc_response) ##FunctionResponse

##FunctionCall
##FunctionResponse
