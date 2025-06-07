from datetime import datetime

from fastapi import APIRouter, HTTPException

from patient.schemas.chatbot import Question
from config import REDIS

openai_router = APIRouter()


@openai_router.post("/chatbot")
async def chatbot_endpoint(question: Question):
    if not question.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    question_data = question.model_dump()
    response = "This is sample API response"

    timestamp = datetime.utcnow().isoformat()  # Get current timestamp

    # Save to Redis
    try:
        chat_data = {
            "question": str(question_data["question"]),
            "response": response,
            "timestamp": timestamp,
        }
        await REDIS.set("last_chat", str(chat_data))

        # Generate prompt
        # openai = OpenAI(str(question))
        # prompt = await openai.generate_prompt()
        # print(prompt)

        # Generate and return the response
        # response = openai.generate_response_with_openai(prompt)
        return {"response": response}

    except Exception as e:
        print("Error saving to Redis:", e)
        raise HTTPException(status_code=500, detail="Failed to save to Redis")


@openai_router.get("/chatbot/history")
async def get_chat_history():
    # Fetch from Redis
    try:
        chat_data = await REDIS.get("last_chat")
        if not chat_data:
            raise HTTPException(status_code=404, detail="No chat history found")

        # Parse the saved data
        chat_data = eval(chat_data)  # Convert string back to dictionary
        return chat_data
    except Exception as e:
        print("Error fetching from Redis:", e)
        raise HTTPException(status_code=500, detail="Failed to fetch from Redis")
