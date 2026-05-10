from openai import OpenAI

client = OpenAI()


class QuizGeneratorAgent:

    def generate_quiz(self, topic):

        prompt = f"""
        Generate 5 multiple-choice questions on:

        {topic}

        Include answers.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.choices[0].message.content