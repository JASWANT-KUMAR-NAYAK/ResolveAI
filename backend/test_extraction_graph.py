from app.ai.extraction_chain import extraction_graph


deviation_text = """
On 25 September 2026, at Plant 1, the storage temperature for Product A
Batch B2409-12 exceeded the approved range for approximately 45 minutes.

The deviation was observed during routine monitoring. The affected process
parameter was storage temperature. No product damage was immediately observed.
"""


result = extraction_graph.invoke(
    {
        "text": deviation_text,
        "result": None,
        "error": None,
    }
)

print(result)
