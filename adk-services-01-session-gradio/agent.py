## need access to session - run from colab
import asyncio
from google.adk.agents import Agent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai import types
from dotenv import load_dotenv
import gradio as gr

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'basic_agent'

async def get_response(runner, user_id, session_id,  message):
    content = types.Content(role='user', parts=[types.Part(text=message)])
    events = runner.run(user_id=user_id, session_id=session_id, new_message=content)
    final_response = None
    for _, event in enumerate(events):
        is_final_response = event.is_final_response()
        if is_final_response:
            final_response = event.content.parts[0].text
    return final_response




# Create InMemory services for session and artifact management
session_service = InMemorySessionService()
artifact_service = InMemoryArtifactService()


root_agent = Agent(
        model="gemini-1.5-flash-002",
        name='user_assistant',
        instruction="""
        You are helpful assistant. Your role is to answer user questions.
        Current user:
            <User>
            {user_info}
            </User>
            Current time: {time}.

        """,
        tools=[]
    )

_state = {
        "user_info": {
        "name": "Lukasz Olejniczak",
        "gender": "male",
        "occupation": "AI Specialist",
        "email": "lolejniczak@google.com",
        "phone": "1234567890"
        },
        "time": "2024-10-23T00:48:45.640722"
    }


runner = Runner(app_name=AGENT_APP_NAME, 
            agent=root_agent, 
            artifact_service=artifact_service,
            session_service=session_service)

session: Session = None

# --- Gradio Chat Function ---
async def chat_interface_fn(message, history):
    """
    This function is called by Gradio for each user message.
    It uses the global session and runner to interact with the agent.
    """
    if not session:
        raise gr.Error("Session not initialized. Please restart the application.")

    # Get the agent's response using the existing logic
    response = await get_response(runner, session.user_id, session.id, message)
    return response

# --- Main Application Setup ---
async def main():
    """
    Initializes the agent session and launches the Gradio web UI.
    """

    global session
    # Create a single, persistent session when the application starts
    session = await session_service.create_session(
        app_name=AGENT_APP_NAME,
        user_id="gradio_user",
        state=_state
    )
    print(f"✅ Session created successfully: {session.id}")

    # --- Gradio Interface Definition ---
    demo = gr.ChatInterface(
        fn=chat_interface_fn,
        chatbot=gr.Chatbot(
            type="messages"
        ),
        title="Agent Assistant Chat",
        description="Ask the assistant any question. It has access to your user information.",
        examples=[["What is my email address"]],
        cache_examples=False, # Set to True to pre-run and cache example outputs
    )

    # Launch the Gradio app
    demo.launch()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down Gradio app.")