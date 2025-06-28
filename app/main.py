from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Instanciar o cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Criar app FastAPI
app = FastAPI()

# Liberar CORS para qualquer origem (ou especifique seu front)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou troque por ["https://seufront.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo da mensagem
class Mensagem(BaseModel):
    mensagem: str

# Rota de resposta da IA
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
