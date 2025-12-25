import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool

# 1. Configuration
gemini_llm = LLM(
    model="gemini/gemini-1.5-flash", # Using stable flash model
    api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)

search_tool = SerperDevTool()

# 2. Define Agents (Keep these general so they work for any topic)
researcher = Agent(
    role='Expert Researcher',
    goal='Provide a deep-dive analysis on {topic}',
    backstory='You are a world-class analyst known for uncovering hidden insights.',
    llm=gemini_llm,
    tools=[search_tool],
    verbose=True
)

writer = Agent(
    role='Technical Content Strategist',
    goal='Create a high-impact summary about {topic}',
    backstory='You turn raw research into professional, easy-to-read executive summaries.',
    llm=gemini_llm,
    verbose=True
)

# 3. Define Tasks with {placeholders}
task1 = Task(
    description='Search for the latest breakthroughs and news related to {topic}.',
    expected_output='A comprehensive list of the top 3-5 findings with supporting facts.',
    agent=researcher
)

task2 = Task(
    description='Using the research provided, write a 3-paragraph executive summary about {topic}.',
    expected_output='A professional markdown-formatted summary.',
    agent=writer
)

# 4. Assemble the Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True
)

# 5. Get User Input and Kickoff
if __name__ == "__main__":
    print("--- Welcome to the AI Research Crew ---")
    user_topic = input("Enter the topic you want a summary for: ")
    
    # The 'inputs' dictionary fills in all the {topic} placeholders above
    result = crew.kickoff(inputs={'topic': user_topic})

    print("\n\n########################")
    print(f"## FINAL SUMMARY FOR: {user_topic.upper()} ##")
    print("########################\n")
    print(result)
