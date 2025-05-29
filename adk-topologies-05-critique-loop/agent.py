from google.adk.agents import SequentialAgent, LlmAgent
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools import agent_tool
from google.adk.tools import google_search
from google.adk.agents import LoopAgent, LlmAgent, BaseAgent
from google.adk.events import Event, EventActions
from google.adk.agents.invocation_context import InvocationContext
from typing import AsyncGenerator

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'writer_assistant'

generator = LlmAgent(
    model=MODEL,
    name="DraftWriter",
    instruction="""You are science journalist and write articles for a user. Read state['draft_text'] (if exists) and feedback state['feedback']. 
    Write a new draft taking into account provided feedback. 
    Save article draft to state['draft_text']""",
    description="Agent that is responsible for generating articles.",
    output_key="draft_text"
)

reviewer = LlmAgent(
    model=MODEL,
    name="Critique",
    instruction="""Review draft or article in state['draft_text'] for factual scientific accuracy and how informative it is to the target audience. 
    Specify what should be improved. Save review status to  state['review_status'] as 'valid' or 'invalid'. 
    Save your constructive feedback as state['feedback'].""",
    description="Agent that is responsible for constructive critique of the provided text",
    output_key="review_status",
    tools=[google_search]
)



class CheckStatusAndEscalate(BaseAgent):
    async def _run_async_impl(self, ctx: InvocationContext) -> AsyncGenerator[Event, None]:
        print(f"--------------------")
        status = ctx.session.state.get("review_status", "invalid")
        print(f"Status: {status}")
        should_stop = (status == "valid")
        print(f"Should stop: {should_stop}")
        print(f"--------------------")
        yield Event(author=self.name, actions=EventActions(escalate=should_stop))

refinement_loop = LoopAgent(
    name="WritigRefinementLoop",
    max_iterations=5,
    sub_agents=[generator, reviewer, CheckStatusAndEscalate(name="StopChecker")],
)

writer_agent_as_tool = agent_tool.AgentTool(agent=refinement_loop) 

root_agent = LlmAgent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="Writes an initial document and then iteratively refines it with critique using an exit tool.",
        instruction="You are helpful assistant to writers",
        sub_agents = [refinement_loop]
)