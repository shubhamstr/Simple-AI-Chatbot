from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import re
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

app = FastAPI(
    title="AI Assistant Chatbot API",
    description="A simple chatbot backend using FastAPI with dummy response logic.",
    version="1.0.0",
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        description="The message sent by the user",
        min_length=1,
        max_length=2000,
        examples=["Hello"],
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Message cannot be empty or contain only whitespace.")
        return cleaned


class ChatResponse(BaseModel):
    response: str = Field(..., description="The response message from the chatbot")


def get_dummy_response(message: str) -> str:
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": message.lower()
            }
        ],
        # temperature=1,
        # max_completion_tokens=2048,
        # top_p=1,
        # reasoning_effort="medium",
        stream=False,
        # stop=None
    )

    return completion.choices[0].message.content
    # for chunk in completion:
    #     print(chunk.choices[0].delta.content or "", end="")


@app.get("/", summary="Health Check")
async def root():
    return {
        "status": "online",
        "service": "AI Assistant Chatbot API",
        "version": "1.0.0",
    }


@app.get("/api/health", summary="API Health Check")
async def health_check():
    return {"status": "healthy"}


@app.post(
    "/api/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Chatbot Interaction Endpoint",
    description="Accepts a user message and returns a chatbot response.",
)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        reply = get_dummy_response(request.message)
        return ChatResponse(response=reply)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while generating the chatbot response: {str(exc)}",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
