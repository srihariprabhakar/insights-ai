# Insights AI

Insights AI is an operational intelligence demo built using DigitalOcean AI services.

The application demonstrates how enterprise operational workflows can dynamically route AI requests to different models depending on workload type, reasoning complexity, latency requirements, and optimization strategy.

Instead of hardcoding a single model, Insights AI uses DigitalOcean Inference Router to intelligently orchestrate model selection across operational workflows such as:

- Event summarization
- Severity classification
- Manager recommendations
- Executive operational reporting

---

# Architecture

```text
Operational Events
        ↓
Insights AI UI
(App Platform / Streamlit)
        ↓
Insights Demo Router
        ↓
Task-based Model Selection
   ↙                     ↘
Fast Models         Premium Reasoning Models
        ↓
AI-generated Operational Insights
