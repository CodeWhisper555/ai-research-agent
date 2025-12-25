import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import SerperDevTool

# 1. FORCE the environment to recognize Gemini
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")

# 2. Initialize Gemini 1.5 Flash
# We explicitly set this as the ONLY brain allowed.
gemini_llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# 3. Setup Tools
search_tool = SerperDevTool()

# 4. Define Agents (Explicitly passing the llm)
researcher = Agent(
    role='Expert Researcher',
    goal='Find the latest 2025 trends in {topic}',
    backstory='You are a specialist in technical discovery.',
    tools=[search_tool],
    llm=gemini_llm, # <--- Gemini assigned
    verbose=True,
    allow_delegation=False
)

writer = Agent(
    role='Tech Writer',
    goal='Write a brief report about {topic}',
    backstory='You turn data into clear summaries.',
    llm=gemini_llm, # <--- Gemini assigned
    verbose=True,
    allow_delegation=False
)

# 5. Define Tasks
research_task = Task(
    description='Search for 3 major advancements in {topic} for 2025.',
    expected_output='A list of 3 key points with links.',
    agent=researcher
)

writing_task = Task(
    description='Write a 2-paragraph summary based on the research.',
    expected_output='A clean markdown summary.',
    agent=writer
)

# 6. Assemble the Crew
# Note: planning is set to FALSE to prevent OpenAI errors.
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential,
    planning=False, # <--- DISABLING internal planner to skip OpenAI check
    verbose=True
)

if __name__ == "__main__":
    print("--- Starting Gemini-Powered Crew ---")
    result = crew.kickoff(inputs={'topic': 'AI Agent Workflows'})
    print("\n\n" + "="*30)
    print("FINAL OUTPUT:")
    print(result)
