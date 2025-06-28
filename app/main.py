from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
import os

# Carrega as variáveis de ambiente
load_dotenv()

# Inicializa o cliente da OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cria a aplicação FastAPI
app = FastAPI()

# Libera o acesso de qualquer origem (útil para desenvolvimento)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, substitua por ["https://seu-front-end.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo da mensagem recebida
class Mensagem(BaseModel):
    mensagem: str

# Rota de resposta
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
