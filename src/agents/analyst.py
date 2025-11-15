from utils.prompts import get_analyst_prompt
from llm import call_llm

class AnalystAgent:
    def analyze_errors(self, example: str, skill_tree) -> str:
        skill_summary = skill_tree.get_summary()
        prompt = get_analyst_prompt(example=example, skill_summary=skill_summary)
        return call_llm(prompt, temp=0.7)