import os
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# 1. Initialize Gemini 3 Flash
gemini_3_flash = LLM(
    model="gemini/gemini-3-flash-preview",
    temperature=1.0,
    api_key=os.environ.get("GEMINI_API_KEY"),
    extra_body={"reasoning_effort": "high"}
)

# 2. Initialize Search Tool (Requires SERPER_API_KEY in .env)
search_tool = SerperDevTool()

# 3. Define Agents
researcher = Agent(
    role='Expert Web Researcher',
    goal='Find the most relevant and up-to-date information about {topic}',
    backstory='You are a master at navigating the web and extracting precise data.',
    llm=gemini_3_flash,
    tools=[search_tool], # Give the agent search powers
    verbose=True
)

writer = Agent(
    role='Content Specialist',
    goal='Write a compelling report about {topic}',
    backstory='You transform raw research into beautiful, readable summaries.',
    llm=gemini_3_flash,
    verbose=True
)

# 4. Define Tasks with Placeholders
research_task = Task(
    description='Search the internet and find the 5 most important facts about {topic}.',
    expected_output='A bulleted list of 5 key findings with sources.',
    agent=researcher
)

write_task = Task(
    description='Using the research provided, write a 2-paragraph summary about {topic}.',
    expected_output='A clean, formatted 2-paragraph summary.',
    agent=writer
)

# 5. Assemble the Crew
crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    verbose=True
)

# 6. Get User Input and Kickoff
if __name__ == "__main__":
    user_query = input("What topic would you like to research? ")
    
    # Pass the user input as a dictionary to the kickoff method
    result = crew.kickoff(inputs={'topic': user_query})
    
    print("\n\n########################")
    print("## FINAL REPORT")
    print("########################\n")
    print(result)
