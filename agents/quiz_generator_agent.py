from openai import OpenAI

client = OpenAI()


class CaseStudyEvaluator:

    def evaluate(self, submission):

        prompt = f"""
        You are a technical evaluator.

        Evaluate the following technical submission.

        Return response in this EXACT format:

        Overall Score: X/10

        Technical Accuracy:
        -

        Strengths:
        -

        Weaknesses:
        -

        Suggested Improvements:
        -

        Final Verdict:
        -

        Submission:
        {submission}
        """
        return response.choices[0].message.content
