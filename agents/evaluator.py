# agents/evaluator.py

from openai import OpenAI

client = OpenAI()


class EvaluatorAgent:

    def evaluate(
        self,
        problem_statement,
        rubric,
        submission_content,
        dataset_info=""
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
OPTIONAL DATASET INFO
========================

{dataset_info}

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
        return response.choices[0].message.content
