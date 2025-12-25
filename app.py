import os
from crewai import Agent, Task, Crew, Process, LLM

# 1. Configuration - Use the model string you confirmed in AI Studio
# As of late 2025, 'gemini-3-flash-preview' is the stable string for this tier.
gemini_llm = LLM(
    model="gemini/gemini-3-flash-preview",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=1.0,  # Gemini 3 performs best at 1.0
    verbose=True
)

# 2. Define Agents
researcher = Agent(
    role='Market Researcher',
    goal='Identify emerging trends in the AI industry for 2026',
    backstory='You are an expert analyst with a knack for spotting "the next big thing."',
    llm=gemini_llm,
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
    description='Analyze the top 3 AI trends based on recent late-2025 breakthroughs.',
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
print("### Starting the Crew Workflow ###")
result = crew.kickoff()

print("\n\n########################")
print("## FINAL OUTPUT ##")
print("########################\n")
print(result)
