import json
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.ai.groq_client import client
from app.ai.investigation_prompt import INVESTIGATION_SYSTEM_PROMPT


class InvestigationState(TypedDict):
    issue_context: str
    questions: list[str]
    error: str | None


def generate_investigation_questions(
    state: InvestigationState,
) -> InvestigationState:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": INVESTIGATION_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": state["issue_context"],
            },
        ],
        response_format={"type": "json_object"},
    )

    raw_result = response.choices[0].message.content

    if not raw_result:
        return {
            **state,
            "questions": [],
            "error": "Groq returned an empty response.",
        }

    result = json.loads(raw_result)
    questions = result.get("questions", [])

    if not isinstance(questions, list):
        return {
            **state,
            "questions": [],
            "error": "AI returned an invalid questions format.",
        }

    return {
        **state,
        "questions": [str(question) for question in questions],
        "error": None,
    }


graph_builder = StateGraph(InvestigationState)

graph_builder.add_node(
    "generate_investigation_questions",
    generate_investigation_questions,
)

graph_builder.add_edge(
    START,
    "generate_investigation_questions",
)

graph_builder.add_edge(
    "generate_investigation_questions",
    END,
)

investigation_graph = graph_builder.compile()