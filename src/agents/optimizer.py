from utils.prompts import get_optimizer_prompt
from llm import call_llm

class OptimizerAgent:
    def optimize(self, lesson_plan: str, feedback: str, skill_tree) -> str:
        skill_summary = skill_tree.get_summary()
        prompt = get_optimizer_prompt(
            lesson_plan=lesson_plan,
            skill_summary=skill_summary,
            feedback=feedback
        )
        return call_llm(prompt, temp=1.0)