from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mysql.connector import Error
from pydantic import BaseModel, Field

from database import conectar, linhas_para_dicts


class Prato(BaseModel):
    nome: str = Field(..., min_length=1, max_length=150)
    categoria: str = Field(..., min_length=1, max_length=50)
    descricao: Optional[str] = Field(None, max_length=500)
    preco: float = Field(..., gt=0)


def verificar_conexao() -> None:
    try:
        conn = conectar()
        try:
            conn.ping(reconnect=True, attempts=1, delay=0)
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM prato LIMIT 1")
        finally:
            conn.close()
    except Error as erro:
        raise RuntimeError(
            f"Não foi possível conectar ao MySQL ({erro}). "
            "Confira back-end/.env e execute banco-dados\\setup.bat"
        ) from erro


@asynccontextmanager
async def lifespan(_app: FastAPI):
    verificar_conexao()
    yield


app = FastAPI(title="API Restaurante Sabor & Arte", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def raiz():
    return {
        "mensagem": "API Restaurante — use GET/POST /pratos",
        "docs": "/docs",
        "banco": "MySQL",
    }


@app.get("/saude")
def saude():
    try:
        conn = conectar()
        try:
            conn.ping(reconnect=True, attempts=1, delay=0)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM prato")
            total = cursor.fetchone()[0]
        finally:
            conn.close()
        return {"status": "ok", "mysql": "conectado", "pratos": total}
    except Error as erro:
        raise HTTPException(status_code=503, detail=str(erro)) from erro


@app.post("/pratos")
def cadastrar_prato(prato: Prato):
    try:
        conn = conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO prato (nome, categoria, descricao, preco)
                VALUES (%s, %s, %s, %s)
                """,
                (prato.nome, prato.categoria, prato.descricao, prato.preco),
            )
            conn.commit()
            novo_id = cursor.lastrowid
        finally:
            conn.close()
    except Error as erro:
        raise HTTPException(status_code=500, detail=str(erro)) from erro

    return {
        "mensagem": "Prato cadastrado no cardápio com sucesso!",
        "id": novo_id,
    }


@app.get("/pratos")
def listar_pratos():
    try:
        conn = conectar()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, nome, categoria, descricao, preco
                FROM prato
                ORDER BY id DESC
                """
            )
            return linhas_para_dicts(cursor)
        finally:
            conn.close()
    except Error as erro:
        raise HTTPException(status_code=500, detail=str(erro)) from erro
