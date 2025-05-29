from google.adk.agents import SequentialAgent, LlmAgent
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools import agent_tool
from google.adk.tools import google_search
from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'writer_assistant'


instruction = "You are creative marketing specialist with the goal to generate one new idea on the provided topic"
number_of_ideas = 10
creative_agents = []
for i in range(number_of_ideas):
    creative_agent = LlmAgent(name=f"Idea{i}", model = MODEL, instruction=instruction, output_key=f"idea{i}")
    creative_agents.append(creative_agent)


gather_concurrently = ParallelAgent(
    name="ConcurrentFetch",
    sub_agents=creative_agents
)

synthesizer = LlmAgent(
    model = MODEL,
    name="Synthesizer",
    instruction="Combine results from state keys and order them by their brilliance. Remove duplicates. Score every from 1 (nothing new) to 10 - genius"
)

overall_workflow = SequentialAgent(
    name="FetchAndSynthesize",
    sub_agents=[gather_concurrently, synthesizer] # Run parallel fetch, then synthesize
)

ideas_as_tool = agent_tool.AgentTool(agent=overall_workflow) 


root_agent = LlmAgent(
        model=MODEL,
        name=AGENT_APP_NAME,
        description="Use FetchAndSynthesize to generate and score new ideas",
        instruction="You are helpful assistant to marketing people generating new ideas",
        tools = [ideas_as_tool]
)