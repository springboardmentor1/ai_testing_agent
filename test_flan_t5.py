from transformers import pipeline

# Load FLAN-T5
llm = pipeline(
    "text2text-generation",
    model="google/flan-t5-base"
)

prompt = """
Return ONLY valid JSON.

Instruction:
open google and search for amazon

JSON:
[
  {
    "action": "navigate",
    "target": "https://www.google.com",
    "value": null
  },
  {
    "action": "type",
    "target": "search_box",
    "value": "amazon"
  },
  {
    "action": "press",
    "target": "enter",
    "value": null
  }
]
"""

result = llm(prompt, max_length=256)

print(result[0]["generated_text"])
