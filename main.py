from fastapi import FastAPI, HTTPException
from umongo import Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from umongo.frameworks.motor_asyncio import MotorAsyncIOInstance
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from bson import ObjectId
from bson.errors import InvalidId
import os

load_dotenv()

app = FastAPI()

# 1. Configuração do MongoDB (usando o nome do serviço do Docker)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017/academic_db")
print(f"--- Conectando ao MongoDB em: {MONGO_URI} ---")
client = AsyncIOMotorClient(MONGO_URI)
db = client.academic_db

# 2. Inicializa o umongo corretamente para a versão 4.0.0
instance = MotorAsyncIOInstance(db)

@app.on_event("startup")
async def startup_event():
    print("--- Aplicação FastAPI iniciada com sucesso! ---")
    print("--- Documentação disponível em: http://localhost:8000/docs ---")

# Modelo de Documento (exemplo: Livro)
@instance.register
class Livro(Document):
    titulo = fields.StringField(required=True)
    autor = fields.StringField(required=True)
    ano_publicacao = fields.IntField(required=True)
    genero = fields.StringField(required=True)

    class Meta:
        collection = db.livros

# Schemas Pydantic para validação de entrada e saída
class LivroIn(BaseModel):
    titulo: str
    autor: str
    ano_publicacao: int
    genero: str

class LivroOut(LivroIn):
    id: str

    class Config:
        from_attributes = True

# Função auxiliar para validar o ObjectId
def validar_id(livro_id: str):
    try:
        return ObjectId(livro_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="ID inválido")

# Rotas CRUD
@app.post("/livros/", response_model=LivroOut)
async def create_livro(livro: LivroIn):
    new_livro = Livro(**livro.model_dump())
    await new_livro.commit()
    return LivroOut(id=str(new_livro.pk), **new_livro.dump())

@app.get("/livros/", response_model=List[LivroOut])
async def read_livros():
    livros = await Livro.find({}).to_list(length=100)
    return [LivroOut(id=str(livro.pk), **livro.dump()) for livro in livros]

@app.get("/livros/{livro_id}", response_model=LivroOut)
async def read_livro(livro_id: str):
    livro = await Livro.find_one({"_id": validar_id(livro_id)})
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return LivroOut(id=str(livro.pk), **livro.dump())

@app.put("/livros/{livro_id}", response_model=LivroOut)
async def update_livro(livro_id: str, livro_data: LivroIn):
    livro = await Livro.find_one({"_id": validar_id(livro_id)})
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    livro.update(livro_data.model_dump())
    await livro.commit()
    return LivroOut(id=str(livro.pk), **livro.dump())

@app.delete("/livros/{livro_id}", status_code=204)
async def delete_livro(livro_id: str):
    livro = await Livro.find_one({"_id": validar_id(livro_id)})
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    await livro.delete()
    return
