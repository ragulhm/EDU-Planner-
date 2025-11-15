"""
OS evaluation prompt templates (clean, error-free)
Provides three helper functions that return ready-to-use prompt strings for
an evaluator, an optimizer, and an analyst agent. Each function accepts the
lesson_plan and skill_summary and returns a formatted prompt that asks the
agent to evaluate using CIDDP criteria: Clarity, Integrity, Depth,
Practicality, Pertinence.
"""
from typing import Literal


def _format_scores_instructions() -> str:
    """Common output format instructions used by all prompts."""
    return (
        "Output ONLY using these five short bracketed labels and a one-line comment for each:\n"
        "[C]:<score 1-5>; short comment  — Clarity\n"
        "[I]:<score 1-5>; short comment  — Integrity\n"
        "[D]:<score 1-5>; short comment  — Depth\n"
        "[P]:<score 1-5>; short comment  — Practicality\n"
        "[P]:<score 1-5>; short comment  — Pertinence\n"
        "Example output:\n"
        "[C]:3; Clear but too brief\n"
        "[I]:4; Good structure\n"
        "[D]:2; Lacks virtual memory details\n"
        "[P]:5; Uses real shell examples\n"
        "[P]:4; Matches beginner level"
    )


def get_evaluator_prompt(lesson_plan: str, skill_summary: str, sample_questions=None) -> str:
    """Return a clean evaluator prompt for assessing an OS lesson plan, skill tree, and sample questions.

    Args:
        lesson_plan: The full lesson plan text to evaluate.
        skill_summary: A one- to three-sentence summary of the student's current skill level and prior knowledge.
        sample_questions: List of sample questions (dicts) to include in the evaluation.

    Returns:
        A formatted prompt string ready to feed to an evaluator LLM agent.
    """
    instructions = _format_scores_instructions()
    questions_section = ""
    if sample_questions:
        questions_section = "Sample Questions for Evaluation:\n"
        for q in sample_questions:
            questions_section += f"Q: {q.get('question')}\nOptions: {', '.join(q.get('options', []))}\nCorrect: {q.get('answer')}\n\n"

    return (
        f"You are an expert Operating Systems instructor. Evaluate the following lesson plan using the CIDDP criteria (Clarity, Integrity, Depth, Practicality, Pertinence).\n\n"
        f"Student Skill Profile: {skill_summary}\n\n"
        f"Lesson Plan:\n{lesson_plan}\n\n"
        f"{questions_section}"
        f"Evaluate on:\n"
        f"- Clarity: Is the content simple, jargon-free, and easy to follow?\n"
        f"- Integrity: Does it cover necessary concepts and provide examples?\n"
        f"- Depth: Does it explain core OS topics (scheduling algorithms, paging, virtual memory, concurrency, etc.) with sufficient depth?\n"
        f"- Practicality: Are real OS examples (Linux/Windows commands, kernel behavior, shell examples) included and accurate?\n"
        f"- Pertinence: Is the lesson matched to the student's level and learning goals?\n\n"
        f"{instructions}"
    )


def get_optimizer_prompt(lesson_plan: str, skill_summary: str, feedback: str = "") -> str:
    """Return a prompt guiding an optimizer agent to suggest concrete improvements."""
    instructions = _format_scores_instructions()
    
    feedback_section = f"Feedback to Address:\n{feedback}\n\n" if feedback.strip() else ""

    return (
        f"You are an expert curriculum optimizer for Operating Systems courses. Using the CIDPP criteria, analyze the lesson plan below and produce concrete, prioritized improvement suggestions (short list).\n\n"
        f"Student Skill Profile: {skill_summary}\n\n"
        f"{feedback_section}"
        f"Lesson Plan:\n{lesson_plan}\n\n"
        f"Tasks:\n"
        f"1) Provide 5 prioritized, actionable improvements (each 1--2 lines).\n"
        f"2) For each improvement, indicate which CIDDP area it affects (C/I/D/P/P).\n"
        f"3) Suggest one small in-lesson exercise or demo (1--3 steps) that addresses the top missing concept.\n\n"
        f"{instructions}"
    )


def get_analyst_prompt(example: str, skill_summary: str) -> str:
    """Prompt to extract common misconceptions from a given OS example or explanation."""
    return (
        f"You are an instructional analyst for Operating Systems. Given the following OS problem explanation or student-facing example, identify likely misconceptions for students at the specified level.\n\n"
        f"Student Skill Profile: {skill_summary}\n\n"
        f"Example:\n\"{example}\"\n\n"
        f"Tasks:\n"
        f"- List exactly 3 common student misconceptions (e.g., confusing deadlock with starvation, thinking threads share stack, etc.).\n"
        f"- Output as bullet points:\n"
        f"  - Misconception 1: ...\n"
        f"  - Misconception 2: ...\n"
        f"  - Misconception 3: ..."
    )

# if _name_ == "_main_":
#     # quick sanity check example
#     example_lesson = "Intro to processes, context switching, simple round-robin scheduling."
#     example_skill = "Beginner: understands basic programming and threads, not OS internals."
#     print(get_evaluator_prompt(example_lesson, example_skill))