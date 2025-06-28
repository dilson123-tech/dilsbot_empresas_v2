from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
import os

# Carrega as variáveis do .env
load_dotenv()

# Cria cliente da OpenAI com a chave da API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Instancia o app FastAPI
app = FastAPI()

# Libera o CORS para permitir conexões do front-end (mesmo de outro domínio)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, substitua pelo domínio específico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define o modelo esperado no body da requisição
class Mensagem(BaseModel):
    mensagem: str

# Rota principal que responde com a IA
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
