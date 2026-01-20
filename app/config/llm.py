import ollama

MODEL_NAME = "gemma:2b"

def call_llm(prompt: str) -> str:
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a strict JSON generator."},
            {"role": "user", "content": prompt}
        ],
        format="json"   
    )
    return response["message"]["content"]
