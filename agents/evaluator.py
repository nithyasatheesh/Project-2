# agents/evaluator_agent.py

from openai import OpenAI

client = OpenAI()


class EvaluatorAgent:

    def evaluate(
        self,
        problem_statement,
        participant_solution
    ):

        prompt = f"""
You are an enterprise technical evaluator.

Evaluate the participant solution based on
the given problem statement.

Problem Statement:
{problem_statement}

Participant Solution:
{participant_solution}

Evaluate using this rubric:

1. Correctness (40%)
2. Optimization (20%)
3. Readability (15%)
4. Error Handling (15%)
5. Best Practices (10%)

Return response in this EXACT format:

Correctness Score:
Optimization Score:
Readability Score:
Error Handling Score:
Best Practices Score:

Final Score:

Strengths:
-

Weaknesses:
-

Suggested Improvements:
-

Final Verdict:
-

Be strict but constructive.
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content
