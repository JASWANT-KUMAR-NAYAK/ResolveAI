import json
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from app.ai.analysis_prompt import ANALYSIS_SYSTEM_PROMPT
from app.ai.groq_client import client
from app.schemas.deviation import (
    ImpactAssessment,
    SeverityAssessment,
)


class AnalysisState(TypedDict):
    deviation: dict
    result: dict | None
    error: str | None


def analyze_deviation(state: AnalysisState) -> AnalysisState:
    deviation_json = json.dumps(state["deviation"], indent=2)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": ANALYSIS_SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": deviation_json,
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


def validate_analysis(state: AnalysisState) -> AnalysisState:
    if state["result"] is None:
        return state

    impact = ImpactAssessment.model_validate(
        state["result"]["impact"]
    )

    severity = SeverityAssessment.model_validate(
        state["result"]["severity"]
    )

    validated_result = {
        "impact": impact.model_dump(),
        "severity": severity.model_dump(),
    }

    return {
        **state,
        "result": validated_result,
        "error": None,
    }


graph_builder = StateGraph(AnalysisState)

graph_builder.add_node("analyze_deviation", analyze_deviation)
graph_builder.add_node("validate_analysis", validate_analysis)

graph_builder.add_edge(START, "analyze_deviation")
graph_builder.add_edge("analyze_deviation", "validate_analysis")
graph_builder.add_edge("validate_analysis", END)

analysis_graph = graph_builder.compile()