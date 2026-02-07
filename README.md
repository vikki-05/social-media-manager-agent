# Social Media Manager Agent 

An autonomous, agentic AI system that analyzes historical social media engagement data and generates optimized content captions and posting strategies.

This project demonstrates how an AI agent can **observe**, **analyze**, **decide**, and **act** without human intervention.

---

##  Key Features

-  Engagement analysis from historical data
-  Autonomous decision-making (Agent Loop)
-  AI-powered caption generation (ScaleDown API)
-  Transparent reasoning (Explainable AI)
-  CLI-based, lightweight, and cost-aware

---
## Creative / Unique Feature

### Explainable Agent Memory
The agent maintains a persistent memory log of its decisions, including:
- Selected content strategy
- Engagement score
- Generated caption
- Reasoning behind the decision

This enables transparency, traceability, and lays the foundation for future self-improving agent behavior.

## Agent Architecture

The agent follows a classic **Agent Loop**:

### 1. Observe
Reads historical social media data (`posts.csv`).

### 2. Analyze
Calculates engagement metrics (likes + comments + shares).

### 3. Decide
Selects:
- Best performing content type
- Best posting time based on past engagement

### 4. Act
Uses an AI model (via ScaleDown) to generate an optimized caption.

### 5. Explain
Outputs reasoning behind its decisions for transparency.
