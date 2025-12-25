import os
import time
import threading
import random
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# 1. Faster Gemini 3 Config
# Note: 'minimal' thinking is perfect for fast search/summarization
fast_gemini = LLM(
    model="gemini/gemini-3-flash-preview",
    temperature=1.0, # Recommended for Gemini 3
    extra_body={"thinking_level": "minimal"} 
)

search_tool = SerperDevTool(n_results=3)

# 2. Optimized Agents (verbose=False to keep terminal clean for the game)
researcher = Agent(
    role='Speed-Data Hunter',
    goal='Scour the digital realm for 5 vital facts on {topic}',
    backstory='You live in the wires. You find truth at the speed of light.',
    llm=fast_gemini,
    tools=[search_tool],
    max_iter=3,
    verbose=False
)

writer = Agent(
    role='The Insight Weaver',
    goal='Distill research into a sharp 2-paragraph summary on {topic}',
    backstory='You turn raw data into narrative gold.',
    llm=fast_gemini,
    verbose=False
)

# 3. Tasks
research_task = Task(description='Find 5 facts about {topic}.', expected_output='5 bullets.', agent=researcher)
write_task = Task(description='Summarize {topic} briefly.', expected_output='2 paragraphs.', agent=writer)

# --- CREATIVE WAIT LOGIC ---
stop_event = threading.Event()

def mini_game():
    items = ["🍎", "🍌", "🍇", "🍊", "🍓"]
    target = random.choice(items)
    print(f"\n[🎮 Quick Game] Catch the {target}! Type it as fast as you can when you see it.")
    
    while not stop_event.is_set():
        time.sleep(random.uniform(2, 5))
        if stop_event.is_set(): break
        
        current = random.choice(items)
        print(f"\nAI is thinking... Current item: {current}")
        if current == target:
            print(f"✨ QUICK! PRESS ENTER TO CATCH THE {target}! ✨")

# --- MAIN ---
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀  GEMINI 3 MULTI-AGENT ORACLE  🚀")
    print("="*50)
    
    user_query = input("\n🔮 What corner of the universe shall we explore? ")
    
    print(f"\n📡 Agents deployed. Gathering intel on '{user_query}'...")
    
    # Start wait-time thread
    game_thread = threading.Thread(target=mini_game, daemon=True)
    game_thread.start()

    # Run Crew
    crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task])
    result = crew.kickoff(inputs={'topic': user_query})

    # Wrap up
    stop_event.set()
    print("\n" + "✅" * 20)
    print("\n📜 THE ORACLE'S REPORT:")
    print(result)
