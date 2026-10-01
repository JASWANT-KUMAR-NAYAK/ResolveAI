from app.ai.analysis_chain import analysis_graph


deviation = {
    "site": "Plant 1",
    "date_of_occurrence": "25 September 2026",
    "title": None,
    "description": (
        "Storage temperature for Product A Batch B2409-12 "
        "exceeded the approved range for approximately 45 minutes. "
        "The deviation was observed during routine monitoring. "
        "No product damage was immediately observed."
    ),
    "related_product": "Product A",
    "related_material": None,
    "batch_number": "B2409-12",
    "process_parameter": "storage temperature",
}


result = analysis_graph.invoke(
    {
        "deviation": deviation,
        "result": None,
        "error": None,
    }
)

print(result)