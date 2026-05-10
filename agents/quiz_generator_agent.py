from openai import OpenAI

client = OpenAI()


class QuizGeneratorAgent:

    def generate_quiz(self, topic):

        prompt = f"""
        Generate 5 technical multiple-choice questions on:

        {topic}

        Return in this JSON-like structure:

        Q1:
        Question:
        Options:
        A.
        B.
        C.
        D.
        Correct Answer:
        Explanation:
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        return response.choices[0].message.content
