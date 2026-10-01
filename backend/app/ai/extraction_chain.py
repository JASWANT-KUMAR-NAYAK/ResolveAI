import json
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.ai.extraction_prompt import EXTRACTION_SYSTEM_PROMPT
from app.ai.groq_client import client
from app.schemas.deviation import DeviationData


class ExtractionState(TypedDict):
    text: str
    result: dict | None
    error: str | None


def extract_deviation(state: ExtractionState) -> ExtractionState:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": EXTRACTION_SYSTEM_PROMPT,
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


def validate_deviation(state: ExtractionState) -> ExtractionState:
    if state["result"] is None:
        return state

    validated = DeviationData.model_validate(state["result"])

    return {
        **state,
        "result": validated.model_dump(),
        "error": None,
    }


graph_builder = StateGraph(ExtractionState)

graph_builder.add_node("extract_deviation", extract_deviation)
graph_builder.add_node("validate_deviation", validate_deviation)

graph_builder.add_edge(START, "extract_deviation")
graph_builder.add_edge("extract_deviation", "validate_deviation")
graph_builder.add_edge("validate_deviation", END)

extraction_graph = graph_builder.compile()