import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

# 1. Ensure keys are set in the environment
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# 2. Define the Gemini LLM using CrewAI's native LLM class
# This is the most stable way to ensure agents use Gemini
gemini_llm = LLM(
    model="gemini/gemini-1.5-flash",
    api_key=os.getenv("GEMINI_API_KEY")
)

# 3. Initialize Search Tool
search_tool = SerperDevTool()

# 4. Define Agents
researcher = Agent(
    role='Expert Researcher',
    goal='Identify top 3 trends in {topic} for 2025',
    backstory='An expert in analyzing emerging technology trends.',
    tools=[search_tool],
    llm=gemini_llm,
    verbose=True
)

writer = Agent(
    role='Tech Summarizer',
    goal='Create a concise report on {topic}',
    backstory='A professional writer who excels at technical summaries.',
    llm=gemini_llm,
    verbose=True
)

# 5. Define Tasks
task1 = Task(
    description='Search for latest news regarding {topic}.',
    expected_output='A summary of 3 key findings.',
    agent=researcher
)

task2 = Task(
    description='Write a 2-paragraph summary based on the findings.',
    expected_output='A markdown formatted report.',
    agent=writer
)

# 6. Create the Crew
# CRITICAL: planning=False avoids the OpenAI API key error
research_crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    process=Process.sequential,
    planning=False, 
    verbose=True
)

if __name__ == "__main__":
    print("🚀 Starting Crew with Gemini...")
    result = research_crew.kickoff(inputs={'topic': 'AI Agentic Workflows'})
    print("\n\n########################")
    print("##    FINAL OUTPUT    ##")
    print("########################\n")
    print(result)
