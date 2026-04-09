from fastapi import FastAPI, HTTPException
from umongo import Document, fields
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import Optional, List
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

# Configuração do MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/academic_db")
client = AsyncIOMotorClient(MONGO_URI)
db = client.academic_db

# Inicializa o umongo
from umongo.frameworks import FastAPI as UmongoFastAPI
instance = UmongoFastAPI()
instance.init_app(app, db)

# Modelo de Documento (exemplo: Livro)
@instance.register
class Livro(Document):
    titulo = fields.Str(required=True)
    autor = fields.Str(required=True)
    ano_publicacao = fields.Int(required=True)
    genero = fields.Str(required=True)

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
    livro = await Livro.find_one({"_id": livro_id})
    if livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return LivroOut(id=str(livro.pk), **livro.dump())

@app.put("/livros/{livro_id}", response_model=LivroOut)
async def update_livro(livro_id: str, livro: LivroIn):
    existing_livro = await Livro.find_one({"_id": livro_id})
    if existing_livro is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    
    existing_livro.update(livro.model_dump())
    await existing_livro.commit()
    return LivroOut(id=str(existing_livro.pk), **existing_livro.dump())

@app.delete("/livros/{livro_id}", status_code=204)
async def delete_livro(livro_id: str):
    result = await Livro.delete_one({"_id": livro_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return
