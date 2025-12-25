import os
import threading
import random
import time
import sys
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# 1. Gemini 3 Configuration
# Thinking Level 'minimal' ensures the Spectre agent acts with lethal speed.
spectre_llm = LLM(
    model="gemini/gemini-3-flash-preview",
    temperature=1.0, 
    extra_body={"thinking_level": "minimal"} 
)

search_tool = SerperDevTool(n_results=3)

# 2. Optimized Agents - Spectre-A Protocol
researcher = Agent(
    role='Spectre Field Operative',
    goal='Unlocking the Spectral Tome to extract 5 hidden truths on {topic}',
    backstory='Code Name: AJAY. An elite ghost operative who scours the deep web for truth.',
    llm=spectre_llm,
    tools=[search_tool],
    max_iter=3,
    verbose=False
)

writer = Agent(
    role='Spectre Lead Analyst',
    goal='Synthesize raw recon into a high-level briefing on {topic}',
    backstory='The strategist behind the shadow. You turn chaos into invincible intelligence.',
    llm=spectre_llm,
    verbose=False
)

# 3. Tasks
research_task = Task(description='Scout 5 facts about {topic}.', expected_output='5 bullet points.', agent=researcher)
write_task = Task(description='Summarize {topic} findings.', expected_output='2 polished paragraphs.', agent=writer)

# --- INTERACTIVE NUMBER GUESSING GAME (ACTIVE WAIT) ---
stop_event = threading.Event()

def play_guessing_game():
    print("\n" + "💀" * 15)
    print("      AJAY PROTOCOL ACTIVE       ")
    print("   READING SPECTRAL TOME...      ")
    print("💀" * 15)
    
    while not stop_event.is_set():
        target = random.randint(1, 100)
        attempts = 0
        print(f"\n[GAME] Cipher Challenge: Crack the code (1-100) to maintain access")
        
        while not stop_event.is_set():
            try:
                user_input = input("Enter Cipher: ")
                if stop_event.is_set(): break
                
                guess = int(user_input)
                attempts += 1
                
                if guess < target: print("   KEY TOO LOW ⬆️")
                elif guess > target: print("   KEY TOO HIGH ⬇️")
                else:
                    print(f"   🎯 ACCESS MAINTAINED! Cipher cracked in {attempts} attempts!")
                    print("   Rotating to next security layer...")
                    break
            except ValueError:
                if not stop_event.is_set(): print("   INVALID DATA. Use numeric keys only.")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    try:
        print("\n" + "━" * 50)
        print("           WELCOME TO SPECTRE-A TERMINAL          ")
        print("     SECURE CONNECTION: Spectral Tome of Knowledge   ")
        print("━" * 50)
        
        user_query = input("\n🕵️ Identify the target for deep recon: ")
        if not user_query: user_query = "Rise of AI Agents"
        
        print(f"\n📡 Deploying agents to investigate: '{user_query}'")

        # Start the interactive game thread
        game_thread = threading.Thread(target=play_guessing_game, daemon=True)
        game_thread.start()

        # Kickoff the Crew
        crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task])
        result = crew.kickoff(inputs={'topic': user_query})

        # Gracefully stop the game
        stop_event.set()
        
        print("\n" + "━" * 50)
        print("✨ AGENTS HAVE RETURNED WITH ENCRYPTED DATA ✨")
        print("━" * 50)
        print(result)
        
    except KeyboardInterrupt:
        stop_event.set()
        print("\n\n🛑 EMERGENCY SHUTDOWN. SPECTRE-A DISCONNECTED.")
        sys.exit(0)
