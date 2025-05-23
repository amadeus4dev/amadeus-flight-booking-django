from fastapi import FastAPI
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from pydantic import BaseModel
from ai import LLM

app = FastAPI()

class QuestionRequest(BaseModel):
    chat_history: list[str]

@app.post("/question", response_model=dict())
def post_question(request: QuestionRequest):
    return LLM.invoke(request.chat_history)