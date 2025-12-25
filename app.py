import os
from crewai import Agent, Task, Crew, Process
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import SerperDevTool

# 1. Configuration & The "Brain" (Gemini 1.5 Flash)
# We use Gemini 1.5 Flash for speed and its massive context window.
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    verbose=True,
    temperature=0.5,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# 2. Tools (The "Eyes")
# SerperDevTool allows the agents to search the live web.
search_tool = SerperDevTool()

# 3. Agents Definition
# A professional "Crew" needs specialized roles.
researcher = Agent(
    role='Lead Market Researcher',
    goal='Uncover cutting-edge developments in {topic} for 2025',
    backstory="""You are an expert at identifying emerging trends and 
    verifying technical breakthroughs. Your reports are known for 
    accuracy and depth.""",
    tools=[search_tool],
    llm=llm,
    allow_delegation=False,
    verbose=True # This shows the agent's internal "thoughts"
)

writer = Agent(
    role='Senior Technical Writer',
    goal='Synthesize research findings into a professional executive summary',
    backstory="""You are a specialist in technical communication. You 
    take complex data and transform it into clear, compelling, 
    and actionable Markdown reports for executives.""",
    llm=llm,
    allow_delegation=True, # Allows the writer to ask the researcher for more info
    verbose=True
)

# 4. Task Definition
# Define WHAT needs to be done.
research_task = Task(
    description="""Search the web to find the top 3 most significant 
    advancements in {topic} during late 2024 and 2025. 
    Focus on verified news and technical papers.""",
    expected_output="A list of 3 detailed bullet points with source links.",
    agent=researcher
)

writing_task = Task(
    description="""Review the research findings and write a 3-paragraph 
    executive report. Include an 'Overview' section, a 'Key Trends' 
    section, and a 'Future Outlook' section.""",
    expected_output="A professional report formatted in Markdown.",
    agent=writer
)

# 5. The Crew (The Team)
# This assembles your agents into a collaborative unit.
research_crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential, # Tasks run one after the other
    memory=True,                # Agents remember the conversation context
    planning=True,              # Agents plan their approach before acting
    verbose=True
)

# 6. Kickoff! 
if __name__ == "__main__":
    print("--- Starting AI Research Crew ---")
    
    # You can change this topic to anything (e.g., "SpaceX Starship", "Green Hydrogen")
    result = research_crew.kickoff(inputs={'topic': 'AI Agentic Workflows'})
    
    print("\n\n########################")
    print("##   FINAL REPORT     ##")
    print("########################\n")
    print(result)
