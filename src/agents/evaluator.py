from llm import call_llm
from utils.prompts import get_evaluator_prompt


class EvaluatorAgent:
    def evaluate(self, lesson_plan: str, skill_tree, sample_questions=None) -> tuple[dict, str]:
        """Call the LLM evaluator and parse CIDDP-style bracketed scores.

        The evaluator expects lines like:
          [C]:3; comment
          [I]:4; comment
          [D]:2; comment
          [P]:5; comment
          [P]:4; comment  # second P maps to Pertinence

        This method normalizes tags and returns a dict of scores plus the raw response.
        """
        skill_summary = skill_tree.get_summary()
        prompt = get_evaluator_prompt(lesson_plan, skill_summary, sample_questions=sample_questions)
        response = call_llm(prompt, temp=0.0)

        scores = {}
        p_count = 0

        for line in response.split('\n'):
            line = line.strip()
            if not line:
                continue

            try:
                if not line.startswith('[') or ']' not in line:
                    continue

                start = line.find('[')
                end = line.find(']')
                if start == -1 or end == -1 or end <= start:
                    continue

                tag = line[start + 1:end].strip()
                rest = line[end + 1:].strip()

                if not rest.startswith(':'):
                    continue

                # Extract score: everything after ':' until ';' or end
                score_str = rest[1:].split(';')[0].strip()
                score = int(score_str)

                # Normalize tags: C, I, D map to names. Handle multiple P tags and Pt.
                key_map = {'C': 'Clarity', 'I': 'Integrity', 'D': 'Depth'}
                if tag in key_map:
                    key = key_map[tag]
                else:
                    t_lower = tag.lower()
                    if t_lower in ('pt', 'pertinence'):
                        key = 'Pertinence'
                    elif tag == 'P':
                        p_count += 1
                        if p_count == 1:
                            key = 'Practicality'
                        elif p_count == 2:
                            key = 'Pertinence'
                        else:
                            key = f'P_{p_count}'
                    else:
                        # unknown tag: keep as-is
                        key = tag

                scores[key] = score
            

            except (ValueError, IndexError, AttributeError):
                # ignore unparsable lines
                continue

        return scores, response