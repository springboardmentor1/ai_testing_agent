from transformers import pipeline
import re, json
import torch

# Load model (runs on Colab GPU)
pipe = pipeline(
    "text-generation",
    model="HuggingFaceH4/zephyr-7b-beta",
    torch_dtype=torch.bfloat16,
    device_map="auto"
)

def extract_json(text):
    match = re.search(r"\{[\s\S]*\}", text)
    return match.group(0) if match else None

def parse_instruction_to_json(instruction):
    prompt = f"""
You are a strict JSON generator.
Return ONLY valid JSON. No explanations.

Instruction:
"{instruction}"

JSON format:
{{
  "actions": [
    {{"action": "open_website","parameters": {{"url": "https://www.google.com"}}}},
    {{"action": "search","parameters": {{"query": "amazon"}}}}
  ]
}}
"""
    outputs = pipe(prompt, max_new_tokens=200, do_sample=False)
    generated_text = outputs[0]["generated_text"]
    json_text = extract_json(generated_text)
    if not json_text:
        return {"error": "No JSON found", "raw_output": generated_text, "actions": []}
    try:
        return json.loads(json_text)
    except json.JSONDecodeError as e:
        return {"error": "Invalid JSON", "details": str(e), "raw_output": json_text, "actions": []}

# Test
instruction = "open Google and search for amazon"
result = parse_instruction_to_json(instruction)
print(json.dumps(result, indent=2))
