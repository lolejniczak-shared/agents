import vertexai
from vertexai.preview import example_stores
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
REGION = os.getenv('GOOGLE_CLOUD_LOCATION')
USE_VERTEXAI = os.getenv('GOOGLE_GENAI_USE_VERTEXAI')

vertexai.init(
    project=PROJECT_ID,
    location=REGION
)

my_example_store = example_stores.ExampleStore.create(
    example_store_config=example_stores.ExampleStoreConfig(
        vertex_embedding_model="text-multilingual-embedding-002"
    )
)

print(my_example_store.resource_name)
## 'projects/680248386202/locations/us-central1/exampleStores/8404051156208189440'
