import os
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

BASE_DIR=Path(__file__).resolve().parent
load_dotenv(BASE_DIR/".env")
API_KEY=os.getenv("OPENAI_API_KEY")
MODEL=os.getenv("OPENAI_MODEL","gpt-5.6")
client=OpenAI(api_key=API_KEY) if API_KEY else None

app=FastAPI(title="Tech Repeated Guide AI",version="1.0.0")

class ChatRequest(BaseModel):
    messages:list

SYSTEM_PROMPT="""You are Tech Repeated Guide, a professional AI technology mentor.
Help users with programming, web development, HTML, CSS, JavaScript, Python, React, Node.js, APIs, databases, Git/GitHub, debugging, software engineering, AI/ML, cybersecurity fundamentals, computer science and technology careers.
Be friendly, clear, practical, professional and beginner-friendly.
For explanations: explain simply, give a practical example, code when useful, explain important parts, mention common mistakes and the next step.
For debugging: identify the problem, explain why it happens, provide corrected code, explain the fix and improvements.
For code generation: use clean readable secure code; never expose secrets; explain how to run it.
Do not pretend you performed actions you did not perform."""

@app.post("/api/chat")
async def chat(request:ChatRequest):
    if not client:
        raise HTTPException(500,"OPENAI_API_KEY is not configured. Add it to .env")
    try:
        msgs=[{"role":"system","content":SYSTEM_PROMPT}]
        for m in request.messages[-30:]:
            if m.get("role") in ("user","assistant") and m.get("content"):
                msgs.append({"role":m["role"],"content":m["content"]})
        response=client.chat.completions.create(model=MODEL,messages=msgs,temperature=0.4,max_tokens=2500)
        return {"reply":response.choices[0].message.content}
    except Exception as e:
        print("AI ERROR:",e)
        raise HTTPException(500,"AI request failed. Check your API key and model name.")

app.mount("/static",StaticFiles(directory=BASE_DIR),name="static")

@app.get("/")
async def home():
    return FileResponse(BASE_DIR/"index.html")
