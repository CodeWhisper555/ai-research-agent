import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

# 1. Environment Setup
# We set a dummy key to bypass CrewAI's internal OpenAI check.
os.environ["OPENAI_API_KEY"] = "NA" 
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# 2. Define Gemini 1.5 Flash
# Changed to 'gemini-1.5-flash-latest' to resolve the 404 API error
gemini_llm = LLM(
    model="gemini/gemini-1.5-flash-latest",
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

# 3. Setup Tools
search_tool = SerperDevTool()

# 4. Define Agents
researcher = Agent(
    role='Market Researcher',
    goal='Find 3 major AI agent trends for 2025',
    backstory='You are an expert at technical trend analysis.',
    tools=[search_tool],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role='Technical Writer',
    goal='Summarize the research into a short report',
    backstory='You translate complex data into readable summaries.',
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

# 5. Define Tasks
research_task = Task(
    description='Analyze the current state of {topic} for 2025.',
    expected_output='A bulleted list of 3 key insights.',
    agent=researcher
)

writing_task = Task(
    description='Write a 2-paragraph summary based on the research.',
    expected_output='A professional markdown report.',
    agent=writer
)

# 6. Assemble the Crew
# planning=False is used to prevent the background OpenAI planner from triggering
research_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    planning=False, 
    verbose=True
)

if __name__ == "__main__":
    print("🚀 Starting the Gemini Research Crew...")
    try:
        result = research_crew.kickoff(inputs={'topic': 'AI Agentic Workflows'})
        print("\n\n########################")
        print(result)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
