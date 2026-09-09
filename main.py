import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
API_KEY=os.getenv("OPENAI_API_KEY")
client=OpenAI(api_key=API_KEY) if API_KEY else None

app=FastAPI(title="Tech Repeated Guide AI",version="1.0.0")

class ChatRequest(BaseModel):
    messages:list

SYSTEM_PROMPT="""You are Tech Repeated Guide, a professional AI technology mentor.
Help with programming, web development, HTML, CSS, JavaScript, Python, React, Node.js, APIs, databases, Git/GitHub, debugging, software engineering, AI/ML, cybersecurity fundamentals, computer science and technology careers.
Be friendly, clear, practical, professional and beginner-friendly.
For explanations: explain simply, give a practical example, code when useful, explain important parts, mention common mistakes and the next step.
For debugging: identify the problem, explain why it happens, provide corrected code, explain the fix and improvements.
For code generation: use clean readable secure code; never expose secrets; explain how to run it.
Do not pretend you performed actions you did not perform. You are Tech Repeated Guide."""

@app.post("/api/chat")
async def chat(request:ChatRequest):
    if not client:
        raise HTTPException(status_code=500,detail="OPENAI_API_KEY is not configured.")
    try:
        msgs=[{"role":"system","content":SYSTEM_PROMPT}]
        for m in request.messages[-30:]:
            if m.get("role") in ("user","assistant") and m.get("content"):
                msgs.append({"role":m["role"],"content":m["content"]})
        response=client.chat.completions.create(model=os.getenv("OPENAI_MODEL","gpt-5.6"),messages=msgs,temperature=0.4,max_tokens=2500)
        return {"reply":response.choices[0].message.content}
    except Exception as error:
        print("AI ERROR:",error)
        raise HTTPException(status_code=500,detail="AI request failed.")

app.mount("/static",StaticFiles(directory="../frontend"),name="static")

@app.get("/")
async def home():
    return FileResponse("../frontend/index.html")
