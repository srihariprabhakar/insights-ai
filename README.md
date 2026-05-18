# Insights AI

Insights AI is an operational intelligence demo built using:

- DigitalOcean App Platform
- DigitalOcean Inference Router
- DigitalOcean Serverless Inference
- Streamlit

The application demonstrates task-aware AI routing for enterprise operational workflows such as:

- Event summarization
- Severity classification
- Manager recommendations
- Executive reporting

Instead of hardcoding a single model, requests are dynamically routed through DigitalOcean Inference Router based on workload type and optimization strategy.

## Architecture

```text
Operational Events
        ↓
Insights AI UI
        ↓
Insights Demo Router
        ↓
Task-based Model Selection
   ↙                     ↘
Fast Models         Premium Reasoning Models
        ↓
AI-generated Operational Insights
