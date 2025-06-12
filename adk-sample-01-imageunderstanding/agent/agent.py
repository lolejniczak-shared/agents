from google.adk.agents import SequentialAgent, LlmAgent
import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.genai import types
from google.adk.tools import agent_tool
from google.adk.tools import google_search
from google.adk.agents import SequentialAgent, ParallelAgent, LlmAgent, LoopAgent
from pydantic import BaseModel
from pydantic import Field

load_dotenv()

MODEL = "gemini-2.0-flash-001"
AGENT_APP_NAME = 'writer_assistant'

instruction = """
You are Retail Shelf Auditor acting as an expert in computer vision. 
It must accurately interpret the visual data within the image, recognizing shelves with breadtuff, different types of bread products, and, most importantly, the empty spaces where products should be.
Instructions: 

Step 1: Initial Assessment

First, determine if the shelves designated for bread products are well-stocked or appear depleted.
Identify any large, empty spaces where bread products are clearly missing HOWEVER take into account that YOU CAN NOT stack products one on the other.
Note any areas where the bread is disorganized or sparse.
Neglect shelves with products which do not belog to breadstuff category. 

Step 2: Coverage Estimation

Based on your initial assessment, estimate how many additional items you would be able to put on every shelf. 
Based on this number estimate the percentage of the shelf space that is currently filled with breadstuff.
Categorize your estimation into one of the following ranges BUT provide justification for every range.
a) 0-20% (Very empty)
b) 20-40% (Significant gaps)
c) 40-60% (Moderately stocked)
d) 60-80% (Well-stocked with minor gaps)
e) 80-100% (Fully or almost fully stocked)

Step 3: Summary

Provide a brief summary of your findings, starting with the overall assessment of how well-equipped the shelves are, followed by the number of items you think would be added in total and estimated coverage range wit hreasoning about every option. 
Format output as JSON with keys: summary, coverage_20_resoning, coverage_40_resoning, coverage_60_reasoning, coverage_80_reasoning, coverage_100_reasoning, selected_coverage, missing_pieces. 
"""
number_of_auditors = 3
auditors = []
for i in range(number_of_auditors):
    auditor = LlmAgent(name=f"Auditor{i}", 
    model = MODEL, 
    instruction=instruction, 
    output_key=f"audit_result_{i}")
    auditors.append(auditor)

gather_concurrently = ParallelAgent(
    name="ConcurrentFetch",
    sub_agents=auditors
)

aggregator = LlmAgent(
    model = MODEL,
    name="Synthesizer",
    instruction="""Combine assessments from all auditors. 
    Review every summary and corresponding sumamry. 
    Provide short summary of results. 
    Make sure final coverage is one of the ranges:
    a) 0-20% (Very empty)
    b) 20-40% (Significant gaps)
    c) 40-60% (Moderately stocked)
    d) 60-80% (Well-stocked with minor gaps)
    e) 80-100% (Fully or almost fully stocked) 
    Finally, generate final response as JSON with key: final_summary, final_coverage.
    """
)

review = SequentialAgent(
    name="FetchAndSynthesize",
    sub_agents=[gather_concurrently, aggregator] # Run parallel fetch, then synthesize
)



##class InputSchema(BaseModel):
##    country: str = Field(description="The country to find the capital of.")

class OutputSchema(BaseModel):
    final_coverage: str = Field(description="The final decision about coverage")
    final_summary: str = Field(description="The final summary of the results")



generate_answer = LoopAgent(
    name="WritigRefinementLoop",
    max_iterations=2,
    sub_agents=[review],
)

structure_answer = Agent(
    model=MODEL,
    name="stuctur",
    instruction="""Structure final answer as JSON""",
    description="""You are agent responsible for structuring the final answer""",
    ##input_schema=InputSchema,
    output_schema=OutputSchema,
)

root_agent = SequentialAgent(
    name="main",
    sub_agents=[generate_answer, structure_answer] # Run parallel fetch, then synthesize
)


