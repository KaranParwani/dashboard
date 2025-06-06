from fastapi import APIRouter, HTTPException

from patient.schemas.chatbot import Question
from patient.services.chatbot import OpenAI

openai_router = APIRouter()

@openai_router.post("/chatbot")
async def chatbot_endpoint(question: Question):
    if not question.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    response = "This is sample API response"
    # Generate prompt
    # openai = OpenAI(str(question))
    # prompt = await openai.generate_prompt()
    # print(prompt)

    # Generate and return the response
    # response = openai.generate_response_with_openai(prompt)
    return {"response": response}