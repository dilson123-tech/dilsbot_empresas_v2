from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class Mensagem(BaseModel):
    mensagem: str

@app.post("/pergunta")
async def responder(mensagem: Mensagem):
    try:
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente profissional que responde perguntas de empresas sobre seus serviços."},
                {"role": "user", "content": mensagem.mensagem}
            ]
        )
        return {"resposta": resposta.choices[0].message.content}
    except Exception as e:
        return {"erro": str(e)}
