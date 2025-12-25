import os
import streamlit as st
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# --- SPECTRE-A CLOUD CONFIGURATION ---
st.set_page_config(page_title="Spectre-A Terminal", page_icon="💀", layout="centered")

# Visual "Tome" Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ff41; font-family: 'Courier New', Courier, monospace; }
    stButton>button { width: 100%; border-radius: 5px; background-color: #1f2937; color: white; border: 1px solid #00ff41; }
    .stStatus { border: 1px solid #00ff41; }
    </style>
    """, unsafe_allow_html=True)

# 🔑 SECRETS SYNCHRONIZATION
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
    os.environ["GEMINI_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
if "SERPER_API_KEY" in st.secrets:
    os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]

# --- THE SPECTRAL TOME ENGINE ---
@st.cache_resource
def initialize_spectre_llm():
    # UPDATED: Using Gemini 3 Flash Preview as identified in your AI Studio
    return LLM(
        model="gemini/gemini-3-flash-preview", 
        temperature=1.0,  # Recommended for Gemini 3 to ensure creative reasoning
        max_retries=5     # Increased retries to handle high-speed "burst" requests
    )

# --- WEB UI ---
st.title("💀 SPECTRE-A TERMINAL")
st.write("---")
st.subheader("SECURE CONNECTION: Spectral Tome of Knowledge")
st.info("Operative AJAY: System online. Prepared for recon.")

user_query = st.text_input("🕵️ Enter Your Topic For Deep Intel:", placeholder="Leave blank for core intel...")

if st.button("EXECUTE PROTOCOL"):
    target_topic = user_query if user_query else "Most Important functions of AI Agents"
    
    if not os.environ.get("GOOGLE_API_KEY") or not os.environ.get("SERPER_API_KEY"):
        st.error("🚨 ACCESS DENIED: API Keys missing in Secrets.")
        st.stop()

    with st.status("📡 Accessing Spectral Tome...", expanded=True) as status:
        try:
            st.write("Initializing Ultra-Stable Gemini 1.5 Architecture...")
            llm = initialize_spectre_llm()
            search_tool = SerperDevTool()

            st.write(f"Deploying Field Operative A to investigate '{target_topic}'...")
            
            # 1. Agents - Optimized with smaller backstories to save tokens
            researcher = Agent(
                role='Spectre Field Operative',
                goal=f'Extract 3 critical truths about {target_topic}',
                backstory='Code Name: AJAY. Elite scout.',
                llm=llm,
                tools=[search_tool],
                verbose=True,
                allow_delegation=False,
                max_iter=3 # Prevents infinite loops from eating quota
            )

            writer = Agent(
                role='Spectre Lead Analyst',
                goal='Synthesize findings into a high-level briefing.',
                backstory='The strategist. Turns raw data into intelligence.',
                llm=llm,
                verbose=True,
                allow_delegation=False
            )

            # 2. Tasks
            tasks = [
                Task(description=f'Find 3 critical facts about {target_topic}.', expected_output='3 bullet points.', agent=researcher),
                Task(description=f'Summarize {target_topic} findings.', expected_output='1 polished paragraph.', agent=writer)
            ]

            # 3. Execution
            crew = Crew(agents=[researcher, writer], tasks=tasks)
            result = crew.kickoff()
            
            status.update(label="✅ Recon Complete!", state="complete", expanded=False)

            # --- FINAL INTEL DISPLAY ---
            st.success(f"Intel Gathered for: {target_topic.upper()}")
            st.markdown("### 📜 THE SPECTRE'S REPORT")
            st.markdown(result.raw)
            
            st.divider()
            st.download_button(
                label="💾 Download Encrypted Intel",
                data=str(result.raw),
                file_name=f"spectre_recon_{target_topic.replace(' ', '_')}.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            status.update(label="🚨 MISSION FAILED", state="error")
            if "429" in str(e):
                st.error("QUOTA EXHAUSTED: The Free Tier is currently full. Wait 60s and try again.")
                
            else:
                st.error(f"Critical System Failure: {str(e)}")

st.write("---")
st.caption("v3.2 | Powered by Gemini 1.5 Flash | High-Stability Mode")
