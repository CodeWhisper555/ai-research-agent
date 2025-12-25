import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import SerperDevTool

# 1. Setup Gemini with explicit key mapping
# We use the 'google_api_key' parameter to be safe.
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# 2. Setup Search Tool
search_tool = SerperDevTool()

# 3. Define Agents
researcher = Agent(
    role='Market Researcher',
    goal='Find breakthroughs in {topic}',
    backstory='You are an expert at searching the web for tech news.',
    tools=[search_tool],
    llm=llm,
    verbose=True
)

writer = Agent(
    role='Content Writer',
    goal='Write a report on {topic}',
    backstory='You are a senior tech writer.',
    llm=llm,
    verbose=True
)

# 4. Define Tasks
research_task = Task(
    description='Research {topic} and find 3 key facts.',
    expected_output='Bullet points with sources.',
    agent=researcher
)

writing_task = Task(
    description='Write a summary based on the research.',
    expected_output='A 3-paragraph executive summary.',
    agent=writer
)

# 5. The Crew (FIXED SECTION)
research_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    # 🚨 CRITICAL FIX: 
    # We turn off "planning" or tell it to use Gemini for planning
    planning=True,
    planning_llm=llm, 
    verbose=True
)

if __name__ == "__main__":
    print("🚀 Starting the Crew with Gemini...")
    result = research_crew.kickoff(inputs={'topic': 'AI Agent Trends 2025'})
    print("\n\n########################")
    print("## FINAL REPORT ##")
    print(result)
