import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

MODEL_ACCESS_KEY = os.getenv("MODEL_ACCESS_KEY")
DO_ROUTER_ID = os.getenv("DO_ROUTER_ID")

API_URL = "https://inference.do-ai.run/v1/chat/completions"

TASKS = {
    "Event Summary": {
        "router_hint": "event_summary",
        "description": "Summarize operational events.",
        "example": """Store #182
Drive-thru wait time increased from 4m to 11m.
POS retry rate increased 37%.
Camera 4 disconnected twice.
Peak traffic occurred at 12:10 PM."""
    },

    "Severity Classification": {
        "router_hint": "severity_classification",
        "description": "Classify severity, urgency, and business impact.",
        "example": """Store #44
Freezer alert triggered 5 times.
Temperature rose from 4F to 19F.
Manager acknowledged after 32 minutes.
Inventory risk: high."""
    },

    "Manager Recommendation": {
        "router_hint": "manager_recommendation",
        "description": "Recommend operational next steps.",
        "example": """Store #91
Kitchen ticket time increased 42%.
Two employees clocked in late.
Customer queue exceeded 14 people for 22 minutes.
Refunds increased during the same period."""
    },

    "Executive Summary": {
        "router_hint": "executive_summary",
        "description": "Create an executive operational summary.",
        "example": """Region: Southwest
12 stores reported higher drive-thru delays.
4 stores had camera disconnects.
Refund volume increased 18%.
Average service time increased from 5.2m to 7.8m."""
    }
}

ROUTING_EXPLANATIONS = {
    "event_summary": "Latency-optimized workflow using fast summarization models for operational dashboards and monitoring.",

    "severity_classification": "Real-time classification workflow optimized for alerting and incident triage.",

    "manager_recommendation": "Reasoning-focused workflow using premium models for operational recommendations and next-step analysis.",

    "executive_summary": "High-context executive synthesis workflow optimized for strategic operational reporting."
}

st.set_page_config(
    page_title="Insights AI",
    layout="wide"
)

st.title("Insights AI")

st.caption(
    "AI-powered operational intelligence using DigitalOcean AI"
)

st.markdown("""
### Architecture

Operational Events  
→ Insights Demo Router  
→ Task-based Model Selection  
→ AI-generated Operational Insights
""")

task_name = st.selectbox(
    "Select task category",
    list(TASKS.keys())
)

task = TASKS[task_name]

st.info(
    f"Router hint: `{task['router_hint']}` - {task['description']}"
)

user_input = st.text_area(
    "Paste operational event data",
    value=task["example"],
    height=220
)


def call_router(task_name, task, user_input):

    system_prompt = f"""
You are an AI operations copilot for enterprise operational analytics.

The UI selected this task:
{task_name}

Return:
1. Summary
2. Severity or priority
3. Likely operational cause
4. Recommended action
5. Business value
"""

    payload = {
        "model": DO_ROUTER_ID,

        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },

            {
                "role": "user",
                "content": f"""
TASK_TYPE: {task["router_hint"]}

TASK_DESCRIPTION:
{task["description"]}

OPERATIONAL_EVENT_DATA:
{user_input}
"""
            }
        ],

        "temperature": 0.3
    }

    headers = {
        "Authorization": f"Bearer {MODEL_ACCESS_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=60
    )

    selected_route = response.headers.get(
        "x-model-router-selected-route",
        "not returned"
    )

    if not response.ok:
        st.error(f"Status code: {response.status_code}")
        st.code(response.text)

    response.raise_for_status()

    data = response.json()

    selected_model = data.get(
        "model",
        "not returned"
    )

    output = data["choices"][0]["message"]["content"]

    return (
        selected_route,
        selected_model,
        output,
        payload
    )


if st.button("Analyze"):

    if not MODEL_ACCESS_KEY or not DO_ROUTER_ID:

        st.error(
            "Missing MODEL_ACCESS_KEY or DO_ROUTER_ID"
        )

    else:

        with st.spinner(
            "Routing through DigitalOcean Inference Router..."
        ):

            (
                selected_route,
                selected_model,
                output,
                payload
            ) = call_router(
                task_name,
                task,
                user_input
            )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "UI Task",
            task_name
        )

        col2.metric(
            "Router-selected route",
            selected_route
        )

        col3.metric(
            "Model chosen",
            selected_model
        )

        st.success(
            f"Selected model: {selected_model}"
        )

        st.info(
            ROUTING_EXPLANATIONS[
                task["router_hint"]
            ]
        )

        st.subheader("AI Output")

        st.write(output)

        with st.expander(
            "Show request sent to router"
        ):

            st.json(payload)
