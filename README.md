# AI Research Crew: Multi-Agent Intelligence

An autonomous research engine that leverages **CrewAI** and **Google Gemini 1.5 Flash** to perform deep-web analysis and professional report generation. This project demonstrates agentic orchestration, tool usage, and secure cloud deployment.

---

## The Architecture
This project uses a "Sequential Process" where multiple AI agents collaborate to achieve a goal.

```mermaid
graph LR
    User((User)) -->|Topic| Crew[CrewAI Orchestrator]
    subgraph Agents
        R[Researcher Agent]
        W[Writer Agent]
    end
    Crew --> R
    R -->|Web Search| S[Serper.dev API]
    S -->|Raw Data| R
    R -->|Structured Findings| W
    W -->|Synthesized Report| User
