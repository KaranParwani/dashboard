import openai
from fastapi import HTTPException

from config import OPENAI_API_KEY


class OpenAI:

    def __init__(self, question: str):
        self.question = question

        # Set your OpenAI API key
        openai.api_key = OPENAI_API_KEY

    # Define a basic template for the input to the AI model
    async def generate_prompt(self) -> str:
        return f"Patient's question: '{self.question}'. Provide a helpful, concise, and professional response tailored for a general audience."

    # Generate AI response using OpenAI API
    @staticmethod
    def generate_response_with_openai(prompt: str) -> str:
        try:
            response = openai.completions.create(
                model="gpt-3.5-turbo-instruct",  # You can replace with "gpt-4" if you have access
                prompt=prompt,
                max_tokens=150,
                temperature=0.7,
            )
            return response.choices[0].text.strip()
        except openai.OpenAIError as e:
            raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")
