import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import SerperDevTool

# 1. Setup the Environment
# This line "tricks" CrewAI into using your Gemini key for internal planning
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

# 2. Initialize the Brain (Gemini 1.5 Flash)
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# 3. Setup the Eyes (Search Tool)
search_tool = SerperDevTool()

# 4. Define Agents
researcher = Agent(
    role='Lead Market Researcher',
    goal='Uncover breakthroughs in {topic}',
    backstory="You are an expert researcher at a top-tier tech firm.",
    tools=[search_tool],
    llm=llm,
    verbose=True
)

writer = Agent(
    role='Senior Technical Writer',
    goal='Write a report on {topic}',
    backstory="You specialize in executive summaries for leadership teams.",
    llm=llm,
    verbose=True
)

# 5. Define Tasks
research_task = Task(
    description='Find 3 key developments in {topic} for 2025.',
    expected_output='A list of 3 bullet points with sources.',
    agent=researcher
)

writing_task = Task(
    description='Create an executive report based on the findings.',
    expected_output='A 3-paragraph Markdown report.',
    agent=writer
)

# 6. The Crew - WITH EXPLICIT PLANNING MODEL
my_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    planning=True,
    planning_llm=llm, # <--- THIS IS THE KEY: Use Gemini for planning!
    verbose=True
)

if __name__ == "__main__":
    print("🚀 Starting the AI Research Crew (Using Gemini)...")
    result = my_crew.kickoff(inputs={'topic': 'AI Agentic Workflows'})
    print("\n\n" + "#"*30 + "\n## FINAL REPORT ##\n" + "#"*30 + "\n")
    print(result)
