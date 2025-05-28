from dotenv import load_dotenv
import os
import requests
from vertexai.preview import example_stores

load_dotenv()

PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
REGION = os.getenv('GOOGLE_CLOUD_LOCATION')
USE_VERTEXAI = os.getenv('GOOGLE_GENAI_USE_VERTEXAI')
EXAMPLE_STORE= os.getenv('EXAMPLE_STORE')

my_example_store = example_stores.ExampleStore(EXAMPLE_STORE)

resp = my_example_store.search_examples(
    parameters={
        "stored_contents_example_key": "What is the exchange rate between polish and EU?"
    },
    # Only fetch the most similar examaple. The default value is 3.
    top_k=1
)

print(resp)