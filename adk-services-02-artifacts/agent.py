import os
from dotenv import load_dotenv
from google.genai import types, Client
from google.adk.tools import agent_tool
from google.adk.agents import LlmAgent, BaseAgent
from google import genai
from google.adk.events import Event
from google.adk.tools import load_artifacts
from google.adk.tools import ToolContext
from google.adk.tools import FunctionTool

## Exper agent (Artist) as tool: Genrate images ...... 
## generate image of a cat sitting on a coach in front of tv eating popcorn

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'artistagent'


client = Client()

async def generate_image(prompt: str, tool_context: 'ToolContext'):
  """Generates an image based on the prompt."""
  response = client.models.generate_images(
      model='imagen-3.0-generate-002',
      prompt=prompt,
      config={'number_of_images': 1},
  )
  if not response.generated_images:
    return {'status': 'failed'}
  image_bytes = response.generated_images[0].image.image_bytes
  await tool_context.save_artifact(
      'user:image.png',
      types.Part.from_bytes(data=image_bytes, mime_type='image/png'),
  )
  return {
      'status': 'success',
      'detail': 'Image generated successfully and stored in artifacts.',
      'filename': 'image.png',
  }


async def list_user_files_py(tool_context: ToolContext) -> str:
    """Tool to list available artifacts for the user."""
    try:
        available_files = await tool_context.list_artifacts()
        if not available_files:
            return "You have no saved artifacts."
        else:
            # Format the list for the user/LLM
            file_list_str = "\n".join([f"- {fname}" for fname in available_files])
            return f"Here are your available Python artifacts:\n{file_list_str}"
    except ValueError as e:
        print(f"Error listing Python artifacts: {e}. Is ArtifactService configured?")
        return "Error: Could not list Python artifacts."
    except Exception as e:
        print(f"An unexpected error occurred during Python artifact list: {e}")
        return "Error: An unexpected error occurred while listing Python artifacts."


list_files_tool = FunctionTool(func=list_user_files_py)

# Parent agent uses the AgentTool
root_agent = LlmAgent(
    name=AGENT_APP_NAME,
    model=MODEL,
    description="""An agent that generates images and answer questions about the images.""",
    instruction="""You are an agent whose job is to generate or edit an image based on the user's prompt.""",
    tools=[generate_image, load_artifacts, list_files_tool],
)