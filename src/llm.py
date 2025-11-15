import ollama

def call_llm(prompt: str, model: str = "deepseek-r1:latest", temp: float = 0.7) -> str:
    response = ollama.generate(
        model=model,
        prompt=prompt,
        options={"temperature": temp}
    )
    print(response['response'].strip())
    return response['response'].strip()