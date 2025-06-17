# import speech_recognition as sr
# import pyttsx3
# import requests
# import json

# # Replace with your Groq API key
# GROQ_API_KEY = "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"

# # Chat settings
# GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
# MODEL = "llama3-8b-8192"  # or llama3-70b-8192, mixtral-8x7b-32768, etc.

# # Setup TTS
# engine = pyttsx3.init()

# def speak(text):
#     print("🤖:", text)
#     engine.say(text)
#     engine.runAndWait()

# def listen():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("\n🎤 Listening...")
#         recognizer.adjust_for_ambient_noise(source)
#         audio = recognizer.listen(source)
#     try:
#         text = recognizer.recognize_google(audio)
#         print("🗣️ You:", text)
#         return text
#     except sr.UnknownValueError:
#         speak("Sorry, I couldn't understand.")
#         return None
#     except sr.RequestError:
#         speak("Speech service error.")
#         return None

# def get_groq_response(prompt):
#     headers = {
#         "Authorization": f"Bearer {GROQ_API_KEY}",
#         "Content-Type": "application/json"
#     }
#     data = {
#         "model": MODEL,
#         "messages": [
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ]
#     }

#     try:
#         response = requests.post(GROQ_API_URL, headers=headers, json=data)
#         result = response.json()
#         return result["choices"][0]["message"]["content"].strip()
#     except Exception as e:
#         return f"Error from Groq: {str(e)}"

# # Main loop
# if __name__ == "__main__":
#     while True:
#         user_input = listen()
#         if user_input:
#             if "exit" in user_input.lower():
#                 speak("Goodbye!")
#                 break
#             response = get_groq_response(user_input)
#             speak(response)
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import requests
import pyttsx3
import sounddevice as sd
import numpy as np
import speech_recognition as sr

app = FastAPI()

# Mount static and template folders
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Groq API details
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama3-8b-8192"

engine = pyttsx3.init()

# AI reply generation
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
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"Error from Groq: {str(e)}"

# TTS
def speak(text):
    print("🤖:", text)
    engine.say(text)
    engine.runAndWait()

# Voice input
def listen():
    recognizer = sr.Recognizer()
    samplerate = 16000
    duration = 5

    print("\n🎤 Listening...")
    try:
        audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
        audio_bytes = audio_data.tobytes()
        audio_file = sr.AudioData(audio_bytes, samplerate, 2)
        text = recognizer.recognize_google(audio_file)
        print("🗣️ You:", text)
        return text
    except sr.UnknownValueError:
        print("🤖 Sorry, I couldn't understand.")
        return None
    except sr.RequestError as e:
        print("🤖 Google API error:", e)
        return None

# 🟢 Home page
@app.get("/", response_class=HTMLResponse)
async def serve_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# 🔁 Chat API
class ChatInput(BaseModel):
    message: str

@app.post("/chat")
async def chat_endpoint(user_input: ChatInput):
    reply = get_groq_response(user_input.message)
    return {"reply": reply}

# 🧪 Test route
@app.get("/test", response_class=HTMLResponse)
async def test_page():
    return HTMLResponse("<h1>✅ FastAPI Test Route Works!</h1>")

# Optional: Uncomment to enable terminal mic
# if __name__ == "__main__":
#     while True:
#         user_input = listen()
#         if user_input:
#             if "exit" in user_input.lower():
#                 speak("Goodbye!")
#                 break
#             response = get_groq_response(user_input)
#             speak(response)
