import json
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


from app.ai.groq_client import client
from app.schemas.issue_extraction import IssueExtractionResult

from app.ai.issue_extraction_prompt import ISSUE_EXTRACTION_SYSTEM_PROMPT
class IssueExtractionState(TypedDict):
    text: str
    result: dict | None
    error: str | None


def extract_issue(state: IssueExtractionState) -> IssueExtractionState:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": ISSUE_EXTRACTION_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": state["text"],
            },
        ],
        response_format={
            "type": "json_object",
        },
    )

    raw_result = response.choices[0].message.content

    if not raw_result:
        return {
            **state,
            "result": None,
            "error": "Groq returned an empty response.",
        }

    result = json.loads(raw_result)

    return {
        **state,
        "result": result,
        "error": None,
    }


def validate_issue(state: IssueExtractionState) -> IssueExtractionState:
    if state["result"] is None:
        return state

    validated = IssueExtractionResult.model_validate(state["result"])

    return {
        **state,
        "result": validated.model_dump(),
        "error": None,
    }


graph_builder = StateGraph(IssueExtractionState)

graph_builder.add_node("extract_issue", extract_issue)
graph_builder.add_node("validate_issue", validate_issue)

graph_builder.add_edge(START, "extract_issue")
graph_builder.add_edge("extract_issue", "validate_issue")
graph_builder.add_edge("validate_issue", END)

issue_extraction_graph = graph_builder.compile()