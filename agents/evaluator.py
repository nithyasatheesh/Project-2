# agents/evaluator.py

from openai import OpenAI

client = OpenAI()


class EvaluatorAgent:

    def evaluate(
        self,
        problem_statement,
        rubric,
        submission_content
    ):

        prompt = f"""
You are an enterprise technical evaluator.

Evaluate the participant submission.

========================
PROBLEM STATEMENT
========================

{problem_statement}

========================
RUBRIC
========================

{rubric}

========================
PARTICIPANT SUBMISSION
========================

{submission_content}

========================

Evaluate thoroughly.

Return in this EXACT format:

# Evaluation Report

## Rubric Scores

- Correctness:
- Optimization:
- Readability:
- Error Handling:
- Best Practices:

## Final Score

-

## Strengths

-

## Weaknesses

-

## Suggested Improvements

-

## Final Verdict

-

Be professional and constructive.
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
