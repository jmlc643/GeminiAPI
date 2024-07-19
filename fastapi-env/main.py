import os
from dotenv import load_dotenv
import google.generativeai as genai
from fastapi import FastAPI
from pydantic import BaseModel
load_dotenv()

genai.configure(api_key=os.getenv('API_KEY'))
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)

app = FastAPI()

# Modelo de datos para el prompt
class Prompt(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"Hello": os.getenv('API_KEY')}

@app.post("/generate")
def prompt(prompt: Prompt):
    chat_session = model.start_chat(
        history=[
        ]
    )

    response = chat_session.send_message(prompt.prompt)
    
    return {"Response:" : response.text}