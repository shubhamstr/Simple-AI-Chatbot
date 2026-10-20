from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
import re

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
    """Generate a dummy chatbot response based on the input message."""
    # Normalize: lowercase, strip extra whitespace, and remove ending punctuation for matching
    normalized = message.lower().strip()
    cleaned = re.sub(r"[!?.~,]+$", "", normalized).strip()

    # Rule-based pattern matching
    if cleaned in ("hello", "hey", "greetings"):
        return "Hello! How can I help you?"
    elif cleaned in ("hi", "hola"):
        return "Hi there! 👋"
    elif cleaned in ("how are you", "how're you", "how are you doing", "how do you do"):
        return "I'm doing great! How can I help you today?"
    elif cleaned in ("what can you do", "who are you", "what is your name"):
        return "I can answer your questions and assist you. Right now, I'm running in demo mode!"
    elif cleaned in ("bye", "goodbye", "see you"):
        return "Goodbye! Have a wonderful day!"
    elif cleaned in ("thanks", "thank you"):
        return "You're very welcome! Let me know if there's anything else I can do."
    else:
        return "This is a dummy chatbot response. AI integration can be added later."


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
