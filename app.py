import os
import time
import threading
import random
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# 1. Faster Gemini 3 Config
fast_gemini = LLM(
    model="gemini/gemini-3-flash-preview",
    temperature=0.7,
    extra_body={"reasoning_effort": "minimal"} 
)

search_tool = SerperDevTool(n_results=3)

# 2. Optimized Agents
researcher = Agent(
    role='Fast Web Researcher',
    goal='Quickly find 5 key facts about {topic}',
    backstory='You are a speed-optimized data hunter.',
    llm=fast_gemini,
    tools=[search_tool],
    max_iter=3,
    max_execution_time=60,
    verbose=False # Set to False so it doesn't interrupt our mini-game
)

writer = Agent(
    role='Concise Writer',
    goal='Summarize findings about {topic} immediately',
    backstory='You value time. You deliver sharp, no-fluff summaries.',
    llm=fast_gemini,
    verbose=False
)

# 3. Tasks
research_task = Task(
    description='Search and find 5 important facts about {topic}.',
    expected_output='5 bullet points with sources.',
    agent=researcher
)

write_task = Task(
    description='Summarize the research on {topic} in 2 short paragraphs.',
    expected_output='A brief summary.',
    agent=writer
)

# --- PASS TIME LOGIC ---
stop_game = False

def play_mini_game():
    """A simple game to play while waiting for the AI."""
    print("\n[ Wait-Time Mini-Game] I'm thinking of a number between 1 and 100...")
    target = random.randint(1, 100)
    attempts = 0
    
    while not stop_game:
        try:
            # Using a short timeout-like check to see if we should stop
            guess = input("\n(Game) Guess the number (or wait for AI): ")
            if stop_game: break
            
            attempts += 1
            guess = int(guess)
            if guess < target: print("Higher! ↑")
            elif guess > target: print("Lower! ↓")
            else:
                print(f" YOU GOT IT in {attempts} tries! Generating a new number...")
                target = random.randint(1, 100)
                attempts = 0
        except ValueError:
            if not stop_game: print("Enter a valid number!")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    print("""
     WELCOME TO THE AI INSIGHT GENERATOR 
    -----------------------------------------
    "The world's knowledge, refined by Gemini 3."
    """)
    
    user_query = input(" What mystery shall we uncover today? (Topic): ")
    
    print(f"\n Launching agents to research: '{user_query}'...")
    print("This usually takes 30-60 seconds. In the meantime...")

    # Start the game thread
    game_thread = threading.Thread(target=play_mini_game, daemon=True)
    game_thread.start()

    # Start the Crew
    crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task])
    result = crew.kickoff(inputs={'topic': user_query})

    # Stop the game
    stop_game = True
    print("\n\n AI Agents have returned from their journey!")
    print("-----------------------------------------")
    print(result)
