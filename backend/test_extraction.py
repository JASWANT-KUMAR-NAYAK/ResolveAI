import json

from app.ai.groq_client import client
from app.ai.extraction_prompt import EXTRACTION_SYSTEM_PROMPT
from app.schemas.deviation import DeviationData


deviation_text = """
On 25 September 2026, at Plant 1, the storage temperature for Product A
Batch B2409-12 exceeded the approved range for approximately 45 minutes.

The deviation was observed during routine monitoring. The affected process
parameter was storage temperature. No product damage was immediately observed.
"""


response = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
        {
            "role": "system",
            "content": EXTRACTION_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": deviation_text,
        },
    ],
    response_format={
        "type": "json_object",
    },
)


raw_result = response.choices[0].message.content

result = json.loads(raw_result)

validated_deviation = DeviationData.model_validate(result)

print(validated_deviation.model_dump_json(indent=4))