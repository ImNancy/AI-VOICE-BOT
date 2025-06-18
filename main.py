from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
import os

app = FastAPI()

# Mount static and template folders
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# Groq API details
GROQ_API_KEY = "YOUR_API_KEY"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"


# AI response generation
def get_groq_response(prompt: str):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        result = response.json()

        print("Groq Raw Response:", result)  # Debug output

        if "choices" in result:
            return result["choices"][0]["message"]["content"].strip()
        else:
            return f"❌ Groq error: {result.get('error', result)}"

    except Exception as e:
        return f"⚠️ Request failed: {str(e)}"

# HTML home
@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Chat API route
class ChatInput(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(user_input: ChatInput):
    reply = get_groq_response(user_input.message)
    return {"reply": reply}

# Test route
@app.get("/test", response_class=HTMLResponse)
async def test_page():
    return HTMLResponse("<h1>✅ FastAPI Test Route Works!</h1>")
