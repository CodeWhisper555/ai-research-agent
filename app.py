import os
import streamlit as st
from crewai import Agent, Task, Crew, LLM
from crewai_tools import SerperDevTool

# --- SPECTRE-A CLOUD CONFIGURATION ---
st.set_page_config(page_title="Spectre-A Terminal", page_icon="💀", layout="centered")

# Injecting CSS for the "Spectral" Dark Theme
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #00ff41; font-family: 'Courier New', Courier, monospace; }
    stButton>button { width: 100%; border-radius: 5px; background-color: #1f2937; color: white; border: 1px solid #00ff41; }
    </style>
    """, unsafe_allow_html=True)

# Link Streamlit Secrets to Environment Variables
if "GOOGLE_API_KEY" in st.secrets:
    os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
if "SERPER_API_KEY" in st.secrets:
    os.environ["SERPER_API_KEY"] = st.secrets["SERPER_API_KEY"]

# --- THE SPECTRAL TOME ENGINE ---
@st.cache_resource
def initialize_spectre_llm():
    # Gemini 3 Flash Preview - Optimized for Dec 2025
    return LLM(
        model="gemini/gemini-3-flash-preview",
        temperature=1.0,
        extra_body={"thinking_level": "minimal"} 
    )

# --- WEB UI ---
st.title("💀 SPECTRE-A TERMINAL")
st.write("---")
st.subheader("SECURE CONNECTION: Spectral Tome of Knowledge")
st.info("Operative AJ: System online. Prepared for recon.")

user_query = st.text_input("🕵️ Enter Your Topic For Deep Intel :", placeholder="Leave blank for core intel...")

if st.button("EXECUTE PROTOCOL"):
    # Fallback logic
    target_topic = user_query if user_query else "Rise of AI Agents"
    
    with st.status("📡 Accessing Spectral Tome...", expanded=True) as status:
        st.write("Initializing Gemini 3 Flash Architecture...")
        llm = initialize_spectre_llm()
        search_tool = SerperDevTool(n_results=3)

        st.write(f"Deploying Field Operative AJ to investigate '{target_topic}'...")
        
        # 1. Agents
        researcher = Agent(
            role='Spectre Field Operative',
            goal=f'Unlocking the Spectral Tome to extract 5 hidden truths on {target_topic}',
            backstory='Code Name: AJAY. An elite ghost operative scouting the deep web.',
            llm=llm,
            tools=[search_tool],
            verbose=True
        )

        writer = Agent(
            role='Spectre Lead Analyst',
            goal=f'Synthesize raw recon into a high-level briefing on {target_topic}',
            backstory='The strategist behind the shadow. You turn chaos into invincible intelligence.',
            llm=llm,
            verbose=True
        )

        # 2. Tasks
        tasks = [
            Task(description=f'Scout 5 facts about {target_topic}.', expected_output='5 bullet points.', agent=researcher),
            Task(description=f'Summarize {target_topic} findings.', expected_output='2 polished paragraphs.', agent=writer)
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
        data=result.raw,
        file_name=f"spectre_recon_{target_topic.replace(' ', '_')}.txt",
        mime="text/plain"
    )

st.write("---")
st.caption("v3.0 | Powered by Gemini 3 Flash | Developed for Operative Ajay")
