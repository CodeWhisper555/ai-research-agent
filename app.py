import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool # NEW: Import the search tool

# 1. Configuration 
# Note: Codespaces automatically makes GEMINI_API_KEY and SERPER_API_KEY 
# available as environment variables if you saved them in Secrets.
gemini_llm = LLM(
    model="gemini/gemini-3-flash-preview",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=1.0, 
    verbose=True
)

# NEW: Initialize the Serper search tool
# It will automatically look for the SERPER_API_KEY in your environment variables
search_tool = SerperDevTool()

# 2. Define Agents
researcher = Agent(
    role='Market Researcher',
    goal='Identify emerging trends in the AI industry for 2026',
    backstory='You are an expert analyst with a knack for spotting "the next big thing."',
    llm=gemini_llm,
    tools=[search_tool],  # NEW: The researcher can now use Google/Serper
    allow_delegation=False,
    verbose=True
)

writer = Agent(
    role='Content Strategist',
    goal='Write a compelling blog post about AI trends',
    backstory='You transform complex data into engaging narratives for a tech audience.',
    llm=gemini_llm,
    verbose=True
)

# 3. Define Tasks
task1 = Task(
    description='Analyze the top 3 AI trends based on recent late-2025 breakthroughs. Use your search tool to find actual events from the last 3 months.',
    expected_output='A bulleted list of 3 trends with a brief explanation for each.',
    agent=researcher
)

task2 = Task(
    description='Use the research to write a 3-paragraph blog post summary.',
    expected_output='A markdown-formatted blog post.',
    agent=writer
)

# 4. Form the Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True
)

# 5. Kickoff
print("### Starting the Crew Workflow with Web Search ###")
result = crew.kickoff()

print("\n\n########################")
print("## FINAL OUTPUT ##")
print("########################\n")
print(result)
